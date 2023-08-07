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


class Context:
    def __init__(self):
        self.context = {"@context": dict()}

        self.fixed_context = [
            "https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld",
            "http://www.w3.org/ns/dcat#",
            "http://data.europa.eu/(xyz)/statdcat-ap/",
            "http://purl.org/dc/terms/",
        ]

        # Dictionary to keep those contexts that are update from the core contexts
        self.context_mapping = dict()
        self.data = dict()

        # By default, the context should include the smart data models context
        self.context["@context"].update(
            {"sdmp": "https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld"}
        )

        # statDCAT-AP contexts
        self.context["@context"].update({"dcat": "http://www.w3.org/ns/dcat#"})

        self.context["@context"].update({"dct": "http://purl.org/dc/terms/"})

        self.context["@context"].update({"stat": "http://data.europa.eu/(xyz)/statdcat-ap/"})

    def add_context(self, context):
        aux = list(context.items())
        key = aux[0][0]
        value = aux[0][1]

        found = False
        k = ""

        # check if the value of the new_context is in one of the values of the previous context
        for k, v in self.context["@context"].items():
            if v == value:
                found = True
                break

        if not found:
            # we did not find a key -> New context, we need to add
            self.context["@context"].update(context)
        else:
            # We found then we need to change the key in the context or add new one and delete the old one
            self.context["@context"].pop(k)
            self.context["@context"].update(context)
            self.context_mapping.update({k: key})

    def get_context(self):
        return self.context

    def get_context_mapping(self):
        return self.context_mapping

    def print_context(self):
        print(self.context)

    def key_used(self):
        def key(json_property):
            aux = json_property.split(":")
            if len(aux) == 2:
                aux = aux[0]
            else:
                aux = ""

            return aux

        # Get the list of keys except id, type, and @context
        keys = list(self.data.keys())
        keys.remove("id")
        keys.remove("type")
        keys.remove("@context")
        prefix_ids = list(map(lambda x: key(json_property=x), keys))
        prefix_ids = list(filter(lambda x: x != "", prefix_ids))
        prefix_ids = [*set(prefix_ids)]

        return prefix_ids

    def reduce_context(self, used_keys):
        # 1st: Get the key-value of the fixed context
        aux = dict((new_val, new_k) for new_k, new_val in self.data["@context"].items())
        aux = list(map(lambda x: aux[x], self.fixed_context))

        # 2nd: Join fixed_context and used_keys
        aux = aux + used_keys

        # 3rd: Get the new context
        new_context = list(map(lambda x: {x: self.data["@context"][x]}, aux))
        new_context = dict((key, val) for k in new_context for key, val in k.items())

        # TODO: we should fix if the rest of context lines are needed or they are duplicated some properties
        return new_context

    def new_analysis(self):
        """
        Simplified the content of the @context property in the JSON-LD
        """
        # 1st step, reduce context to the really needed elements plus the corresponding to statDCAT-AP
        # 'sdmp': 'https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld'
        # 'dcat': 'http://www.w3.org/ns/dcat#'
        # 'stat': 'http://data.europa.eu/(xyz)/statdcat-ap/'
        # 'dct': 'http://purl.org/dc/terms/
        used_keys = self.key_used()

        new_context = self.reduce_context(used_keys=used_keys)
        self.data["@context"] = new_context

    def order_context(self):
        # I want that the content of the dict, 1st id, 2nd type, last context
        # Get all the keys and initialize the order
        keys = list(self.data.keys())
        keys.remove("type")
        keys.remove("id")
        keys.remove("@context")

        # initializing order
        ord_list = ["id", "type"] + keys + ["@context"]

        # Custom order dictionary
        # Using dictionary comprehension
        self.data = {key: self.data[key] for key in ord_list}

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data


if __name__ == "__main__":
    a = Context()

    a.print_context()
    a.add_context({"rdf": "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>"})
    a.print_context()
    print()

    data = {
        "type": "Dataset",
        "id": "urn:ngsi-ld:Dataset:dsd3001",
        "dc:title": "http://bauhaus/structuresDeDonnees/structure/dsd3001",
        "dc:identifier": "dsd3001",
        "dc:language": {"type": "Property", "value": ["en", "fr"]},
        "dc:description": {
            "type": "Property",
            "value": {"en": "SDMX DSD NA_MAIN", "fr": "SDMX NA_MAIN"},
        },
        "@context": {
            "sdmp": "https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld",
            "dcat": "http://www.w3.org/ns/dcat#",
            "stat": "http://data.europa.eu/(xyz)/statdcat-ap/",
            "qb": "http://purl.org/linked-data/cube#",
            "dc11": "http://purl.org/dc/elements/1.1/",
            "dc": "http://purl.org/dc/terms/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "ns0": "http://rdf.insee.fr/def/base#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "owl": "http://www.w3.org/2002/07/owl#",
        },
        "dc11:contributor": "DG75-H250",
        "dc11:creator": "DG57-L201",
        "dc:created": "2022-01-15T08:00:00+00:00",
        "dc:modified": "2022-01-15T10:00:00+00:00",
        "other_thing": "foo",
    }

    a.set_data(new_data=data)
    a.new_analysis()
    print(a.get_data())
    a.order_context()
    print(a.get_data())
