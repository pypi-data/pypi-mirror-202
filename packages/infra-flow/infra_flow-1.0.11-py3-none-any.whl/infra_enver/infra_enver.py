import requests
from . import config
from . import infra_enver_exceptions as ee
import typing as t
from . import cache
import redis

REQUEST_TIME_OUT = 5


class Enver(object):
    """
    Attributes:
        service_url - url of settings service.

        is_fallback_enabled - if lib can't get setting from redis,
            infra_enver will try to get setting directly from settings service.
    """

    project_name: str
    secret_key: str
    is_fallback_enabled: bool
    redis_connection: redis.Redis

    def __getattr__(self, item):
        return self.get_setting(item)

    def __init__(
            self,
            project_name: str,
            secret_key: str,
            redis_host: str,
            redis_db_num: int,
            redis_password: str,
            service_url: str,
            is_fallback_enabled: bool = False,
    ):
        self.project_name = project_name
        self.secret_key = secret_key
        self.is_fallback_enabled = is_fallback_enabled
        self.redis_connection = redis.Redis(host=redis_host, port=6379, db=redis_db_num, password=redis_password)
        self.settings_service_url = service_url + config.SETTINGS_URL
        self.experiments_service_url = service_url + config.EXPERIMENT_URL

    def get_setting(self, setting_name: str):
        try:
            return cache.get_value(self.redis_connection, setting_name)
        except Exception as ex:
            if self.is_fallback_enabled:
                json = {
                    "project_name": self.project_name,
                    "secret_key": self.secret_key
                }
                r = requests.post(self.settings_service_url + setting_name, json=json, timeout=REQUEST_TIME_OUT)
                if not r.ok:
                    raise ee.InfraEnverException(r.text)
                return r.json()['value']
            raise ee.InfraEnverException(ex)

    def get_experiment(self, experiment_name: str, arg: t.Any, fallback_value: t.Any = None):
        json = {
            "project_name": self.project_name,
            "secret_key": self.secret_key,
            "experiment_name": experiment_name,
            "arg": arg
        }
        try:
            r = requests.post(self.experiments_service_url, json=json, timeout=REQUEST_TIME_OUT)
            if not r.ok:
                return fallback_value
            return r.json()
        except Exception as ex:
            if fallback_value is not None:
                return fallback_value
            else:
                raise ee.InfraEnverException(str(ex))
