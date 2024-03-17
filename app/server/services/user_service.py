from server.models.user_models import UsersResponse
from .graphql_service import execute_graphql_query


async def get_users(token: str):
    query = """
    query {
        users {
            count
            users {
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
    users_data = response.get("data", {}).get("users", {})
    return UsersResponse(**users_data)


async def get_user(user_id: int, token: str):
    query = """
    query GetUser($id: Int!) {
        user(id: $id) {
            user {
                id
                firstName
                lastName
                email
                phoneNumber
                location
                averageRating
                createdAt
                updatedAt
            }
            trips {
                count
                trips {
                    id
                    origin
                    destination
                }
            }
        }
    }
    """
    variables = {"id": user_id}
    response = await execute_graphql_query(query, variables, token)
    user_data = response.get("data", {}).get("user", {})
    return user_data
