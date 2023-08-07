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
from os.path import join, exists, dirname, abspath

# Settings file is inside Basics directory, therefore I have to go back to the parent directory
# to have the Code Home directory
MODULEHOME = dirname(dirname(abspath(__file__)))
GRAMMARFOLDER = join(MODULEHOME, "grammar")
GRAMMARFILE = join(GRAMMARFOLDER, "grammar.lark")

if not exists(GRAMMARFILE):
    msg = (
        "\nERROR: There is not Lark grammar file in the expected folder. "
        "\n       Unable to parse the RDF Turtle file."
        "\n\n       Please correct it if you do not want to see these messages.\n\n\n"
    )

    print(msg)

    exit(1)
