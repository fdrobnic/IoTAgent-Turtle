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
from sdmx2jsonld.transform.parser import Parser
from io import StringIO
from os import listdir, unlink
from os.path import join, isfile, dirname
from pathlib import Path


class TestCommonClass(TestCase):
    def setUp(self) -> None:
        examples_folder = dirname(dirname(__file__))
        output_folder = dirname(examples_folder)

        examples_folder = join(examples_folder, "files")
        self.output_folder = join(output_folder, "output")

        tests_files = [
            "observations.ttl",
            "structures-accounts.ttl",
            "structures-tourism.ttl",
        ]
        self.tests_files = [join(examples_folder, x) for x in tests_files]

        self.parser = Parser()

    def clean_output_dir(self) -> None:
        for a in listdir(self.output_folder):
            file_path = join(self.output_folder, a)
            try:
                if isfile(file_path):
                    unlink(file_path)
            except Exception as e:
                print("----------------------------")
                print(e)
                print("----------------------------")

    def test_files_from_StringIO_web_interface_loop(self):
        print("Testing test_files_from_StringIO_web_interface_loop")
        for a in self.tests_files:
            print(f"Parsing: {a}")
            self.clean_output_dir()

            # Read the RDF Turtle file
            with open(a, "r") as rf:
                rdf_data = rf.read()

            # Parsing the RDF
            try:
                _ = self.parser.parsing(content=StringIO(rdf_data), out=False)
            except Exception as e:
                assert False, f"\nThe parser was not completed," f"\n   file: {a}" f"\n   exception:\n {e.message}"

            print("Parsing completed...\n")

        print("Test finished...\n")

    def test_files_from_TextIOWrapper_cli_with_generating_files(self):
        print("Testing test_files_from_TextIOWrapper_cli_with_generating_files")
        for a in self.tests_files:
            print(f"Parsing: {a}")
            self.clean_output_dir()

            # Read the RDF Turtle file
            with open(a, "r") as rf:
                rdf_data = rf.read()

            # Parsing the RDF
            try:
                _ = self.parser.parsing(content=rdf_data, out=True)
            except Exception as e:
                assert False, f"\nThe parser was not completed," f"\n   file: {a}" f"\n   exception:\n {e.message}"

            print("Parsing completed...\n")

        print("Test finished...\n")

    def test_file_from_TextIOWrapper_cli_only_printing_result(self):
        print("Testing test_files_from_TextIOWrapper_cli_with_generating_files")
        for a in self.tests_files:
            print(f"Parsing: {a}")
            self.clean_output_dir()

            # Read the RDF Turtle file
            with open(a, "r") as rf:
                rdf_data = rf.read()

            # Parsing the RDF
            try:
                _ = self.parser.parsing(content=rdf_data, out=False)
            except Exception as e:
                assert False, f"\nThe parser was not completed," f"\n   file: {a}" f"\n   exception:\n {e.message}"

            print("Parsing completed...\n")

        print("Test finished...\n")
