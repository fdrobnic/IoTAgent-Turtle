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
from sdmx2jsonld.common.commonclass import CommonClass


class SDMXDimension(CommonClass):
    def __init__(
        self,
        entity_id,
        identifier,
        entity_range,
        label=None,
        description=None,
        concept_id=None,
    ):
        super().__init__(entity="DimensionProperty")
        self.data = {
            "id": f"urn:ngsi-ld:DimensionProperty:{entity_id}",
            "type": "DimensionProperty",
            "language": {"type": "Property", "value": ["en"]},
            "label": {
                "type": "Property",
                "value": {
                    "en": label,
                },
            },
            "description": {
                "type": "Property",
                "value": {
                    "en": description,
                },
            },
            "concept": {
                "type": "Relationship",
                "object": f"urn:ngsi-ld:Concept:{concept_id}",
            },
            "identifier": {"type": "Property", "value": identifier},
            "range": {"type": "Property", "value": entity_range},
            "@context": [
                "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
            ],
        }

        # We need to check if some of the parameters are None, in that case we have to pop the key from data
        if label is None:
            self.data.pop("label")

        if description is None:
            self.data.pop("description")

        if concept_id is None:
            self.data.pop("concept")
