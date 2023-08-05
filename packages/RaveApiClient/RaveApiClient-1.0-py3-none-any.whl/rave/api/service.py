from json import JSONDecodeError, dumps

from requests import get as _get, post as _post, delete as _delete, put as _put

from . import headers
from .exceptions import handle_exception


class Service:
  def __init__(self, proxies: dict = None):
    self.api = "https://api.red.wemesh.ca{}".format
    self.mojoauth = "https://api.mojoauth.com{}".format
    self.proxies = proxies
    self.deviceId = None
    self.sessionId = None

  def __compose(self, response):

    try:
      body = response.json()
    except JSONDecodeError:
      print (response.text)
      body = {}
    
    return body

  def mojo_post(self, path: str, data: dict = None, params: dict = None) -> dict:
    data = dumps(data)
    response = _post(self.mojoauth(path), data=data, params=params, headers=headers.Headers().mojo, proxies=self.proxies)
    return self.__compose(response)
    
  def mojo_get(self, path: str, params: dict = None) -> dict:
    response = _get(self.mojoauth(path), params=params, headers=headers.Headers().mojo, proxies=self.proxies)
    return self.__compose(response)

  def post(self, path: str, data: dict = None, params: dict = None) -> dict:
    data = dumps(data)
    response = _post(self.api(path), data=data, params=params, headers=headers.Headers(data).headers, proxies=self.proxies)
    return self.__compose(response)

  def get(self, path: str, params: dict = None) -> dict:
    response = _get(self.api(path), params=params, headers=headers.Headers().headers, proxies=self.proxies)
    return self.__compose(response)
    
  def delete(self, path: str, params: dict = None) -> dict:
    response = _delete(self.api(path), params=params, headers=headers.Headers().headers, proxies=self.proxies)
    return self.__compose(response)
    
  def put(self, path: str, data: dict = None) -> dict:
    response = _put(self.api(path), data=data, headers=headers.Headers(data).headers, proxies=self.proxies)
    return self.__compose(response)

  def getRequest(self, url: str, params: dict = {}):
    response = _get(url, params=params, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}, proxies=self.proxies)
    return response

  def postRequest(self, url: str, data: dict = None, params: dict = None, headers: dict = {}) -> dict:
    response = _post(url, data=data, params=params, headers=headers, proxies=self.proxies)
    return response

  def deleteRequest(self, url: str, params: dict = None) -> dict:
    response = _delete(url, params=params, headers=headers.Headers().headers, proxies=self.proxies)
    return response
    
  def putRequest(self, url: str, data: dict = None, _headers: dict = {}) -> dict:
    response = _put(url, data=data, headers=_headers, proxies=self.proxies)
    return self.__compose(response)

	

  
    
    
