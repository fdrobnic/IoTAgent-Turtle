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
from sdmx2jsonld.sdmxattributes.observationStatus import ObsStatus
from sdmx2jsonld.exceptions.exceptions import ClassObsStatusError


class TestObsStatus(TestCase):
    def setUp(self):
        self.conversion = ObsStatus()

    def test_fix_value_data_in_predefined_values(self):
        value = "A"
        expected = "A"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nobsStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

        value = "a"
        expected = "A"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nobsStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_fix_value_data_in_predefined_values_with_prefix(self):
        value = "obsStatus-A"
        expected = "A"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nobsStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

        value = "obsstatus-a"
        expected = "A"
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, (
            f"\nobsStatus was not the expected," f"\n    got     : {obtained}" f"\n    expected: {expected}"
        )

    def test_fix_value_data_with_valid_prefix_but_not_expected_value(self):
        value = "obsStatus-EEEEE"
        expected = (
            "obsStatus-EEEEE -> ObsStatus value is not included in the list of available values,\n"
            + "    got:obsStatus-EEEEE\n"
            + "    expected:['obsStatus-A', 'obsStatus-B', 'obsStatus-D', 'obsStatus-E', 'obsStatus-F', "
            "'obsStatus-G', 'obsStatus-I', 'obsStatus-K', 'obsStatus-W', 'obsStatus-O', 'obsStatus-M', "
            "'obsStatus-P', 'obsStatus-S', 'obsStatus-L', 'obsStatus-H', 'obsStatus-Q', 'obsStatus-J', "
            "'obsStatus-N', 'obsStatus-U', 'obsStatus-V']"
        )

        with self.assertRaises(ClassObsStatusError) as error:
            _ = self.conversion.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_fix_value_unexpected_value_without_prefix(self):
        value = "EEEE"
        expected = "EEEE -> ObsStatus value is not the expected"
        with self.assertRaises(ClassObsStatusError) as error:
            _ = self.conversion.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_fix_value_unexpected_prefix(self):
        value = "lkdjlks-A"
        expected = "lkdjlks-A -> ObsStatus value is not the expected"
        with self.assertRaises(ClassObsStatusError) as error:
            _ = self.conversion.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)
