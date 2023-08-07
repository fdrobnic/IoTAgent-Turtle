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
from lark.exceptions import UnexpectedEOF as LarkUnexpectedEOF
from lark.exceptions import UnexpectedInput as LarkUnexpectedInput
from lark.exceptions import UnexpectedToken as LarkUnexpectedToken


class UnexpectedEOF(LarkUnexpectedEOF):
    def __init__(self, expected, state=None, terminals_by_name=None):
        super(LarkUnexpectedEOF, self).__init__(expected=expected, state=state, terminals_by_name=terminals_by_name)


class UnexpectedInput(LarkUnexpectedInput):
    def __init__(self):
        super(LarkUnexpectedInput, self).__init__()


class UnexpectedToken(LarkUnexpectedToken):
    def __init__(
        self,
        token,
        expected,
        considered_rules=None,
        state=None,
        interactive_parser=None,
        terminals_by_name=None,
        token_history=None,
    ):
        super(LarkUnexpectedToken, self).__init__(
            token=token,
            expected=expected,
            considered_rules=considered_rules,
            state=state,
            interactive_parser=interactive_parser,
            terminals_by_name=terminals_by_name,
            token_history=token_history,
        )
