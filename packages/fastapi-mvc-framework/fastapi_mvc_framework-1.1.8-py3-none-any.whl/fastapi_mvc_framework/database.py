from sqlalchemy import create_engine,Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text,TextClause
 
from alembic import command
from alembic.config import Config
import configparser
import re,os
from typing import Union
from .config import _log

engine:Engine=None 
class Base(DeclarativeBase):
    pass
class Service():
    @classmethod
    def execute(cls,cmd:Union[str,TextClause],**kwargs):
        if not isinstance(cmd,TextClause):
            cmd = text(str)
        with engine.begin() as conn:
            ret = conn.execute(cmd,**kwargs)
        return ret
     

def sanitize_path(path):
    # 匹配非法字符
    illegal_chars = r'[\\/:\*\?"<>\|]'
    # 将非法字符替换为下划线
    sanitized_path = re.sub(illegal_chars, '_', path)
    return sanitized_path

def __check_migration(engine,uri,alembic_ini): 
    def _update_uri_to_ini(): 
        #auto update alembic.ini sqlalchemy.url section 
        config = configparser.ConfigParser() 
        # read ini config
        config.read(alembic_ini)
        config.set('alembic','sqlalchemy.url',uri)
        # save modified ini file
        with open(alembic_ini, 'w') as f:
            config.write(f)
        #makesure the migrations directory exists
        reversions_dir = config.get("alembic",'script_location')
        reversions_dir = os.path.join(reversions_dir,"versions")
        if not os.path.exists(reversions_dir):
            os.makedirs(reversions_dir,exist_ok=True)

    _update_uri_to_ini()
    #  
    alembic_cfg = Config(alembic_ini)   
    #  
     
    try:
        command.check(config=alembic_cfg)
    except Exception as e: 
        msg = sanitize_path(str(e.args)) 
        command.revision(alembic_cfg, autogenerate=True, message=msg) 
        # upgrade the db
        command.upgrade(alembic_cfg, "head") 

def init_database( uri:str,debug:bool=False,alembic_ini:str=""):
    '''
    params :uri sqlalchemy connection string
    :params debug mode of debug 
    :params alembic_ini alembic config file path,when debug=True will auto migrate the changes 
    '''
    engine = create_engine(uri, echo=debug)
    
    if debug and alembic_ini:
        try:
            #Base.metadata.create_all(engine)
            __check_migration(engine,uri,alembic_ini)
        except Exception as e:
            _log.error(e.args)
    #test connect
    try:
        with engine.connect() as conn:
            _log.disabled = False
            _log.debug('database connection successed:' + str(conn))

    except Exception as e:
        _log.disabled = False
        _log.error("database connection failed!")  
         
        exit(1)  

    return engine
 