# Turn the black formatter off for this file to avoid long lists of numbers
# being extended to one-line-per-element
# fmt: off

# Turn off pylint warnings unavoidable with pytest
# pylint: disable=missing-module-docstring, redefined-outer-name, missing-function-docstring, line-too-long

import copy
import json
import os
import pytest


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def loaded_schema():
    """Load the schema only once per test session for speed"""
    with open(os.path.join(ROOT_DIR, "power-curve-schema/schema.json"), 'r', encoding="utf-8") as fp:
        loaded = json.load(fp)
    return loaded


@pytest.fixture()
def schema(loaded_schema):
    """A fresh deep copy of the schema so it can be mutated on a per-test basis"""
    return copy.deepcopy(loaded_schema)



@pytest.fixture()
def generic_document_metadata():
    return {
        "document_metadata": [
            {
                "identifier": "my-uuid",
            },
            {
                "format": "IEC61400-16",
            },
            {
                "source": "Doc 12345 - Rev 01"
            }
        ]
    }


@pytest.fixture()
def generic_design_basis():
    return {
        "design_basis": {
        }
    }

@pytest.fixture()
def one_dimensional_mode():
    return {
        "label": "one-dimensional",
        "description": "A typical mode where there are values for only the reference air density. In practicality this is the same as a two-dimensional example, just with a single air density value.",
        "cut": {
            "type": "in_out_re",
            "value": [3, 25, 23]
        },
        "parameters": [
            {
                "label": "air-density",
                "dimension": 0,
                "points": [1.225]
            },
            {
                "label": "wind-speed",
                "dimension": 1,
                "points": [
                    3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0,9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5,15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0,20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0
                ]
            }
        ],
        "cp_is_coefficient": False,
        "ct_is_coefficient": True,
        "cp": [
            [22000.0, 78000.0, 150000.0, 237000.0, 340000.0, 466000.0, 617000.0, 796000.0, 1006000.0, 1247000.0, 1522000.0, 1871000.0, 2178000.0, 2544000.0, 2905000.0, 3201000.0, 3374000.0, 3435000.0, 3448000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0, 3450000.0,3450000.0, 3450000.0]
        ],
        "ct": [
            [0.873, 0.849, 0.834, 0.828, 0.827, 0.825, 0.82, 0.816, 0.805, 0.804, 0.794, 0.79, 0.789, 0.772, 0.733, 0.666, 0.58, 0.494, 0.421, 0.362, 0.316, 0.281, 0.249, 0.223, 0.199, 0.18, 0.164, 0.149, 0.137, 0.125, 0.115, 0.107, 0.098, 0.091, 0.085, 0.079, 0.074, 0.07, 0.066, 0.062, 0.058, 0.055, 0.052, 0.049, 0.046]
        ]
    }


