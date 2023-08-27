#### Miami 4 + 1 Masters Application Object Oriented Project
#### Matthew O'Connor

# Imports
from pymongo_get_database import get_database
import pymongo

# All information within the tournaments document is dropped
# @return None
def drop_all_tourneys():
    dbname = get_database()
    collection_name = dbname["tournaments"]

    result = collection_name.delete_many({})

    return None

# All information within the links document is dropped
# @return None
def drop_all_links():
    dbname = get_database()
    collection_name = dbname["links"]

    result = collection_name.delete_many({})

    return None   


    
