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

from sdmx2jsonld.transform.transformer import TreeToJson
from lark import Lark
from pprint import pprint
from io import TextIOWrapper, TextIOBase, StringIO
from json import dumps
from logging import getLogger
from sdmx2jsonld.exceptions import UnexpectedEOF, UnexpectedInput, UnexpectedToken
from sdmx2jsonld.common.rdf import turtle_terse


logger = getLogger(__name__)
__version__ = "0.5.0"


class Parser:
    def __init__(self):
        # Open the grammar file
        with open("./sdmx2jsonld/grammar/grammar.lark") as f:
            grammar = f.read()

        self.parser = Lark(grammar, start='start', parser='lalr')

    def parsing(self, content: TextIOBase, out: bool = False):
        """
        Function that parses the RDF Turtle file to generate the JSON-LD content to be sent to the FIWARE Context Broker
        :param content: RDF Context in TextIOBase superclass. It could be a StringIO content or a TextIOWrapper
        :param out: Boolean to indicate if we want to generate the proper JSON-LD files or just show the parser results
                    on the screen
        :return: Nothing
        """

        match content:
            case StringIO():
                result = self.parsing_string(content=content)
                return result
            case TextIOWrapper():
                self.parsing_file(content=content, out=out)

    def parsing_file(self, content: TextIOWrapper, out: bool):
        transform = TreeToJson()

        content = content.read()
        content = turtle_terse(rdf_content=content)

        try:
            tree = self.parser.parse(content)
        except UnexpectedToken as err:
            raise err
        except UnexpectedInput as err:
            raise err
        except UnexpectedEOF as err:
            raise err

        transform.transform(tree)

        if out:
            # Save the generated content into files
            logger.info('Save the generated content into files')
            transform.save()
        elif content is not None:
            print()
            pprint(transform.get_catalogue())
            pprint(transform.get_dataset())
            [pprint(x.get()) for x in transform.get_dimensions()]
            [pprint(x.get()) for x in transform.get_attributes()]
            [pprint(x.get()) for x in transform.get_conceptSchemas()]
            [pprint(x.get()) for x in transform.get_conceptLists()]

    def parsing_string(self, content: StringIO):
        transform = TreeToJson()

        # file is an UploadFile aka File
        content = turtle_terse(rdf_content=content.read())

        tree = self.parser.parse(content)
        transform.transform(tree)

        # Serializing json payload
        result = list()
        result.append(transform.get_catalogue())
        result.append(transform.get_dataset())
        [result.append(x.get()) for x in transform.get_dimensions()]
        [result.append(x.get()) for x in transform.get_attributes()]
        [result.append(x.get()) for x in transform.get_conceptSchemas()]
        [result.append(x.get()) for x in transform.get_conceptLists()]

        json_object = dumps(result, indent=4, ensure_ascii=False)

        with open("final.jsonld", "w") as outfile:
            outfile.write(json_object)

        return json_object
