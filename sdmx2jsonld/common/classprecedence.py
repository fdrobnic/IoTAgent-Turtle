#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2022 FIWARE Foundation, e.V.
#
# This file is part of IoTAgent-SDMX (RDF Turtle)
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##


entities = {
    "qb:DataStructureDefinition": "Dataset",
    "qb:ComponentSpecification": "Component",
    "qb:AttributeProperty": "Attribute",
    "qb:DimensionProperty": "Dimension",
    "qb:CodedProperty": "Dimension",
    "rdfs:Class": "Class",
    "owl:Class": "Class",
    "skos:ConceptScheme": "ConceptScheme",
    "skos:Concept": "Range",
}


class Precedence:
    def __init__(self):
        self.classes = {
            "qb:DataStructureDefinition": 1000,
            "qb:ComponentSpecification": 500,
            "qb:DimensionProperty": 250,
            "qb:AttributeProperty": 250,
            "qb:MeasureProperty": 250,
            "qb:CodedProperty": 125,
            "skos:ConceptScheme": 75,
            "skos:Concept": 40,
            "rdfs:Class": 20,
            "owl:Class": 20,
            "qb:SliceKey": 10,
        }

    def get_value(self, aclass: str) -> int:
        try:
            return self.classes[aclass]
        except KeyError:
            return 0

    def precedence(self, data: list) -> str:
        classes_values = list(map(lambda x: self.get_value(x), data))

        # We need to check if all element of the list are the value 250 because could not be possible to have at
        # the same time a DimensionProperty and AttributeProperty, this is an ERROR therefore we need to report it.
        result = all(element == 250 for element in classes_values) and len(data) > 1
        if result is True:
            raise ClassPrecedencePropertyError(data)

        # In case that we have several values identical of type Class, we need to report a WARNING message because maybe
        # it is not needed multi-type in that case.
        result = all(element == 20 for element in classes_values) and len(data) > 1
        if result is True:
            raise ClassPrecedenceClassError(data)

        # In other case, we return the max value of the list
        aux = data[classes_values.index(max(classes_values))]

        return aux


class ClassPrecedenceError(Exception):
    """Base class for other exceptions"""

    def __init__(self, data, message):
        self.message = message
        self.data = data

    def __str__(self):
        return f"{self.data} -> {self.message}"


class ClassPrecedencePropertyError(ClassPrecedenceError):
    """Raised when the input value is too small"""

    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="Incompatible multiclass definition"):
        super().__init__(data=data, message=message)


class ClassPrecedenceClassError(ClassPrecedenceError):
    """Raised when the input value is too large"""

    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="Possible redundant Class definition"):
        super().__init__(data=data, message=message)


if __name__ == "__main__":
    pre = Precedence()
    obtained = pre.precedence(["qb:DataStructureDefinition"])
