import pandas as pd
from collections import Counter

from server.services.graphql_service import execute_graphql_query


async def get_driver_data(token: str):
    driver_query = """
    query {
        drivers {
            drivers {
                id
                firstName
                lastName
                averageRating
                trips {
                    id
                }
                availability
            }
        }
    }
    """
    response = await execute_graphql_query(driver_query, token=token)
    driver_data = response.get("data", {}).get("drivers", {}).get("drivers", [])
    return driver_data

async def get_driver_performance(token: str):
    driver_data = await get_driver_data(token)

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(driver_data)

    # Añadir columna con el nombre completo
    df['fullName'] = df['firstName'] + ' ' + df['lastName']

    # Calificaciones más altas y más bajas
    top_rated_drivers = df.sort_values(by='averageRating', ascending=False).head()
    low_rated_drivers = df.sort_values(by='averageRating', ascending=True).head()

    # Conductores más activos
    df['trip_count'] = df['trips'].apply(len)
    most_active_drivers = df.sort_values(by='trip_count', ascending=False).head()

    # Análisis de disponibilidad
    availability_counts = Counter(df['availability'])

    # Mapear 'true' y 'false' a 'available' y 'not available'
    availability_analysis = {
        "Available" if k else "Not available": v for k, v in availability_counts.items()
    }

    return {
        "Top rated drivers": top_rated_drivers[['fullName', 'averageRating']].to_dict(orient='records'),
        "Low rated drivers": low_rated_drivers[['fullName', 'averageRating']].to_dict(orient='records'),
        "Most active drivers": most_active_drivers[['fullName', 'trip_count']].to_dict(orient='records'),
        "Availability analysis": availability_analysis
    }
