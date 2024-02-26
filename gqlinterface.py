from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from user import User

class GqlInterface:
    def __init__(self):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://graphql.40eggs.com/v1/graphql")

        # Create a GraphQL client using the defined transport
        self.client = Client(transport=transport, fetch_schema_from_transport=False)
    
    def getUsers(self):
        query = gql(
        """
            query GetUsers {
                fitness_data_users(order_by: {}, where: {}) {
                    created_at
                    id
                    updated_at
                    username
                }
            }
        """
        )
        users = None
        try:
            result = self.client.execute(query)
            users = []
            for user in result["fitness_data_users"]:
                users.append(User(user["id"], user["username"], user["created_at"], user["updated_at"]))
        except Exception as e:
            print("Unable to get users: " + repr(e))
            return None
        return users
    
    def addWeight(self, userId, weight, date):
        query = gql(
        f"""
            mutation AddWeight {{
            insert_fitness_data_daily_weights(objects: {{date: "{date}", user_id: "{userId}", weight: "{weight}"}}) {{
                returning {{
                created_at
                id
                date
                updated_at
                user_id
                weight
                }}
            }}
            }}
        """
        )
        result = None
        try:
            result = self.client.execute(query)
        except Exception as e:
            print("Unable to add weight: " + repr(e))
            return None
        print(result)
        return result
    
fitnessGql = GqlInterface()
print(fitnessGql.getUsers())