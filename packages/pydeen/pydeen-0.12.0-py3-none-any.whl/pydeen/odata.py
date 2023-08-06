"""
    basic features to support the odata protocol
"""

from pydeen.types import Base, EntityMetaInfo, Result, ResultSingle
from pydeen.utils import FileTransferUtil
from xml.dom.minidom import parseString, Document, Element
import json

class ODataMetaEntity(EntityMetaInfo):

    def __init__(self, metadata_util, entity:str) -> None:
        super().__init__()
        self.type = "pydeen.ODataMetaEntity"
        self.util:ODataMetadata = metadata_util
        self.entity = entity

    def get_columns(self) -> list:
        try:
            entity_type = self.util.get_entity_type_mapping(self.entity)
            entity_attributes = self.util.get_entity_type_attributes(entity_type)
            return list(entity_attributes[ODataMetadata.PROP_ENTITITY_PROPS].keys())
        except Exception as exc:                   
            self.error(f"OData get columns failed: {type(exc)} - {exc}")
            return None

    def get_column_properties(self, column) -> dict:
        try:
            entity_type = self.util.get_entity_type_mapping(self.entity)
            entity_attributes = self.util.get_entity_type_attributes(entity_type)
            return entity_attributes[ODataMetadata.PROP_ENTITITY_PROPS][column]
        except Exception as exc:                   
            self.error(f"OData get column {column} properties failed: ", type(exc), exc)
            return None

    def get_column_type(self, column) -> str:
        try:
            entity_type = self.util.get_entity_type_mapping(self.entity)
            entity_attributes = self.util.get_entity_type_attributes(entity_type)
            return entity_attributes[ODataMetadata.PROP_ENTITITY_PROPS][column]["Type"]
        except Exception as exc:                   
            self.error(f"OData get column {column} type failed: {type(exc)} {exc}")
            return None


