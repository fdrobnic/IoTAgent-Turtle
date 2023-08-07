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
from sdmx2jsonld.common.listmanagement import get_rest_data, get_property_value
from sdmx2jsonld.transform.context import Context
from random import getrandbits

logger = getLogger()


class Catalogue(CommonClass):
    def __init__(self):
        super().__init__(entity="Catalogue")

        self.data = {
            "id": str(),
            "type": "Catalogue",
            "dataset": {"type": "Relationship", "object": str()},
            "language": {"type": "Property", "value": list()},
            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "rdfs:label": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "description": {"type": "Property", "value": dict()},
            "publisher": {"type": "Property", "value": str()},
            "title": {"type": "Property", "value": list()},
            "@context": [
                "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
            ],
        }

        self.concept_id = str()
        self.keys = {k: k for k in self.data.keys()}

    def add_dataset(self, dataset_id):
        self.concept_id = dataset_id

        # generate hash id
        random_bits = getrandbits(128)
        hash1 = "%032x" % random_bits

        # Add the id
        self.data["id"] = "urn:ngsi-ld:Catalogue:" + hash1

        # Add dataset id
        self.data["dataset"]["object"] = dataset_id

    def add_data(self, title, dataset_id, data):
        # We need to complete the data corresponding to the Catalogue: rdfs:label
        self.__complete_label__(title=title, data=data)

        # Add the title
        key = self.keys["title"]
        self.data[key]["value"] = title

        # Add the id
        self.data["id"] = "urn:ngsi-ld:Catalogue:" + dataset_id

        # Add the publisher
        key = self.get_key(requested_key="dcterms:publisher")
        position = data.index(key) + 1
        self.data["publisher"]["value"] = data[position][0]

        # Check if we have 'issued' in the original, then we need to create the releaseDate property
        index, key, value = get_property_value(data=data, property_name="issued")
        if index != -1:
            # We found an 'issued' data
            self.data.update(self.__generate_property__(key="releaseDate", value=value[0][0]))

        # Get the rest of the data, qb:structure has the same value of qb:dataset, so we decide to
        # use only qb:dataset in CatalogueDCAT-AP
        data = get_rest_data(
            data=data,
            not_allowed_keys=["label", "publisher", "structure", "issued", "title"],
        )

        # add the new data to the dataset structure
        self.patch_data(data, False)

        # Order Context keys
        a = Context()
        a.set_data(new_data=self.data)
        a.order_context()
        self.data = a.get_data()

    def patch_data(self, data, language_map):
        if language_map:
            self.__complete_label__(title="Not specified", data=data)
        else:
            # TODO: Add only those properties that are expected, if they are not know or unexpected discard and provide
            #  a logging about the property is discarded due to it is not considered in the statSCAT-AP spec.
            [self.data.update(self.__generate_property__(key=k, value=v)) for k, v in data.items()]

    def __complete_label__(self, title, data):
        try:
            key = self.get_key(requested_key="rdfs:label")
            position = data.index(key) + 1
            description = data[position]

            descriptions = [x[0].replace('"', "") for x in description]

            languages = list()
            try:
                languages = [x[1].replace("@", "").lower() for x in description]
            except IndexError:
                logger.warning(f"The Catalogue {title} has a " f"rdfs:label without language tag: {description}")

                aux = len(description)
                if aux != 1:
                    logger.error(f"Catalogue: there is more than 1 description ({aux}), values: {description}")
                else:
                    # There is no language tag, we use by default 'en'
                    languages = ["en"]
                    logger.warning('Catalogue: selecting default language "en"')

            ###############################################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            ###############################################################################
            # for i in range(0, len(languages)):
            #     self.data['rdfs:label']['LanguageMap'][languages[i]] = descriptions[i]
            ###############################################################################
            for i in range(0, len(languages)):
                key = self.keys["description"]
                self.data[key]["value"][languages[i]] = descriptions[i]

            # Complete the information of the language with the previous information
            key = self.keys["language"]
            self.data[key]["value"] = languages
        except ValueError:
            logger.info(f"Dataset without rdfs:label detail: {title}")

    def get(self):
        return self.data

    def get_id(self):
        return self.data["id"]

    def get_key(self, requested_key):
        try:
            key = self.keys[requested_key]
            return key
        except KeyError:
            # The key did not exist therefore we add to the list with this value
            self.keys[requested_key] = requested_key
            return requested_key
