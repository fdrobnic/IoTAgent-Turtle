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


class CogConceptSchema(CommonClass):
    def __init__(self):
        # sdmx-concept:cog a skos:ConceptScheme;
        #   rdfs:label "Content Oriented Guidelines concept scheme"@en;
        #   rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf>.
        super().__init__(entity="ConceptSchema")

        self.data = {
            "id": "urn:ngsi-ld:ConceptSchema:cog",
            "type": "ConceptScheme",
            "language": {"type": "Property", "value": ["en"]},
            "prefLabel": {
                "type": "Property",
                "value": {"en": "Content Oriented Guidelines concept scheme"},
            },
            "@context": [
                "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
            ],
        }
