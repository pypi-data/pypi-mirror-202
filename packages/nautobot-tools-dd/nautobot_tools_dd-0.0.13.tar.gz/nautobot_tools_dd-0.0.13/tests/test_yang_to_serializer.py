import os
from pathlib import Path

from django.test import TestCase
from rest_framework import serializers
from yangson import DataModel
from yangson.datatype import Decimal64Type

from nautobot_tools.serializers import YANGModelSerializer
from utils import get_model


class SimpleCase(TestCase):
    TESTS_PATH = Path(__file__).resolve().parent

    def test_yangson_debug(self):
        model = get_model(
            (self.TESTS_PATH / 'example_files/ex2').as_posix(), '/yang-library-ex2.json',
            (
                (self.TESTS_PATH / 'example_files/ex2').as_posix(),
                (self.TESTS_PATH / 'example_files/yang-modules/ietf').as_posix()
            )
        )
        # temporary playground here
        t = model.children[0].children[2].type
        self.assertTrue(isinstance(t, Decimal64Type))

    def test_simple_yang_to_serializer_1(self):
        # ===== initial data =====
        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                model = get_model(
                    (self.TESTS_PATH / 'example_files/ex1').as_posix(), '/yang-library-ex1.json'
                )
                fields = '__all__'

        # ===== test =====
        data = {
            "example-1:greeting": "Hi!"
        }
        example_serializer = ExampleSerializer(data=data)
        example_serializer.is_valid(raise_exception=True)

        self.assertEqual(example_serializer.validated_data['example-1:greeting'], "Hi!")

    def test_simple_yang_to_serializer_2(self):
        # ===== initial data =====
        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                model = get_model(
                    'tests/example_files/ex2', 'yang-library-ex2.json',
                    (".", "../yang-modules/ietf")
                )
                fields = '__all__'

        # ===== test =====
        data = {
            "example-2:bag": {
                "foo": [
                    {
                        "number": 6,
                        "in-words": "six"
                    },
                    {
                        "@": {
                            "ietf-origin:origin": "ietf-origin:system"
                        },
                        "number": 3,
                        "prime": True,
                        "in-words": "three"
                    },
                    {
                        "number": 7,
                        "prime": True,
                        "in-words": "seven"
                    },
                    {
                        "number": 8,
                        "in-words": "eight"
                    }
                ],
                "bar": True
            }
        }
        example_serializer = ExampleSerializer(data=data)
        example_serializer.is_valid(raise_exception=True)
        self.assertEqual(example_serializer.validated_data['example-2:bag']['bar'], True)

    def test_simple_yang_to_serializer_3(self):
        # ===== initial data =====
        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                model = get_model(
                    'tests/example_files/ex3', 'yang-library-ex3.json',
                    (".", "../yang-modules/ietf")
                )
                fields = '__all__'

        # ===== test =====
        example_serializer = ExampleSerializer(data={})
        example_serializer.is_valid(raise_exception=False)

    def test_simple_yang_to_serializer_4(self):
        # ===== initial data =====
        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                model = get_model(
                    'tests/example_files/ex4', 'yang-library-ex4.json',
                    (".", "../yang-modules/ietf")
                )
                fields = '__all__'

        # ===== test =====
        data = {
            "example-4-a:bag": {
                "foo": 42,
                "bar": False,
                "example-4-b:fooref": 42
            },
            "example-4-b:quux": [
                "3.1415",
                "0"
            ]
        }
        example_serializer = ExampleSerializer(data=data)
        example_serializer.is_valid(raise_exception=True)
        self.assertEqual(example_serializer.validated_data['example-4-a:bag']['example-4-b:fooref'], '42')

    def test_simple_yang_to_serializer_5(self):
        # ===== initial data =====
        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                model = get_model(
                    'tests/example_files/ex5', 'yang-library-ex5.json'
                )
                fields = '__all__'

        # ===== test =====
        data = {
            "example-5-a:string-leaf": "xuy"
        }
        example_serializer = ExampleSerializer(data=data)
        example_serializer.is_valid(raise_exception=True)
        self.assertEqual(example_serializer.validated_data['example-5-a:string-leaf'], 'xuy')

    def test_simple_yang_to_serializer_1_customized(self):
        # ===== initial data =====
        class ExampleSerializer(YANGModelSerializer):
            show_me = serializers.BooleanField(default=True)

            class Meta:
                model = get_model('tests/example_files/ex1', 'yang-library-ex1.json')
                fields = '__all__'

        # ===== test =====
        example_serializer = ExampleSerializer(data={})
        example_serializer.is_valid(raise_exception=True)

        self.assertEqual(example_serializer.validated_data['example-1:greeting'], "Hello, world!")
        self.assertIn("show_me", example_serializer.validated_data)
        self.assertTrue(example_serializer.validated_data['show_me'])
