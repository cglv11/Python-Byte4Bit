import httpx

async def fetch_graphql_data(token: str, query: str, variables: dict = None):
    url = 'http://localhost:3000/transport-app'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    json_data = {'query': query, 'variables': variables}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json_data, headers=headers)
        return response.json()
