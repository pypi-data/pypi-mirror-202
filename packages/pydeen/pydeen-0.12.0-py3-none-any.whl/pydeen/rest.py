"""
This module contains functions for supporting simple rest services
"""

import json

from pydeen.types import Result, ResultSingle, Backend, Factory
from pydeen.http import HTTPConnector, HTTPRequest
from pydeen.exits import MenuExitCallback
from pydeen.pandas import PandasResultDataframe
from pydeen.menu import UserInput, MenuSelection

class HTTPRestConnector(HTTPConnector, MenuExitCallback):
    
    MENU_REST_PANDAS_EXPORT             = "rest_pandas_export_list"
    
    def __init__(self, backend: Backend = None, url_or_endpoint: str = "") -> None:
        super().__init__(backend, url_or_endpoint)
        self.type = "pydeen.HTTPRestConnector"
        self.menu_title = "HTTP REST Connector - Menu"


    
    def reset_menu_result(self):
        self.menu_result = None
        self.menu_result_single = None
        self.MENU_RESULT_PANDAS = None

    def get_list(self, path:str=None, parameters:dict=None) -> Result:
        
        request = self.create_request()
        http_code = request.get(path, parameters=parameters)

        if self.is_http_code_success(http_code) and request.is_response_json():
            json_data = request.get_response_json()
            if type(json_data) != list:
                self.error("REST result is not a list. Retry as object.")
                return None
            else:
                return Result(json_data, self.menu_entity)
        else:
            return None

    def get_object(self, path:str=None, parameters:dict=None) -> ResultSingle:
        
        request = self.create_request()
        http_code = request.get(path, parameters=parameters)

        if self.is_http_code_success(http_code) and request.is_response_json():
            json_data = request.get_response_json()
            if type(json_data) != dict:
                self.error("REST result is not an object. Retry as table.")
                return None
            else:
                return ResultSingle(json_data, self.menu_entity)
        else:
            return None


    def post_data(self, data:str, path:str=None, parameters:dict=None, content_type:str=None) -> bool:        
        request = self.create_request()
        if content_type != None:
            request.set_content_type(content_type)

        http_code = request.post(payload=data, path_append=path, parameters=parameters)

        print(http_code, request.get_response_text())

        if self.is_http_code_success(http_code):
            return True
        else:
            return False

    def post_list(self, data:list, path:str=None, parameters:dict=None, single_post:bool=False) -> bool:
        
        if single_post:
            for record in data:
                if self.post_data(json.dumps(record), path=path, parameters=parameters, content_type="application/json; charset=utf-8") == False:
                    return False
        else:
            if self.post_data(json.dumps(data), path=path, parameters=parameters, content_type="application/json; charset=utf-8") == False:
                    return False

        return True        


    def menu_enter_rest_path(self) -> str:
        current_endpoint = self.get_endpoint_url()
        path = UserInput(F"Append further path info to the current REST URL if required {current_endpoint}").get_input(True)
        if path != None and len(path) > 0:
            self.menu_entity = path
        else:
            self.menu_entity = None
        return path

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        # own entries
        entries = {}
        entries[HTTPConnector.MENU_ENTITY_SELECT] = "Get table data from REST endpoint"
        entries[HTTPConnector.MENU_ENTITY_SINGLE] = "Get object data from REST endpoint"
        
        # mixit
        super_entries = super().menu_get_entries()
        entries.update(super_entries)
        return entries


    def menu_process_selection(self, selected: str, text: str = None) -> bool:
        try:
            if selected == HTTPConnector.MENU_ENTITY_SELECT:
                self.reset_menu_result()
                self.menu_result = self.get_list(self.menu_enter_rest_path())
                print()
                if self.menu_result == None:
                    print("No result or Errors occured")
                else:
                    lines = self.menu_result.get_count()
                    print(f"Selected records in result: {lines}")
            elif selected == HTTPConnector.MENU_ENTITY_SINGLE:
                self.reset_menu_result()
                self.menu_result_single = self.get_object(self.menu_enter_rest_path())
                print()
                if self.menu_result_single == None:
                    print("No result or Errors occured")
                else:
                    len_rest = self.menu_result_single.get_count()
                    print(f"Selected object data from REST endpoint with length of {len_rest}.")
                    if self.menu_entity == None:
                        self.menu_entity = self.backend.get_name()
                    if self.menu_entity == None:
                        self.menu_entity = self.backend.get_description()
                    self.menu_result_single.set_description(self.menu_entity)
                    if self.menu_result_single.search_for_tables_in_result():
                        found = self.menu_result_single.get_result_tables_count()
                        print(f"There are {found} tables found in this result.\nOpen single record menu and follow these tables.")
            else:
                super().menu_process_selection(selected, text)
        except Exception as exc:
            print("Errors occured while processing HTTPRestConnector command:", type(exc), exc)

    def exit_menu_get_entries_bottom(self, exit, owner) -> dict:
        entries = {}
        if isinstance(owner, PandasResultDataframe):
            entries[HTTPRestConnector.MENU_REST_PANDAS_EXPORT] = "Export entries to REST Service"
            return entries
        else:
            return super().exit_menu_get_entries_bottom(exit, owner)
        

    def exit_menu_process_selection(self, exit, owner, selected: str, text: str = None) -> bool:
        if selected == HTTPRestConnector.MENU_REST_PANDAS_EXPORT:
            post_data = PandasResultDataframe.get_as_list_of_dict(owner)
            if post_data == None:
                print("No data to send")
            else:
                if self.post_list(post_data, path=self.menu_enter_rest_path()):
                    print("Data was sent")
                else:
                    print("Error while sending data")   
            return True
        else:
            return super().exit_menu_process_selection(exit, owner, selected, text)