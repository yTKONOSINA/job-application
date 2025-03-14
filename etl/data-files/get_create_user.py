from uuid import UUID, uuid4
from typing import Annotated
from bson.objectid import ObjectId
from zenml import step, log_artifact_metadata
from database import DataBase
from datetime import datetime

users_collection = DataBase().users_collection

@step(enable_cache=False)
def get_create_user(user_full_name: str) -> Annotated[ObjectId, 'User ID']:
    """
    Searches or creates a user using their full name
    Args:
        user_full_name (str): The full name of the user to search for or create
    Returns:
        ObjectId: The MongoDB ObjectId of the existing or newly created user
    """
    # Search for existing user by full name
    existing_user = users_collection.find_one({"full_name": user_full_name})
    
    # If user exists, return their ObjectId
    if existing_user:
        return ObjectId(existing_user["_id"])
    
    # If user doesn't exist, create new user and return their ObjectId
    new_user = {
        "full_name": user_full_name,
        "created_at": datetime.now(),
        "uuid": uuid4()
    }
    result = users_collection.insert_one(new_user)

    log_artifact_metadata(
        artifact_name = f"User_ID",
        version = None,
        metadata = {"User's full name is " : user_full_name}
    )

    return ObjectId(result.inserted_id)

if __name__ == '__main__':
    user_id = get_create_user("John Doe")
    print(user_id)
