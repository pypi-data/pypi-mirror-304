import typer
from typing_extensions import Annotated
import pandas as pd
from dynatrace import Dynatrace
from dynatrace.environment_v2.extensions import MonitoringConfigurationDto
from dynatrace.http_client import TOO_MANY_REQUESTS_WAIT
from rich.progress import track
from rich import print
import yaml

from typing import Optional, List, Dict, Union
import json
import logging

from .models import CustomDBQuery
from .utils import slugify

TIMEFRAME = "now-1y"


def lookup_columns_for_query(dt: Dynatrace, query_name: str):
    column_names = []
    query = f'custom.db.query:filter(eq(query_name,"{query_name}")):splitBy(column,query_name)'
    metric_series_collections = dt.metrics.query(
        query, time_from=TIMEFRAME, resolution="Inf"
    )
    for collection in metric_series_collections:
        for series in collection.data:
            column = series.dimension_map.get("column")
            if column:
                column_names.append(column)

    return column_names


def queries_from_ef1_config(properties: dict):
    properties.update(
        {
            "database_type": properties["database_type"],
            "group_name": properties["group_name"],
            "database_host": properties["database_host"],
            "database_name": properties["database_name"],
            "database_username": properties["database_username"],
            "custom_device_name": properties["custom_device_name"],
        }
    )

    configured_queries: List[CustomDBQuery] = []
    query_index = 1
    while query_index < 11:
        if properties[f"query_{query_index}_value"]:
            configured_queries.append(
                CustomDBQuery(
                    properties[f"query_{query_index}_name"],
                    properties[f"query_{query_index}_schedule"],
                    properties[f"query_{query_index}_value"],
                    properties[f"query_{query_index}_value_columns"],
                    properties[f"query_{query_index}_dimension_columns"],
                    properties[f"query_{query_index}_extra_dimensions"],
                )
            )
        query_index += 1
    return configured_queries


def ef2_datasource(db_type: str):
    if db_type == "Oracle":
        return "sqlOracle"
    elif db_type == "DB2":
        return "sqlDb2"
    elif db_type == "SQL Server":
        return "sqlServer"
    elif db_type == "MySQL":
        return "sqlMySql"
    elif db_type == "PostgreSQL":
        return "sqlPostgres"
    elif db_type == "SAP HANA":
        return "sqlHana"
    else:
        raise Exception(f"Unsupported database type: {db_type}")


def activation(endpoint_name: str, props: dict):
    activation_config = {
        "enabled": False,
        "description": f"Migrated extension from EF1 db queries config {endpoint_name}.",
        "version": "1.0.0",
        f"{ef2_datasource(props['database_type'])}Remote": {
            "endpoints": [
                {
                    "host": props["database_host"],
                    "port": props["database_port"],
                    "databaseName": props["database_name"],
                    "authentication": {
                        "scheme": "basic",
                        "useCredentialVault": False,
                        "username": props["database_username"],
                        "password": "dummy",
                    },
                }
            ]
        },
    }

    return activation_config


class EF2SqlExtension:
    def __init__(
        self, dt: Dynatrace, endpoint_name: str, ef1_config_properties: Union[Dict, List]
    ) -> None:
        

        if type(ef1_config_properties) == list:
            # have to merge queries from multiple configs into one
            queries = []
            db_type = ef2_datasource(ef1_config_properties[0]["database_type"])
            for conf_prop in ef1_config_properties:
                queries.extend(queries_from_ef1_config(conf_prop))
            self.activation_config = activation(endpoint_name, ef1_config_properties[0])
        else:
            db_type = ef2_datasource(ef1_config_properties["database_type"])
            queries = queries_from_ef1_config(ef1_config_properties)
            self.activation_config = activation(endpoint_name, ef1_config_properties)

        
        extension = {
            "name": f"custom:db.query.{slugify(endpoint_name)[:30] if len(slugify(endpoint_name)) > 30 else slugify(endpoint_name)}",
            "version": "1.0.0",
            "minDynatraceVersion": "1.301",
            "author": {"name": "Dynatrace"},
            db_type: [],
        }

        group_number = 1
        subgroup_number = 0

        group = {
                "group": f"queries-{group_number}",
                "subgroups": []
            }

        for query in queries:
            if subgroup_number == 10:
                extension[db_type].append(group)
                group_number+=1
                group = {
                    "group": f"queries-{group_number}",
                    "subgroups": []
                }
            metric_columns = query.value_columns
            if not metric_columns:
                metric_columns = lookup_columns_for_query(dt, query.name)
            else:
                metric_columns = metric_columns.split(",")
            extra_dimensions = query.extra_dimensions

            safe_query_name = slugify(query.name)

            subgroup = {
                "subgroup": query.name,
                "query": query.value,
                "schedule": query.schedule,
                "metrics": [],
                "dimensions": [{"key": "query_name", "value": f"const:{query.name}"}],
            }

            for column in metric_columns:
                subgroup["metrics"].append(
                    {
                        "key": f"{safe_query_name}.{slugify(column)}",
                        "value": f"col:{column}",
                        "type": "gauge",
                    }
                )
            subgroup_number += 1
            group['subgroups'].append(subgroup)


        # extension[db_type].append(group)
        extension[db_type].append(group)

        self.name = "custom:" + extension["name"].split(":")[1]
        self.version = extension["version"]
        self.dictionary = extension
