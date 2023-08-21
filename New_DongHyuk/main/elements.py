from abc import ABC, abstractmethod

####IT IS FOR DEBUGGING####
from json import dump
from os import makedirs
from shutil import rmtree

class Element(ABC):
    @abstractmethod
    def build_to_rhino(self):
        pass


class BuildingElement(Element):
    
    def __init__(self, dict_properties: dict):
        self.floor = dict_properties["층수"]
        self.name = dict_properties["주기"]
        self.type = dict_properties["종류"]
        self.usage = dict_properties["용도"]
        self.geometry = dict_properties["geometry"]
        print(self.geometry)
        self.dictionary_prop = dict_properties

    def build_to_rhino(self):
        pass
    
    def __str__(self):
        return f"Building Element Object : Floor : {self.floor} | Name : {self.name} | Type : {self.type} | Usage : {self.usage}"


class VegetationElement(Element):
    def __init__(self, dict_properties: dict):
        # TODO : define properties
        pass

    def build_to_rhino(self):
        pass


class ContourElement(Element):
    def __init__(self, dict_properties: dict):
        # TODO : define properties
        pass

    def build_to_rhino(self):
        pass


class RoadElement(Element):
    def __init__(self, dict_properties: dict):
        # TODO : define properties
        pass

    def build_to_rhino(self):
        pass
