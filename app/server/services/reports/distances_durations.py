import pandas as pd

from server.services.graphql_service import execute_graphql_query

# Asegúrate de ajustar estas importaciones a tu estructura de proyecto y nombres de archivo.

async def get_trips_data_for_distance_duration(token: str):
    trips_query = """
    query {
        trips {
            trips {
                distance
                duration
            }
        }
    }
    """
    response = await execute_graphql_query(trips_query, token=token)
    trips_data = response.get("data", {}).get("trips", {}).get("trips", [])
    return trips_data

async def get_distance_duration_averages(token: str):
    trips_data = await get_trips_data_for_distance_duration(token)

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(trips_data)

    # Calcular promedios
    average_distance = df['distance'].mean()
    average_duration = df['duration'].mean()

    return {
        "Average distance": average_distance,
        "Average duration": average_duration
    }
