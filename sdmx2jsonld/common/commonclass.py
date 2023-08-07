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
from json import dumps
from sdmx2jsonld.common.regparser import RegParser
from os.path import exists
from os import mkdir


class CommonClass:
    def __init__(self, entity):
        self.data = dict()
        self.keys = dict()
        self.entity = entity

    def add_context(self, context, context_mapping):
        # Set the context as it is received and mixed with the core context
        self.data["@context"] = context["@context"]

        # Fix the prefix of the core properties of the Dataset entity
        new_data = dict()

        for k, v in self.data.items():
            # Return if the string matched the ReGex
            out = k.split(":")

            if len(out) == 2 and out[0] in context_mapping.keys():
                new_prefix = context_mapping[out[0]]
                new_key = new_prefix + ":" + out[1]

                new_data[new_key] = self.data[k]
                self.keys[k] = new_key
            else:
                new_data[k] = v

        self.data = new_data

    def get(self):
        return self.data

    def save(self):
        data = self.get()

        aux = data["id"].split(":")
        length_aux = len(aux)

        # We need to check that the output folder exist
        if exists("./output") is False:
            # We need to create the folder because it does not exist
            mkdir("./output")

        filename = "./output/" + "_".join(aux[length_aux - 2 :]) + ".jsonld"

        # Serializing json
        json_object = dumps(data, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)

    def generate_id(self, value, entity=None, update_id=False):
        parse = RegParser()
        aux = parse.obtain_id(value)

        if entity is None:
            new_aux = "urn:ngsi-ld:" + self.entity + ":" + aux
        else:
            new_aux = "urn:ngsi-ld:" + entity + ":" + aux

        if update_id:
            self.data["id"] = new_aux
            return new_aux
        else:
            return aux, new_aux

    def __generate_property__(self, key, value):
        result = {key: {"type": "Property", "value": value}}

        return result
