"""
    HTTP features for HTTP based backends and requests 
"""

import requests
import ssl
import pathlib

from pydeen.types import Base, Request, Connector, Result, Backend, Auth, ResultSingle, Result, Factory
from pydeen.pandas import PandasResultDataframe
from pydeen.exits import MenuExitCallback
from pydeen.menu import MenuSelection
class HTTPRequest(Request, MenuExitCallback):

    HEADER_CONTENT_TYPE = "Content-Type"

    def __init__(self, connector: Connector) -> None:
        super().__init__()
        self.headers = {
            'user-agent': 'python-request (pydeen)'
        }
        self.connector = connector
        self.http_request = None
        self.params  = {}
        self.result  = None
        self.url:str = None
        self.status_code:int = 0
        self.status_text:str = ""
        self.payload:str = None
        self.response:str = None


    def get_params(self):
        params = {}
        backend_params = self.connector.get_backend().get_params()
        if len(backend_params) > 0:
            params += backend_params        
        
        if len(self.connector.params) > 0:
            params += self.connector.params

        if len(self.params) > 0:
            params += self.params
        return params

    def get_response_text(self) -> str:
        if self.http_request != None:
            return self.http_request.text
        else: 
            return None    

    def get_response_json(self):
        try:
            return self.http_request.json()
        except:
            return None

    def is_response_availabe(self) -> bool:
        if self.http_request == None:
            return False
        else:
            return True 

    def is_response_json(self) -> bool:
        if self.get_response_json() == None:
            return False
        else:
            return True 

    def get_status_code(self) -> int:
        return self.status_code

    def set_header(self, key:str, value:str):
        self.headers[key] = value

    def set_content_type(self, content_type:str):
        self.set_header(HTTPRequest.HEADER_CONTENT_TYPE, content_type)

    def set_result_from_request(self):
        # check http result is given
        self.result = None
        if self.http_request == None:
            self.status_code = 500
            self.status_text = "unknown"            
            return None
        
        # set status code and reason
        self.status_code = self.http_request.status_code
        self.status_text = self.http_request.reason

        # check result type
        self.response = self.http_request.text
        try:    
            result = self.http_request.json()
        except:
            result = self.response
            self.trace("request result is no json. set text")

        # set result object
        if result != None:
            self.result = Result(result)
        return self.result         

    def prepare_auth_headers(self, auth:any) -> dict:
        if auth != None:
            return self.headers
        else:
            result = {}
            if self.headers != None and len(self.headers) > 0:
                result.update(self.headers)

            auth_headers = self.connector.get_backend().get_auth_info().get_auth_headers()
            if auth_headers != None and len(auth_headers) > 0:
                result.update(auth_headers)
            return result


    def get(self, path_append="", parameters:dict=None) -> int:
        # prepare url with params
        url = self.connector.build_url(path_append, parameters)
        params = self.get_params()
        self.trace(f"URL: {url}, params = {params}")
        self.url = url
        self.payload = None

        # prepare auth and headers
        auth = self.connector.get_backend().get_auth_info().get_auth_for_request()
        headers = self.prepare_auth_headers(auth)

        # execute
        self.http_request = requests.get(url, params=params, headers=headers, auth=auth)
        self.set_result_from_request()
        if self.http_request == None:
            self.error(f"request get failed: URL {url}")
        
        self.trace(f"request get result: {self.status_code}")    
        return self.status_code

    def post(self, payload:str=None, path_append="", parameters:dict=None) -> int:
        # prepare url
        url = self.connector.build_url(path_append, parameters)
        params = self.get_params()
        self.trace(f"URL: {url}, params = {params}")
        
        self.url = url
        if payload != None: 
            self.payload  = payload
        else:
            self.trace("use loaded payload for post request")    

        # prepare auth and headers
        auth = self.connector.get_backend().get_auth_info().get_auth_for_request()
        headers = self.prepare_auth_headers(auth)

        # execute
        self.http_request = requests.post(url, self.payload, params=params, headers=headers, auth=auth)
        self.set_result_from_request()    
        if self.http_request == None:
            self.error(f"request post failed: URL {url}")
        
        self.trace(f"request post result: {self.status_code}")    
        return self.status_code

    def load_payload(self, filename:str) -> bool:
        try:
           self.payload = None
           self.payload = pathlib.Path(filename).read_text()
           if self.payload != None:
            self.trace(f"request payload loaded from file {filename}")
            return True
           else:
            self.error(f"Error while loading payload from file {filename}")
            return False 
        except Exception as exc:
            self.error(f"Error while loading payload: {type(exc)} - {exc}")
            return False


    def menu_action_reset(self):
        self.menu_result = None
        self.menu_entity = None
        self.menu_request = None
        self.menu_pandas_df = None
        self.menu_request_params = {}
        print("Menu context cleared.")


    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = super().menu_get_entries(prefilled)
       
       # final own features
        if Factory.get_datahub().get_count() > 0:
            entries[HTTPConnector.MENU_DATAHUB] = "Open Datahub menu"

        entries[HTTPConnector.MENU_RESET] = "Reset menu context"
        return entries

    def menu_process_selection(self, selected: str, text: str = None) -> bool:
        try:
            if selected == HTTPConnector.MENU_RESET:
                self.menu_action_reset()
            elif selected == HTTPConnector.MENU_RESULT_SINGLE_MENU:
                self.menu_result_single.menu(menu_exit=self)
            elif selected == HTTPConnector.MENU_RESULT_PANDAS:
                df = self.menu_result.get_result_as_pandas_df()
                self.menu_pandas_df = PandasResultDataframe(
                    name=self.menu_result.result_name, df=df)
                print(df)
            elif selected == HTTPConnector.MENU_RESULT_MENU:
                self.menu_result.menu()
            elif selected == HTTPConnector.MENU_PANDAS_MENU:
                self.menu_pandas_df.menu()
            elif selected == HTTPConnector.MENU_DATAHUB:
                Factory.get_datahub().menu()
            else:
                super().menu_process_selection(selected, text)
        except Exception as exc:
            print("Errors occured:", type(exc), exc)


