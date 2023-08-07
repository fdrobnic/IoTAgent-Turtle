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
from sdmx2jsonld.exceptions.exceptions import ClassCode


class Code:
    status: list
    type: str
    data_range: range

    def __init__(self, typecode):
        self.typecode = typecode

        if typecode == "decimals":
            self.data_range = range(0, 15)
        elif typecode == "unitMult":
            self.data_range = range(0, 13)

    def fix_value(self, value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form decimals-<value> or unitMult-<value>, so we have to extract
        # the substring and return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        number: int() = 0

        m = search(f"sdmx-code:{self.typecode}-(.*)", str(value))

        if m is not None:
            number = int(m.group(1))
        else:
            # The data is not following the sdmx-code:<value> we have to check which one
            # 1) Check if there is a value without the prefix
            m = search(f"{self.typecode}-(.*)", str(value))

            if m is not None:
                number = int(m.group(1))
            else:
                # We need to check is there is an integer number between a valid range
                if isinstance(value, int):
                    # Need to check the range
                    number = value
                elif isinstance(value, str):
                    try:
                        number = int(value)
                    except ValueError:
                        raise ClassCode(data=value, message=f"Data is not a valid value")

        if number not in self.data_range:
            raise ClassCode(
                data=value,
                message=f"{self.typecode} out of range, got: {number}   {self.data_range}",
            )

        return number
