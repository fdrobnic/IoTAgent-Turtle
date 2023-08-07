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
from sdmx2jsonld.common.listmanagement import get_rest_data
from sdmx2jsonld.transform.context import Context

logger = getLogger()


class Property(CommonClass):
    def __init__(self, entity):
        super().__init__(entity=entity)

        self.data = {
            "id": str(),
            "type": "",
            "language": {"type": "Property", "value": list()},
            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "label": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "label": {"type": "Property", "value": dict()},
            "codeList": {"type": "Relationship", "object": str()},
            "concept": {"type": "Relationship", "object": str()},
            "@context": [
                "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
            ],
        }

        self.keys = {k: k for k in self.data.keys()}

    def add_data(self, property_id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the Dimension: rdfs:label
        position = data.index("rdfs:label") + 1
        description = data[position]

        descriptions = [x[0].replace('"', "") for x in description]

        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            logger.warning(f"The Property {property_id} has a " f"rdfs:label without language tag: {description}")

            aux = len(description)
            if aux != 1:
                logger.error(f"Property: there is more than 1 description ({aux}), values: {description}")
            else:
                # There is no language tag, we use by default 'en'
                languages = ["en"]
                logger.warning('Property: selecting default language "en"')

        ###############################################################################
        # TODO: New ETSI CIM NGSI-LD specification 1.4.2
        # Pending to implement in the Context Broker
        ###############################################################################
        # for i in range(0, len(languages)):
        #     self.data['label']['LanguageMap'][languages[i]] = descriptions[i]
        ###############################################################################
        for i in range(0, len(languages)):
            self.data["label"]["value"][languages[i]] = descriptions[i]

        # Complete the information of the language with the previous information
        key = self.keys["language"]
        self.data[key]["value"] = languages

        # qb:codeList, this attribute might not be presented, so we need to check it.
        # TODO: We need to control that the codeList id extracted here are the same that we analyse afterwards.
        try:
            position = data.index("qb:codeList") + 1
            code_list = self.generate_id(entity="ConceptSchema", value=data[position][0])
            self.data["codeList"]["object"] = code_list
        except ValueError:
            logger.warning(f"Property: {property_id} has not qb:codeList, deleting the key in the data")

            # If we have not the property, we delete it from data
            self.data.pop("codeList")

        # qb:concept
        # TODO: the concept id need to check if it is a normal id or an url
        position = data.index("qb:concept") + 1
        concept = self.generate_id(entity="Concept", value=data[position][0])
        self.data["concept"]["object"] = concept

        # Get the rest of the data
        data = get_rest_data(
            data=data,
            not_allowed_keys=[
                "sliceKey",
                "component",
                "disseminationStatus",
                "validationState",
                "notation",
                "label",
                "codeList",
                "concept",
            ],
            further_process_keys=["component", "label"],
        )

        # add the new data to the dataset structure
        [self.data.update(self.__generate_property__(key=k, value=v)) for k, v in data.items()]

        # Order the keys in the final json-ld
        a = Context()
        a.set_data(new_data=self.data)
        a.order_context()
        self.data = a.get_data()

    def get(self):
        return self.data
