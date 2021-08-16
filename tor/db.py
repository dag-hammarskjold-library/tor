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
    transform['table_title'] = '$table_title.' + lang
    transform['table_note'] = '$table_note.' + lang
    transform['sequence'] = '$sequence.' + lang

    transform_stage = {}
    transform_stage['$project'] = transform

    pipeline.append(match_stage)
    pipeline.append(transform_stage)

    try:
        #print(list(db.templates.aggregate(pipeline)))
        return list(db.templates.aggregate(pipeline))

    except Exception as e:
        return e

def get_ga_regular(lang, session):
    """ 
    Get the GA Regular Session table info by language and session
    """
    pipeline = []

    match_stage = {
        '$match': {
            'template': 'Regular Sessions', 
            'session': str(session)
        }
    } 

    transform = {}
    transform['_id'] = 0

    transform['res_doc'] = '$resolution.doc_symbol'
    transform['res_url'] = '$resolution.url_suffix'
    transform['plen_ctte'] = 1
    transform['agenda'] = 1
    transform['meet_doc'] = '$meeting.doc_symbol'
    transform['meet_url'] = '$meeting.url_suffix'
    transform['date'] = '$date.' + lang 
    

    if lang == 'es':
        press_lang = 'en'
    else:
        press_lang = lang

    transform['press_yr'] = '$press.year'
    transform['press_release'] = '$press.release.' + press_lang 
    transform['press_url'] =  {
        '$let': {
            'vars': {
                'release': {'$split': ['$press.release.' + press_lang, '/']}}, 
            'in': {
                '$concat': [
                    {'$toLower': {'$arrayElemAt': ['$$release', 0]}}, 
                    {'$arrayElemAt': ['$$release', 1]}
                ]
            }
        }
    } 
    transform['vote'] = '$vote.' + lang 
    transform['draft'] = '$draft'
    transform['topic'] = '$topic.' + lang

    transform_stage = {}
    transform_stage['$project'] = transform

    pipeline.append(match_stage)
    pipeline.append(transform_stage)

    try:
        return list(db.records.aggregate(pipeline))

    except Exception as e:
        return e

def get_sc_veto(lang):
    """ 
    Get the SC Veto table info by language
    """
    pipeline = []

    match_stage = {
        '$match': {
            'template': 'Vetoes', 
        }
    } 

    transform = {}
    transform['_id'] = 0

    transform['date'] = '$date.' + lang 
    transform['draft'] = 1
    transform['written_record'] = 1 
    transform['agenda_item'] = '$agenda_item.' + lang 
    transform['pm_negative_vote'] = '$pm_negative_vote.' + lang 

    transform_stage = {}
    transform_stage['$project'] = transform

    pipeline.append(match_stage)
    pipeline.append(transform_stage)

    try:
        return list(db.records.aggregate(pipeline))

    except Exception as e:
        return e
