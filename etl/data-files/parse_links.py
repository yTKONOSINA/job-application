from uuid import UUID, uuid4
from basefile import User
from bson.objectid import ObjectId
from parsers import Director
from zenml import step

@step(enable_cache=False)
def parse_links(user_uuid : ObjectId, links : list):
    director = Director()
    user = User(uuid=user_uuid)
    for link in links:
        file_contents = director.extract(link=link)
        # if change the file depending on the content, not always gitrepo
        user.create_gitrepo().write_to_mongo(content=file_contents)

if __name__ == '__main__':
    pass