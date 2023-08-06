import decimal
import json
import logging
import logging.config
import logging.handlers
import os
import warnings
from abc import abstractmethod
from contextlib import contextmanager
from copy import deepcopy
from typing import Optional, List, Union

import redis
from elasticsearch import Elasticsearch
from pydantic import BaseSettings, Field, BaseConfig, Extra
from pydantic.typing import StrPath
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from joeypan import RESOURCE_JOEYPAN_DIR

# disable warning: pydantic set alias_namefor klass -> class
warnings.filterwarnings("ignore", category=FutureWarning)
LOG = logging.getLogger(__name__)


class InjectSettings:
    __DEFAULT_LOG_DIR = os.environ.get("LOG_DIR") or os.path.join(os.getcwd(), "logs")

    @property
    def default_log_dir(self) -> str:
        return self.__DEFAULT_LOG_DIR

    def set_default_log_dir(self, log_dir: StrPath):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.__DEFAULT_LOG_DIR = log_dir


inject_settings = InjectSettings()


class AbstractSettings(BaseSettings):
    def update(self, new):
        old_data = self.dict()
        new_data = new.dict()
        old_data.update(new_data)
        return new.__class__(**old_data)

    @property
    def namespace(self):
        return self.__class__.__name__

    class Config(BaseConfig):
        env_prefix: str = 'joeypan__'
        env_nested_delimiter: Optional[str] = "__"
        secrets_dir: Optional[StrPath] = None
        validate_all: bool = True
        extra: Extra = Extra.allow
        case_sensitive: bool = False
        anystr_strip_whitespace: bool = True
        fields = {"klass": {"alias": "class"}}

    def json(self, *args, **kwargs) -> str:
        return super().json(by_alias=True)

    def dict(self, *args, **kwargs):
        return super().dict(by_alias=True)


class Servlet(AbstractSettings):
    context_path: str = Field(default=os.getcwd())


class Server(AbstractSettings):
    port: int = Field(8080, description="服务端口")
    servlet: Servlet = Field(default_factory=Servlet)


class Datasource(AbstractSettings):
    SCOPED_SESSION: scoped_session = None
    url: str = Field(
        default="mysql+pymysql://user:password@localhost:3306/foo?charset=utf8mb4")
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 10
    pool_timeout: int = 3
    pool_recycle: int = 10
    pool_use_lifo: bool = True
    query_cache_size: int = 500

    @property
    def __session(self) -> scoped_session:
        if self.SCOPED_SESSION:
            return self.SCOPED_SESSION
        cfg = self.dict()
        cfg.pop("SCOPED_SESSION", None)
        url = cfg.pop("url", None)
        engine = create_engine(url, **cfg)
        session_factory = sessionmaker(engine)
        self.SCOPED_SESSION = scoped_session(session_factory)
        return self.SCOPED_SESSION

    @property
    @contextmanager
    def session(self) -> Session:
        session = self.__session()
        try:
            yield session
            session.commit()
        except Exception as e:
            LOG.error(f"commit failed: {e}")
            session.rollback()
            raise e
        finally:
            session.close()


class JedisPool(AbstractSettings):
    pass


class Redis(AbstractSettings):
    POOL: Union[redis.Redis, redis.RedisCluster] = None
    db: int = Field(default=0)
    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    password: str = None,
    startup_nodes: list = None
    jedis: JedisPool = Field(default_factory=JedisPool)

    @property
    def session(self):
        if not self.POOL:
            if self.startup_nodes:
                kwargs = self.jedis.dict()
                klass = redis.RedisCluster
            else:
                kwargs = {
                    "db": self.db,
                    "host": self.host,
                    "port": self.port,
                    "password": self.password
                }
                kwargs.update(self.jedis.dict())
                klass = redis.Redis
            self.POOL = klass(**kwargs)
        return self.POOL


class LogFormat(AbstractSettings):
    pass


class SimpleFormat(LogFormat):
    format: str = Field(default='%(asctime)s %(levelname)s %(message)s')


class UpgradeFormat(LogFormat):
    format: str = Field(
        default="%(asctime)s -Loc %(filename)s -Pid %(process)d -%(name)s -%(levelname)s - %(message)s")


class LogFormats(AbstractSettings):
    simple: SimpleFormat = Field(default_factory=SimpleFormat)
    upgrade: UpgradeFormat = Field(default_factory=UpgradeFormat)


class LogHandler(AbstractSettings):
    pass


class LogConsoleHandler(LogHandler):
    klass: str = Field(default="logging.StreamHandler")
    level: int = Field(default=logging.DEBUG)
    formatter: str = Field(default="simple")
    stream: str = Field(default="ext://sys.stdout")


class LogFileHandler(LogHandler):
    klass: str = Field(default="logging.handlers.RotatingFileHandler")
    level: int = Field(default=logging.DEBUG)
    formatter: str = Field(default="upgrade")
    filename: StrPath = Field(default="all.log")
    maxBytes: int = Field(default=4194304)  # 4MB
    backupCount: int = Field(default=50)  # 保留多少个log文件
    encoding: str = Field(default="utf8")


