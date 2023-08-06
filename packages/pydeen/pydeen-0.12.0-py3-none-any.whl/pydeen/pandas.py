"""
This module contains functions for integrating the pandas library
"""


import pandas as pd
import pandas.api.types as pd_types
import json
import numpy

from pydeen.menu import UserInput, MenuSelection, MenuMultiSelection
from pydeen.types import Result, Factory, Base
from pydeen.utils import FileTransferUtil, UUIDUtil

class PandasResultDataframe(Result):
    
    MENU_PANDAS_DISPLAY         = "pandas_display"
    MENU_PANDAS_INFO            = "pandas_info"
    MENU_PANDAS_RESULT_NAME     = "pandas_result_name"
    MENU_PANDAS_SET_DESC        = "pandas_set_desc"
    MENU_PANDAS_HEAD_TAIL       = "pandas_head_tail"
    MENU_PANDAS_DESCRIBE        = "pandas_describe"
    MENU_PANDAS_DATATYPES       = "pandas_datatypes"
    MENU_PANDAS_VALUE_DIST      = "pandas_value_dist"
    MENU_PANDAS_SAVE_CSV        = "pandas_save_csv"
    MENU_PANDAS_SAVE_XLS        = "pandas_save_xls"
    MENU_PANDAS_SAVE_PICKLE     = "pandas_save_pickle"
    MENU_PANDAS_LOAD_CSV        = "pandas_load_csv"
    MENU_PANDAS_LOAD_PICKLE     = "pandas_load_pickle"
    MENU_PANDAS_LOAD_XLS        = "pandas_load_xls"
    MENU_PANDAS_DATAHUB_EXPORT  = "pandas_export_datahub"
    MENU_PANDAS_DATAHUB_IMPORT  = "pandas_import_datahub"
    
    MENU_PANDAS_EXP_OPTION          = "pandas_expert_options"
    MENU_PANDAS_EXP_COL_SELECT      = "pandas_expert_select_column"
    MENU_PANDAS_EXP_COL_DELETE      = "pandas_expert_delete_column"
    MENU_PANDAS_EXP_COL_CONVERT     = "pandas_expert_convert_column"
    MENU_PANDAS_EXP_COL_SET_TEXT    = "pandas_expert_set_column_text"
    MENU_PANDAS_EXP_COL_SET_TYPE    = "pandas_expert_set_column_type"
    MENU_PANDAS_EXP_TAB_SCHEMA      = "pandas_expert_generate_table_schema"
    MENU_PANDAS_EXP_GENERATE_KEY    = "pandas_expert_generate_key"
    MENU_PANDAS_EXP_UNIQUE_KEY      = "pandas_expert_set_unique_key"
    MENU_PANDAS_EXP_UNIQUE_KEYS     = "pandas_expert_set_unique_keys"

    MENU_PANDAS_TAB_SCHEMA_DXP      = "pandas_table_schema_dxp"
    MENU_PANDAS_TAB_SCHEMA_SQLITE   = "pandas_table_schema_sqlite"





    def __init__(self, name:str, df:pd.DataFrame=None) -> None:
        super().__init__(df)
        self.type = "pydeen.PandasResultDataFrame"
        self.result_df:pd.DataFrame = df 
        self.result_name:str = name
        self.menu_title = "Pandas DataFrame - Menu"
        self.column_text = {}
        self.column_type = {}
        self.column_default = {}
        self.unique_key_field:str=None          # if there a single primary key field - use this
        self.unique_key_fields:list=None        # 1..n field for combined primary key

    def get_count(self) -> int:
        if self.is_empty():
            return 0
        else:
            return len(self.result_df.index)

    def get_dataframe(self) -> pd.DataFrame:
        return self.result_df
        
    def get_description(self) -> str:
        if self.result_name != None:
            super_desc = super().get_description()
            if super_desc == None:
                return f"{self.result_name}"
            else:
                return f"{self.result_name} {super_desc}"    
        else:
            return super().get_description()

    def get_default_filename(self, default:str=None) -> str:
        result = self.result_name
        if result == None or result == "":
            result = default
        if result == None or result == "":
            result = "DataFrame"
        return result.replace("/", "x")

    def reset_columns_info(self):
        self.column_default = {}
        self.column_text = {}
        self.column_type = {}
        return super().reset_columns_info()

    def get_columns(self) -> list:
        try:
            return self.result_df.columns.tolist()
        except Exception as exc:
            self.trace(f"Error occured while determing columns of DataFrame: {type(exc)} - {exc}")
            return super().get_columns()

        

    def is_unique_key_field_available(self) -> bool:
        if self.unique_key_field == None:
            return False
        else:
            return True

    def get_unique_key_field(self) -> str:
        return self.unique_key_field

    def set_unique_key_field(self, key_field:str) -> bool:
        if key_field == None:
            self.unique_key_field = None
            return True
        elif not self.is_column_available(colname=key_field):
            return False
        else:
            self.unique_key_field = key_field
            return True
    
    def set_unique_key_fields(self, key_fields:list) -> bool:
        try:
            new_keys = []
            for new_key in key_fields:
                if not self.is_column_available(new_key) or new_key in new_keys:
                    self.error(f"Column {new_key} not valid or duplicate")
                    return False
                else:
                    new_keys.append(new_key)
            self.unique_key_fields = new_keys
            return True
        except:
            return False
    
    def is_unique_keys_available(self) -> bool:
        if self.unique_key_fields == None or len(self.unique_key_fields) == 0:
            return False
        else:
            return True

    def get_unique_key_fields(self) -> list:
        return self.unique_key_fields


    def is_empty(self) -> bool:
        try:
            if type(self.result_df) == pd.DataFrame:
                return self.result_df.empty
            else:
                return True
        except Exception as exc:
            print("Error: ",type(exc), exc)
            return True

    
    def is_column_text_available(self, column_name:str) -> bool:
        if column_name in self.column_text:
            return True
        else:
            return False

    def get_column_text(self, column_name:str, append_key:bool=True) -> str:
        if not self.is_column_text_available(column_name):
            return column_name
        else:
            col_text = self.column_text[column_name]
            if append_key:
                return f"{col_text} ({column_name})"
            else:
                return col_text

    def set_column_text(self, column_name:str, column_text:str):
        self.column_text[column_name] = column_text

    def is_column_type_available(self, column_name:str) -> bool:
        if column_name in self.column_type:
            return True
        else:
            return False

    def get_column_type(self, column_name:str, default:str=None) -> str:
        if self.is_column_type_available(column_name):
            return self.column_type[column_name]
        else:
            if default == None:
                return self.detect_column_type(column_name)
            else:
                return default

    def set_column_type(self, column_name:str, column_type:str):
        self.column_type[column_name] = column_type


    def is_column_default_available(self, column_name:str) -> bool:
        if column_name in self.column_default:
            return True
        else:
            return False

    def get_column_default(self, column_name:str, default=None) -> str:
        if self.is_column_default_available(column_name):
            return self.column_default[column_name]
        else:
            return default

    def set_column_default(self, column_name:str, column_default):
        self.column_default[column_name] = column_default


    def detect_column_type(self, column_name:str) -> str:
        try:
            pd_col = self.result_df[column_name]
            if pd_types.is_string_dtype(pd_col):
                return Result.DATA_TYPE_TEXT
            elif pd_types.is_bool_dtype(pd_col):
                return Result.DATA_TYPE_BOOLEAN
            elif pd_types.is_datetime64_any_dtype(pd_col):
                return Result.DATA_TYPE_TIMESTAMP
            elif pd_types.is_integer_dtype(pd_col):
                return Result.DATA_TYPE_INTEGER
            elif pd_types.is_float_dtype(pd_col):
                return Result.DATA_TYPE_DECIMAL
            else:
                print(f"unknown pandas datatype for column {column_name}. set text.")
                return Result.DATA_TYPE_TEXT
        except Exception as exc:                    
            print(f"Error while detecting pandas df column type for {column_name} ({self.result_df[column_name].object_d}): {type(exc)} - {exc}")
            return Result.DATA_TYPE_TEXT

    def detect_has_column_null_values(self, column_name:str) -> bool:
        if self.result_df[column_name].isnull().sum() > 0:
            return True
        else:
            return False

    def detect_is_column_unique(self, column_name:str) -> bool:
        return False
        if self.result_df[column_name].unique().sum() == 0:
            return True
        else:
            return False


    def drop_columns(self, columns:list) -> bool:
        existing_cols = self.get_columns()
        if existing_cols == None or len(existing_cols) == 0:
            return False
        
        for col_name in columns:
            if col_name in existing_cols:
                self.result_df = self.result_df.drop(col_name, axis=1)
                self.info(f"Column {col_name} dropped.")
            else:
                self.error(f"Error while dropping column {col_name}.")
                return False        
        return True

    def get_cell_value(self, row:int, colname:str):
        if self.is_empty():
            return None
        try:
            value = self.result_df[colname].loc[row]
            #if value == "NaN" or str(value) == "NaN":
            #    print("NaN detected: ", type(value))
            #    value = None
            return value
        except:
            return None
    
    def generate_unique_key(self, row:int, columns_for_key:list, method:str=None) -> str:
        try:
            if len(columns_for_key) == 0:
                return None
            
            keys = []
            for col in columns_for_key:
                value = self.get_cell_value(row, col)
                keys.append(str(value))

            keys_to_hash = json.dumps(keys)
            unique_key = UUIDUtil.build_unique_key(keys_to_hash)    
            return unique_key, keys_to_hash
        except Exception as exc:
            self.error(f"Error while creating unique key: {exc}")
            return None    

    def generate_unique_key_column(self, key_col_name:str, columns_for_key:list) -> bool:
        try:
            # check
            cols = self.get_columns()
            if key_col_name in cols:
                self.error(f"Column exists already: {key_col_name}")
                return False

            # prepare access
            df   = self.result_df

            # loop rows
            data = []
            key_memory = {}

            for i in range(len(df)):
                unique_key, keys_to_hash = self.generate_unique_key(i,columns_for_key)
                if unique_key == None or unique_key in data:
                    used_by = key_memory[unique_key]
                    self.error(f"invalid unique key or duplicate in row {i} for key info {keys_to_hash}: {unique_key} used in row index {used_by[0]} for key {used_by[1]}.")
                    return False
                else:
                    data.append(unique_key)
                    key_memory[unique_key] = (i, keys_to_hash)
            # add  new key col
            self.result_df.insert(0, key_col_name, data)  

            # remember that key
            if not self.is_unique_key_field_available():
                self.set_unique_key_field(key_col_name)
                self.info(f"Unique key field {key_col_name} set to pandas dataframe object")

            return True 
        except Exception as exc:
            self.error(f"Error while key column: {exc}")
            return False

    def get_as_list_of_dict(self) -> list:
        # check
        if self.is_empty():
            return None
        
        
        # prepare access
        result = []
        cols = self.get_columns()
        df   = self.result_df

        # loop rows
        for i in range(len(df)):
            record = {}
            for col in cols:
                value_raw = df[col].loc[i]
                key   = col
                
                value_type = type(value_raw)
                if value_type == numpy.int64:
                    value = int(value_raw)
                elif value_type == numpy.float64:
                    value = float(value_raw)
                elif value_type == numpy.bool_:
                    value = bool(numpy)        
                else:                    
                    value = value_raw

                record[key] = value
            result.append(record)

        return result

    def generate_table_schema_dxp(self) -> str:
        # check
        columns = self.get_columns()
        if columns == None or len(columns) == 0:
            return None

        # build schema
        result = {}
        result["id"]          = UUIDUtil.new_uuid32_separated_string()
        result["name"]        = self.get_name()
        result["description"] = self.get_description()

        # build field list
        dxp_reserved = [
            "id",
            "updatedAt",
            "changedBy",
            "createdAt",
            "createdBy"
        ]  
        fields = []
        
        for colname in columns:
            # ignore reserved
            if colname in dxp_reserved:
                continue
            
            field = {
                "id" : UUIDUtil.new_uuid32_separated_string(),
                "fieldName" : colname,
                #"Default" : "test",
                "description" : self.get_column_text(colname),
                "fieldType" : self.get_column_type(colname),
                "isNullable": self.detect_has_column_null_values(colname),
                "isUnique" : self.detect_is_column_unique(colname)
            }
            fields.append(field)
        
        if len(fields) == 0:
            self.error("Empty DXP field list")
            return None
        else:
            result["fields"] = fields
        
        # return as json string
        return json.dumps(result)

    def generate_table_schema_sqlite(self) -> str:
        # check
        columns = self.get_columns()
        if columns == None or len(columns) == 0:
            return None

        # build schema
        result = f"CREATE TABLE IF NOT EXISTS {self.get_name().upper().strip()} (\n"

        index = 0
        for colname in columns:

            col_text    = self.get_column_text(colname)
            col_default = self.get_column_default(colname)
            col_type    = self.get_column_type(colname)     
            col_is_nullable = self.detect_has_column_null_values(colname)
            col_is_unique = self.detect_is_column_unique(colname) 
            
            if index > 0:
                result += ",\n"

            if col_type == Result.DATA_TYPE_BOOLEAN:
                sql_type = "INTEGER"
            elif col_type == Result.DATA_TYPE_DECIMAL:
                sql_type = "REAL"
            elif col_type == Result.DATA_TYPE_TIMESTAMP:
                sql_type = "TEXT"
            elif col_type == Result.DATA_TYPE_BINARY:
                sql_type = "BLOB"
            else:
                sql_type = col_type.upper()

            result += f"   {colname.upper()} {sql_type}"
            
            if index == 0:
                result += " PRIMARY KEY"
            
            if not col_is_nullable:
                result += " NOT NULL"

            if col_is_unique:
                result += " UNIQUE"

            if col_default != None:
                if col_type == Result.DATA_TYPE_TEXT:
                    result += " DEFAULT " + '"' + col_default + '"'
                else:
                    result += " DEFAULT " + col_default
            index += 1

        # append closing
        result += "\n)"
        
        # return 
        return result


    def menu_print_table_schema(self, schema_string:str, layout:str, extension:str="json"):
        if schema_string == None or len(schema_string) == 0:
            print("Table schema generation failed.")
        else:
            print(f"Table schema in '{layout}' layout:\n\n{schema_string}\n")  
            if UserInput("Save as file").get_input_yes_no(default_yes=False):
                name = self.get_name()
                FileTransferUtil().enter_filename_and_save_text(f"Save {layout} table layout", name, schema_string, extension=extension)

    def menu_generate_unique_key(self):
        # checks
        if self.is_empty():
            return None
        
        columns = self.get_columns()
        if columns == None or len(columns) == 0:
            return

        # get key column
        key_col = UserInput("Enter a name for the new key colum").get_input(empty_allowed=True)
        if key_col == None or key_col == "":
            return

        if self.is_column_available(key_col):
            self.error(f"Column name '{key_col}' exists.")
            return

        # enter columns to create key
        use_col = self.get_unique_key_fields()
        if use_col == None or len(use_col) == 0:
            use_col = self.menu_select_columns("Select columns for creating unique key")
        if use_col == None or len(use_col) == 0:
            return

        # generate key col now
        if self.generate_unique_key_column(key_col, use_col) == True:
            print(f"New unique key column '{key_col}' created.")
        else:
            print(f"New unique key column '{key_col}' not created.")


    def menu_select_table_schema_option(self):
        # checks
        if self.is_empty():
            return None
        
        columns = self.get_columns()
        if columns == None or len(columns) == 0:
            return

        # loop columns and create menu items
        entries = {}
        entries[PandasResultDataframe.MENU_PANDAS_TAB_SCHEMA_SQLITE] = "SQLite create statement"
        entries[PandasResultDataframe.MENU_PANDAS_TAB_SCHEMA_DXP] = "DXP table definition layout"


        # execute selection
        action = MenuSelection("Select table schema type", entries).show_menu()       
        if action.is_cancel_entered():
            return None
        
        # get and process selection
        selected  = action.get_selection()
        if selected == PandasResultDataframe.MENU_PANDAS_TAB_SCHEMA_DXP:
            self.menu_print_table_schema(self.generate_table_schema_dxp(), "DXP", extension="json")
        elif selected == PandasResultDataframe.MENU_PANDAS_TAB_SCHEMA_SQLITE:
            self.menu_print_table_schema(self.generate_table_schema_sqlite(), "SQLite", extension="sql")
        else:
            print(f"Unknown table generation option: {selected}")

    def menu_select_column(self, title:str=None) -> str:
        columns = self.get_columns()
        use_title = title
        if use_title == None:
            use_title = "Select column"
        return UserInput(use_title).get_selection_from_list("Show value distribution for dataframe column", columns)

    def menu_select_columns(self, title:str=None, selected:list=None) -> list:
        # checks
        if self.is_empty():
            return None
        
        columns = self.get_columns()
        if columns == None or len(columns) == 0:
            return

        # loop columns and create menu items
        entries = {}
        for col_name in columns:
            col_text = self.get_column_text(col_name)
            entries[col_name] = col_text 

        # execute selection
        use_title = title
        if use_title == None:
            use_title = "Select columns"
        action = MenuMultiSelection(use_title, entries, selected=selected).show_menu()       
        if action.is_cancel_entered():
            return None
        else:
            result = action.get_multi_selection()
            return result    

    def menu_expert_options(self):
        
        entries = {}
        if not self.is_unique_keys_available():
            entries[PandasResultDataframe.MENU_PANDAS_EXP_UNIQUE_KEYS] = "Set the columns for a unique key"
        
        if not self.is_unique_key_field_available():
            entries[PandasResultDataframe.MENU_PANDAS_EXP_UNIQUE_KEY] = "Set the unique primary key column"
            entries[PandasResultDataframe.MENU_PANDAS_EXP_GENERATE_KEY] = "Generate unique key column"
        
        entries[PandasResultDataframe.MENU_PANDAS_EXP_TAB_SCHEMA] = "Generate table schema"
        
        entries[PandasResultDataframe.MENU_PANDAS_EXP_COL_DELETE] = "Delete columns"

        # process menus
        action = MenuSelection("Select expert option", entries).show_menu()
        if action.is_cancel_entered():
            return
        else:
            selected = action.get_selection()
            if selected == PandasResultDataframe.MENU_PANDAS_EXP_COL_DELETE:
                selection = self.menu_select_columns()
                if selection != None and len(selection) > 0:
                    if self.drop_columns(selection):
                        print("Selected columns dropped.")
                    else:
                        print("Error while dropping columns.")
            elif selected == PandasResultDataframe.MENU_PANDAS_EXP_TAB_SCHEMA:
                self.menu_select_table_schema_option()
            elif selected == PandasResultDataframe.MENU_PANDAS_EXP_GENERATE_KEY:
                self.menu_generate_unique_key()
            elif selected == PandasResultDataframe.MENU_PANDAS_EXP_UNIQUE_KEYS:
                new_keys = self.menu_select_columns("Select columns to build an unique key", self.get_unique_key_fields())
                if new_keys != None and len(new_keys) > 0:
                    self.set_unique_key_fields(new_keys)
                    print(f"Selected columns {new_keys} are set as combined unique key for this dataframe.")
            elif selected == PandasResultDataframe.MENU_PANDAS_EXP_UNIQUE_KEY:
                new_key = self.menu_select_column("Select column for the unique key")
                if new_key != None and len(new_key) > 0:
                    self.set_unique_key_field(new_key)
                    print(f"Column {new_key} is set as unique key for this dataframe.")
            else:
                print(f"unknown expert option or not handled: {selected}")

    def menu_get_subtitle(self) -> str:
        if self.is_empty():
            return None
        else:
            result_count = self.get_count()
            result_type = type(self.result)
            result_columns = self.get_columns()
            result_col_count = 0
            if result_columns != None:
                result_col_count = len(result_columns)
            result =  f"Pandas Dataframe result rows {result_count} x columns {result_col_count}"
            if self.is_unique_key_field_available():
                result += f"\nUnique key field: {self.get_unique_key_field()}"
            if self.is_unique_keys_available():
                result += f"\nUnique combined key fields: {self.get_unique_key_fields()}"
            return result        

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = Base.menu_get_entries(self,prefilled)
        try:
            if type(self.result_df) == pd.DataFrame:
                entries[PandasResultDataframe.MENU_PANDAS_RESULT_NAME] = f"Rename dataframe ({self.result_name})"
                entries[PandasResultDataframe.MENU_PANDAS_SET_DESC] = f"Set description dataframe ({super().get_description()})"
                entries[PandasResultDataframe.MENU_PANDAS_DISPLAY] = "Display dataframe"
                entries[PandasResultDataframe.MENU_PANDAS_INFO] = "Display dataframe info"

                if not self.is_empty():
                    entries[PandasResultDataframe.MENU_PANDAS_HEAD_TAIL] = "Display dataframe head/tail"
                    entries[PandasResultDataframe.MENU_PANDAS_DESCRIBE] = "Describe dataframe"
                    entries[PandasResultDataframe.MENU_PANDAS_DATATYPES] = "Display dataframe types"
                    entries[PandasResultDataframe.MENU_PANDAS_VALUE_DIST] = "Show value distribution of column"
                    entries[PandasResultDataframe.MENU_PANDAS_SAVE_CSV] = "Save dataframe to csv file"
                    entries[PandasResultDataframe.MENU_PANDAS_SAVE_XLS] = "Save dataFrame to excel file"
                    entries[PandasResultDataframe.MENU_PANDAS_SAVE_PICKLE] = "Save dataframe to pickle file"
                    entries[PandasResultDataframe.MENU_PANDAS_DATAHUB_EXPORT] = "Export to Datahub"
                    entries[PandasResultDataframe.MENU_PANDAS_EXP_OPTION] = "Expert options"
            else:
                entries[PandasResultDataframe.MENU_PANDAS_LOAD_CSV] = "Load csv file"
                entries[PandasResultDataframe.MENU_PANDAS_LOAD_XLS] = "Load from dataframe excel file"
                entries[PandasResultDataframe.MENU_PANDAS_LOAD_PICKLE] = "Load from dataframe pickle file"
                entries[PandasResultDataframe.MENU_PANDAS_DATAHUB_EXPORT] = "Import from Datahub"
        except Exception as exc:
            self.error(f"errors occured in pandas df menu {exc}")
        
        return entries

    def menu_process_selection(self, selected: str, text: str = None):
        if selected == PandasResultDataframe.MENU_PANDAS_DISPLAY:
            print(self.result_df)
        elif selected == PandasResultDataframe.MENU_PANDAS_RESULT_NAME:
            new_name = UserInput("Enter new name for dataframe", self.result_name).get_input(empty_allowed=True)
            if new_name != None and len(new_name) > 0 and self.result_name != new_name:
                self.result_name = new_name
                print(f"dataframe renamed to {new_name}")
        elif selected == PandasResultDataframe.MENU_PANDAS_SET_DESC:
            new_desc = UserInput("Enter new description for dataframe", super().get_description()).get_input(empty_allowed=True)
            if new_desc != None and len(new_desc) > 0:
                self.set_description(new_desc)
                print(f"dataframe description set to {new_desc}")
        elif selected == PandasResultDataframe.MENU_PANDAS_INFO:
            print(self.result_df.info())
        elif selected == PandasResultDataframe.MENU_PANDAS_HEAD_TAIL:
            print(self.result_df.head())
            print(self.result_df.tail())
        elif selected == PandasResultDataframe.MENU_PANDAS_DESCRIBE:
            print(self.result_df.describe())
        elif selected == PandasResultDataframe.MENU_PANDAS_DATATYPES:
            print(self.result_df.dtypes)
        elif selected == PandasResultDataframe.MENU_PANDAS_VALUE_DIST:
            selected = self.menu_select_column()
            if selected != None:
                print(f"values of column {selected}:")
                print(self.result_df[selected].value_counts())   
        elif selected == PandasResultDataframe.MENU_PANDAS_SAVE_CSV:
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_save("Save current dataframe to csv", result_name, "csv", use_datetime_prefix=True)
            if filename != None:
                self.result_df.to_csv(filename, sep="\t", index=False)
                print(f"dataframe saved to csv file {filename}")
        elif selected == PandasResultDataframe.MENU_PANDAS_SAVE_XLS:
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_save("Save current dataframe to excel", result_name, "xlsx", use_datetime_prefix=True)
            if filename != None:
                self.result_df.to_excel(filename, sheet_name='pydeen_dataframe', header=True, index = False)
                print(f"dataframe saved to excel file {filename}")
        elif selected == PandasResultDataframe.MENU_PANDAS_SAVE_PICKLE:
            result_name = self.get_default_filename("dataframe_pickle")                
            filename = FileTransferUtil().enter_filename_to_save("Save current dataframe as pickle file", result_name, "pkl", use_datetime_prefix=True)
            if filename != None:
                print(f"Start save dataframe pickle file as {filename}...", self.result_df, type(self.result_df))    
                self.result_df.to_pickle(filename)
                print(f"dataframe pickle file saved as {filename}")    
        
        elif selected == PandasResultDataframe.MENU_PANDAS_LOAD_PICKLE:                
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_load("Load dataframe from pickle file", name=result_name, extension="pkl")
            if filename != None:
                new_df = pd.read_pickle(filename)
                if type(new_df) != pd.DataFrame:
                    print("Loading pandas pickle file failed or cancelled")
                else:
                    self.result_df = new_df
                    print(f"dataframe pickle file loaded from {filename}")    
        elif selected == PandasResultDataframe.MENU_PANDAS_LOAD_CSV:                
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_load("Load dataframe from csv file", name=result_name, extension="csv")
            if filename != None:
                new_df = pd.read_csv(filename, sep="\t")
                if type(new_df) != pd.DataFrame:
                    print("Loading csv file into pandas dataframe failed or cancelled")
                else:
                    self.result_df = new_df
                    print(f"dataframe loaded from csv file {filename}")    

        elif selected == PandasResultDataframe.MENU_PANDAS_LOAD_XLS:                
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_load("Load dataframe from excel file", name=result_name, extension="xlsx")
            if filename != None:
                new_df = pd.read_excel(filename)
                if type(new_df) != pd.DataFrame:
                    print("Loading excel file into pandas dataframe failed or cancelled")
                else:
                    self.result_df = new_df
                    print(f"dataframe loaded from excel file {filename}")    
        elif selected == PandasResultDataframe.MENU_PANDAS_DATAHUB_EXPORT:
                if Factory.get_datahub().register_object_with_userinput(self) == True:
                    print("Pandas dataframe result exported to datahub.")
                else:
                    print("Pandas dataframe result not exported to datahub.")        
        elif selected == PandasResultDataframe.MENU_PANDAS_DATAHUB_IMPORT:
                try:
                    dh = Factory.get_datahub()
                    df_key = dh.menu_select_key("Select dataframe result object", PandasResultDataframe)
                    if df_key != None and df_key != "":
                        dh_object = dh.get_object(df_key)
                        self.result_df = PandasResultDataframe.get_pd.DataFrame(dh_object)
                        if self.result_df != None:
                            print("Pandas dataframe loaded from datahub.")
                            print(self.result_df.info())
                        else:
                            print("Pandas dataframe not loaded from datahub.")        
                except Exception as exc:
                    print(f"Loading from datahub failed: {type(exc)} - {exc}")    
        elif selected == PandasResultDataframe.MENU_PANDAS_EXP_OPTION:
            self.menu_expert_options()

        else:    
            return super().menu_process_selection(selected, text)    
