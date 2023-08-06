from sqlalchemy import create_engine,Engine
from sqlalchemy.orm import DeclarativeBase
from alembic import command
from alembic.config import Config
import configparser
import re,os
engine:Engine=None 
class Base(DeclarativeBase):
    pass


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
        # 读取配置文件
        config.read(alembic_ini)
        config.set('alembic','sqlalchemy.url',uri)
        # 保存修改后的配置文件
        with open(alembic_ini, 'w') as f:
            config.write(f)
        reversions_dir = config.get("alembic",'script_location')
        if not os.path.exists(reversions_dir):
            os.makedirs(reversions_dir,exist_ok=True)

    _update_uri_to_ini()
    # 创建 alembic 配置对象
    alembic_cfg = Config(alembic_ini)   
    # 自动检测变更并生成迁移脚本
     
    try:
        command.check(config=alembic_cfg)
    except Exception as e: 
        msg = sanitize_path(str(e.args)) 
        command.revision(alembic_cfg, autogenerate=True, message=msg) 
        # 执行数据库迁移
        command.upgrade(alembic_cfg, "head") 

def init_database( uri:str,debug:bool=False,alembic_ini:str=""):
    '''
    params :uri sqlalchemy 的连接字符串
    :params debug 是否调试模式
    :params alembic_ini alembic的配置文件路径,debug=True时则会执行数据迁移
    '''
    engine = create_engine(uri, echo=debug)
    if debug and alembic_ini:
        __check_migration(engine,uri,alembic_ini)
    return engine
 