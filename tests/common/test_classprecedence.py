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
from sdmx2jsonld.common.classprecedence import (
    Precedence,
    ClassPrecedencePropertyError,
    ClassPrecedenceClassError,
)


class Test(TestCase):
    def setUp(self):
        self.pre = Precedence()

    def test_precedence_one_class(self):
        """
        The precedence of one Class will be ALWAYS that Class
        """
        obtained = self.pre.precedence(["qb:DataStructureDefinition"])
        expected = "qb:DataStructureDefinition"
        assert obtained == expected, f"'qb:DataStructureDefinition' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["skos:Concept"])
        expected = "skos:Concept"
        assert obtained == expected, f"'skos:Concept' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["qb:SliceKey"])
        expected = "qb:SliceKey"
        assert obtained == expected, f"'qb:SliceKey' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["qb:DimensionProperty"])
        expected = "qb:DimensionProperty"
        assert obtained == expected, f"'qb:DimensionProperty' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["qb:AttributeProperty"])
        expected = "qb:AttributeProperty"
        assert obtained == expected, f"'qb:AttributeProperty' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["skos:ConceptScheme"])
        expected = "skos:ConceptScheme"
        assert obtained == expected, f"'skos:ConceptScheme' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["owl:Class"])
        expected = "owl:Class"
        assert obtained == expected, f"'owl:Class' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["qb:ComponentSpecification"])
        expected = "qb:ComponentSpecification"
        assert obtained == expected, f"'qb:ComponentSpecification' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["qb:MeasureProperty"])
        expected = "qb:MeasureProperty"
        assert obtained == expected, f"'qb:MeasureProperty' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["skos:ConceptScheme"])
        expected = "skos:ConceptScheme"
        assert obtained == expected, f"'skos:ConceptScheme' expected, got: '{obtained}'"

    def test_precedence_classes_with_dimension_and_attribute_values(self):
        """
        Currently the classes with the same value are:
                1) "qb:DimensionProperty", "qb:AttributeProperty", "qb:MeasureProperty" (it is not expected to have
                different from this, therefore we should return an error)
                2) "rdfs:Class", "owl:Class"
        """
        with self.assertRaises(ClassPrecedencePropertyError) as error:
            _ = self.pre.precedence(["qb:DimensionProperty", "qb:AttributeProperty"])

        self.assertEqual(
            str(error.exception),
            "['qb:DimensionProperty', 'qb:AttributeProperty'] -> Incompatible multiclass definition",
        )

    def test_precedence_classes_with_attribute_and_measure_values(self):
        with self.assertRaises(ClassPrecedencePropertyError) as error:
            _ = self.pre.precedence(["qb:AttributeProperty", "qb:MeasureProperty"])

        self.assertEqual(
            str(error.exception),
            "['qb:AttributeProperty', 'qb:MeasureProperty'] -> Incompatible multiclass definition",
        )

    def test_precedence_classes_with_dimension_and_measure_values(self):
        with self.assertRaises(ClassPrecedencePropertyError) as error:
            _ = self.pre.precedence(["qb:DimensionProperty", "qb:MeasureProperty"])

        self.assertEqual(
            str(error.exception),
            "['qb:DimensionProperty', 'qb:MeasureProperty'] -> Incompatible multiclass definition",
        )

    def test_precedence_classes_with_class_values(self):
        with self.assertRaises(ClassPrecedenceClassError) as error:
            _ = self.pre.precedence(["rdfs:Class", "owl:Class"])

        self.assertEqual(
            str(error.exception),
            "['rdfs:Class', 'owl:Class'] -> Possible redundant Class definition",
        )

    def test_attribute_and_coded_property(self):
        obtained = self.pre.precedence(["qb:AttributeProperty", "qb:CodedProperty"])
        expected = "qb:AttributeProperty"
        assert obtained == expected, f"'qb:AttributeProperty' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["qb:CodedProperty", "qb:AttributeProperty"])
        expected = "qb:AttributeProperty"
        assert obtained == expected, f"'qb:AttributeProperty' expected, got: '{obtained}'"

    def test_coded_and_dimension_property(self):
        obtained = self.pre.precedence(["qb:CodedProperty", "qb:DimensionProperty"])
        expected = "qb:DimensionProperty"
        assert obtained == expected, f"'qb:DimensionProperty' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["qb:DimensionProperty", "qb:CodedProperty"])
        expected = "qb:DimensionProperty"
        assert obtained == expected, f"'qb:DimensionProperty' expected, got: '{obtained}'"

    def test_concept_and_other_property(self):
        obtained = self.pre.precedence(["skos:Concept", "<http://bauhaus/codes/concept/AjustementSaisonnier>"])
        expected = "skos:Concept"
        assert obtained == expected, f"'skos:Concept' expected, got: '{obtained}'"

        obtained = self.pre.precedence(["<http://bauhaus/codes/concept/HebergementNombresEtoiles>", "skos:Concept"])
        expected = "skos:Concept"
        assert obtained == expected, f"'skos:Concept' expected, got: '{obtained}'"
