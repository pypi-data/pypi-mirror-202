# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from requests import post

import natml

def query (query: str, input: dict=None, access_key: str=None) -> dict:
    """
    Issue a query to the NatML Graph API.

    Parameters:
        query (str): Graph query.
        input (dict): Input variables.
        access_key (str): NatML access key.

    Returns:
        dict: Response dictionary.
    """
    access_key = access_key or natml.access_key
    headers = { "Authorization": f"Bearer {access_key}" } if access_key else {}
    response = post(
        natml.api_url,
        json={ "query": query, "variables": { "input": input } },
        headers=headers
    ).json()
    # Check error
    if "errors" in response:
        raise RuntimeError(response["errors"][0]["message"])
    # Return
    result = response["data"]
    return result