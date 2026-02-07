from dataclasses import dataclass

from environs import Env


@dataclass
class JWToken:
    pass


@dataclass
class DataBaseSession:
    database_url: str


@dataclass
class Config:
    jwtoken: JWToken
    databasesession: DataBaseSession


def load_config(path: str | None = None) -> Config:
    env = Env
    env.read_env(path)
    return Config(databasesession=DataBaseSession(database_url="DATABASE_URL"))