class LogServerHandler(LogFileHandler):
    klass: str = Field(default="logging.handlers.RotatingFileHandler")
    level: int = Field(default=logging.DEBUG)
    formatter: str = Field(default="simple")
    filename: StrPath = Field(default="server.log")
    maxBytes: int = Field(default=4194304)  # 4MB
    backupCount: int = Field(default=20)  # 保留多少个log文件
    encoding: str = Field(default="utf8")


class LogHandlers(AbstractSettings):
    console_handler: LogHandler = Field(default_factory=LogConsoleHandler)
    file_handler: LogHandler = Field(default_factory=LogFileHandler)
    server_handler: LogHandler = Field(default_factory=LogServerHandler)


class LoggerInstance(AbstractSettings):
    level: int = Field(default=logging.DEBUG)
    handlers: List[str] = Field(default=["console_handler"])


class LoggerInstances(AbstractSettings):
    server: LoggerInstance = Field(
        default=LoggerInstance(handlers=["server_handler"]))
    platform: LoggerInstance = Field(
        default=LoggerInstance(handlers=["platform_handler"]))
    security: LoggerInstance = Field(
        default=LoggerInstance(handlers=["security_handler"]))
    audit: LoggerInstance = Field(
        default=LoggerInstance(handlers=["audit_handler"]))
    access: LoggerInstance = Field(
        default=LoggerInstance(handlers=["access_handler"]))


class Logger(AbstractSettings):
    version: int = Field(default=1)
    disable_existing_loggers: bool = Field(default=True)
    formatters: LogFormats = Field(default_factory=LogFormats)
    handlers: LogHandlers = Field(default_factory=LogHandlers)
    loggers: LoggerInstances = Field(default_factory=LoggerInstances)


class ES(AbstractSettings):
    INSTANCE: Elasticsearch = None
    hosts: List[dict] = Field(default=[{"host": "localhost", "port": 9200}])
    kwargs: dict = Field(default_factory=dict)

    @property
    def session(self) -> Elasticsearch:
        if not self.INSTANCE:
            self.INSTANCE = Elasticsearch(hosts=self.hosts, **self.kwargs)
        return self.INSTANCE


class DefaultSettings(AbstractSettings):
    server: Server = Field(default_factory=Server)
    datasource: Datasource = Field(default_factory=Datasource)
    redis: Redis = Field(default_factory=Redis)
    log: Logger = Field(default_factory=Logger)
    es: ES = Field(default_factory=ES)


class UserSettings(DefaultSettings):
    pass


class SettingsLoader(object):

    @abstractmethod
    def load(self) -> dict:
        pass


class JsonLoader(SettingsLoader):
    # json.loads加载Loader
    def __int__(self, data: str):
        self.data = data

    def load(self):
        return json.loads(self.data, parse_float=decimal.Decimal)


class DictLoader(SettingsLoader):
    # 最简单的字典Loader
    def __init__(self, data: dict):
        self.data = data

    def load(self):
        return self.data


class FileLoader(SettingsLoader):
    def __init__(self, file_path: StrPath):
        self.data = file_path

    def load(self):
        with open(self.data, mode="r", encoding="utf-8") as fh:
            return json.load(fh, parse_float=decimal.Decimal)


class SettingsFactory:
    INSTANCE = {}

    @classmethod
    def create_settings_by_loader(cls, loader: SettingsLoader):
        return cls.create(loader.load())

    @classmethod
    def create(cls, data_json: dict) -> UserSettings:
        name = data_json.pop("joeypan_settings_name",
                             None) or "default_joeypan_settings"
        if name in cls.INSTANCE:
            return cls.INSTANCE.get(name)
        _instance = UserSettings(**data_json)
        cls.INSTANCE[name] = _instance
        cls.setup_log(_instance.log)
        return cls.INSTANCE.get(name)

    @classmethod
    def setup_log(cls, cfg: Logger):
        def update_log_path(file_name):
            if file_name and os.path.basename(file_name) == file_name:
                return os.path.join(inject_settings.default_log_dir, file_name)
            return file_name

        def update_dict(data: dict):
            if data.get("filename"):
                data["filename"] = update_log_path(data.get("filename"))
            return data

        temp_cfg = deepcopy(cfg)
        temp_handlers = {}
        for name, handler in cfg.handlers:
            if isinstance(name, (str, bytes)):
                if isinstance(handler, LogHandler):
                    if hasattr(handler, "filename"):
                        handler.filename = os.path.join(inject_settings.default_log_dir, handler.filename)
                    temp_handlers[name] = handler
                elif isinstance(handler, dict):
                    temp_handlers[name] = update_dict(handler)
        temp_cfg.handlers = temp_handlers
        logging.config.dictConfig(temp_cfg.dict())

    @classmethod
    def default(cls):
        config_json_path = os.path.join(RESOURCE_JOEYPAN_DIR, "template.json")
        with open(config_json_path, "r", encoding="utf-8") as f:
            return cls.create(json.load(f))
