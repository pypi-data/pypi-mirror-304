"""
Naumen Servive Desk python API client.
"""

import requests
import urllib3
from json import loads

# from naumen_service_desk_client.types import HeaderModel

class NaumenSDClient:
    """
    Naumen Servive Desk Client class.
    Require:
        - base_url: NSD instanse url
        - token: NSD token
    """

    def __init__(self, base_url: str, token: str) -> None:
        urllib3.disable_warnings()
        self.session = requests.Session()
        self.base_url = base_url
        self.token = token

    def create_class_from_attributes(class_name:str, attributes:dict[str:str]):
        annotations = {}
        class_dict = {}
        
        for attr, attr_type in attributes:
            annotations[attr] = attr_type
            class_dict[attr] = None 

        class_dict['__annotations__'] = annotations
        new_class = type(class_name, (object,), class_dict)    
        return new_class

    def __get_request_module_url(self, function:str, params:list[any]) -> str:
        """Get url for a request with a token"""
        query = ""
        for attr in params:
            query += f"\"{attr}\","
        return f"{self.base_url}/sd/services/rest/exec?func={function}&params={query}&accessKey={self.token}"
    
    def __return_attrs_forrmater(self, params:list[str]) -> str:
        result = "&attrs="
        for attr in params:
            result += f"{attr},"
        return result
    
    def __get_base_request_url(self, method:str, attrs_for_return:list[str] = None):
        url = f"{self.base_url}/sd/services/rest/{method}?accessKey={self.token}"

        if attrs_for_return:
            url += self.__return_attrs_forrmater(attrs_for_return)

        return url

    def __get_request(self, method:str, attrs_for_return:list[str] = None, return_json:bool = True):
        response = self.session.get( 
            self.__get_base_request_url(method, attrs_for_return), 
            verify=False 
        )

        if response.status_code > 400:
            raise ValueError(response.text)

        if response.status_code < 300:
            if return_json:
                return response.json()
        
        return response.text
    
    def __post_request(self, method:str, body:dict, attrs_for_return:list[str], return_json:bool=True):
        response = self.session.post( 
            self.__get_base_request_url(method, attrs_for_return), 
            json=body,
            verify=False 
        )

        if response.status_code > 400:
            raise ValueError(response.text)
        
        if response.status_code < 300:
            if return_json:
                return response.json()
            
        return response.text

    def __send_file_request(self, url:str, file):
        response = self.session.post( 
            url, 
            files=file,
            verify=False 
        )

        if response.status_code > 400:
            raise ValueError(response.text)
        
        if response.status_code < 300:
            try:
                return response.json()
            except Exception:
                return response.text
            
        return response.text

    def module(self, module_name:str, method_name:str, params:list) -> dict:
        response = self.session.get(
            self.__get_request_module_url(f"modules.{module_name}.{method_name}", params),
            verify=False,
        )
        response.raise_for_status()
        return response.json()
    
    def get_properties_theme_by_code(self, code:str) -> dict:
        response = self.session.get(
            f"{self.base_url}/sd/jspresource?id=common&method=theme&theme={code}",
            verify=False,
        )
        response.raise_for_status()
        durty_test = response.text
        return loads(durty_test.replace('var themeProperties = ' , '').replace(';', ''))
    
    def health_check(self) -> str:
        response = self.session.get(
            f"{self.base_url}/sd/services/rest/check-status",
            verify=False,
        )
        response.raise_for_status()
        return response.text
    
    def find(self, meta_class:str, filter:dict = {}, attrs_for_return:list[str] = None) -> list[dict]:
        return self.__post_request(f"find/{meta_class}", filter, attrs_for_return)

    def get(self, uuid:str, attrs_for_return:list[str] = None) -> dict:
        return self.__get_request(f"get/{uuid}", attrs_for_return)
    
    def delete(self, uuid:str) -> None:
        self.__get_request(method=f"delete/{uuid}")

    def create(self, meta_class:str, attributes:dict, attrs_for_return:list[str] = None) -> dict:
        return self.__post_request(f"create-m2m/{meta_class}", attributes, attrs_for_return)

    def edit(self, meta_class:str, attributes:dict, attrs_for_return:list[str] = None) -> dict:
        return self.__post_request(f"edit-m2m/{meta_class}", attributes, attrs_for_return)

    def exec(self, file_path:str):
        with open(file_path, 'rb') as file:
            return self.__send_file_request(
                self.__get_base_request_url("exec"),
                {'script': file}
            )