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
from json import load
from random import getrandbits
from os.path import dirname, join

logger = getLogger()


class Distribution(CommonClass):
    def __init__(self):
        super().__init__(entity="Distribution")
        self.data = {
            "id": "urn:ngsi-ld:Distribution:",
            "type": "Distribution",
            "accessUrl": {
                "type": "Property",
                "value": ["/ngsi-ld/v1/entities?type=https://smartdatamodels.org/dataModel.SDMX/Observation"],
            },
            "description": {
                "type": "Property",
                "value": "Distribution of statistical data observations.",
            },
            "format": {"type": "Property", "value": "JSON_LD"},
            "language": {"type": "Property", "value": list()},
            "status": {"type": "Property", "value": "Completed"},
            "title": {"type": "Property", "value": list()},
            "@context": [
                "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
            ],
        }

    def generate_data(self, catalogue):
        # Generate random id for the distribution
        random_bits = getrandbits(128)
        hash1 = "%032x" % random_bits
        self.data["id"] += hash1

        # Title is extracted from the dcterms:title from the Catalogue
        self.data["title"]["value"] = catalogue.data["title"]["value"]

        # language es obtained from language from the Catalogue
        self.data["language"]["value"] = catalogue.data["language"]["value"]

        # accessURL is generated from the configuration file.
        config_path = dirname(dirname(dirname(__file__)))
        config_path = join(join(config_path, "common"), "config.json")
        with open(config_path) as config_file:
            config = load(config_file)

        self.data["accessUrl"]["value"][0] = config["broker"] + self.data["accessUrl"]["value"][0]