@pytest.fixture()
def two_dimensional_mode():
   return  {
        "label": "two-dimensional",
        "description": "A typical mode where both air density and wind speed vary",
        "cut": {
            "type": "in_out_re",
            "value": [3, 30, 30]
        },
        "parameters": [
            {
                "label": "air-density",
                "dimension": 0,
                "points": [1.1, 1.125, 1.15, 1.175, 1.2, 1.225, 1.25, 1.275]
            },
            {
                "label": "wind-speed",
                "dimension": 1,
                "points": [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0]
            }
        ],
        "cp_is_coefficient": False,
        "ct_is_coefficient": True,
        "cp": [
            [
            76000.0, 310666.667, 641333.333, 1073333.3299999998,
            1601333.3299999998, 2228000.0, 2972000.0, 3850666.67, 4892000.0,
            6081333.33, 7434666.67, 8954666.67, 10645333.3, 12428000.0,
            14332000.0, 16380000.0, 18324000.0, 19516000.0, 19926666.700000003,
            19993333.299999997, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 19940000.0, 19340000.0, 17600000.0,
            15476000.0, 14133333.3, 13540000.0, 13406666.7, 13350666.7,
            13185333.3, 12926666.7, 12677333.3, 12516000.0, 12432000.0, 12402666.7
            ],
            [
            80000.0, 321333.333, 660000.0, 1101333.3299999998, 1642666.6700000002,
            2284000.0, 3045333.33, 3944000.0, 5009333.33, 6224000.0, 7606666.67,
            9158666.67, 10881333.3, 12698666.7, 14633333.3, 16632000.0,
            18585333.299999997, 19628000.0, 19950666.700000003, 19996000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 19952000.0, 19432000.0, 17752000.0, 15592000.0,
            14178666.7, 13552000.0, 13409333.3, 13354666.7, 13190666.7,
            12937333.3, 12684000.0, 12520000.0, 12434666.7, 12404000.0
            ],
            [
            84000.0, 333333.333, 678666.667, 1130666.6700000002, 1684000.0,
            2341333.33, 3117333.33, 4037333.33, 5125333.33, 6368000.0, 7778666.67,
            9362666.67, 11117333.3, 12969333.3, 14933333.3, 16882666.700000003,
            18849333.299999997, 19740000.0, 19976000.0, 19997333.299999997,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 19964000.0, 19524000.0, 17904000.0, 15709333.3,
            14224000.0, 13564000.0, 13410666.7, 13357333.3, 13197333.3,
            12946666.7, 12690666.7, 12522666.7, 12436000.0, 12404000.0
            ],
            [
            89333.33330000001, 344000.0, 697333.333, 1160000.0,
            1725333.3299999998, 2397333.33, 3190666.67, 4130666.6699999995,
            5241333.33, 6509333.33, 7949333.33, 9564000.0, 11352000.0, 13237333.3,
            15221333.3, 17165333.299999997, 19005333.299999997,
            19797333.299999997, 19982666.700000003, 19998666.700000003,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 19970666.700000003, 19590666.700000003,
            18054666.700000003, 15830666.7, 14270666.7, 13576000.0, 13412000.0,
            13360000.0, 13202666.7, 12954666.7, 12696000.0, 12526666.7,
            12437333.3, 12404000.0
            ],
            [
            94666.66669999999, 354666.667, 717333.333, 1189333.3299999998,
            1766666.6700000002, 2453333.33, 3264000.0, 4225333.33, 5358666.67,
            6650666.67, 8120000.0, 9765333.33, 11586666.7, 13505333.3, 15512000.0,
            17450666.700000003, 19162666.700000003, 19854666.700000003,
            19989333.299999997, 19998666.700000003, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 19977333.299999997,
            19657333.299999997, 18204000.0, 15952000.0, 14317333.3, 13586666.7,
            13412000.0, 13362666.7, 13209333.3, 12961333.3, 12702666.7,
            12529333.3, 12438666.7, 12405333.3
            ],
            [
            98666.66669999999, 365333.333, 736000.0, 1218666.6700000002,
            1808000.0, 2509333.33, 3336000.0, 4318666.67, 5474666.67, 6793333.33,
            8290666.670000001, 9968000.0, 11821333.3, 13773333.3, 15800000.0,
            17733333.299999997, 19320000.0, 19910666.700000003, 19996000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 19984000.0, 19724000.0, 18353333.299999997,
            16073333.3, 14364000.0, 13597333.3, 13413333.3, 13365333.3,
            13216000.0, 12969333.3, 12709333.3, 12533333.3, 12441333.3, 12405333.3
            ],
            [
            104000.0, 377333.333, 754666.667, 1248000.0, 1850666.6700000002,
            2565333.33, 3409333.33, 4412000.0, 5590666.67, 6934666.67, 8460000.0,
            10166666.7, 12052000.0, 14037333.3, 16073333.3, 18026666.700000003,
            19426666.700000003, 19934666.700000003, 19997333.299999997,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 19989333.299999997, 19770666.700000003,
            18498666.700000003, 16196000.0, 14412000.0, 13616000.0, 13416000.0,
            13368000.0, 13220000.0, 12977333.3, 12714666.7, 12537333.3,
            12442666.7, 12405333.3
            ],
            [
            109333.333, 388000.0, 773333.333, 1277333.3299999998, 1892000.0,
            2621333.33, 3482666.67, 4505333.33, 5708000.0, 7074666.67, 8628000.0,
            10365333.3, 12282666.7, 14300000.0, 16346666.7, 18320000.0,
            19533333.299999997, 19957333.299999997, 19997333.299999997,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 20000000.0, 20000000.0, 20000000.0,
            20000000.0, 20000000.0, 19993333.299999997, 19817333.299999997,
            18644000.0, 16317333.3, 14460000.0, 13636000.0, 13417333.3,
            13370666.7, 13225333.3, 12986666.7, 12718666.7, 12541333.3,
            12445333.3, 12406666.7
            ]
        ],
        "ct": [
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.805, 0.804, 0.802, 0.8,
            0.796, 0.792, 0.786, 0.781, 0.771, 0.731, 0.674, 0.594, 0.508, 0.435,
            0.377, 0.332, 0.294, 0.262, 0.235, 0.212, 0.192, 0.175, 0.16, 0.147,
            0.135, 0.125, 0.115, 0.106, 0.099, 0.092, 0.086, 0.08, 0.075, 0.07,
            0.067, 0.062, 0.057, 0.049, 0.041, 0.035, 0.032, 0.03, 0.029, 0.027,
            0.025, 0.024, 0.022, 0.021, 0.02
            ],
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.805, 0.804, 0.802, 0.799,
            0.796, 0.791, 0.785, 0.78, 0.768, 0.72, 0.664, 0.58, 0.495, 0.424,
            0.368, 0.324, 0.287, 0.256, 0.23, 0.208, 0.188, 0.171, 0.156, 0.144,
            0.132, 0.122, 0.112, 0.104, 0.097, 0.09, 0.084, 0.079, 0.074, 0.069,
            0.065, 0.061, 0.056, 0.048, 0.04, 0.035, 0.032, 0.03, 0.028, 0.027,
            0.025, 0.023, 0.022, 0.021, 0.02
            ],
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.804, 0.804, 0.802, 0.799,
            0.795, 0.79, 0.784, 0.778, 0.765, 0.71, 0.654, 0.566, 0.481, 0.412,
            0.359, 0.316, 0.281, 0.251, 0.225, 0.203, 0.184, 0.168, 0.153, 0.141,
            0.13, 0.12, 0.11, 0.102, 0.095, 0.088, 0.083, 0.077, 0.072, 0.068,
            0.064, 0.06, 0.055, 0.048, 0.04, 0.034, 0.031, 0.029, 0.028, 0.026,
            0.025, 0.023, 0.022, 0.021, 0.02
            ],
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.804, 0.804, 0.801, 0.798,
            0.794, 0.789, 0.783, 0.777, 0.76, 0.703, 0.64, 0.552, 0.469, 0.403,
            0.351, 0.31, 0.275, 0.245, 0.22, 0.199, 0.181, 0.164, 0.15, 0.138,
            0.127, 0.117, 0.108, 0.1, 0.093, 0.087, 0.081, 0.076, 0.071, 0.067,
            0.063, 0.059, 0.055, 0.048, 0.039, 0.034, 0.031, 0.029, 0.027, 0.026,
            0.024, 0.023, 0.021, 0.02, 0.019
            ],
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.804, 0.803, 0.801, 0.798,
            0.793, 0.788, 0.782, 0.775, 0.756, 0.696, 0.626, 0.538, 0.457, 0.393,
            0.343, 0.303, 0.269, 0.24, 0.216, 0.195, 0.177, 0.161, 0.147, 0.136,
            0.125, 0.115, 0.106, 0.098, 0.092, 0.085, 0.08, 0.075, 0.07, 0.066,
            0.062, 0.058, 0.054, 0.047, 0.039, 0.033, 0.03, 0.028, 0.027, 0.025,
            0.024, 0.022, 0.021, 0.02, 0.019
            ],
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.804, 0.803, 0.801, 0.797,
            0.793, 0.787, 0.78, 0.773, 0.751, 0.688, 0.613, 0.524, 0.445, 0.383,
            0.335, 0.296, 0.263, 0.235, 0.211, 0.191, 0.173, 0.158, 0.144, 0.133,
            0.122, 0.113, 0.104, 0.097, 0.09, 0.084, 0.078, 0.073, 0.069, 0.064,
            0.061, 0.057, 0.053, 0.047, 0.039, 0.033, 0.03, 0.028, 0.026, 0.025,
            0.023, 0.022, 0.021, 0.02, 0.019
            ],
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.804, 0.803, 0.8, 0.797,
            0.792, 0.786, 0.779, 0.771, 0.745, 0.682, 0.599, 0.511, 0.435, 0.375,
            0.328, 0.29, 0.258, 0.231, 0.207, 0.187, 0.17, 0.155, 0.142, 0.131,
            0.12, 0.111, 0.102, 0.095, 0.088, 0.082, 0.077, 0.072, 0.067, 0.063,
            0.06, 0.056, 0.052, 0.046, 0.038, 0.032, 0.029, 0.027, 0.026, 0.024,
            0.023, 0.021, 0.02, 0.019, 0.018
            ],
            [
            0.817, 0.815, 0.813, 0.812, 0.809, 0.807, 0.803, 0.802, 0.8, 0.796,
            0.791, 0.784, 0.778, 0.769, 0.739, 0.676, 0.586, 0.499, 0.424, 0.367,
            0.321, 0.284, 0.253, 0.226, 0.203, 0.184, 0.167, 0.152, 0.139, 0.128,
            0.118, 0.109, 0.101, 0.093, 0.087, 0.081, 0.076, 0.071, 0.066, 0.062,
            0.059, 0.055, 0.052, 0.046, 0.038, 0.032, 0.029, 0.027, 0.025, 0.024,
            0.023, 0.021, 0.02, 0.019, 0.018
            ]
      ]
    }


