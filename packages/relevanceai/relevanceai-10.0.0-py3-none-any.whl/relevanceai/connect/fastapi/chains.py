import os
import json
import atexit
import requests
from typing import List
from fastapi.routing import APIRoute
from relevanceai.auth import config


def routes_to_chains(api_routes, url, id_suffix=""):
    chains_list = []
    id_list = []
    for route in api_routes:
        if isinstance(route, APIRoute):
            id_list.append(route.unique_id + id_suffix)
            input_schema = {}
            request_body = {}
            if route.body_field:
                input_schema = json.loads(route.body_field.type_.schema_json())
                for k, v in input_schema["properties"].items():
                    if v["type"] == "string":
                        request_body[k] = f"{{{{ params.{k} }}}}"
                    else:
                        request_body[k] = f"{{{{ params.{k} }}}}"
                # request_body = "{ " + request_body[:-1] + " }"

            output_schema = {}
            if route.response_field:
                output_raw_schema = json.loads(route.response_field.type_.schema_json())
                for k, v in output_raw_schema["properties"].items():
                    output_schema[
                        k
                    ] = f"{{{{ steps.api_call.output.response_body.{k} }}}}"

            if url.endswith("/"):
                full_path = url[:-1] + route.path
            else:
                full_path = url + route.path

            chains_list.append(
                {
                    "public": False,
                    "studio_id": route.unique_id + id_suffix,
                    "params_schema": input_schema,
                    "publicly_triggerable": False,
                    "project": config.auth.project,
                    "title": route.summary if route.summary else route.name,
                    "description": route.description,
                    "tags": {"type": "transformation"},
                    "transformations": {
                        "steps": [
                            {
                                "name": "api_call",
                                "transformation": "api_call",
                                "params": {
                                    "url": full_path,
                                    "method": "POST",
                                    "headers": {
                                        "Content-Type": "application/json",
                                        # **headers
                                    },
                                    "body": request_body,
                                    "response_type": "json",
                                },
                                "output": {
                                    "response_body": "{{response_body}}",
                                    "status": "{{status}}",
                                },
                            }
                        ],
                        "output": output_schema,
                    },
                }
            )
    return chains_list, id_list


def upload_chains(chains):
    url = f"https://api-{config.auth.region}.stack.tryrelevance.com"
    results = requests.post(
        f"{url}/latest/studios/bulk_update",
        headers=config.auth.headers,
        json={"updates": chains},
    )
    print("Uploaded chains: ", results.json())
    print("Trace-id ", results.headers.get("x-trace-id"))


def cleanup_chains(chain_id_list):
    results = requests.post(
        f"https://api-{config.auth.region}.stack.tryrelevance.com/latest/studios/bulk_delete",
        headers=config.auth.headers,
        json={"ids": chain_id_list},
    )
    print("Successfully deleted chains from cloud: ", results.json())
    print("Trace-id ", results.headers.get("x-trace-id"))


def connect_chains(api_routes, url, id_suffix="", cleanup=True, export_json=False):
    chains, chain_id_list = routes_to_chains(api_routes, url, id_suffix=id_suffix)
    if export_json:
        import json

        with open("chain_export.json", "w") as outfile:
            json.dump({"export": chains}, outfile)
    else:
        upload_chains(chains)
    if cleanup:
        atexit.register(cleanup_chains, chain_id_list)
    return chain_id_list
