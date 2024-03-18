import pandas as pd

from ..graphql_service import execute_graphql_query

async def get_user_data(token: str):
    user_query = """
    query {
        users {
            users {
                id
                firstName
                lastName
                averageRating
                trips {
                    id
                    origin
                }
            }
        }
    }
    """
    response = await execute_graphql_query(user_query, token=token)
    user_data = response.get("data", {}).get("users", {}).get("users", [])
    return user_data

async def get_user_behavior_insights(token: str):
    user_data = await get_user_data(token)

    # Preparar los datos de los usuarios
    for user in user_data:
        # Concatenar el nombre completo
        user['fullName'] = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip()
        # Preparar la cuenta de viajes
        user['trip_count'] = len(user.get('trips', []))

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(user_data)

    # Asegúrate de que 'averageRating' y 'trip_count' sean numéricos y no tengan valores NaN
    df['averageRating'] = pd.to_numeric(df['averageRating'], errors='coerce')
    df.dropna(subset=['averageRating', 'trip_count'], inplace=True)

    # Usuarios más activos
    most_active_users = df.nlargest(5, 'trip_count')[['fullName', 'averageRating', 'trip_count']]

    # Calcular la correlación entre la frecuencia de viajes y la calificación promedio
    correlation = None
    if not df.empty and 'trip_count' in df and 'averageRating' in df:
        correlation = df['trip_count'].corr(df['averageRating'])

    # Análisis de ubicación
    all_origins = [trip.get('origin') for user in user_data for trip in user.get('trips', []) if 'origin' in trip]
    location_counts = pd.Series(all_origins).value_counts().to_dict() if all_origins else {}

    return {
        "Most active users": most_active_users.to_dict(orient='records'),
        "Trip rating correlation": correlation,
        "Common origins": location_counts
    }

