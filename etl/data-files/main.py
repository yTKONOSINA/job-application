# import zenml
from bson.objectid import ObjectId
from zenml import pipeline, ExternalArtifact
from loguru import logger

from get_create_user import get_create_user
from parse_links import parse_links

@pipeline(enable_cache=False)
def digital_data_etl(user_full_name : str, links : list[str]):
    user_id = get_create_user(user_full_name)
    logger.info(f"user's full name is {user_full_name} and the id is {user_id}")
    external_links = ExternalArtifact(value = links)
    parse_links(user_id, links)

if __name__ == '__main__':

    # disables all caching in a pipeline
    # first_pipeline = first_pipeline.with_options(enable_cache=False)
    # i can also do the same with a step
    
    import yaml

    with open('../users.yaml', 'r') as file:
        data = yaml.safe_load(file)
    
    for user in data['users']:
        links = [link for link in user['links']]
        digital_data_etl(user['full_name'], links)