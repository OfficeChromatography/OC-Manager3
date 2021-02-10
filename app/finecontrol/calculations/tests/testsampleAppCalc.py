from decimal import Decimal
from unittest import TestCase
from ..sampleAppCalc import *


class TestSampleApp(TestCase):
    def setUp(self) -> None:
        self.data = {'size_x': Decimal('100'),
                     'size_y': Decimal('100'),
                     'offset_left': Decimal('1'),
                     'offset_right': Decimal('1'),
                     'offset_top': Decimal('1'),
                     'offset_bottom': Decimal('1'),
                     'main_property': Decimal('1'),
                     'value': Decimal('2'),
                     'height': Decimal('0'),
                     'gap': Decimal('4'),
                     'motor_speed': Decimal('1000'),
                     'delta_x': Decimal('0.75'),
                     'delta_y': Decimal('0.75'),
                     'pressure': Decimal('5'),
                     'frequency': Decimal('1400'),
                     'temperature': Decimal('0'),
                     'nozzlediameter': 'atomizer 67k',
                     'zero_x': Decimal('20'),
                     'zero_y': Decimal('20'),
                     'table': [{'band_number': '1',
                                'description': '',
                                'volume': '1',
                                'type': 'Water',
                                'density': '',
                                'viscosity': '',
                                'estimated_volume': '0.000',
                                'estimated_drop_volume': '0.075',
                                'minimum_volume': '4.797'},

                               {'band_number': '2',
                                'description': '',
                                'volume': '2',
                                'type': 'Water',
                                'density': '',
                                'viscosity': '',
                                'estimated_volume': '0.000',
                                'estimated_drop_volume': '0.075',
                                'minimum_volume': '4.797'}]
                     }

    def tearDown(self) -> None:
        pass

    def test_calculate(self):
        calculate(self.data)