class HTTPBackend(Backend):

    def __init__(self, name:str, url:str, auth:Auth=None):
        super().__init__(name, auth)
        self.type = "pydeen.HTTPBackend"
        self.set_property(Backend.BACKEND_PROP_URL, url)
        self.ssl_verify_mode:ssl.VerifyMode=None

    def get_ssl_verify_mode(self) -> ssl.VerifyMode:
        return self.ssl_verify_mode

    def set_ssl_verify_mode(self, ssl_verify_mode:ssl.VerifyMode):
        self.ssl_verify_mode = ssl_verify_mode
        self.trace(f"SSL Verify mode set to: {self.ssl_verify_mode}")    


    def set_ssl_verify_mode_none(self):
        self.ssl_verify_mode = ssl.CERT_NONE
        self.trace("SSL Verify mode deactivated")    

    def set_ssl_verify_mode_client_with_pem(self, path_to_pem:str, ssl_method:ssl._SSLMethod=ssl.PROTOCOL_TLS_CLIENT) -> bool:
        try:
            ssl_context = ssl.SSLContext(ssl_method)
            pem_file = pathlib.Path(path_to_pem)
            ssl_context.load_verify_locations(cafile=pem_file)
            self.set_ssl_verify_mode(ssl_context)
            return True               
        except Exception as exc:
            self.error(f"Error while setting SSL context: {type(exc)} - {exc}")    
            return False

    def set_ssl_verify_mode_ignore_all(self, protocol:ssl._SSLMethod=None) -> bool:
        ssl_context = ssl.SSLContext(protocol=protocol)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return True

