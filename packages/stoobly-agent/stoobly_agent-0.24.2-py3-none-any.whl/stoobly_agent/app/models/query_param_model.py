import pdb
import requests

from typing import Union

from stoobly_agent.app.models.types.request_components import QueryParamIndexResponse
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import Logger

from .factories.resource.query_param import QueryParamResourceFactory
from .model import Model

class QueryParamModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
    self.adapter =  QueryParamResourceFactory(self.settings.remote).local_db()

  def as_remote(self):
    #raise('Not yet supported.')
    pass

  def index(self, request_id: str, **query_params) -> Union[QueryParamIndexResponse, None]:
    try:
      return self.adapter.index(request_id, **query_params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def __handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")