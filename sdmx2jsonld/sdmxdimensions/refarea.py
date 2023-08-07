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
from sdmx2jsonld.sdmxdimensions.sdmxdimension import SDMXDimension


class RefArea(SDMXDimension):
    def __init__(self):
        # sdmx-dimension:refArea a qb:DimensionProperty, rdf:Property;
        #   rdfs:range rdfs:Resource;
        #   qb:concept sdmx-concept:refArea;
        #   rdfs:label "Reference Area"@en;
        #   rdfs:comment "The country or geographic area to which the measured statistical phenomenon relates."@en;
        #   rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf>.
        super().__init__(
            entity_id="refArea",
            label="Reference Area",
            description="The country or geographic area to which the measured statistical " "phenomenon relates.",
            concept_id="refArea",
            identifier="refArea",
            entity_range="xsd:string",
        )
