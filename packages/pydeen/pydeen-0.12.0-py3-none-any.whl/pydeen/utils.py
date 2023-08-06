"""
    some utils for PyDEEN
"""

import base64
import datetime
import hashlib
import os
import pathlib
import sys
import uuid
import argparse
import shutil

from datetime import datetime
from argparse import ArgumentParser
from cryptography.fernet import Fernet
from pydeen.menu import UserInput


class CryptEngine():
    
    PROP_SALT = "salt"
    PROP_ENGINE  = "engine"
    PROP_ENCODED = "encoded"
    
    def __init__(self, context:bytes=None, salt:bytes=None) -> None:
        self.context:bytes = context
        self.salt:bytes = salt
        self.engine:str = "unknown"  
    
    def encode(self, content:str):
        return content

    def decode(self, content:any):
        return content    

    def set_salt(self, salt:bytes):
        self.salt = salt        

    def set_context(self, context:bytes):
        self.context = context        

class CryptEngineDefault(CryptEngine):
    def __init__(self, context: bytes = None, salt: bytes = None) -> None:
        super().__init__(context, salt)
        self.engine = "default"
    
    def get_key(self) -> bytes:
        if self.context == None:
            self.context = CryptUtil.get_context_key()

        if self.salt == None:
            self.salt = CryptUtil.create_salt_key()  

        lenc = len(self.context)
        if lenc < 16:
            key = self.context + self.salt
        else:
            key = self.context[:16] + self.salt[:16]   

        return base64.urlsafe_b64encode(key) 

    def encode(self, content:str):        
        f = Fernet(self.get_key())
        e = f.encrypt(content.encode())
        result = {}
        result[CryptEngine.PROP_ENGINE] = self.engine
        result[CryptEngine.PROP_SALT] = CryptUtil.byte_to_base64(self.salt)
        result[CryptEngine.PROP_ENCODED] = CryptUtil.byte_to_base64(e)
        return result

    def decode(self, content:dict):
        try:
            engine = content[CryptEngine.PROP_ENGINE]
            if engine != self.engine:
                return content # wrong engine
            else:
                salt_b64 = content[CryptEngine.PROP_SALT]
                encoded_b64 = content[CryptEngine.PROP_ENCODED]
                self.salt = CryptUtil.base64_to_bytes(salt_b64)
                encoded = CryptUtil.base64_to_bytes(encoded_b64)    
                return Fernet(self.get_key()).decrypt(encoded).decode()
        except:
            print("Error", sys.exc_info()[0], "occurred.")
            return content  

class CryptUtil():
    
    @classmethod
    def __init__(cls) -> None:
        cls.engines = {}

    @staticmethod
    def get_context_key() -> bytes:
        context = str(pathlib.Path().resolve())
        context = context.replace("\\","")
        context = context.replace(":","")
        return hashlib.md5(context.encode()).digest()

    @staticmethod
    def create_salt_key() -> bytes:
        return base64.urlsafe_b64decode(Fernet.generate_key())

    @classmethod
    def register_engine(cls, name:str, engine:CryptEngine):
        cls.engines[name] = engine

    @classmethod
    def get_engine(cls, name:str=None, context:bytes=None, salt:bytes=None) -> CryptEngine:
        if name == None or name == "default" or len(name) == 0:
            return CryptEngineDefault(context, salt)
        
        if name in cls.engines.keys():
            return cls.engines[name]         

    @staticmethod
    def byte_to_base64(content:bytes) -> str:
        if content == None:
            return ""
        else:
            return base64.b64encode(content).decode()        

    @staticmethod
    def base64_to_bytes(base64_str:str) -> bytes:
        if base64_str == None or base64_str == "":
            return b""
        else:    
            return base64.b64decode(base64_str)    
class UUIDUtil():
    @staticmethod
    def new_uuid32_separated_string() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def new_uuid32_string() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def build_unique_key(key_str, namespace_str32:str=None) -> str:
        if namespace_str32 == None:
            use_ns_str = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        else:
            use_ns_str = namespace_str32

        ns = uuid.UUID(hex=use_ns_str)
        generated = str(uuid.uuid3(ns, key_str))
        return generated

