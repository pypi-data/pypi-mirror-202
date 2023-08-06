import os
from pathlib import Path

from django.test import TestCase
from rest_framework import serializers
from yangson import DataModel
from yangson.datatype import Decimal64Type

from nautobot_tools.serializers import YANGModelSerializer
from utils import get_model


class DiscoverYANGFilesDirectory(TestCase):
    TESTS_PATH = Path(__file__).resolve().parent

    def test_discover_yang_module_by_default(self):
        from django.template.loader import get_template
        get_template

        # ===== initial data =====
        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                yang_library = 'yang-library-ex1.json'
                model = get_model('tests/example_files/ex1', 'yang-library-ex1.json')
                fields = '__all__'

        # ===== test =====
        example_serializer = ExampleSerializer(data={})
        example_serializer.is_valid(raise_exception=True)

        self.assertEqual(example_serializer.validated_data['example-1:greeting'], "Hello, world!")
        self.assertIn("show_me", example_serializer.validated_data)
        self.assertTrue(example_serializer.validated_data['show_me'])
