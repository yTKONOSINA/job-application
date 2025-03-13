import uuid
from abc import ABC, abstractmethod
from pymongo import MongoClient 


from database import users_collection

class Document:
    def __init__(self, uuid):  # Added default value for info
        self.uuid = uuid

    def write_to_mongo(self, content):
        result = users_collection.update_one(
            {'_id': self.uuid},  # Query to find user by UUID
            {'$push': {'content': {'$each': content}}},  # Append each item in the list
            upsert=False  # Don't create new document if user isn't found
        )

        assert result.matched_count > 0, 'The user does not exist'


class PDFDocument(Document):
    @classmethod
    def create(cls, basedocument):
        return cls(uuid=basedocument.uuid)

class WordDocument(Document):
    @classmethod
    def create(cls, basedocument):
        return cls(uuid=basedocument.uuid)

class GitRepo(Document):
    @classmethod
    def create(cls, basedocument):
        return cls(uuid=basedocument.uuid)

class User:
    def __init__(self, uuid):
        self.basedocument = Document(uuid=uuid)  # Fixed info reference

    def create_pdf(self):
        return PDFDocument.create(basedocument=self.basedocument)

    def create_word(self):
        return WordDocument.create(basedocument=self.basedocument)
    
    def create_gitrepo(self):
        return GitRepo.create(basedocument=self.basedocument)

if __name__ == "__main__":

    # Using it
    user1 = User(uuid=123)
    print(type(user1.create_pdf()) == PDFDocument)
    user1.create_pdf().write_to_mongo(content={"data": "PDF content"})
    user1.create_word().write_to_mongo(content={"data": "Word content"})
    print('\n')
    user2 = User(uuid=288)
    user2.create_pdf().write_to_mongo(content={"data": "PDF content"})
    user2.create_word().write_to_mongo(content={"data": "funny content"})