class ODataMetadata(Base):

    PROP_METADATA           = "metadata"
    PROP_METADATA_XML       = "metadata_xml"    
    PROP_ENTITITY_TYPES     = "entityTypes"    
    PROP_ENTITIES           = "entities"    
    PROP_ENTITITY_KEYS      = "keys"
    PROP_ENTITITY_PROPS     = "properties"
    PROP_ENTITITY_ASSOCS    = "associations"

    MENU_METADATA_XML_DISP  = "metadata_xml_display"
    MENU_METADATA_XML_SAVE  = "metadata_xml_save"
    MENU_METADATA_JSON_DISP = "metadata_json_display"
    MENU_METADATA_JSON_SAVE = "metadata_json_save"


    def __init__(self, name:str=None) -> None:
        super().__init__()
        self.type = "pydeen.ODataMetadata"
        self.metadata_xml:str=None
        self.menu_title = "OData Metainfo - Menu"
        self.name = name

    def parse_entity_type_properties(self, entity_type:Element) -> dict:
        result = {}
        
        properties = entity_type.getElementsByTagName("Property")
        for prop in properties:
            prop_meta = {}
            prop_name = prop.getAttribute("Name")
            for attr_key in prop.attributes.keys():
                prop_meta[attr_key] = prop.getAttribute(attr_key)
            result[prop_name] = prop_meta   

        return result

    def parse_entity_type_nav_properties(self, entity_type:Element) -> dict:
        result = {}
        
        properties = entity_type.getElementsByTagName("NavigationProperty")
        for prop in properties:
            prop_meta = {}
            prop_name = prop.getAttribute("Name")
            for attr_key in prop.attributes.keys():
                prop_meta[attr_key] = prop.getAttribute(attr_key)
            result[prop_name] = prop_meta   

        return result

    def parse_entity_type_keys(self, entity_type:Element) -> list:
        result = []
        
        ent_keys = entity_type.getElementsByTagName("PropertyRef")
        for ent_key in ent_keys:
            key_name = ent_key.getAttribute("Name")
            result.append(key_name)        

        return result

    def parse_dom_entity_types(self, dom:Document) -> dict:
        result = {}

        entity_types = dom.getElementsByTagName("EntityType")
        for entity_type in entity_types:
            # EntityType
            entity_json = {}
            entity_name = entity_type.getAttribute("Name")
            for ent_attr in entity_type.attributes.keys():
                entity_json[ent_attr] = entity_type.getAttribute(ent_attr) 

            #build together        
            entity_json[ODataMetadata.PROP_ENTITITY_PROPS] = self.parse_entity_type_properties(entity_type)
            entity_json[ODataMetadata.PROP_ENTITITY_KEYS] = self.parse_entity_type_keys(entity_type) 
            entity_json[ODataMetadata.PROP_ENTITITY_ASSOCS] = self.parse_entity_type_nav_properties(entity_type)
            
            result[entity_name] = entity_json

        return result

    def parse_dom_entities(self, dom:Document) -> dict:
        result = {}
        
        ent_sets = dom.getElementsByTagName("EntitySet")
        for ent_set in ent_sets:
            entity_set = {}
            ent_set_name = ent_set.getAttribute("Name")
            ent_set_type = ent_set.getAttribute("EntityType")
            
            if ent_set_type.find(".") > 0:
                ent_set_type_parts = ent_set_type.split(".")
                entity_set["Type"] = ent_set_type_parts[-1]
            else:
                entity_set["Type"] = ent_set_type
            
            for ent_set_attr_key in ent_set.attributes.keys():
                entity_set[ent_set_attr_key] = ent_set.getAttribute(ent_set_attr_key)
            
            result[ent_set_name] = entity_set
        
        return result

    def get_metadata_xml(self) -> str:
        try:
            return self._properties[ODataMetadata.PROP_METADATA_XML] 
        except:
            self.error("metadata xml not available")
            return None    
    
    def get_metadata_json(self) -> str:
        try:
            return self._properties[ODataMetadata.PROP_METADATA] 
        except:
            self.error("metadata json not available")
            return None   

    def parse_metadata_xml(self, metadata:str, name:str=None) -> bool:
        try:
            # init dom
            self.name = None
            dom = parseString(metadata)        
            if dom == None:
                self.error("error dom parsing")
                return False

            # prepare
            meta_json = {}
            meta_json[ODataMetadata.PROP_ENTITITY_TYPES] = self.parse_dom_entity_types(dom)
            meta_json[ODataMetadata.PROP_ENTITIES] = self.parse_dom_entities(dom)
            # store            
            self._properties[ODataMetadata.PROP_METADATA] = meta_json
            self._properties[ODataMetadata.PROP_METADATA_XML] = metadata
            self.name = name
            return True
        except:
            return False

    def get_entity_keys(self) -> list:
        try:
            return self._properties[ODataMetadata.PROP_METADATA][ODataMetadata.PROP_ENTITIES].keys()
        except:
            self.error("invalid odata metadata entity keys")
            return None    

    def get_entity_type_keys(self) -> list:
        try:
            return self._properties[ODataMetadata.PROP_METADATA][ODataMetadata.PROP_ENTITITY_TYPES].keys()
        except:
            self.error("invalid odata metadata entity set keys")
            return None               

    def get_entity_type_mapping(self, entity:str) -> str:
        try:
            return self._properties[ODataMetadata.PROP_METADATA][ODataMetadata.PROP_ENTITIES][entity]["Type"]
        except:
            self.error("invalid odata metadata entity type mapping")
            return None  
    
    def get_entity_attributes(self, entity:str) -> dict:
        try:
            return self._properties[ODataMetadata.PROP_METADATA][ODataMetadata.PROP_ENTITIES][entity]
        except:
            self.error("invalid odata metadata entity attributes")
            return None  

    def get_entity_type_attributes(self, entity_type:str) -> dict:
        try:
            return self._properties[ODataMetadata.PROP_METADATA][ODataMetadata.PROP_ENTITITY_TYPES][entity_type]
        except:
            self.error("invalid odata metadata entity type attributes")
            return None  

    def get_entity_util(self, entity:str) -> ODataMetaEntity:
                
        return ODataMetaEntity(self, entity)

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = super().menu_get_entries(prefilled)
        entries[ODataMetadata.MENU_METADATA_XML_DISP] = f"Display metadata XML"
        entries[ODataMetadata.MENU_METADATA_XML_SAVE] = f"Save metadata XML"
        entries[ODataMetadata.MENU_METADATA_JSON_DISP] = f"Display metadata JSON"        
        entries[ODataMetadata.MENU_METADATA_JSON_SAVE] = f"Save metadata JSON"        
        return entries

    def menu_process_selection(self, selected: str, text: str = None):
        if selected == ODataMetadata.MENU_METADATA_XML_DISP:
            print(self.get_metadata_xml())
        elif selected == ODataMetadata.MENU_METADATA_XML_SAVE:
            FileTransferUtil().enter_filename_and_save_text("Save metadata XML to", f"metainfo_{self.name}",  self.get_metadata_xml(), with_datetime_prefix=True, extension="xml")            
        elif selected == ODataMetadata.MENU_METADATA_JSON_DISP:
            print(self.get_metadata_json())
        elif selected == ODataMetadata.MENU_METADATA_JSON_SAVE:
            FileTransferUtil().enter_filename_and_save_text("Save metadata JSON to", f"metainfo_{self.name}",  json.dumps(self.get_metadata_json()), with_datetime_prefix=True, extension="json")
        else:       
            return super().menu_process_selection(selected, text)    


class ODataResult(Result):

    def __init__(self, result, name:str=None) -> None:
        super().__init__(result=result, name=name)
        self.type = "pydeen.ODataResult"

class ODataResultSingle(ResultSingle):

    def __init__(self, result, name:str=None) -> None:
        super().__init__(result=result, name=name)
        self.type = "pydeen.ODataResultSingle"

    def set_from_raw_result_single(self, result_single:ResultSingle):
        self._properties = {}
        self._properties.update(result_single._properties)
        self.interactive = result_single.interactive
        self.debug = result_single.debug
        self.entityMetaInfo = result_single.entityMetaInfo
        self.columns = result_single.columns

    def get_navigation_properties(self) -> dict:
        if self.result != None and type(self.result) == dict:
            keys = dict(self.result).keys()
            result = {}            
            for key in keys:
                offset = key.find("___deferred_uri")
                if offset > 0:
                    name = key[:offset]
                    url = dict(self.result)[key]
                    result[name] = url
        
            return result
        else:
            return None