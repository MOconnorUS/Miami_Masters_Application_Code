from pymongo_get_database import get_database
import pymongo

def drop_all_tourneys():
    dbname = get_database()
    collection_name = dbname["tournaments"]

    result = collection_name.delete_many({})

    return None

def drop_all_links():
    dbname = get_database()
    collection_name = dbname["links"]

    result = collection_name.delete_many({})

    return None   

# drop_all()

    