@pytest.fixture(scope="session")
def loaded_generic_117_3():
    """Provides the generic 117m 3.45MW turbine as a test instance, loaded from disc only once per session
    NOTE: Do not use this fixture directly, to avoid mutation of fixtures for other tests.
    Instead, use a deep copy of this fixture (to accelerate tests copmared to loading from disc on each test).
    """

    with open(os.path.join(ROOT_DIR, "power-curve-schema", "examples", "generic-117-3.json"), 'r', encoding="utf-8") as fp:
        instance = json.load(fp)
    return instance

@pytest.fixture()
def generic_117_3(loaded_generic_117_3):
    """A fresh deep copy of the generic 117m 3.45MW turbine as a test instance"""
    return copy.deepcopy(loaded_generic_117_3)


@pytest.fixture(scope="session")
def loaded_generic_274_20():
    """Provides the generic 274m 20MW turbine as a test instance, loaded from disc only once per session
    NOTE: Do not use this fixture directly, to avoid mutation of fixtures for other tests.
    Instead, use a deep copy of this fixture (to accelerate tests copmared to loading from disc on each test).
    """
    with open(os.path.join(ROOT_DIR, "power-curve-schema", "examples", "generic-274-20.json"), 'r', encoding="utf-8") as fp:
        instance = json.load(fp)
    return instance

@pytest.fixture()
def generic_274_20(loaded_generic_274_20):
    """A fresh deep copy of the generic 274m 20MW turbine as a test instance"""
    return copy.deepcopy(loaded_generic_274_20)


@pytest.fixture()
def generic_turbine_metadata(generic_117_3):
    return {
        "turbine_metadata": generic_117_3.pop('turbine_metadata')
    }
