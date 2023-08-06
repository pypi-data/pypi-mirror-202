import urllib
import jsons
from .utilities import getRequest, postRequest, putRequest, getMaterialsApiTarget, getClientAliasId
from .entities import Material, MaterialComponentData

import json

class MaterialInfo:
    def __init__(self, id: str, displayName: str) -> None:
        self.id = id
        self.displayName = displayName

class MaterialCasIdInfo:
    def __init__(self, name: str, casId: str):
        self.name = name
        self.casId = casId

# CAS Controller  
def getAllCasIds() -> list[MaterialCasIdInfo]():

    """Gets a list containing the names of all available materials and their CAS IDs.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
         List[MaterialCasIdInfo]: The list of available materials names and their CAS IDs.
    """

    url = f'{getMaterialsApiTarget()}cas?clientId={getClientAliasId()}'
    print(url)
    response = getRequest(url)

    if response.ok:

        materials = json.loads(response.text)

        materialsInfoList = list[MaterialCasIdInfo]()

        for material in materials:
            materialsInfoList.append(MaterialCasIdInfo(material["casId"], material["name"]))

        return materialsInfoList

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)
    
def getMaterialByCasId(casId: str) -> Material:
    
    """Gets a material by CAS ID.

    Args:
        casId (str): The CAS ID to search for,

    Raises:
        ValueError: Any communication error with the PWS APIs or if a material with the supplied CAS ID cannot be found.

    Returns:
        Material: The material which has the supplied CAS ID.
    """

    url = f'{getMaterialsApiTarget()}cas/{casId}?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materialJson = json.loads(response.text)
        material = Material()
        material.initialiseFromDictionary(materialJson)

        return material
    
    elif response.status_code == 404: 
        raise ValueError('Material with the specifid CAS ID not found.', casId)

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)

# Components Controller
def getDNVComponents() -> list[MaterialComponentData]: 

    """Gets all of the DNV components.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
        list[MaterialComponentData]: A list of MaterialComponentData objects for each of the DNV components.
    """
    url = f'{getMaterialsApiTarget()}components?clientId={getClientAliasId()}&sources=1'

    response = getRequest(url)

    if response.ok:

        materialComponents = list[MaterialComponentData]()

        for json_def in json.loads(response.text):
            component = MaterialComponentData()
            component.id = json_def['id']
            component.name = json_def['displayName']
            component.displayName = json_def['displayName']
            component.casId = json_def['extendedProperties']['casId']
            materialComponents.append(component)

        return materialComponents
    else:
        raise ValueError('Failed to get components', response.status_code, response.text)
    
def getDIPPRComponents() -> list[MaterialComponentData]: 

    """Gets all of the DIPPR components.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
        list[MaterialComponentData]: A list of MaterialComponentData objects for each of the DIPPR components.
    """
    url = f'{getMaterialsApiTarget()}components?clientId={getClientAliasId()}&sources=2'

    response = getRequest(url)

    if response.ok:

        materialComponents = list[MaterialComponentData]()

        for json_def in json.loads(response.text):
            component = MaterialComponentData()
            component.id = json_def['id']
            component.name = json_def['displayName']
            component.displayName = json_def['displayName']
            component.casId = json_def['extendedProperties']['casId']
            materialComponents.append(component)

        return materialComponents
    else:
        raise ValueError('Failed to get components', response.status_code, response.text)
    
def getUserComponents() -> list[MaterialComponentData]: 

    """Gets all of the user created components.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
        list[MaterialComponentData]: A list of MaterialComponentData objects for each of the user created components.
    """
    url = f'{getMaterialsApiTarget()}components?clientId={getClientAliasId()}&sources=3'

    response = getRequest(url)

    if response.ok:

        materialComponents = list[MaterialComponentData]()

        for json_def in json.loads(response.text):
            component = MaterialComponentData()
            component.id = json_def['id']
            component.name = json_def['displayName']
            component.displayName = json_def['displayName']
            component.casId = json_def['extendedProperties']['casId']
            materialComponents.append(component)

        return materialComponents
    else:
        raise ValueError('Failed to get components', response.status_code, response.text)

def getComponentById(id: str) -> MaterialComponentData:

    """Gets a material component using the id supplied.

    Args:
        id (str): The id of the component

    Raises:
        ValueError: Any communication error with the PWS APIs or if a component with the supplied id cannot be found.

    Returns:
        MaterialComponentData: The material component with the supplied id.
    """
    id = urllib.parse.quote(id)

    url = f'{getMaterialsApiTarget()}components/id={id}?clientId={getClientAliasId()}'

    response = getRequest(url)

    if response.ok:

        foundMaterialComponentData = list[MaterialComponentData]()

        componentJson = json.loads(response.text)
        component = MaterialComponentData()
        component.initialiseFromDictionary(componentJson)

        return component
    
    elif response.status_code == 404: 
        raise ValueError('Component with the provided id not found.', id)

    else:
        raise ValueError('Failed to get component data', response.status_code, response.text)
    
def getComponentByName(name: str) -> MaterialComponentData:

    """Gets a material component using the name supplied.

    Args:
        name (str): The name of the component

    Raises:
        ValueError: Any communication error with the PWS APIs or if a component with the supplied name cannot be found.

    Returns:
        MaterialComponentData: The material component with the supplied name.
    """
    name = urllib.parse.quote(name)

    url = f'{getMaterialsApiTarget()}components/name={name}?clientId={getClientAliasId()}'

    response = getRequest(url)

    if response.ok:

        foundMaterialComponentData = list[MaterialComponentData]()

        componentJson = json.loads(response.text)
        component = MaterialComponentData()
        component.initialiseFromDictionary(componentJson)

        return component
    
    elif response.status_code == 404: 
        raise ValueError('Component with the provided name not found.', name)

    else:
        raise ValueError('Failed to get component data', response.status_code, response.text)

