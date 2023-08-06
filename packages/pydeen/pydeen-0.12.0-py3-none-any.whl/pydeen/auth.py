"""
This module contains authorization functionality. 
"""


from pydeen.types import Auth
from pydeen.menu import MenuSelection, UserInput
from pydeen.utils import CryptUtil
from base64 import b64encode
import requests

class AuthBasic(Auth):

    MENU_SET_AUTH_NAME          = "set_auth_name"
    MENU_SET_AUTH_PATH          = "set_auth_path"
    MENU_SET_BASIC_AUTH         = "set_basic_auth"
    MENU_RESET_AUTH             = "reset_auth"
    MENU_LOAD_AUTH              = "load_auth"
    MENU_SAVE_AUTH              = "save_auth"
    MENU_HTTP_HEADER_AUTH       = "generate_http_header_auth"



    def __init__(self):
        super().__init__()
        self.type = "pydeeen.AuthBasic"
        self.menu_name = "default"
        self.menu_path = None
        self.menu_ext  = "auth"
        
    def is_available(self) -> bool:
        if self._properties != None and len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) != None:
            return True
        else:
            return False
    
    def is_basic_auth_available(self) -> bool:
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_BASIC:
            return True
        else:
            return False    

    def set_basic_auth(self, user:str, password:str) -> bool:
        enc_pw = CryptUtil.get_engine().encode(password)  
        self._properties = {}
        self.set_property(Auth.AUTH_PROP_TYPE, Auth.AUTH_TYPE_BASIC)
        self.set_property(Auth.AUTH_PROP_USER, user)
        self.set_property(Auth.AUTH_PROP_PASS, enc_pw)
        return True

    def init_from_config(self, type, config) -> bool:
        if type == Auth.AUTH_TYPE_BASIC:
            self._properties = {}
            self.set_property(Auth.AUTH_PROP_TYPE, Auth.AUTH_TYPE_BASIC)
            self.set_property(Auth.AUTH_PROP_USER, config[Auth.AUTH_PROP_USER])
            self.set_property(Auth.AUTH_PROP_PASS, config[Auth.AUTH_PROP_PASS])
            return True
        else:
            return False      

    def get_username(self) -> str:
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_BASIC:
            return self.get_property(Auth.AUTH_PROP_USER)
        else:
            return None

    def get_password(self) -> str:
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_BASIC:
            return self.get_property(Auth.AUTH_PROP_PASS)
        else:
            return None

    def get_auth_for_request(self):
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_BASIC:
            username = self.get_property(Auth.AUTH_PROP_USER)
            password = self.get_property(Auth.AUTH_PROP_PASS)
            
            if len(username) == 0 or len(password) == 0:
                return None 
            
            return (username,password)
        else:
            return None    

    def get_auth_for_requests_session(self):
        self.trace("set basic auth info as requests session")
        s = requests.Session()
        s.auth = (self.get_username(), self.get_password())
        return s


    def get_auth_headers(self) -> dict:
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_BASIC:
            username = self.get_property(Auth.AUTH_PROP_USER)
            password = self.get_property(Auth.AUTH_PROP_PASS)
            
            if len(username) == 0 or len(password) == 0:
                return None 
            
            user_pass = f'{username}:{password}'
            basic_credentials = b64encode(user_pass.encode()).decode()
            return {'Authorization': f'Basic {basic_credentials}'}
        else:
            return None    

    def get_menu_filename(self) -> str:
        if self.menu_path != None:
            filename = f"{self.menu_path}/{self.menu_name}.{self.menu_ext}"
        else:
            filename = f"{self.menu_name}.{self.menu_ext}"   
        return filename    

    def set_menu_context(self, name, path:str=None, extension:str="auth"):
        self.menu_path = path
        self.menu_name = name
        self.menu_ext = extension

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = super().menu_get_entries(prefilled)
        entries[AuthBasic.MENU_SET_AUTH_PATH] = f"Set path for auth info ({self.menu_path})"
        entries[AuthBasic.MENU_SET_AUTH_NAME] = f"Set name auth info ({self.menu_name})"
        
        if self.is_basic_auth_available() == True:
            entries[AuthBasic.MENU_SAVE_AUTH] = "Save current auth info"
            entries[AuthBasic.MENU_HTTP_HEADER_AUTH] = "Generate HTTP Header Authorization parameter"
            entries[AuthBasic.MENU_RESET_AUTH] = "Reset auth info"
        else:
            entries[AuthBasic.MENU_LOAD_AUTH] = "Load auth info"
            entries[AuthBasic.MENU_SET_BASIC_AUTH] = "Set user password"
        
        return entries

    def menu_process_selection(self, selected: str, text: str = None):
        if selected == AuthBasic.MENU_RESET_AUTH:
            self._properties = {}
            print("authentification cleared")
        elif selected == AuthBasic.MENU_SET_AUTH_NAME:
            self.menu_name = UserInput("Enter name", self.menu_name).get_input()
            print(f"use name {self.menu_name} for auth")
        elif selected == AuthBasic.MENU_SET_AUTH_PATH:
            self.menu_path = UserInput("Enter save path for auth info", self.menu_path).get_input(empty_allowed=True)
            print(f"use path {self.menu_name} for auth storage")
        elif selected == AuthBasic.MENU_SET_BASIC_AUTH:
            user = UserInput("Enter username", self.get_username()).get_input()
            pw = UserInput("Enter password", None).get_password(empty_allowed=True)
            if pw == None:
                print("Set auth info skipped")
            else:
                self.set_basic_auth(user, pw)
                print("auth info set")    
            print(f"use name {self.menu_name} for auth")
        elif selected == AuthBasic.MENU_SAVE_AUTH:
            filename = UserInput("Enter filename for save auth info", self.get_menu_filename()).get_input(empty_allowed=True)
            if filename == None:
                print("save auth info skipped")
            else:
                if self.save_config(filename) == True:
                    print(f"current auth info saved to file {filename}")
                else:
                    print(f"Error while saving current auth info to {filename}")       
        elif selected == AuthBasic.MENU_LOAD_AUTH:
            filename = UserInput("Enter filename for load auth info", self.get_menu_filename()).get_input(empty_allowed=True)
            if filename == None:
                print("load auth info skipped")
            else:
                if self.load_config(filename) == True:
                    print(f"current auth info loaded from file {filename}")
                else:
                    print(f"Error while loading current auth info from {filename}")       
        elif selected == AuthBasic.MENU_HTTP_HEADER_AUTH:
            print(self.get_auth_headers())
        else:
            return super().menu_process_selection(selected, text)


