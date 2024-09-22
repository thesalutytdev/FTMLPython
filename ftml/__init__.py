from enum import Enum
import re
import os

class UnknownType(Exception):
    serialVersionUID: int = 1;
    str: str = "[FTMLException::UnknownType] Unknown type of '%TYPE%'";
    type: str
    
    def __init(self, unknownType: str):
        type = unknownType
        
    def __str__(self):
        return self.str.replace("%TYPE%", type)
    
class ObjectType(Enum):
    String = "String"
    Integer = "Integer"
    Double = "Double"
    Float = "Float"
    Boolean = "Boolean"
    List = "List"

    @staticmethod
    def from_String(value):
        parsed_value = value.strip()

        if (parsed_value.startswith("\"") and parsed_value.endswith("\"")) or \
           (parsed_value.endswith("'") and parsed_value.startswith("'")) or \
           (parsed_value.startswith("`") and parsed_value.endswith("`")):
            return ObjectType.String
        elif parsed_value.isdigit() or (parsed_value.startswith('-') and parsed_value[1:].isdigit()):
            return ObjectType.Integer
        elif parsed_value.count('.') == 1 and parsed_value.replace('.', '').isdigit():
            return ObjectType.Float
        elif parsed_value.count('.') == 1 and parsed_value.replace('.', '').lstrip('-').isdigit():
            return ObjectType.Double
        elif parsed_value.lower() in ["true", "false"]:
            return ObjectType.Boolean
        elif parsed_value.startswith("[") and parsed_value.endswith("]"):
            return ObjectType.List
        else:
            raise UnknownType(parsed_value)

objects: list = []
class FTMLObject:
    __key: str
    __value: any
    __type: ObjectType
    
    def __init__(self, key: str, value: any, type: ObjectType):
        self.__key = key
        self.__value = value
        self.__type = type
    
    @staticmethod
    def from_String(String):
        split = String.split(":")
        key = split[0].strip()
        value = split[1].strip()
        obj_type = None

        for obj in objects:
            if obj.key() == value:
                value = obj.value()
                obj_type = obj.type()
                break

            if obj.key() == key:
                raise ValueError("Key already exists!")

        if obj_type is None:
            obj_type = ObjectType.from_String(split[1].strip())

        obj = FTMLObject(key, value, obj_type)

        objects.append(obj)

        return obj
    
    def get_value(self):
        return self.value

    def __str__(self):
        return f"FTMLObject{{key: {self.key()}, value: {self.value()}, type: {self.type()}}}"

    def value(self):
        if self.type() == ObjectType.List:
            return ListObject.of(self)
        else:
            return str(self.__value)

    def __str__(self):
        return f"{self.__key}: {self.__value}"
    
    def key(self):
        return self.__key

    def type(self):
        return self.__type

class ListObject:
    def __init__(self, obj):
        self._object = obj

    def to_array(self):
        split = self._object.get_value().strip().replace("[", "").replace("]", "").split(",")
        array = []
        for i in range(len(split)):
            found = False

            for obj in objects:
                if obj.key() == split[i].strip():
                    array.append(obj.get_value())
                    found = True
                    break

            if not found:
                array.append(split[i].strip())
        return array

    @staticmethod
    def of(obj):
        return ListObject(obj)

    def __str__(self):
        return str(self.to_array())

    def str(self):
        return f"ListObject:{{key: {self._object.key()}, value: {self.to_array()}, type: {self._object.type()}}}"

    def key(self):
        return self._object.key()

    def value(self):
        return self.to_array()

class FTMLParser:
    @staticmethod
    def parse_file(file_name):
        if file_name is None:
            raise ValueError("File name cannot be null")
        if not file_name.endswith(".ftml"):
            raise ValueError("File name must end with .ftml")
        if not os.path.exists(file_name):
            raise ValueError("Invalid path. File does not exist")

        try:
            with open(file_name, 'r') as file:
                file_objects = []
                for line in file:
                    line = line.strip()
                    if line and not (line.startswith("#") 
                                     or line.startswith("!") 
                                     or line.startswith(" ")):
                        file_objects.append(FTMLParser.parse_object(line))

                return file_objects
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def parse_object(line):
        return FTMLObject.from_String(line)

