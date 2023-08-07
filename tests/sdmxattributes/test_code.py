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
from sdmx2jsonld.sdmxattributes.code import Code
from sdmx2jsonld.exceptions.exceptions import ClassCode


class TestConfStatus(TestCase):
    def test_code_value_with_prefix(self):
        value = "sdmx-code:decimals-1"
        expected = 1

        code = Code(typecode="decimals")
        obtained = code.fix_value(value=value)
        assert obtained == expected, (
            f"\ncode was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_code_negative_value_with_prefix(self):
        value = "sdmx-code:decimals--1"
        expected = "sdmx-code:decimals--1 -> decimals out of range, got: -1   range(0, 15)"

        code = Code(typecode="decimals")

        with self.assertRaises(ClassCode) as error:
            _ = code.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_code_value_bigger_than_maximum_with_prefix(self):
        value = "sdmx-code:decimals-67"
        expected = "sdmx-code:decimals-67 -> decimals out of range, got: 67   range(0, 15)"

        code = Code(typecode="decimals")

        with self.assertRaises(ClassCode) as error:
            _ = code.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_code_value_without_prefix(self):
        value = "unitMult-1"
        expected = 1

        code = Code(typecode="unitMult")
        obtained = code.fix_value(value=value)
        assert obtained == expected, (
            f"\ncode was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_code_negative_value_without_prefix(self):
        value = "unitMult--1"
        expected = "unitMult--1 -> unitMult out of range, got: -1   range(0, 13)"

        code = Code(typecode="unitMult")

        with self.assertRaises(ClassCode) as error:
            _ = code.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_code_value_bigger_than_maximum_without_prefix(self):
        value = "unitMult-67"
        expected = "unitMult-67 -> unitMult out of range, got: 67   range(0, 13)"

        code = Code(typecode="unitMult")

        with self.assertRaises(ClassCode) as error:
            _ = code.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_code_integer_value(self):
        value = 2
        expected = 2

        code = Code(typecode="unitMult")
        obtained = code.fix_value(value=value)
        assert obtained == expected, (
            f"\ncode was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_code_integer_value_out_of_range(self):
        value = 25
        expected = "25 -> unitMult out of range, got: 25   range(0, 13)"

        code = Code(typecode="unitMult")

        with self.assertRaises(ClassCode) as error:
            _ = code.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_code_string_value(self):
        value = "2"
        expected = 2

        code = Code(typecode="unitMult")
        obtained = code.fix_value(value=value)
        assert obtained == expected, (
            f"\ncode was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_code_string_value_out_of_range(self):
        value = "25"
        expected = "25 -> unitMult out of range, got: 25   range(0, 13)"

        code = Code(typecode="unitMult")

        with self.assertRaises(ClassCode) as error:
            _ = code.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_any_other_code(self):
        value = "sadf"
        expected = "sadf -> Data is not a valid value"

        code = Code(typecode="unitMult")

        with self.assertRaises(ClassCode) as error:
            _ = code.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)
