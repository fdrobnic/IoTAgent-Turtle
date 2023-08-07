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
class ClassSDMXAttributeError(Exception):
    """Base class for other exceptions"""

    def __init__(self, data, message):
        self.message = message
        self.data = data

    def __str__(self):
        return f"{self.data} -> {self.message}"


class ClassConfStatusError(ClassSDMXAttributeError):
    """Raised when the input value is not included in the list of available values for confStatus"""

    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="ConfStatus value is not the expected"):
        super().__init__(data=data, message=message)


class ClassObsStatusError(ClassSDMXAttributeError):
    """Raised when the input value is not included in the list of available values for obsStatus"""

    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="ObsStatus value is not the expected"):
        super().__init__(data=data, message=message)


class ClassCode(ClassSDMXAttributeError):
    """Raised when the input value is not included in the list of available values for unitMult and decimals"""

    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="Decimals value is not the expected"):
        super().__init__(data=data, message=message)


class ClassFreqError(ClassSDMXAttributeError):
    """Raised when the input value is not included in the list of available values for Freq"""

    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="Decimals value is not the expected"):
        super().__init__(data=data, message=message)


class ClassExtractPrefixError(ClassSDMXAttributeError):
    """Raised when the input value is None or Empty or includes several prefixes"""

    """Exception raised for errors in the input data.

    Attributes:
        data -- input data which caused the error
        message -- explanation of the error
    """

    def __init__(self, data, message="Value is not the expected"):
        super().__init__(data=data, message=message)
