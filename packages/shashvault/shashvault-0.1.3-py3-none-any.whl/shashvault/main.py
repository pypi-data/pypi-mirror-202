#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import argparse
import os
import aiohttp
import asyncio
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def check_env_var(var_name, default_val=None, sys_exit=False, verbose=True):
    env_var = os.environ.get(var_name)
    if env_var is None or env_var == "":
        if default_val is not None:
            return default_val
        print(f"{var_name} environment variable is not defined")
        if sys_exit:
            sys.exit(1)
    else:
        # if verbose:
        #    print(f"{var_name} is set to {env_var}")
        return env_var


async def get_paths_async(
    vault_addr, vault_token, kv_path, vault_skip_verify, search_path, current_path=""
):
    headers = {"X-Vault-Token": vault_token}
    url = f"{vault_addr}/v1/{kv_path}/metadata{current_path}?list=true"

    async with aiohttp.ClientSession(headers=headers) as session:
        # exception handling reported by SA due to permissions
        try:
            async with session.get(url, verify_ssl=not vault_skip_verify) as response:
                response.raise_for_status()
                json_response = await response.json()
                keys = json_response["data"]["keys"]
        except aiohttp.ClientResponseError as e:
            if e.status == 403:
                return []
            else:
                raise e

    matching_paths = []
    tasks = []
    for key in keys:
        if key.endswith("/"):
            tasks.append(
                get_paths_async(
                    vault_addr,
                    vault_token,
                    kv_path,
                    vault_skip_verify,
                    search_path,
                    f"{current_path}/{key.strip('/')}",
                )
            )
        elif search_path.lower() in key.lower():
            matching_paths.append(f"{current_path}/{key}".strip("/"))

    subpaths = await asyncio.gather(*tasks)
    for subpath in subpaths:
        matching_paths.extend(subpath)

    return matching_paths


def get_paths(vault_addr, vault_token, kv_path, vault_skip_verify, search_path):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        get_paths_async(
            vault_addr, vault_token, kv_path, vault_skip_verify, search_path
        )
    )


def get_secret(vault_addr, vault_token, kv_path, VAULT_SKIP_VERIFY, search_secret):
    headers = {"X-Vault-Token": vault_token}
    url = f"{vault_addr}/v1/{kv_path}/data/{search_secret}"
    response = requests.get(url, headers=headers, verify=not VAULT_SKIP_VERIFY)
    response.raise_for_status()
    secret_data = response.json()["data"]["data"]
    return secret_data


def run():
    parser = argparse.ArgumentParser(
        description="Search and display secrets in HashiCorp Vault"
    )
    parser.add_argument(
        "-sp",
        "--search-path",
        dest="search_path",
        metavar="SEARCH_PATH",
        type=str,
        help="Text to search paths",
    )
    parser.add_argument(
        "-ss",
        "--search-secret",
        dest="search_secret",
        metavar="SECRET_PATH",
        type=str,
        help="Path to a specific secret",
    )

    args = parser.parse_args()

    if args.search_path is None and args.search_secret is None:
        parser.print_help()
        sys.exit(1)

    VAULT_ADDR = check_env_var("VAULT_ADDR", sys_exit=True)
    VAULT_SKIP_VERIFY = check_env_var("VAULT_SKIP_VERIFY", default_val="0") == "1"
    VAULT_TOKEN = check_env_var("VAULT_TOKEN", sys_exit=True)
    VAULT_KV_PATH = check_env_var("VAULT_KV_PATH", sys_exit=True)

    if VAULT_SKIP_VERIFY:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    if args.search_path:
        matching_paths = get_paths(
            VAULT_ADDR, VAULT_TOKEN, VAULT_KV_PATH, VAULT_SKIP_VERIFY, args.search_path
        )
        print("Matching paths:")
        for item in matching_paths:
            print(item)

    if args.search_secret:
        secret_data = get_secret(
            VAULT_ADDR,
            VAULT_TOKEN,
            VAULT_KV_PATH,
            VAULT_SKIP_VERIFY,
            args.search_secret,
        )
        print("Secret data:")
        for key, value in secret_data.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    run()
