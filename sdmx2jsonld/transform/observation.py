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

from logging import getLogger
from sdmx2jsonld.common.commonclass import CommonClass
from sdmx2jsonld.sdmxattributes.confirmationStatus import ConfStatus
from sdmx2jsonld.sdmxattributes.observationStatus import ObsStatus
from sdmx2jsonld.sdmxattributes.code import Code
from sdmx2jsonld.sdmxdimensions.frequency import Frequency
from sdmx2jsonld.common.regparser import RegParser
from re import search, compile

logger = getLogger()


class Observation(CommonClass):
    def __init__(self):
        super().__init__(entity="Observation")

        self.data = {
            "id": str(),
            "type": "Observation",
            "title": {"type": "Property", "value": str()},
            "identifier": {"type": "Property", "value": str()},
            "dataSet": {"type": "Relationship", "object": str()},
            "confStatus": {"type": "Property", "value": str()},
            "decimals": {"type": "Property", "value": int()},
            "obsStatus": {"type": "Property", "value": str()},
            "unitMult": {"type": "Property", "value": int()},
            "freq": {"type": "Property", "value": str()},
            "refArea": {"type": "Property", "value": str()},
            "timePeriod": {"type": "Property", "value": str()},
            "obsValue": {"type": "Property", "value": float()},
            "dimensions": {"type": "Property", "value": list()},
            "@context": ["https://raw.githubusercontent.com/smart-data-models/dataModel.SDMX/master/context.jsonld"],
        }

        self.concept_id = str()
        self.keys = {k: k for k in self.data.keys()}
        self.regexpDimension = compile("ns1:.*")

    def add_data(self, title, observation_id, data):
        # We have a list of dimensions, a dataset, a list of attributes, a list of dimensions attributes
        # and an observation

        # Add the confStatus
        key = self.__assign_property__(requested_key="sdmx-attribute:confStatus", data=data)
        self.data[key]["value"] = ConfStatus().fix_value(value=self.data[key]["value"])

        # Add the id
        self.data["id"] = "urn:ngsi-ld:Observation:" + observation_id
        self.data["identifier"]["value"] = observation_id

        # Add title, the url string as it is in the turtle document
        self.data["title"]["value"] = title

        # Add the decimals
        key = self.__assign_property__(requested_key="sdmx-attribute:decimals", data=data)
        self.data[key]["value"] = Code(typecode=key).fix_value(value=self.data[key]["value"])

        # Add obsStatus
        key = self.__assign_property__(requested_key="sdmx-attribute:obsStatus", data=data)
        self.data[key]["value"] = ObsStatus().fix_value(value=self.data[key]["value"])

        # Add unitMult
        key = self.__assign_property__(requested_key="sdmx-attribute:unitMult", data=data)
        self.data[key]["value"] = Code(typecode=key).fix_value(value=self.data[key]["value"])

        # Add freq "pattern": "^_[OUZ]|[SQBNI]|OA|OM|[AMWDH]_*[0-9]*$"
        # TODO: Add verification of coded data following the pattern
        key = self.__assign_property__(requested_key="sdmx-dimension:freq", data=data)
        self.data[key]["value"] = Frequency().fix_value(value=self.data[key]["value"])

        # Add reference Area
        # TODO: Add verification of coded data following ISO-2, ISO-3, or M49 code
        _ = self.__assign_property__(requested_key="sdmx-dimension:refArea", data=data)

        # Add timePeriod
        _ = self.__assign_property__(requested_key="sdmx-dimension:timePeriod", data=data)

        # Add obsValue
        _ = self.__assign_property__(requested_key="sdmx-measure:obsValue", data=data)

        # Add dataset
        parser = RegParser()
        key = self.__assign_property__(requested_key="qb:dataSet", data=data, key_property="object")
        identifier = parser.obtain_id(self.data[key]["object"])
        self.data[key]["object"] = "urn:ngsi-ld:CatalogueDCAT-AP:" + identifier

        # Add dimensions
        result = self.__assign_dimensions__(data=data)
        self.data["dimensions"]["value"] = result

    def __assign_dimensions__(self, data):
        def create_data(key, value):
            new_dimension = {"key": key, "value": value}

            return new_dimension

        parser = RegParser()

        # We need to get the list of available dimension keys
        dimension_keys = [a for a in data if self.regexpDimension.match(a.__str__()) is not None]

        # We need to get the list of values for these keys, if there is an url, it is considered a
        values = [self.get_data(data[data.index(a) + 1]) for a in dimension_keys]
        values = [parser.obtain_id(a, prefix_string="urn:ngsi-ld:Concept:") for a in values]

        # Get the list of Entity IDs
        entity_ids = ["urn:ngsi-ld:DimensionProperty:" + b.split("ns1:", 1)[1] for b in dimension_keys]

        result = [create_data(key=entity_ids[i], value=values[i]) for i in range(0, len(values))]

        return result

    def __assign_property__(self, requested_key, data, key_property="value"):
        key = self.get_key(requested_key=requested_key)
        position = data.index(requested_key) + 1
        self.data[key][key_property] = self.get_data(data[position])

        return key

    def get_key(self, requested_key):
        try:
            key = self.keys[requested_key]
            return key
        except KeyError:
            # The key did not exist therefore we add to the list with this value
            # We need to check if it exists without prefix
            m = search("(.*):(.*)", requested_key)

            if m is not None:
                subfix = m.group(2)

                try:
                    key = self.keys[subfix]
                    return key
                except KeyError:
                    # Even subfix is not in the list, decide to add to the list of keys
                    self.keys[requested_key] = requested_key
                    return requested_key
            else:
                # Weird situation, it is an key without prefix and not recognised, decide to add it
                self.keys[requested_key] = requested_key

                return requested_key

    def get(self):
        return self.data

    def get_data(self, data):
        result = data
        if isinstance(data, list):
            result = self.get_data(data[0])

        if isinstance(result, str):
            m = search('"+(.*)"+', result)
            if m is not None:
                result = m.group(1)

        return result
