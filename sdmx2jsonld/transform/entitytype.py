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

from sdmx2jsonld.transform.dataset import Dataset
from sdmx2jsonld.transform.dimension import Dimension
from sdmx2jsonld.transform.conceptschema import ConceptSchema
from sdmx2jsonld.transform.concept import Concept
from sdmx2jsonld.transform.attribute import Attribute
from sdmx2jsonld.transform.catalogue import CatalogueDCATAP
from logging import getLogger
from datetime import datetime
from sdmx2jsonld.common.regparser import RegParser
from sdmx2jsonld.common.classprecedence import Precedence, ClassesPrecedencePropertyError, ClassesPrecedenceClassError

logger = getLogger()


class EntityType:
    def __init__(self):
        self.entities = {
            'qb:DataStructureDefinition': 'Dataset',
            'qb:ComponentSpecification': 'Component',
            'qb:AttributeProperty': 'Attribute',
            'qb:DimensionProperty': 'Dimension',
            'qb:CodedProperty': 'Dimension',
            'rdfs:Class': 'Class',
            'owl:Class': 'Class',
            'skos:ConceptScheme': 'ConceptScheme',
            'skos:Concept': 'Range'
        }

        self.dataset = Dataset()
        self.dimensions = list()
        self.attributes = list()
        self.conceptSchemas = list()
        self.conceptLists = list()
        self.conceptListsIds = dict()
        self.context = dict()
        self.context_mapping = dict()
        self.catalogue = CatalogueDCATAP()

        self.pre = Precedence()

    def __find_entity_type__(self, string):
        """
        Find the index position of the 'a' SDMX key and return the following data with the corresponding EntityType
        """
        is_new = bool()

        # Index maybe 0 in case of ComponentSpecification or 1 in case of DataStructureDefinition
        index = len(string) - 1
        string1 = string[index]

        # We can get a 'verb' 'objectlist' or an 'objectlist', where verb is 'a'
        # in case that there is no verb, we are talking about a triples whose id was previously
        # created.
        try:
            position = string1.index('a') + 1

            try:
                data = self.pre.precedence(string1[position])

                # We have two options, a well-know object list to be found in the self.entities or
                # the conceptList defined in the turtle file
                data = self.entities[data]
            except ClassesPrecedencePropertyError as error:
                logger.error(str(error))
                data = self.entities[data[0]]
            except ClassesPrecedenceClassError as error:
                logger.warning(str(error))
                data = self.entities['rdfs:Class']
            except KeyError:
                # We found a CodeList or any other thing, check the list of codeList found in the turtle file
                if data not in self.conceptListsIds:
                    logger.warning(f"Received a unexpected entity type: {data}")
                else:
                    data = 'Range'

            is_new = True
        except ValueError:
            logger.info(f'Not a definition triples {string}, need to find the proper structure')
            is_new = False
            data = self.__get_subject__(title=string[0])
            string1 = string[1:]

        return data, string1, is_new

    def transform(self, string):
        if len(self.context) == 0:
            raise AssertionError("Context should be passed before to the EntityType Class, "
                                 "call EntityType.set_context() before, {'__file__': this_file}))")

        data_type, new_string, is_new = self.__find_entity_type__(string=string)

        if is_new:
            self.create_data(type=data_type, data=new_string, title=string[0])
        else:
            logger.info(f'Checking previous subjects to find if it was created previously')
            self.patch_data(datatype=data_type, data=new_string)

    def patch_data(self, datatype, data):
        def flatten_value(y):
            if isinstance(y, list):
                return flatten_value(y[0])
            elif isinstance(y, datetime):
                return y
            else:
                return y.replace('"', '')

        flatten_data = [item for sublist in data for item in sublist]

        if flatten_data[0] != 'rdfs:label':
            flatten_data = {flatten_data[i]: flatten_value(flatten_data[i + 1]) for i in range(0, len(flatten_data), 2)}
            language_map = False
        else:
            language_map = True

        if datatype == 'Dataset':
            self.dataset.patch_data(data=flatten_data, language_map=language_map)

    def create_data(self, type, data, title):
        parser = RegParser()

        if type == 'Component':
            self.dataset.add_components(context=self.context, component=data)
        elif type == 'Dataset':
            identifier = parser.obtain_id(title)
            self.dataset.add_context(context=self.context, context_mapping=self.context_mapping)
            self.dataset.add_data(title=title, dataset_id=identifier, data=data)

            # Create the CatalogueDCAT-AP and assign the dataset id
            self.catalogue.add_dataset(dataset_id=self.dataset.data['id'])
        elif type == 'Dimension':
            dimension = Dimension()
            dimension.add_context(context=self.context, context_mapping=self.context_mapping)
            dimension_id = parser.obtain_id(title)
            dimension.add_data(id=dimension_id, data=data)
            self.dimensions.append(dimension)
        elif type == 'Attribute':
            attribute = Attribute()
            attribute.add_context(context=self.context, context_mapping=self.context_mapping)
            attribute_id = parser.obtain_id(title)
            attribute.add_data(attribute_id=attribute_id, data=data)
            self.attributes.append(attribute)
        elif type == 'ConceptScheme':
            concept_schema = ConceptSchema()
            concept_schema.add_context(context=self.context, context_mapping=self.context_mapping)
            concept_schema_id = parser.obtain_id(title)
            concept_schema.add_data(concept_schema_id=concept_schema_id, data=data)
            self.conceptSchemas.append(concept_schema)
        elif type == 'Class':
            # We need the Concept because each of the Range description is of the type Concept
            concept_list = Concept()
            concept_list.add_context(context=self.context, context_mapping=self.context_mapping)
            concept_list_id = parser.obtain_id(title)
            concept_list.add_data(concept_id=concept_list_id, data=data)
            self.conceptLists.append(concept_list)
            self.conceptListsIds[title] = concept_list.get_id()
        elif type == 'Range':
            # TODO: Range is associated to a Concept and identified properly in the ConceptSchema
            data_range = Concept()
            data_range.add_context(context=self.context, context_mapping=self.context_mapping)
            data_range_id = parser.obtain_id(title)
            data_range.add_data(concept_id=data_range_id, data=data)
            self.conceptLists.append(data_range)
            self.conceptListsIds[title] = data_range.get_id()

            # for i in range(0, len(self.conceptSchemas)):
            #    concept_schema = self.conceptSchemas[i].data
            #    has_top_concept_values = concept_schema['skos:hasTopConcept']['value']
            #
            #    out = [data_range.data['skos:notation']
            #           if x == data_range.data['id'] else x for x in has_top_concept_values]
            #
            #    self.conceptSchemas[i].data['skos:hasTopConcept']['value'] = out

    def __get_subject__(self, title):
        if self.dataset.get()['dct:title'] == title:
            return 'Dataset'
        else:
            AssertionError(f"Still not defined: {title}")

    def get_catalogue(self):
        return self.catalogue.get()

    def get_dataset(self):
        return self.dataset.get()

    def get_dimensions(self):
        return self.dimensions

    def get_attributes(self):
        return self.attributes

    def get_conceptSchemas(self):
        return self.conceptSchemas

    def get_conceptList(self):
        return self.conceptLists

    def set_context(self, context, mapping):
        self.context = context
        self.context_mapping = mapping

    def save(self, param):
        getattr(self, param).save()
