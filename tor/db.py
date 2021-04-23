#from flask import current_app, g
from tor.config import Config
from pymongo import MongoClient
from werkzeug.local import LocalProxy

### connection
myMongoURI=Config.connect_string
myClient = MongoClient(myMongoURI)
myDatabase=Config.dbname

## collections used
templates = "templates"


def get_db():
    """
    Configuration method to return db instance.
    Maximum connection pool size to 50 active connections.
    Write concern timeout limit to 2500 milliseconds to prevent the program from waiting indefinitely.
    """

    db_URI = Config.connect_string
    db_NAME = Config.dbname
    db = MongoClient(db_URI,
        maxPoolSize=50,
        wTimeoutMS=2500)[db_NAME]
    
    return db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def get_coll_names():
    return list(db.list_collection_names())

def get_table_info(lang, body, template):
    """ 
    Get the header info by language
    """
    pipeline = []

    match_stage = {
        '$match': {
            'body': body, 
            'template': template
        }
    } 
    
    transform = {}
    transform['_id'] = 0
    transform['column_span'] = 1
    transform['summary'] = '$summary.' + lang
    transform['sequence'] = '$sequence.' + lang
    transform['links_txt'] = '$links_txt.' + lang
    transform['column_headers'] = '$column_headers.' + lang

    transform_stage = {}
    transform_stage['$project'] = transform

    pipeline.append(match_stage)
    pipeline.append(transform_stage)

    try:
        #print(list(db.templates.aggregate(pipeline)))
        return list(db.templates.aggregate(pipeline))

    except Exception as e:
        return e