class HTTPConnector(Connector, MenuExitCallback):
    """
        Connector for HTTP Calls
    """
    MENU_FIND_ENDPOINTS         = "find_endpoints"
    MENU_FIND_ENTITIES          = "find_entities"
    MENU_ENTITY_SELECT          = "select_entity"
    MENU_ENTITY_BY_KEY          = "select_entity_key"
    MENU_ENTITY_SINGLE          = "select_entity_single"
    MENU_LAST_REQUEST           = "last_request"
    MENU_REQUEST_CONFIGURE      = "configure_request"
    MENU_METADATA_INFO          = "metadata_info"
    MENU_METADATA_XML           = "metadata_xml"
    MENU_METADATA_JSON          = "metadata_json"
    MENU_RESULT_SINGLE_CHOOSE   = "result_record_single_choose"
    MENU_RESULT_SINGLE_MENU     = "result_record_single_menu"
    MENU_RESULT_RAW             = "result_raw"
    MENU_RESULT_PANDAS          = "result_pandas"
    MENU_RESULT_MENU            = "result_menu"
    MENU_PANDAS_MENU            = "pandas_menu"
    MENU_RESET                  = "reset"
    MENU_DATAHUB                = "datahub"
    MENU_PANDAS_IMPORT          = "pandas_import"
    MENU_FOLLOW_ASSOC           = "follow_assocation"
    MENU_EXPERT                 = "menu_expert"
    MENU_IMPORT                 = "menu_import"
    MENU_IMPORT_DH_RESULT       = "menu_import_datahub_result"
    MENU_IMPORT_DH_RESULT_SINGLE = "menu_import_datahub_result_single"
    MENU_IMPORT_DH_PANDAS_DF     = "menu_import_datahub_pandas_df"

    HTTP_HEADER_CONTENT_TYPE    = 'Content-type'
    HTTP_CNTTYPE_APPL_JSON      = "application/json"
    HTTP_CNTTYPE_APPL_XML       = "application/xml"
    HTTP_CNTTYPE_TEXT           = "text/text"
    HTTP_CNTTYPE_HTML           = "text/html"

    def __init__(self, backend:Backend=None, url_or_endpoint:str="") -> None:
            
        # check backend 
        self.backend:HTTPBackend=None
        if backend == None:
            raise Exception("HTTP Connector via url not implemented yet")
            self.endpoint = ""    
            # if url_or_endpoint == "" or url_or_endpoint.find("://") < 1:
            #     raise Exception("invalid URL if no backend is given") 
            
            # split_protocol = url.split("://")
            # protocol = split_protocol[0]
            # rest_protocol = split_protocol[1]

            # pos_path = rest_protocol.find("/")
            # if pos_path > 0:
            #     hostname = rest_protocol.left(pos_path)
            #     path = rest_protocol.
        else:
            self.endpoint = url_or_endpoint

        Connector.__init__(self, backend)
        self.type = "pydeen.HTTPConnector"

        # remember last request
        self.last_request:HTTPRequest = None        
        self.headers: dict = {}
        self.menu_title = "HTTP Connector - Menu"
        self.menu_entity:str = None
        self.menu_result:Result = None
        self.menu_result_single:ResultSingle = None
        self.menu_pandas_df:PandasResultDataframe = None
        self.menu_request_params = {}

    def menu_action_reset(self):
        self.menu_entity = None
        self.menu_result = None
        self.menu_result_single = None
        self.menu_pandas_df = None
        self.menu_request_params = {}
        self.last_request = None
        print("Menu context cleared.")

            
    def path_append(self, path, append) -> str:
        if append == "" or append == None:
            return path
        if path == "":
            return append
        if path[-1] == "/" or append[0] == "/":
            return path + append
        else:
            return path + "/" + append

    def get_endpoint_url(self) -> str:
        return self.build_url(None)    

    def set_header(self, key:str, value:str):
        self.headers[key] = value

    def set_content_type(self, content_type:str, charset:str=None):
        header_value = content_type
        if charset != None:
            header_value += f"; charset={charset}"
        self.set_header(HTTPConnector.HTTP_HEADER_CONTENT_TYPE, header_value)

    def build_url(self, path_append, parameters:dict=None) -> str:
        # check url is given by backend or parameter
        if path_append != None and path_append.find("://") > 0:
            url = path_append
        else:     
            url = self.get_backend().get_property(Backend.BACKEND_PROP_URL)
        
        # no: build via backend fragments    
        if url == None or url == "":
            result = self.get_backend().get_property(Backend.BACKEND_PROP_PROTOCOL) + "://"
            result += self.get_backend().get_property(Backend.BACKEND_PROP_HOST)
            port = self.get_backend().get_property(Backend.BACKEND_PROP_PORT)
            if port != None and port != "":
                result += ":" + port
        
            result = self.path_append(result, self.get_backend().get_property(Backend.BACKEND_PROP_PATH))
            result = self.path_append(result, self.endpoint)
            result = self.path_append(result, path_append)
        else:
        # yes: use this without further fragments except append info    
            if url != path_append:
                result = self.path_append(url, path_append)
            else:
                result = url

        # check for parameters
        if parameters != None:
            self.trace("build url with parameters detected")
            url_params = ''
            for name in parameters.keys():
                sep = "="
                if name == "$filter":
                    value = str(parameters[name]).lower()
                    if value.find("contains") >= 0:
                        self.trace(f"OData filter exception found for {value}")
                        sep = " "

                url_param = name + sep + parameters[name]
                if url_params == '':
                    url_params = url_param
                else:
                    url_params += '&' + url_param

            if result.find("?") < 0:
                result += "?" + url_params
            else:
                parts = result.split("?")
                result = parts[0] + '?' + parts[1] + '&' + url_params


        print("URL:", result)
        return result

    def create_request(self) -> HTTPRequest:
        request = HTTPRequest(self)   
        request.debug = self.debug   # forward debug mode 
        request.interactive = self.interactive
        request.headers = self.headers
        self.last_request = request
        return request   

    
    def is_http_code_success(self, code:int) -> bool:
        if code >= 200 and code <= 300:
            return True
        else:
            return False

    def menu_import_action_datahub(self, title:str, filter_class:any) -> any:
        try:
            dh = Factory.get_datahub()
            df_key = dh.menu_select_key(title, filter_class)
            if df_key != None and df_key != "":
                dh_object = dh.get_object(df_key)
                if dh_object != None:
                    print(f"Data object {df_key} loaded from datahub.")
                    Base.set_description(dh_object, df_key, overwrite=False)
                    if self.menu_entity == None:
                        self.menu_entity = df_key
                        self.trace(f"set connector entity to used datahub key")
                    return dh_object
                else:
                    print("Data object not loaded from datahub.")        
        except Exception as exc:
            print(f"Loading from datahub failed: {type(exc)} - {exc}")    

    def menu_import_options(self):
        
        entries = {}
        if self.menu_pandas_df == None:
            entries[HTTPConnector.MENU_PANDAS_IMPORT] = "Import pandas dataframe from file"
            if Factory.get_datahub().get_count(PandasResultDataframe) > 0:
                entries[HTTPConnector.MENU_IMPORT_DH_PANDAS_DF] = "Import pandas dataframe from datahub"
        
        if self.menu_result == None and Factory.get_datahub().get_count(Result) > 0:
            entries[HTTPConnector.MENU_IMPORT_DH_RESULT] = "Import result from datahub"
        
        if self.menu_result_single == None and Factory.get_datahub().get_count(ResultSingle) > 0:
            entries[HTTPConnector.MENU_IMPORT_DH_RESULT_SINGLE] = "Import single result from datahub"

        if len(entries) == 0:
            print("No import options available")
            return None

        # process menus
        action = MenuSelection("Select import option", entries).show_menu()
        if action.is_cancel_entered():
            return
        else:
            selected = action.get_selection()
            if selected == HTTPConnector.MENU_PANDAS_IMPORT:
                import_df = PandasResultDataframe("dataframe")
                import_df.menu()
                print(import_df.get_count())
                if not import_df.is_empty():
                    self.menu_pandas_df = import_df
            elif selected == HTTPConnector.MENU_IMPORT_DH_RESULT:
                self.menu_result = self.menu_import_action_datahub("Select result from datahub", Result)                
            elif selected == HTTPConnector.MENU_IMPORT_DH_RESULT_SINGLE:
                self.menu_result_single = self.menu_import_action_datahub("Select single result from datahub", ResultSingle)
            elif selected == HTTPConnector.MENU_IMPORT_DH_PANDAS_DF:
                self.menu_pandas_df = self.menu_import_action_datahub("Select pandas datadframe from datahub", PandasResultDataframe)
            else:
                print(f"unknown expert option or not handled: {selected}")


    def menu_expert_options(self):
        
        entries = {}
        # http
        if self.last_request != None:
            entries[HTTPConnector.MENU_LAST_REQUEST] = "Show last HTTP request"

        if len(entries) == 0:
            print("No expert options available.")
            return None

        # process menus
        action = MenuSelection("Select expert option", entries).show_menu()
        if action.is_cancel_entered():
            return
        else:
            selected = action.get_selection()
            if selected == HTTPConnector.MENU_LAST_REQUEST:
                print(f"HTTP Status Code: {self.last_request.get_status_code()}")
                response = self.last_request.get_response_text()
                if response == None:
                    print("No HTTP Response")
                elif len(response) < 20000:
                    print(f"Response:\n{self.last_request.get_response_text()}")
                else:
                    print(f"Response length {len(response)}. Too large to display.")
            else:
                print(f"unknown expert option or not handled: {selected}")


    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = super().menu_get_entries()

        # result options
        if self.menu_result != None:
            result_count = self.menu_result.get_count()
            entries[
                HTTPConnector.MENU_RESULT_MENU] = f"Enter current result menu (entity {self.menu_entity} records {result_count})"
            if result_count > 0:
                
                # pandas transformation                    
                if self.menu_pandas_df == None:
                    entries[
                        HTTPConnector.MENU_RESULT_PANDAS] = f"Get current result as pandas dataframe (entity {self.menu_entity})"

        # single result support
        if self.menu_result_single != None:
            entries[
                HTTPConnector.MENU_RESULT_SINGLE_MENU] = f"Open single record menu (record {self.menu_result_single.get_description()})"

        # pandas support
        if self.menu_pandas_df != None:
            entries[HTTPConnector.MENU_PANDAS_MENU] = f"Open menu for current pandas dataframe '{self.menu_pandas_df.get_name()}'"
        
        # expert sub menus
        entries[HTTPConnector.MENU_IMPORT] = "Import data"
        entries[HTTPConnector.MENU_EXPERT] = "Expert options"

        # final own features
        if Factory.get_datahub().get_count() > 0:
            entries[HTTPConnector.MENU_DATAHUB] = "Open Datahub menu"

            
        entries[HTTPConnector.MENU_RESET] = "Reset menu context"
        return entries


    def menu_process_selection(self, selected: str, text: str = None) -> bool:
        try:
            if selected == HTTPConnector.MENU_RESET:
                self.menu_action_reset()
            elif selected == HTTPConnector.MENU_RESULT_SINGLE_MENU:
                self.menu_result_single.menu()
            elif selected == HTTPConnector.MENU_RESULT_PANDAS:
                df = self.menu_result.get_result_as_pandas_df()
                self.menu_pandas_df = PandasResultDataframe(
                    name=self.menu_result.result_name, df=df)
                print(df)
                self.menu_pandas_df.menu(menu_exit=self)
            elif selected == HTTPConnector.MENU_RESULT_MENU:
                self.menu_result.menu(menu_exit=self)
            elif selected == HTTPConnector.MENU_PANDAS_MENU:
                self.menu_pandas_df.menu(menu_exit=self)
            elif selected == HTTPConnector.MENU_EXPERT:
                self.menu_expert_options()
            elif selected == HTTPConnector.MENU_IMPORT:
                self.menu_import_options()
            elif selected == HTTPConnector.MENU_DATAHUB:
                Factory.get_datahub().menu()
            else:
                super().menu_process_selection(selected, text)
        except Exception as exc:
            print("Errors occured while processing HTTP Connector commands:", type(exc), exc)

    def exit_menu_get_entries_bottom(self, exit, owner) -> dict:
        return super().exit_menu_get_entries_bottom(exit, owner)

    def exit_menu_get_entries_top(self, exit, owner) -> dict:
        return super().exit_menu_get_entries_top(exit, owner)

    def exit_menu_process_selection(self, exit, owner, selected: str, text: str = None) -> bool:
        return super().exit_menu_process_selection(exit, owner, selected, text)