def getComponentByCasId(casId: str) -> MaterialComponentData:

    """Gets a material component using the casId supplied.

    Args:
        casId (str): The casId of the component

    Raises:
        ValueError: Any communication error with the PWS APIs or if a component with the supplied casId cannot be found.

    Returns:
        MaterialComponentData: The material component with the supplied casId.
    """
    casId = urllib.parse.quote(casId)

    url = f'{getMaterialsApiTarget()}components/casId={casId}?clientId={getClientAliasId()}'

    response = getRequest(url)

    if response.ok:

        foundMaterialComponentData = list[MaterialComponentData]()

        componentJson = json.loads(response.text)
        component = MaterialComponentData()
        component.initialiseFromDictionary(componentJson)

        return component
    
    elif response.status_code == 404: 
        raise ValueError('Component with the provided casId not found.', casId)

    else:
        raise ValueError('Failed to get component data', response.status_code, response.text) 

def storeMaterialComponent(materialComponentData: MaterialComponentData) -> Material: 

    """Stores the provided material component data and creates a material that contains it.

    Args:
        MaterialComponentData: The component data to store

    Raises:
        ValueError: Any communication error with the PWS APIs or validation error with the provided data.

    Returns:
        The newly created material object.
    """

    url = f'{getMaterialsApiTarget()}components?clientId={getClientAliasId()}'

    jsonText = jsons.dumps(materialComponentData, use_enum_name=False)

    response = postRequest(url, jsonText)

    if response.ok and response.status_code == 201:

        materialUrl = response.headers['location']

        response = getRequest(materialUrl)

        if response.ok:
            materialJson = json.loads(response.text)
            material = Material()
            material.initialiseFromDictionary(materialJson)
            return material
    
    else:
        raise ValueError('Failed to store material component', response.status_code, response.text)
    
def updateMaterialComponent(materialComponentData: MaterialComponentData) -> bool: 

    """Updates the provided material component.

    Args:
        None.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
        If successful True.
    """

    url = f'{getMaterialsApiTarget()}components?clientId={getClientAliasId()}'

    jsonText = jsons.dumps(materialComponentData, use_enum_name=False)

    response = putRequest(url, jsonText)

    if response.ok and response.status_code == 204:

        return True
    
    else:
        raise ValueError('Failed to update material component', response.status_code, response.text)
    
# Materials Controller

def getMaterials() -> list[Material]:

    """Gets the full detais of all materials.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
        List[Material]: The list of materials.
    """

    url = f'{getMaterialsApiTarget()}materials?clientId={getClientAliasId()}'

    response = getRequest(url)

    if response.ok:

        materials = list[Material]()

        for json_def in json.loads(response.text):
            material = Material()
            material.initialiseFromDictionary(json_def)
            materials.append(material)

        return materials
        
    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)

def getMaterialById(id: str) -> Material: 

    """Gets a material by ID.

    Args:
        id (str): The ID to search for,

    Raises:
        ValueError: Any communication error with the PWS APIs or if a material with the supplied ID cannot be found.

    Returns:
        Material: The material which has the supplied ID.
    """

    url = f'{getMaterialsApiTarget()}materials/id={id}?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materialJson = json.loads(response.text)
        material = Material()
        material.initialiseFromDictionary(materialJson)

        return material
    
    elif response.status_code == 404: 
        raise ValueError('Material with the specifid ID not found.', id)

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)

def getMaterialByName(name: str) -> Material: 

    """Gets a material by name.

    Args:
        id (str): The name to search for,

    Raises:
        ValueError: Any communication error with the PWS APIs or if a material with the supplied name cannot be found.

    Returns:
        Material: The material which has the supplied name.
    """

    url = f'{getMaterialsApiTarget()}materials/name={name}?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materialJson = json.loads(response.text)
        material = Material()
        material.initialiseFromDictionary(materialJson)

        return material
    
    elif response.status_code == 404: 
        raise ValueError('Material with the specifid name not found.', name)

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)

def getMaterialByCasId(casId: str) -> Material: 

    """Gets a material by casId.

    Args:
        id (str): The casId to search for,

    Raises:
        ValueError: Any communication error with the PWS APIs or if a material with the supplied casId cannot be found.

    Returns:
        Material: A material that has a single component matching the given casId.
    """

    url = f'{getMaterialsApiTarget()}materials/casid={casId}?clientId={getClientAliasId()}'
    response = getRequest(url)

    if response.ok:

        materialJson = json.loads(response.text)
        material = Material()
        material.initialiseFromDictionary(materialJson)

        return material
    
    elif response.status_code == 404: 
        raise ValueError('Material with the specifid cas id not found.', casId)

    else:
        raise ValueError('Failed to get material data', response.status_code, response.text)

def getMaterialNames() -> list[MaterialInfo]: 

    """Gets all of the available material names and IDs.

    Raises:
        ValueError: Any communication error with the PWS APIs.

    Returns:
        list[EntityDescriptor]: A list of MaterialInfo objects for all available materials.
    """
    url = f'{getMaterialsApiTarget()}materials/descriptors?clientId={getClientAliasId()}'

    response = getRequest(url)

    if response.ok:

        materialInfos = list[MaterialInfo]()

        for json_def in json.loads(response.text):
            info = MaterialInfo(json_def['id'], json_def['displayName'])
            materialInfos.append(info)

        return materialInfos
    else:
        raise ValueError('Failed to get materials', response.status_code, response.text)