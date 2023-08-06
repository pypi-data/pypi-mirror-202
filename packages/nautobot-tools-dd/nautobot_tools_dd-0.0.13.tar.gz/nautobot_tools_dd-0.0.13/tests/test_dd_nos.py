import os
import pdb
from pathlib import Path

from nautobot.utilities.testing import TestCase
from nautobot.dcim.models import Device, Site, DeviceRole, DeviceType, Manufacturer
from nautobot.extras.models import StatusModel, Status
from rest_framework import serializers
from yangson import DataModel
from yangson.datatype import Decimal64Type

from manage import NAUTOBOT_ROOT
from nautobot_tools.serializers import YANGModelSerializer
from nautobot_tools.utils import get_model


class NOSTestCase(TestCase):
    def test_yangson_debug(self):
        model = get_model(
            'tests/example_files/ex2', 'yang-library-ex2.json',
            (".", "../yang-modules/ietf")
        )
        # temporary playground here
        t = model.children[0].children[2].type
        self.assertTrue(isinstance(t, Decimal64Type))

    def prepare_manufacturer_data(self):
        # manufacturer
        manufacturer_data = {
            "name": "Cisco",
            "slug": "cisco"
        }
        return Manufacturer.objects.create(**manufacturer_data)

    def prepare_device_type_data(self):
        manufacturer_object = self.prepare_manufacturer_data()
        # device type
        device_type_data = {
            "manufacturer": manufacturer_object,
            "model": "Catalyst 4500",
            "slug": "catalyst-4500",
            "u_height": 10,
            "is_full_depth": True
        }
        return DeviceType.objects.create(**device_type_data)

    def prepare_device_role_data(self):
        # device role
        device_role_data = {
            "name": "Access",
            "slug": "access",
            "color": "c0c0c0",
            "vm_role": False
        }
        return DeviceRole.objects.create(**device_role_data)

    def prepare_status_data(self):
        # status
        return Status.objects.first()

    def prepare_site_data(self):
        status_object = self.prepare_status_data()
        # site
        site_data = {
            "status": status_object,
            "name": "Cisco DK Lab",
            "slug": "cisco-dk-lab",
        }
        return Site.objects.create(**site_data)

    def prepare_device(self, device_data):
        device = Device.objects.create(**device_data)
        self.assertTrue(
            Device.objects.filter(**device_data).exists()
        )
        return device

    def test_nautobot_object_scanner_yang_ref(self):
        # ===== initial data =====
        device_role_object = self.prepare_device_role_data()
        device_type_object = self.prepare_device_type_data()
        status_object = self.prepare_status_data()
        site_object = self.prepare_site_data()

        device_data = {
            "name": "c4500",
            "device_role": device_role_object,
            "device_type": device_type_object,
            "site": site_object,
            "status": status_object,
        }
        device = self.prepare_device(device_data)

        device2_data = {
            **device_data,
            "name": "IOSXR-1"
        }
        device2 = self.prepare_device(device2_data)

        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                model = get_model(
                    (Path(__file__).resolve().parent / 'example_files/nautobot_ref/').as_posix(),
                    '/yang-library.json'
                )
                fields = '__all__'

        # ===== test =====
        data = {
            'nautobot-ref:device': device.id,
            'nautobot-ref:device2': device2.id,
        }
        example_serializer = ExampleSerializer(data=data)
        example_serializer.is_valid(raise_exception=True)

        self.assertEqual(
            example_serializer.validated_data['nautobot-ref:device'].name,
            device_data['name']
        )
        self.assertEqual(
            example_serializer.validated_data['nautobot-ref:device2'].name,
            device2_data['name']
        )

    def test_nautobot_object_scanner_yang_ref_with_action(self):
        # ===== initial data =====
        device_role_object = self.prepare_device_role_data()
        device_type_object = self.prepare_device_type_data()
        status_object = self.prepare_status_data()
        site_object = self.prepare_site_data()

        device_data = {
            "name": "c4500",
            "device_role": device_role_object,
            "device_type": device_type_object,
            "site": site_object,
            "status": status_object,
        }
        device = self.prepare_device(device_data)

        device2_data = {
            **device_data,
            "name": "IOSXR-1"
        }
        device2 = self.prepare_device(device2_data)

        class ExampleSerializer(YANGModelSerializer):
            class Meta:
                model = get_model(
                    (Path(__file__).resolve().parent / 'example_files/nautobot_ref_rpc/').as_posix(),
                    '/yang-library.json'
                )
                fields = '__all__'

            def run(self, validated_data):
                device_obj: Device = validated_data['nautobot-ref:device-name-update-rpc'][
                    'nautobot-ref:input']['device']
                device_obj.name = validated_data['nautobot-ref:device-name-update-rpc'][
                    'nautobot-ref:input']['name']
                device_obj.save()

                device_obj: Device = validated_data['nautobot-ref:device-name-update']['device']
                device_obj.name = validated_data['nautobot-ref:device-name-update']['name']
                device_obj.save()

                return validated_data

        # ===== test =====
        data = {
            'nautobot-ref:device-name-update-rpc': {
                'nautobot-ref:input': {
                    'device': device.id,
                    'name': device_data['name'] + "_updated",
                }
            },
            'nautobot-ref:device-name-update': {
                'device': device2.id,
                'name': device2_data['name'] + "_updated",
            }
        }
        example_serializer = ExampleSerializer(data=data)
        example_serializer.is_valid(raise_exception=True)
        self.assertEqual(
            example_serializer.validated_data['nautobot-ref:device-name-update-rpc']
            ['nautobot-ref:input']['device'].name,
            device_data['name']
        )
        self.assertEqual(
            example_serializer.validated_data['nautobot-ref:device-name-update']['device'].name,
            device2_data['name']
        )

        example_serializer.save()

        self.assertEqual(
            example_serializer.validated_data['nautobot-ref:device-name-update-rpc']
            ['nautobot-ref:input']['device'].name,
            data['nautobot-ref:device-name-update-rpc']['nautobot-ref:input']['name']
        )
        self.assertEqual(
            example_serializer.validated_data['nautobot-ref:device-name-update']['device'].name,
            data['nautobot-ref:device-name-update']['name']
        )
