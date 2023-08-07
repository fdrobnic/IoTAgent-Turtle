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


class TimeFormatConcept(SDMXConcept):
    def __init__(self):
        # sdmx-concept:timeFormat a sdmx:Concept, skos:Concept ;
        #     rdfs:label "Time Format"@en ;
        #     rdfs:comment """Technical format in which time is represented for the measured phenomenon."""@en ;
        #     rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf> ;
        #     skos:notation "urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:
        #     CROSS_DOMAIN_CONCEPTS[1.0].TIME_FORMAT";
        #     skos:inScheme sdmx-concept:cog .
        super().__init__(
            entity_id="timeFormat",
            label="Time Format",
            notation="urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:" "CROSS_DOMAIN_CONCEPTS[1.0].TIME_FORMAT",
        )
