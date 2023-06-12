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
from sdmx2jsonld.common.regparser import RegParser
from sdmx2jsonld.transform.context import Context

logger = getLogger()


class Concept(CommonClass):
    def __init__(self):
        super().__init__(entity='Concept')

        self.data = {
            "id": str(),
            "type": "Concept",
            "dct:language": {
                "type": "Property",
                "value": list()
            },
            "skos:inScheme": {
                "type": "Relationship",
                "value": str()
            },
            "rdfs:subClassOf": {
                "type": "Property",
                "value": str()
            },

            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "skos:prefLabel": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "skos:prefLabel": {
                "type": "Property",
                "value": dict()
            },


            "@context": dict()
        }

        self.concept_id = str()

    def add_data(self, concept_id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the ConceptSchema: skos:prefLabel
        # TODO: we need to extract the attribute from the context or we will have problems (e.g. skos:prefLabel should
        #       be equal to rdfs:label
        self.concept_id = concept_id

        try:
            position = data.index('skos:prefLabel') + 1
        except ValueError:
            # We could not find skos:prefLabel, try to find rdfs:label
            logger.warning(f'The Concept {concept_id} does not contain skos:prefLabel but rdfs:label. We use its '
                           f'content to fill in the skos:prefLabel property')
            try:
                position = data.index('rdfs:label') + 1
            except ValueError:
                # We could not find rdfs:label
                logger.warning(f'The Concept {concept_id} does not contain skos:prefLabel neither rdfs:label.')

        description = data[position]
        descriptions = [x[0].replace("\"", "") for x in description]

        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            logger.warning(f'The Concept {concept_id} has a '
                           f'skos:prefLabel without language tag: {description}')

            aux = len(description)
            if aux != 1:
                logger.error(f"Concept: there is more than 1 description ({aux}), values: {description}")
            else:
                # There is no language tag, we use by default 'en'
                languages = ['en']
                logger.warning('Concept: selecting default language "en"')

        # Complete the skos:prefLabel
        ###############################################################################
        # TODO: New ETSI CIM NGSI-LD specification 1.4.2
        # Pending to implement in the Context Broker
        ###############################################################################
        # for i in range(0, len(languages)):
        #     self.data['skos:prefLabel']['LanguageMap'][languages[i]] = descriptions[i]
        ###############################################################################
        for i in range(0, len(languages)):
            self.data['skos:prefLabel']['value'][languages[i]] = descriptions[i]

        # Complete the information of the language with the previous information
        #key = self.keys['dct:language']
        key = 'dct:language'
        self.data[key]['value'] = languages

        # Add the id
        self.data['id'] = "urn:ngsi-ld:Concept:" + concept_id

        # rdfs:seeAlso
        self.need_add_in_scheme(data=data)

        # rdfs:subClassOf
        self.need_add_subclass(data=data)

        # skos:notation
        self.need_add_notation(data=data)

        # Simplify Context and order keys
        a = Context()
        a.set_data(data=self.data)
        a.new_analysis()
        a.order_context()
        self.data = a.get_data()

    def get(self):
        return self.data

    def get_id(self):
        return self.data['id']

    def need_add_subclass(self, data):
        try:
            position = data.index('rdfs:subClassOf') + 1
            self.data['rdfs:subClassOf']['value'] = data[position][0]
        except ValueError:
            logger.info(f'The Concept {self.concept_id} has no rdfs:subClassOf property, deleting the key in the data')

            # We delete the "rdfs:subClassOf" property from the final structure
            self.data.pop('rdfs:subClassOf')

    def need_add_in_scheme(self, data):
        position = 0

        try:
            position = data.index('rdfs:seeAlso') + 1
        except ValueError:
            # We will try to find the skos:inScheme
            try:
                position = data.index('skos:inScheme') + 1
            except ValueError:
                logger.info(f'The Concept {self.concept_id} has neither rdfs:seeAlso or skos:inScheme properties, '
                            f'deleting the key in the data')

                # We delete the "skos:inScheme" property from the final structure
                self.data.pop('skos:inScheme')
                position = 0

        if position > 0:
            parser = RegParser()
            concept_schema = data[position][0]
            concept_schema = "urn:ngsi-ld:ConceptSchema:" + parser.obtain_id(concept_schema)
            self.data['skos:inScheme']['value'] = concept_schema

    def need_add_notation(self, data):
        try:
            position = data.index('skos:notation') + 1

            self.data['skos:notation'] = {
                    'type': 'Property',
                    'value': data[position][0][0].replace("\"", "")
            }
        except ValueError:
            logger.info(f'The Concept {self.concept_id} has no skos:notation property')
