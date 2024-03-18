import pandas as pd

from server.services.graphql_service import execute_graphql_query


async def get_trips_data(token: str):
    trips_query = """
    query {
        trips {
            trips {
                fare
                startDateTime
            }
        }
    }
    """
    response = await execute_graphql_query(trips_query, token=token)
    trips_data = response.get("data", {}).get("trips", {}).get("trips", [])
    return trips_data

async def get_earnings(token: str):
    trips_data = await get_trips_data(token)

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(trips_data)
    df['startDateTime'] = pd.to_datetime(df['startDateTime'])
    df['day'] = df['startDateTime'].dt.date
    df['week'] = df['startDateTime'].dt.isocalendar().week
    df['month'] = df['startDateTime'].dt.month

    # Calcular ingresos totales
    daily_earnings = df.groupby('day')['fare'].sum()
    weekly_earnings = df.groupby('week')['fare'].sum()
    monthly_earnings = df.groupby('month')['fare'].sum()

    # Convertir los pandas Series a diccionarios con valores de tipo flotante de Python
    return {
        "Daily earnings": {f"Day: {str(key)}": float(value) for key, value in daily_earnings.items()},
        "Weekly earnings": {f"Week {str(key)}": float(value) for key, value in weekly_earnings.items()},
        "Monthly earnings": {f"Month {str(key)}": float(value) for key, value in monthly_earnings.items()}
    }