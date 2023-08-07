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
import random

logger = getLogger()


class CatalogueDCATAP(CommonClass):
    def __init__(self):
        super().__init__(entity='CatalogueDCAT-AP')

        self.data = {
            "id": str(),
            "type": "CatalogueDCAT-AP",
            "dataset": {
                "type": "object",
                "value": str()
            },

            "language": {
                "type": "Property",
                "value": list()
            },


            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "rdfs:label": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "description": {
                "type": "Property",
                "value": dict()
            },

            "publisher": {
                "type": "Property",
                "value": str()
            },

            "title": {
                "type": "Array",
                "value": list()
            },


            "@context": [
                "https://raw.githubusercontent.com/SEMICeu/DCAT-AP/master/releases/1.1/dcat-ap_1.1.jsonld",
                "https://raw.githubusercontent.com/smart-data-models/dataModel.DCAT-AP/master/context.jsonld"
            ]
        }

        self.concept_id = str()

    def add_dataset(self, dataset_id):
        self.concept_id = dataset_id

        # generate hash id
        random_bits = random.getrandbits(128)
        hash1 = "%032x" % random_bits

        # Add the id
        self.data['id'] = "urn:ngsi-ld:CatalogueDCAT-AP:" + hash1

        # Add dataset id
        self.data['dataset']['value'] = dataset_id

    def get(self):
        return self.data

    def get_id(self):
        return self.data['id']
