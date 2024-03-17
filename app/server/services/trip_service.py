from server.models.trip_models import TripsResponse
from .graphql_service import execute_graphql_query


async def get_trips(token: str):
    query = """
    query {
        trips {
            count
            trips {
                id
                origin
                destination
                distance
                fare
                duration
                startDateTime
                endDateTime
                status
                createdAt
                updatedAt
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
                user {
                    id
                    firstName
                    lastName
                    email
                    phoneNumber
                    registrationDate
                    averageRating
                    location
                    createdAt
                    updatedAt
                }
            }
        }
    }

    """
    response = await execute_graphql_query(query, None, token)
    trips_data = response.get("data", {}).get("trips", {})
    return TripsResponse(**trips_data)


async def get_trip(trip_id: int, token: str):
    query = """
    query {
        trip(id: 4) {
            id
            origin
            destination
            distance
            fare
            duration
            startDateTime
            endDateTime
            status
            createdAt
            updatedAt
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
            user {
                id
                firstName
                lastName
                email
                phoneNumber
                registrationDate
                averageRating
                location
                createdAt
                updatedAt
            }
        }
    }
    """
    variables = {"id": trip_id}
    response = await execute_graphql_query(query, variables, token)
    trip_data = response.get("data", {}).get("trip", {})
    return trip_data
