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

import re


class RegParser:
    def __init__(self):
        regex = "http[s]?:\/\/(.+)"

        # Compile the Regex
        self.re = re.compile(regex)

    def obtain_id(self, string_to_parse, prefix_string=""):
        # Return if the string matched the ReGex
        out = self.re.match(string_to_parse)

        if out is None:
            # Check if the prefixed name include ':'
            try:
                obtained_id = string_to_parse.split(":")[1]
            except IndexError:
                # We have a normal prefix or data
                obtained_id = string_to_parse
        else:
            # We have a URIREF
            out = out.group(1)
            out = out.split("/")

            # we get the last value which corresponds to the id
            obtained_id = prefix_string + out[(len(out) - 1) :][0]

        return obtained_id
