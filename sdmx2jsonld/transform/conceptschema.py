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
from sdmx2jsonld.transform.context import Context
from sdmx2jsonld.common.listmanagement import flatten_value

logger = getLogger()


class ConceptSchema(CommonClass):
    def __init__(self):
        super().__init__(entity="ConceptScheme")

        self.data = {
            "id": str(),
            "type": "ConceptScheme",
            "language": {"type": "Property", "value": list()},
            "hasTopConcept": {"type": "Relationship", "object": list()},
            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "skos:prefLabel": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "prefLabel": {"type": "Property", "value": dict()},
            "@context": [
                "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
            ],
        }

        self.keys = {k: k for k in self.data.keys()}

    def add_data(self, concept_schema_id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the ConceptSchema: skos:prefLabel
        position = data.index("skos:prefLabel") + 1
        description = data[position]

        descriptions = [x[0].replace('"', "") for x in description]
        languages = list()

        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            logger.warning(
                f"The ConceptSchema {concept_schema_id} has a " f"skos:prefLabel without language tag: {description}"
            )

            aux = len(description)
            if aux != 1:
                logger.error(f"ConceptSchema: there is more than 1 description ({aux}), values: {description}")
            else:
                # There is no language tag, we use by default 'en'
                languages = ["en"]
                logger.warning('ConceptSchema: selecting default language "en"')

        # Complete the skos:prefLabel
        ###############################################################################
        # TODO: New ETSI CIM NGSI-LD specification 1.4.2
        # Pending to implement in the Context Broker
        ###############################################################################
        # for i in range(0, len(languages)):
        #     self.data['skos:prefLabel']['LanguageMap'][languages[i]] = descriptions[i]
        ###############################################################################
        for i in range(0, len(languages)):
            self.data["prefLabel"]["value"][languages[i]] = descriptions[i]

        # Complete the information of the language with the previous information
        key = self.keys["language"]
        self.data[key]["value"] = languages

        # Add the id
        self.data["id"] = "urn:ngsi-ld:ConceptSchema:" + concept_schema_id

        # TODO: We need to control that the concept id extracted here are the same that we analyse afterwards.
        # skos:hasTopConcept, this is a list of ids
        position = data.index("skos:hasTopConcept") + 1
        result = list(map(lambda x: self.generate_id(value=x, entity="Concept"), data[position]))
        self.data["hasTopConcept"]["object"] = result

        # Get the rest of data, dct:created and dct:modified properties
        try:
            position = data.index("dct:created") + 1
            self.data["created"] = {
                "type": "Property",
                "value": flatten_value(data[position]),
            }
        except ValueError:
            logger.warning(f"dct:created is not present in the Concept Schema: {concept_schema_id}")

        try:
            position = data.index("dct:modified") + 1
            self.data["modified"] = {
                "type": "Property",
                "value": flatten_value(data[position]),
            }
        except ValueError:
            logger.warning(f"dct:modified is not present in the Concept Schema: {concept_schema_id}")

        # Order the keys in the final json-ld
        a = Context()
        a.set_data(new_data=self.data)
        a.order_context()
        self.data = a.get_data()

    def get(self):
        return self.data

    # TODO: It should be a function of the RegParser class
    # @staticmethod
    # def __generate_id__(entity, value):
    #     parse = RegParser()
    #     aux = parse.obtain_id(value)
    #     aux = "urn:ngsi-ld:" + entity + ":" + aux
    #     return aux
