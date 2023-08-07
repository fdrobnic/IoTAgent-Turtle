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
from re import search
from sdmx2jsonld.exceptions.exceptions import ClassFreqError
from sdmx2jsonld.sdmxdimensions.sdmxdimension import SDMXDimension


class MeasureType(SDMXDimension):
    def __init__(self):
        # qb:measureType a qb:DimensionProperty, rdf:Property;
        #     rdfs:label "measure type"@en;
        #     rdfs:comment "Generic measure dimension, the value of this dimension indicates which measure (from the set of measures in the DSD) is being given by the obsValue (or other primary measure)"@en;
        #     rdfs:range  qb:MeasureProperty;
        #     rdfs:isDefinedBy <http://purl.org/linked-data/cube>;
        super().__init__(
            entity_id="measureType",
            label="measure type",
            description="Generic measure dimension, the value of this dimension indicates which measure "
            "(from the set of measures in the DSD) is being given by the obsValue "
            "(or other primary measure).",
            concept_id=None,
            identifier="measureType",
            entity_range="xsd:string",
        )
