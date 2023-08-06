import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, aliased, Session
from sqlalchemy import *
from sqlalchemy import and_, or_
from sqlalchemy.engine.base import Engine
from typing import Dict, Any


class AlbertWarehouseInterface:
    # Interface which can be used to run sqlalchemy queries against the db warehouse
    def __init__(
        self,
        username: str | None,
        password: str | None,
        host: str | None,
        port: int | None,
        database: str | None,
    ):
        self._db_username: str | None = username
        self._db_password: str | None = password
        self._db_host: str | None = host
        self._db_port: int | None = port
        self._db_database: str | None = database
        self.__db_engine: Engine | None = None
        self.__db_session: Session | None = None

    def db_open(self):
        def valid(val: str | int | None):
            return val not in [None, ""]

        if (
            not valid(self._db_username)
            or not valid(self._db_password)
            or not valid(self._db_host)
            or not valid(self._db_port)
            or not valid(self._db_database)
        ):
            raise ValueError(
                "missing db configuration data, check that all values are"
                " supplied before calling db_open"
            )

        self.__db_engine = create_engine(
            f"mysql+pymysql://{self._db_username}:{self._db_password}@{self._db_host}:{self._db_port}/{self._db_database}",
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"init_command": "SET SESSION max_execution_time = 600000"},
        )
        self.__db_engine.connect()
        self.__db_session = sessionmaker(bind=self.__db_engine)()

    def db_close(self) -> None:
        if self.__db_session is not None:
            self.__db_session.close()
        self.__db_session = None
        self.__db_engine = None

    def DWH_Session(self) -> Session:
        if self.__db_session is None:
            self.db_open()

        # Make sure we are returning a valid session object
        assert self.__db_session is not None, "unable to create valid warehouse session"
        return self.__db_session

    def raw_query(self, query: str) -> Any:
        return self.DWH_Session().execute(text(query))

    def __getstate__(self) -> Dict[str, Any]:
        """
        Custom getstate to avoid trying to pickle the engine or session objects
        since they are stateful and we don't want to try to pass them
        """
        return {
            "host": self._db_host,
            "password": self._db_password,
            "user": self._db_username,
            "port": self._db_port,
            "db": self._db_database,
        }

    def __setstate__(self, state_info: Dict[str, Any]):
        self._db_host = state_info["host"]
        self._db_password = state_info["password"]
        self._db_username = state_info["user"]
        self._db_port = state_info["port"]
        self._db_database = state_info["db"]
