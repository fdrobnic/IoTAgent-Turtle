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

from unittest import TestCase
from sdmx2jsonld.common.commonclass import CommonClass
import os
import json


class TestCommonClass(TestCase):
    def setUp(self) -> None:
        pass

    def test_instance_class(self):
        cclass = CommonClass("test.common.entity")
        urnid = cclass.generate_id("https://string-to-parse-ur/entity_id", update_id=True)
        assert urnid == "urn:ngsi-ld:test.common.entity:entity_id"
        # urnid = cclass.generate_id("")
        # print(urnid)

    def test_save(self):
        context = {
            "@context": "https://raw.githubusercontent.com/smart-data-models/data-models/master/context/merge_subjects_config_example.json"
        }
        context_map = {
            "address": "https://smartdatamodels.org/address",
            "alternateName": "https://smartdatamodels.org/alternateName",
            "status": "ngsi-ld:status",
        }
        cclass = CommonClass("test.common.entity")
        urnid = cclass.generate_id("https://string-to-parse-ur/entity_id", update_id=True)
        assert urnid == "urn:ngsi-ld:test.common.entity:entity_id"

        cclass.add_context(context, context_map)

        os.makedirs("/tmp/commonclass", exist_ok=True)
        os.chdir("/tmp/commonclass")
        cclass.save()

        with open("/tmp/commonclass/output/test.common.entity_entity_id.jsonld", "r") as f:
            data = json.load(f)
        assert data["id"] == urnid
        assert data["@context"] == context["@context"]

    # TODO - Add tests with cclass.generate_id using update_id with a False value
