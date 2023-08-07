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
from unittest import TestCase
from sdmx2jsonld.common.listmanagement import (
    get_rest_data,
    flatten_value,
    extract_prefix,
    get_property_value,
)
from sdmx2jsonld.exceptions.exceptions import ClassExtractPrefixError


class TestRegToParser(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_rest_data(self):
        data = [
            "a",
            ["qb:AttributeProperty"],
            "rdfs:label",
            [['"SDMX attribute COMMENT_OBS"', "@en"], ['"Attribut SDMX "', "@fr"]],
            "dct:created",
            [["2022-01-15T06:00:00+00:00"]],
            "dct:identifier",
            [['"a3003"']],
            "dct:modified",
            [["2022-01-15T06:30:00+00:00"]],
            "qb:concept",
            ["http://bauhaus/concepts/definition/c4303"],
            "insee:disseminationStatus",
            ["http://id.insee.fr/codes/base/statutDiffusion/Prive"],
            "insee:validationState",
            [['"Unpublished"']],
            "rdfs:range",
            ["xsd:string"],
            "skos:notation",
            [['"COMMENT_OBS"']],
        ]
        not_allowed_keys = [
            "sliceKey",
            "component",
            "disseminationStatus",
            "validationState",
            "notation",
            "label",
            "codeList",
            "concept",
        ]
        further_process_keys = ["component", "label"]
        expected_res = {
            "created": "2022-01-15T06:00:00+00:00",
            "identifier": "a3003",
            "modified": "2022-01-15T06:30:00+00:00",
            "range": "xsd:string",
        }
        res = get_rest_data(data, not_allowed_keys, further_process_keys)
        assert expected_res == res

    def test_flatten_value(self):
        data = [
            ['"SDMX attribute PRE_BREAK_VALUE"', "@en"],
            ['"Attribut SDMX "', "@fr"],
        ]
        expected_res = {"en": "SDMX attribute PRE_BREAK_VALUE", "fr": "Attribut SDMX "}
        got_data = flatten_value(data)
        assert got_data == expected_res

    # data = ['', None, 'dct:created', 'dct:identifier', 'dct:modified', 'rdfs:range', 'uno', 'a:b:c']
    def test_extract_prefix_with_a_prefix(self):
        data = "a:b"
        expected_res = "b"
        got_res = extract_prefix(data)
        assert got_res == expected_res

    def test_extract_prefix_with_several_prefixes(self):
        data = "a:b:c"
        expected = "Unexpected number of prefixes: 'a:b:c'"
        with self.assertRaises(ClassExtractPrefixError) as error:
            _ = extract_prefix(attribute=data)

        self.assertEqual(str(error.exception.message), expected)

    def test_extract_prefix_with_None_value(self):
        data = None
        expected = "Unexpected data received: 'None'"
        with self.assertRaises(ClassExtractPrefixError) as error:
            _ = extract_prefix(attribute=data)

        self.assertEqual(str(error.exception.message), expected)

    def test_extract_prefix_with_empty_value(self):
        data = ""
        expected = "Unexpected data received: ''"
        with self.assertRaises(ClassExtractPrefixError) as error:
            _ = extract_prefix(attribute=data)

        self.assertEqual(str(error.exception.message), expected)

    def test_extract_prefix_with_a_value_without_prefix(self):
        data = "a"
        expected_res = "a"
        got_res = extract_prefix(data)
        assert got_res == expected_res

    def test_get_property_data_from_array_property_without_prefix(self):
        data = [
            "a",
            ["qb:DataSet"],
            "rdfs:label",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
            "dcterms:issued",
            [["2022-04-01T06:00:00+00:00"]],
            "dcterms:publisher",
            ["http://id.insee.fr/organisations/insee"],
            "dcterms:title",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
            "qb:structure",
            ["http://bauhaus/structuresDeDonnees/structure/dsd3001"],
            "sdmx-attribute:title",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
        ]
        expected = [
            ['"GDP and main components (current prices)"', "@en"],
            ['"PIB et principales composantes (prix courants)"', "@fr"],
        ]

        index, key, obtained = get_property_value(data=data, property_name="title")

        self.assertEqual(index, 8)
        self.assertEqual(key, "dcterms:title")
        self.assertEqual(expected, obtained)

    def test_get_property_data_from_array_property_with_prefix(self):
        data = [
            "a",
            ["qb:DataSet"],
            "rdfs:label",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
            "dcterms:issued",
            [["2022-04-01T06:00:00+00:00"]],
            "dcterms:publisher",
            ["http://id.insee.fr/organisations/insee"],
            "dcterms:title",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
            "qb:structure",
            ["http://bauhaus/structuresDeDonnees/structure/dsd3001"],
            "sdmx-attribute:title",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
        ]
        expected = [
            ['"GDP and main components (current prices)"', "@en"],
            ['"PIB et principales composantes (prix courants)"', "@fr"],
        ]

        index, key, obtained = get_property_value(data=data, property_name="dcterms:title")

        self.assertEqual(index, 8)
        self.assertEqual(key, "dcterms:title")
        self.assertEqual(expected, obtained)

    def test_get_property_data_from_array_invalid_property(self):
        data = [
            "a",
            ["qb:DataSet"],
            "rdfs:label",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
            "dcterms:issued",
            [["2022-04-01T06:00:00+00:00"]],
            "dcterms:publisher",
            ["http://id.insee.fr/organisations/insee"],
            "dcterms:title",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
            "qb:structure",
            ["http://bauhaus/structuresDeDonnees/structure/dsd3001"],
            "sdmx-attribute:title",
            [
                ['"GDP and main components (current prices)"', "@en"],
                ['"PIB et principales composantes (prix courants)"', "@fr"],
            ],
        ]
        expected = ""

        index, key, obtained = get_property_value(data=data, property_name="any")

        self.assertEqual(index, -1)
        self.assertEqual(key, "")
        self.assertEqual(expected, obtained)
