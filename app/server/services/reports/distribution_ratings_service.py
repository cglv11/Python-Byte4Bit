import pandas as pd

from server.services.graphql_service import execute_graphql_query


async def get_drivers_ratings(token: str):
    drivers_query = """
    query {
        drivers {
            drivers {
                averageRating
            }
        }
    }
    """
    response = await execute_graphql_query(drivers_query, token=token)
    drivers_data = response.get("data", {}).get("drivers", {}).get("drivers", [])
    # Extract only the ratings to a list
    ratings = [driver["averageRating"] for driver in drivers_data]
    return ratings

async def get_users_ratings(token: str):
    users_query = """
    query {
        users {
            users {
                averageRating
            }
        }
    }
    """
    response = await execute_graphql_query(users_query, token=token)
    users_data = response.get("data", {}).get("users", {}).get("users", [])
    # Extract only the ratings to a list
    ratings = [user["averageRating"] for user in users_data]
    return ratings

async def get_rating_distribution(token: str):
    driver_ratings = await get_drivers_ratings(token)
    user_ratings = await get_users_ratings(token)

    # Crear DataFrames de pandas directamente con la lista de calificaciones
    df_drivers = pd.DataFrame(driver_ratings, columns=['averageRating'])
    df_users = pd.DataFrame(user_ratings, columns=['averageRating'])

    # Definir rangos de calificación para la distribución
    rating_bins = pd.interval_range(start=1, end=5, freq=1)

    # Obtener la distribución de las calificaciones
    driver_ratings_dist = df_drivers['averageRating'].value_counts(bins=rating_bins, sort=False).sort_index()
    user_ratings_dist = df_users['averageRating'].value_counts(bins=rating_bins, sort=False).sort_index()

    # Convertir las series de pandas a un formato JSON serializable
    driver_ratings_distribution = {str(interval): int(count) for interval, count in driver_ratings_dist.items()}
    user_ratings_distribution = {str(interval): int(count) for interval, count in user_ratings_dist.items()}

    return {
        "Driver rating distribution": driver_ratings_distribution,
        "User rating distribution": user_ratings_distribution
    }
