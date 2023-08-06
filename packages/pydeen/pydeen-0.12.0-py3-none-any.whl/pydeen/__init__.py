"""
PyDEEN init module. Defines main types and include sub modules
"""
__version__ = "0.12.0"

# import sub modules
import pydeen.core as core
import pydeen.types as types

import pydeen.menu as menu
import pydeen.service as service
import pydeen.auth as auth
import pydeen.odata as odata
#import pydeen.pyodata as pyodata
import pydeen.sap_abap as sap_abap
import pydeen.cloudevents as cloudevents
import pydeen.pandas as pandas

# import classes and main types
from pydeen.core import PyDEEN

from pydeen.types import Auth
from pydeen.types import Backend
from pydeen.types import Connector
from pydeen.types import Request
from pydeen.types import Result

# http support
from pydeen.http import HTTPBackend
from pydeen.http import HTTPConnector
from pydeen.http import HTTPRequest

# rest support
from pydeen.rest import HTTPRestConnector

# service support 
from pydeen.service import Service
from pydeen.service import ServiceContext
from pydeen.service import ServiceAction
from pydeen.service import ServiceActionCommands
from pydeen.service import ServiceCommand


# local service support
from pydeen.websocket import WebSocketService


def menu():
    print("menu not implemented yet")
    