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
from hidateinfer import infer  # type: ignore[import]
from datetime import datetime, timezone
from re import compile, sub
from dateutil import parser
import pytz
from sdmx2jsonld.common.tzinfos import whois_timezone_info


class DataTypeConversion:
    def __init__(self):
        self.types = {
            "xsd:dateTime": "stoutc",
            "xsd:int": "stoi",
            "xsd:boolean": "stob",
            "xsd:float": "stof",
        }

        self.regex_12hour = compile(r"(^.*T%)(I)(.*)$")
        self.regex_microseconds = compile(r"^(.*T%.*:%S\.)(%H)*$")
        self.regex_microseconds2 = compile(r"^(.*T%.*:%S\.)(%y)*$")
        self.regex_false_date = compile(r"^%Y-%d-%y(.*)%m")
        self.regex_false_date2 = compile(r"^%Y-%d-%m(.*)%f")

    def correct_datatype_format(self, format_dt: str, hour24: bool = True):
        if hour24:
            format_dt = sub(self.regex_12hour, r"\1H\3", format_dt)

        format_dt = sub(self.regex_microseconds, r"\1%f", format_dt)
        format_dt = sub(self.regex_microseconds2, r"\1%f", format_dt)

        format_dt = sub(self.regex_false_date, r"%Y-%m-%d\1%f", format_dt)
        format_dt = sub(self.regex_false_date2, r"%Y-%m-%d\1%f", format_dt)

        return format_dt

    def convert(self, data, datatype):
        def stoutc(value):
            """
            Converts a date in string format to UTC date using
            """
            dt = parser.parse(value, tzinfos=whois_timezone_info)
            dt = dt.astimezone(pytz.UTC)
            return dt.replace(tzinfo=timezone.utc).isoformat()

        def stodt(value):
            if isinstance(value, str):
                result = infer([value])
            elif isinstance(value, list):
                result = infer(value)
            else:
                raise Exception(f"Invalid format received: {type(value)}")

            result = self.correct_datatype_format(result)
            result = datetime.strptime(value, result).replace(tzinfo=timezone.utc).isoformat()

            return result

        def stoi(value):
            """
            Converts 'something' to int. Raises exception for invalid formats
            """
            if isinstance(value, str):
                result = value.replace('"', "")
            elif isinstance(value, int):
                result = value
            else:
                raise Exception(f"Invalid format received: {type(value)}")

            return int(result)

        def stof(value):
            """
            Converts 'something' to float. Raises exception for invalid formats
            """
            if isinstance(value, str):
                result = value.replace('"', "")
            elif isinstance(value, float):
                result = value
            else:
                raise Exception(f"Invalid format received: {type(value)}")

            return float(result)

        def stob(value):
            """
            Converts 'something' to boolean. Raises exception for invalid formats
                Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
                Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
            """
            if str(value).lower() in ("yes", "y", "true", "t", "1"):
                return True

            if str(value).lower() in (
                "no",
                "n",
                "false",
                "f",
                "0",
                "0.0",
                "",
                "none",
                "[]",
                "{}",
            ):
                return False

            # logger.error(f'Invalid value for boolean conversion: {str(value)}')
            raise Exception(f"Invalid value for boolean conversion: {str(value)}")

        try:
            # jicg - function = self.types[datatype] + f'(value="{data}")'
            function = self.types[datatype] + "(value=" + data + ")"
            return eval(function)
        except KeyError:
            # logger.error(f'Datatype not defined: {datatype}')
            print(f"Datatype not defined: {datatype}")
            raise Exception(f"Datatype not defined: {datatype}")
        except NameError:
            # logger.error(f"name '{data}' is not defined")
            print(f"name '{data}' is not defined")
            raise Exception(f"name '{data}' is not defined")


if __name__ == "__main__":
    from lark import Token

    data1 = [
        '"2022-01-15T08:00:00.000"',
        Token("FORMATCONNECTOR", "^^"),
        "xsd:dateTime",
    ]
    data2 = ['"2"', Token("FORMATCONNECTOR", "^^"), "xsd:int"]
    data22 = ["2", Token("FORMATCONNECTOR", "^^"), "xsd:int"]
    data23 = ["asdfs", Token("FORMATCONNECTOR", "^^"), "xsd:int"]
    data3 = ['"true"', Token("FORMATCONNECTOR", "^^"), "xsd:boolean"]
    data4 = ['"fake"', Token("FORMATCONNECTOR", "^^"), "otraCosa"]
    data5 = [
        '"2022-01-10T09:00:00.000"',
        Token("FORMATCONNECTOR", "^^"),
        "xsd:dateTime",
    ]
    data6 = ['"2021-07-01T11:50:37.3"', Token("FORMATCONNECTOR", "^^"), "xsd:dateTime"]
    data7 = ['"2021-09-28T15:31:24.05"', Token("FORMATCONNECTOR", "^^"), "xsd:dateTime"]

    print(infer(["Mon Jan 13 09:52:52 MST 2014"]))
    print(infer([data1[0]]))
    print()

    print(infer(["2022-01-15T08:00:00"]))
    print(infer([data1[0]]))
    print()

    # Resolve problem in the library
    # if we are working with 24h, infer should return %Y-%m-%dT%H:%M:%S.%f but return %Y-%m-%dT%I:%M:%S.%f
    # if we have seconds with milliseconds, infer should return %Y-%m-%dT%I:%M:%S.%f but return %Y-%m-%dT%I:%M:%S.%H
    # There is some problem with the library and the date is not inferred properly, specially in the case
    # '2022-01-10T09:00:00.000' which is inferred as %Y-%d-%yT%I:%M:%S.%m, should be %Y-%m-%dT%H:%M:%S.%f

    dataConversionType = DataTypeConversion()
    print(dataConversionType.convert(data1[0], data1[2]))

    print(dataConversionType.convert(data2[0], data2[2]) + 10)
    print(dataConversionType.convert(data22[0], data22[2]) + 10)
    # print(dataConversionType.convert(data23[0], data23[2]) + 10)

    print(dataConversionType.convert(data3[0], data3[2]))

    try:
        print(dataConversionType.convert(data4[0], data4[2]))
    except Exception:
        print("Exception")

    # Convert datetime generated into UTC format: 2021-12-21T16:18:55Z or 2021-12-21T16:18:55+00:00, ISO8601

    print(dataConversionType.convert(data5[0], data5[2]))

    print(dataConversionType.convert(data6[0], data6[2]))

    print(dataConversionType.convert(data7[0], data7[2]))

    data101 = ['"3016.9"', Token("FORMATCONNECTOR", "^^"), "xsd:float"]
    print(dataConversionType.convert(data101[0], data101[2]))