class AuthToken(Auth):
    
    MENU_SET_AUTH_TOKEN         = "set_auth_token"

    def __init__(self):
        super().__init__()
        self.type = "pydeeen.AuthToken"
        self.menu_name = "default"
        self.menu_path = None
        self.menu_ext  = "auth"
        
    def is_available(self) -> bool:
        if self._properties != None and len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) != None:
            return True
        else:
            return False
    
    def is_token_auth_available(self) -> bool:
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_TOKEN:
            return True
        else:
            return False    

    def set_token_auth(self, token:str) -> bool:
        enc_token = CryptUtil.get_engine().encode(token)  
        self._properties = {}
        self.set_property(Auth.AUTH_PROP_TYPE, Auth.AUTH_TYPE_TOKEN)
        self.set_property(Auth.AUTH_PROP_TOKEN, enc_token)
        return True

    def init_from_config(self, type, config) -> bool:
        if type == Auth.AUTH_TYPE_TOKEN:
            self._properties = {}
            self.set_property(Auth.AUTH_PROP_TYPE, Auth.AUTH_TYPE_TOKEN)
            self.set_property(Auth.AUTH_PROP_TOKEN, config[Auth.AUTH_PROP_TOKEN])
            return True
        else:
            return False      


    def get_token(self) -> str:
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_TOKEN:
            return self.get_property(Auth.AUTH_PROP_TOKEN)
        else:
            return None

    def get_auth_for_request(self):
        # no auth object for tokens
        return None
 
    def get_auth_for_requests_session(self):
        self.trace("set bearer token auth info as requests session")
        # check token
        token = self.get_token()
        if token == None:
            return None
        # set session object
        s = requests.Session()
        if s.headers == None:
            s.headers = {}
        s.headers["Authorization"] = f"Bearer {token}"
        return s

    def get_auth_headers(self) -> dict:
        if len(self._properties) > 0 and self.get_property(Auth.AUTH_PROP_TYPE) == Auth.AUTH_TYPE_TOKEN:
            token = self.get_property(Auth.AUTH_PROP_TOKEN)
            
            if len(token) == 0:
                return None 
            
            return {'Authorization': f'Bearer {token}'}
        else:
            return None    

    def get_menu_filename(self) -> str:
        if self.menu_path != None:
            filename = f"{self.menu_path}/{self.menu_name}.{self.menu_ext}"
        else:
            filename = f"{self.menu_name}.{self.menu_ext}"   
        return filename    

    def set_menu_context(self, name, path:str=None, extension:str="auth"):
        self.menu_path = path
        self.menu_name = name
        self.menu_ext = extension

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = super().menu_get_entries(prefilled)
        entries[AuthToken.MENU_SET_AUTH_PATH] = f"Set path for auth info ({self.menu_path})"
        entries[AuthToken.MENU_SET_AUTH_NAME] = f"Set name auth info ({self.menu_name})"
        
        if self.is_token_auth_available() == True:
            entries[AuthToken.MENU_SAVE_AUTH] = "Save current auth info"
            entries[AuthToken.MENU_HTTP_HEADER_AUTH] = "Generate HTTP Header Authorization parameter"
            entries[AuthToken.MENU_RESET_AUTH] = "Reset auth info"
        else:
            entries[AuthToken.MENU_LOAD_AUTH] = "Load auth info"
            entries[AuthToken.MENU_SET_AUTH_TOKEN] = "Set token"
        
        return entries

    def menu_process_selection(self, selected: str, text: str = None):
        if selected == AuthToken.MENU_RESET_AUTH:
            self._properties = {}
            print("authentification cleared")
        elif selected == AuthToken.MENU_SET_AUTH_NAME:
            self.menu_name = UserInput("Enter name", self.menu_name).get_input()
            print(f"use name {self.menu_name} for auth")
        elif selected == AuthToken.MENU_SET_AUTH_PATH:
            self.menu_path = UserInput("Enter save path for auth info", self.menu_path).get_input(empty_allowed=True)
            print(f"use path {self.menu_name} for auth storage")
        elif selected == AuthToken.MENU_SET_AUTH_TOKEN:
            token = UserInput("Enter token", self.get_token()).get_input()
            if token == None:
                print("Set auth info skipped")
            else:
                self.set_token_auth(token)
                print("auth info set")    
            print(f"use name {self.menu_name} for auth")
        elif selected == AuthToken.MENU_SAVE_AUTH:
            filename = UserInput("Enter filename for save auth info", self.get_menu_filename()).get_input(empty_allowed=True)
            if filename == None:
                print("save auth info skipped")
            else:
                if self.save_config(filename) == True:
                    print(f"current auth info saved to file {filename}")
                else:
                    print(f"Error while saving current auth info to {filename}")       
        elif selected == AuthToken.MENU_LOAD_AUTH:
            filename = UserInput("Enter filename for load auth info", self.get_menu_filename()).get_input(empty_allowed=True)
            if filename == None:
                print("load auth info skipped")
            else:
                if self.load_config(filename) == True:
                    print(f"current auth info loaded from file {filename}")
                else:
                    print(f"Error while loading current auth info from {filename}")       
        elif selected == AuthToken.MENU_HTTP_HEADER_AUTH:
            print(self.get_auth_headers())
        else:
            return super().menu_process_selection(selected, text)

