import httpx
from fastapi import HTTPException
from decouple import config


async def execute_graphql_query(query: str, variables: dict = None, token: str = ""):
    api_url = config("API_HOST", default="http://localhost:3000/transport-app")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}" if token else "",
    }
    json_data = {"query": query, "variables": variables}

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, json=json_data, headers=headers)
        response_data = response.json()

        if "errors" in response_data:
            raise HTTPException(status_code=400, detail=response_data["errors"])

        return response_data
