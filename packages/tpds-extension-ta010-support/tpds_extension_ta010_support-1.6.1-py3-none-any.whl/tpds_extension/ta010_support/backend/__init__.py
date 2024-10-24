import os
from tpds.devices import TpdsDevices
from tpds.xml_handler import XMLProcessingRegistry
from tpds.app.vars import get_app_ref
from .api.apis import router
from ecc204_support.api.ecc204_xml_updates import ECC204_TA010_TFLXAUTH_XMLUpdates, ECC204_TA010_TFLXWPC_XMLUpdates
from ecc204_support import msg_handler

TpdsDevices().add_device_info(os.path.dirname(__file__))
XMLProcessingRegistry().add_handler('TA010_TFLXAUTH', ECC204_TA010_TFLXAUTH_XMLUpdates('TA010_TFLXAUTH'))
XMLProcessingRegistry().add_handler('TA010_TFLXWPC', ECC204_TA010_TFLXWPC_XMLUpdates('TA010_TFLXWPC'))

if get_app_ref():
    get_app_ref()._messages.register(msg_handler.symm_auth_user_inputs)
    get_app_ref()._messages.register(msg_handler.wpc_user_inputs)