class ArgumentUtil():
    def __init__(self, prog:str=None, desc:str=None, epilog:str=None, usage:str=None) -> None:
        self.parser:argparse.ArgumentParser = None
        self.args:argparse.Namespace = None
        self.prog = prog
        self.desc = desc
        self.epilog = epilog
        self.usage = usage

    def get_parser(self) -> ArgumentParser:
        if self.parser is None:
            self.parser = argparse.ArgumentParser(prog=self.prog, description=self.desc, epilog=self.epilog, usage=self.usage)
        return self.parser

    def set_parser(self, parser:ArgumentParser):
        self.parser = parser

    def get_arguments(self) -> argparse.Namespace:
        if self.args is None:
            self.args = self.get_parser().parse_args()
        return self.args

    def get_argument(self, name:str, default:any=None) -> any:
        arg_list = self.get_arguments()._get_kwargs()
        for argname, argvalue in arg_list:
            if argname == name:
                return argvalue
        return default

class DateTimeUtil():

    def __init__(self) -> None:
        self.datetime:datetime=None

    def is_datetime_available(self) -> bool:
        if self.datetime is None:
            return False
        else:
            return True

    def reset(self):
        self.datetime = None 

    def set_datetime(self, dt:datetime):
        self.datetime = dt

    def get_datetime(self) -> datetime:
        return self.datetime        

    def now(self) -> datetime:
        self.datetime = datetime.now()
        return self.datetime  

    def sap_timestamp(self) -> int:
        if self.datetime is None:
            return 0
        else:
            result =  self.datetime.year     * 10000000000 
            result += self.datetime.month    * 100000000
            result += self.datetime.day      * 1000000
            result += self.datetime.hour     * 10000
            result += self.datetime.minute   * 100
            result += self.datetime.second
            return result  

    def sap_timestamp_long(self) -> float:
        if self.datetime is None:
            return 0
        else:
            ms_len = len(str(self.datetime.microsecond))
            result = self.datetime.microsecond / ( 10 ** ms_len )
            result += self.datetime.year     * 10000000000 
            result += self.datetime.month    * 100000000
            result += self.datetime.day      * 1000000
            result += self.datetime.hour     * 10000
            result += self.datetime.minute   * 100
            result += self.datetime.second
            return result  

