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


class TimePeriod(SDMXDimension):
    def __init__(self):
        # sdmx-dimension:timePeriod a qb:DimensionProperty, rdf:Property;
        #   rdfs:range rdfs:Resource;
        #   qb:concept sdmx-concept:timePeriod;
        #   rdfs:label "Time Period"@en;
        #   rdfs:comment "The period of time or point in time to which the measured observation refers."@en;
        #   rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf>.
        super().__init__(
            entity_id="timePeriod",
            label="Time Period",
            description="The period of time or point in time to which the measured observation refers.",
            concept_id="timePeriod",
            identifier="timePeriod",
            entity_range="xsd:string",
        )

    @staticmethod
    def fix_value(value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form freq-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        value_upper = value.upper()

        m = search("FREQ-(.*)", value_upper)

        if m is not None:
            status = m.group(1)
            return status
        else:
            # We received a value that it is not following the template format
            raise ClassFreqError(value)
