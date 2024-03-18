import pandas as pd

from server.services.graphql_service import execute_graphql_query

async def get_trips_data_for_rates(token: str):
    trips_query = """
    query {
        trips {
            trips {
                fare
            }
        }
    }
    """
    response = await execute_graphql_query(trips_query, token=token)
    trips_data = response.get("data", {}).get("trips", {}).get("trips", [])
    return trips_data

async def get_rates_info(token: str):
    trips_data = await get_trips_data_for_rates(token)

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(trips_data)

    # Calcular estadísticas de tarifas
    average_fare = df['fare'].mean()
    max_fare = df['fare'].max()
    min_fare = df['fare'].min()

    # Calcular distribución de tarifas
    fare_bins = pd.cut(df['fare'], bins=[0, 10, 20, 30, 40, 50, 100, 200, df['fare'].max()])
    fare_distribution = fare_bins.value_counts().sort_index()

    # Convertir Interval a string para serialización
    fare_distribution = {str(interval): int(count) for interval, count in fare_distribution.items()}

    return {
        "Average fare": average_fare,
        "Max fare": max_fare,
        "Min fare": min_fare,
        "Fare distribution": fare_distribution
    }