class FileTransferUtil():
    
    def get_datetime_prefix(self, with_time:bool=True, format:str=None) -> str:
        now = datetime.now() # current date and time
        if format != None:
            myformat = format
        else:
            myformat = "%Y%m%d"
            if with_time == True:
                myformat = myformat + "_%H%M%S"

        return now.strftime(myformat)        

    def enter_filename_to_save(self, title:str, name:str, extension:str="txt", use_datetime_prefix:bool=True, show_current_path:bool=True) -> str:
        # current path
        if show_current_path:
            cur_path = pathlib.Path().resolve()
            print(f"Current working directory is {cur_path}")        
        
        # prepare filename
        filename = f"{name}"
        if use_datetime_prefix == True:
            filename = self.get_datetime_prefix() + "_" + filename

        if filename.find(".") < 0:
            filename = f"{filename}.{extension}"

        filename = UserInput(title,filename).get_input(empty_allowed=True)
        if filename == None or len(filename) == 0:
            return None

        return filename      

    def enter_filename_to_load(self, title:str, name:str=None, extension:str="txt", show_current_path:bool=True, show_files_with_ext:bool=True) -> str:
        # current path
        if show_current_path:
            cur_path = pathlib.Path().resolve()
            print(f"Current working directory is {cur_path}")

            if show_files_with_ext and extension != None:
                relevant_path = str(cur_path)
                included_extensions = []
                included_extensions.append(extension.lower())
                included_extensions.append(extension.upper())
                file_names = [fn for fn in os.listdir(relevant_path)
                    if any(fn.endswith(ext) for ext in included_extensions)]
                
                if file_names != None and len(file_names) > 0:
                    print(f"Files found in {cur_path}:\n")
                    for file_name in file_names:
                        print(file_name)
                else:
                    print(f"No files with extension {extension} found in {cur_path}.")

        # prepare filename    
        filename = f"{name}"
        if filename.find(".") < 0:
            filename = f"{filename}.{extension}"

        filename = UserInput(title,filename).get_input(empty_allowed=True)
        if filename == None or len(filename) == 0:
            return None

        return filename      


    def save_file(self, filename:str, content:str, print_msg:bool=True) -> bool:
        try:
            with open(filename, "w") as text_file:
                text_file.write(content)
            if print_msg == True:
                print(f"File saved as {filename}")
            return True
        except Exception as exc:
            print(f"Errors occured while writing file {filename}: {type(exc)} - {exc}")
            return False

    def enter_filename_and_save_text(self, title:str, name:str, content:str, with_datetime_prefix:bool=True, extension:str="txt") -> bool:
            if name == None or len(name) == 0:
                filename = "unknown"
            else:
                filename = name.replace("/", "x")

            filename = self.enter_filename_to_save(title, f"{filename}", extension=extension, use_datetime_prefix=with_datetime_prefix)
            if filename != None and filename.find(".") > 0:
                return self.save_file(filename, content)  
            else:
                print("Save file skipped.")
                return False              

    def get_files_from_path(self, pathname:str=None, extension:str="csv") -> list:

        if pathname is None:
            cur_path = pathlib.Path().resolve()
            relevant_path = str(cur_path)
        else:
            relevant_path = pathname

        included_extensions = [extension.lower(), extension.upper()]

        file_names = [fn for fn in os.listdir(relevant_path)
                      if any(fn.endswith(ext) for ext in included_extensions)]

        result = []
        if file_names != None and len(file_names) > 0:
            for file in file_names:
                if pathname is None:
                    result.append(file)
                else:
                    result.append(pathname + "/" + file)

        return result

    def get_list_from_file(self, filename:str) -> list:
        try:            
            with open(self.get_processed_filename(), "r") as f:
                lines = f.readlines()

            if lines is None:
                self.error(f"file {filename} empty or error while reading")
                return None
            else:
                result = []
                for line in lines:
                    result.append(line.strip())

                self.info(f"File {filename} loaded with {len(self.processed)} lines.")
                return result
        except Exception as exc:
            self.error(f"Read file {filename} error: {exc}")
            return None

    def rename_file_with_extension(self, filename:str, extension:str=".processed") -> bool:
        try:
            os.rename(filename, f"{filename}.{extension}")
            return True
        except Exception as exc:
            self.error(f"Error while renaming file {filename} - {exc}")
            return False

    def move_file_to_directory(self, filename:str, directory:str="./processed") -> bool:
        try:
            only_filename = os.path.basename(filename)
            new_path = os.path.join(directory, only_filename)
            try:
                shutil.copy(filename, new_path)
            except IOError as io_err:
                os.makedirs(os.path.dirname(new_path))
                shutil.copy(filename, new_path)     
            return True
        except Exception as exc:
            self.error(f"Error while moving file {filename} to {directory}- {exc}")
            return False


class FileLoaderUtil(FileTransferUtil):
    def __init__(self, context:str) -> None:
        super().__init__()
        self.processed: list = None
        self.processed_context: str = context 
        self.processed_file_prefix: str = 'processed'
        self.processed_file_extension: str = 'txt'

    def info(self, msg):
        print(msg)

    def error(self, msg):
        print("Error: ", msg)

    def get_processed_filename(self) -> str:
        return f"{self.processed_file_prefix}_{self.processed_context}.{self.processed_file_extension}"

    def load_processed(self) -> bool:
        try:            
            with open(self.get_processed_filename(), "r") as f:
                lines = f.readlines()

            if lines is None:
                self.error(f"Processed file empty or error while reading")
                return False
            else:
                self.processed = []
                for line in lines:
                    self.processed.append(line.strip())

                self.info(f"Processed file loaded with {len(self.processed)} lines.")
                return True
        except:
            self.info("no processed file detected")
            self.processed = []
            return True

    def save_processed(self) -> bool:
        if self.processed is None:
            return False

        with open(self.get_processed_filename(), "w") as f:
            f.writelines(self.processed)

        return True

    def append_processed(self, filename:str) -> bool:
        if self.processed is None:
            if not self.load_processed():
                return False
        self.processed.append(filename)
        with open(self.get_processed_filename(), 'a+') as f:
            f.write(f"{filename}\n")
        self.info(f"file {filename} marked as processed.")
        return True

    def is_processed(self,filename:str) -> bool:
        try:
            if self.processed is None:
                if not self.load_processed():
                    return True
            if filename in self.processed:
                return True
            else:
                return False
        except Exception as exc:
            self.error(f"Exception in is_processed {exc} - {filename} in {self.processed}")
            return False





    


if __name__ == "__main__":
    
    print(UUIDUtil.build_unique_key("test"))
    print(UUIDUtil.build_unique_key("test"))
    print(UUIDUtil.build_unique_key("test"))

    print("test_utils finished")            