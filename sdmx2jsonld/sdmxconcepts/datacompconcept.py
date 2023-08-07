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
from sdmx2jsonld.sdmxconcepts.sdmxconcept import SDMXConcept


class DataCompConcept(SDMXConcept):
    def __init__(self):
        # sdmx-concept:dataComp a sdmx:Concept, skos:Concept ;
        #     rdfs:label "Data Compilation"@en ;
        #     rdfs:comment """Operations performed on data to derive new information according
        #     to a given set of rules."""@en ;
        #     rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf> ;
        #     skos:notation
        #     "urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:CROSS_DOMAIN_CONCEPTS[1.0].DATA_COMP";
        #     skos:inScheme sdmx-concept:cog .
        super().__init__(
            entity_id="dataComp",
            label="Data Compilation",
            notation="urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=" "SDMX:CROSS_DOMAIN_CONCEPTS[1.0].DATA_COMP",
        )
