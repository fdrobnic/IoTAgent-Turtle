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
from sdmx2jsonld.sdmxattributes.confirmationStatus import ConfStatus
from sdmx2jsonld.exceptions.exceptions import ClassConfStatusError


class TestConfStatus(TestCase):
    def setUp(self):
        self.conversion = ConfStatus()

    def test_fix_value_data_in_predefined_values(self):
        value = "F"
        expected = "F"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nconfStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

        value = "f"
        expected = "F"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nconfStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_fix_value_data_in_predefined_values_with_prefix(self):
        value = "confStatus-A"
        expected = "A"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nconfStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

        value = "confstatus-a"
        expected = "A"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nconfStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_fix_value_data_with_valid_prefix_but_not_expected_value(self):
        value = "confStatus-EEEEE"
        expected = (
            "confStatus-EEEEE -> ConfStatus value is not included in the list of available values,\n"
            + "    got:confStatus-EEEEE\n"
            + "    expected:['confStatus-F', 'confStatus-N', 'confStatus-C', 'confStatus-D', 'confStatus-S', "
            "'confStatus-A', 'confStatus-O', 'confStatus-T', 'confStatus-G', 'confStatus-M', 'confStatus-E', "
            "'confStatus-P']"
        )

        with self.assertRaises(ClassConfStatusError) as error:
            _ = self.conversion.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_fix_value_unexpected_value_without_prefix(self):
        value = "EEEE"
        expected = "EEEE -> ConfStatus value is not the expected"
        with self.assertRaises(ClassConfStatusError) as error:
            _ = self.conversion.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_fix_value_unexpected_prefix(self):
        value = "lkdjlks-A"
        expected = "lkdjlks-A -> ConfStatus value is not the expected"
        with self.assertRaises(ClassConfStatusError) as error:
            _ = self.conversion.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)
