from server.models.admin_models import Admin
from .graphql_service import execute_graphql_query


async def authenticate_admin(email: str, password: str):
    graphql_mutation = """
    mutation LoginAdmin($email: String!, $password: String!) {
        loginAdmin(email: $email, password: $password) {
            admin {
                id
                firstName
                lastName
                email
                phoneNumber        
            }
            token
        }
    }
    """
    variables = {"email": email, "password": password}
    response = await execute_graphql_query(graphql_mutation, variables)

    admin_data = response.get("data", {}).get("loginAdmin", {})

    if not admin_data:
        return None

    admin = Admin(**admin_data["admin"])
    token = admin_data["token"]

    if admin and token:
        return admin, token
    else:
        return None, None
