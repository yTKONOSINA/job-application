# import zenml
from bson.objectid import ObjectId
from zenml import pipeline

from get_create_user import get_create_user
from parse_links import parse_links

@pipeline
def digital_data_etl(user_full_name : str, links : list[str]):
    user_id = get_create_user(user_full_name)
    parse_links(user_id, links)

if __name__ == '__main__':
    
    import yaml

    with open('../users.yaml', 'r') as file:
        data = yaml.safe_load(file)
    
    for user in data['users']:
        links = [link for link in user['links']]
        digital_data_etl(user['full_name'], links)