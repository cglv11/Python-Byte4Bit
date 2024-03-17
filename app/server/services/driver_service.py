from server.models.driver_models import DriversResponse
from .graphql_service import execute_graphql_query


async def get_drivers(token: str):
    query = """
    query {
        drivers {
            count
            drivers {
                id
                firstName
                lastName
                email
                phoneNumber
                licenseNumber
                averageRating
                availability
                createdAt
                updatedAt
                trips {
                    id
                    origin
                    destination
                    startDateTime
                    endDateTime
                    distance
                    fare
                    duration
                    createdAt
                    updatedAt
                }
            }
        }
    }

    """
    response = await execute_graphql_query(query, None, token)
    drivers_data = response.get("data", {}).get("drivers", {})
    return DriversResponse(**drivers_data)


async def get_driver(driver_id: int, token: str):
    query = """
    query {
        driver(id: 3) {
            driver {
                id
                firstName
                lastName
                email
                phoneNumber
                licenseNumber
                averageRating
                availability
                createdAt
                updatedAt
            }
            trips {
                count
                trips {
                    id
                    origin
                    destination
                    startDateTime
                    endDateTime
                    distance
                    fare
                    duration
                    createdAt
                    updatedAt
                }
            }
        }
    }
    """
    variables = {"id": driver_id}
    response = await execute_graphql_query(query, variables, token)
    driver_data = response.get("data", {}).get("driver", {})
    return driver_data
