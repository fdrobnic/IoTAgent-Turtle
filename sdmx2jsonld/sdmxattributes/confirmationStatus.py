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
from sdmx2jsonld.exceptions.exceptions import ClassConfStatusError
from sdmx2jsonld.sdmxattributes.sdmxattribute import SDMXAttribute


class ConfStatus(SDMXAttribute):
    status: list = ["F", "N", "C", "D", "S", "A", "O", "T", "G", "M", "E", "P"]

    def __init__(self):
        # sdmx-attribute:confStatus a qb:AttributeProperty, rdf:Property  ;
        #     qb:concept sdmx-concept:confStatus ;
        #     rdfs:label "Confidentiality - status"@en ;
        #     rdfs:comment """Information about the confidentiality status of the object to which this
        #     attribute is attached."""@en ;
        #     rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf> .
        super().__init__(
            entity_id="confStatus",
            label="Confidentiality - status",
            description="Information about the confidentiality status of the object "
            "to which this attribute is attached.",
            concept_id="confStatus",
            identifier="confStatus",
            entity_range="xsd:string",
        )

    def fix_value(self, value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form confStatus-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        value_upper = value.upper()

        if value_upper in self.status:
            return value_upper
        else:
            # we could receive a value in the format confStatus-<value>
            m = search("CONFSTATUS-(.*)", value_upper)

            if m is not None:
                status = m.group(1)

                if status in self.status:
                    return status
                else:
                    message = (
                        f"ConfStatus value is not included in the list of available values,\n"
                        f"    got:{value}\n"
                        f"    expected:{['confStatus-'+x for x in self.status]}"
                    )

                    raise ClassConfStatusError(data=value, message=message)

            else:
                # We received a value that it is not following the template format
                raise ClassConfStatusError(value)
