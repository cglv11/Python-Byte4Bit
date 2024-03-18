import pandas as pd

from server.services.graphql_service import execute_graphql_query


async def get_trip_data(token: str):
    trip_query = """
    query {
        trips {
            trips {
                origin
                destination
                startDateTime
                endDateTime
                status
            }
        }
    }
    """
    response = await execute_graphql_query(trip_query, token=token)
    trip_data = response.get("data", {}).get("trips", {}).get("trips", [])
    return trip_data

async def get_trip_analysis(token: str):
    trip_data = await get_trip_data(token)

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(trip_data)
    df['startDateTime'] = pd.to_datetime(df['startDateTime'])
    df['endDateTime'] = pd.to_datetime(df['endDateTime'], errors='coerce')  # Convierte a NaT donde haya nulos

    # Extraer la hora de startDateTime y crear la columna 'hour'
    df['hour'] = df['startDateTime'].dt.hour

    # Calcular la duración solo para los viajes que tienen un endDateTime
    df['duration'] = df.apply(
        lambda row: (row['endDateTime'] - row['startDateTime']).total_seconds() / 60
        if pd.notnull(row['endDateTime']) else None, axis=1
    )
    
    # Convertir la columna 'duration' a tipo flotante
    df['duration'] = df['duration'].astype(float)

    # Rutas más comunes
    route_counts = df.groupby(['origin', 'destination']).size().sort_values(ascending=False).head(5)
    most_common_routes = route_counts.reset_index().rename(columns={0: 'count'}).to_dict(orient='records')

    # Calcular horas pico de demanda
    peak_hours = df['hour'].value_counts().nlargest(1)
    peak_demand_hours = {f"{hour} hour": count for hour, count in peak_hours.items()}

    # Viajes con mayor duración - filtrar nulos y ordenar
    longest_trips = df.dropna(subset=['duration']).nlargest(5, 'duration')[['origin', 'destination', 'duration']].to_dict(orient='records')

    # Viajes que han sido cancelados o no completados
    cancelled_or_incomplete = df[df['status'].isin(['Cancelled', 'Incomplete'])][['origin', 'destination', 'status']].to_dict(orient='records')

    # Asegúrate de construir la respuesta final correctamente
    response = {
        "Most common routes": most_common_routes,
        "Peak demand hours": peak_demand_hours,
        "Longest trips": longest_trips,
        "Cancelled or incomplete trips": cancelled_or_incomplete,
    }

    return response
