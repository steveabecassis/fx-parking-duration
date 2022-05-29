import os
import unittest
import json
from unittest.mock import patch
from extractor.DX_ParkingDuration import DX_ParkingDuration
from extractor.extractor import ParkingDurationExtractor
from beehive_infra.common.ErrorHandler import ErrorCodes, ErrorHandler
from beehive_infra.common.common_constants import *

class TestPreBuild(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up test suite...')
        os.environ['SERVICE_DATA_BUCKET'] = "barmoach-ocr-production"
        os.environ['SERVICE_DATA_ROOT_FOLDER'] = "NexusData"
        os.environ['ROOT_LOG_LEVEL'] = "DEBUG"
        os.environ['USE_REDIS_CACHE'] = "False"
        os.environ['USE_DATADOG'] = "False"
        os.environ['MODE'] = "local"
        cls.extractor = DX_ParkingDuration()
        cls.worker = ParkingDurationExtractor(extractor=cls.extractor)

    @staticmethod
    def is_nexus_compliant(response: dict):
        try:
            serialized_output = json.dumps(response)
        except Exception as err:
            print(err)
            return False
        if 'NaN' in serialized_output:
            return False

        return True

    def test_example_test(self):
        """
        This is a worker test example. You can modify/base your unit tests on it.
        """
        payload = '{"imaginaryId": "61018a6d36000027539a9b59", "step": "DataExtraction1"}'  # Insert the id of the asset you would like to test against
        response, results, extractor_error_code = self.worker.manual_cycle(payload) # simulate running the worker
        print(results)
        self.assertTrue(extractor_error_code is None) # use to verify the worker had no errors
        self.assertTrue(results['conclusion'])  # use to verify the extractor returned some conclusion
        self.assertTrue(self.is_nexus_compliant(response), 'Response is not Nexus compliant!') # Always include this line to verify your extractor's response is valid!

    @classmethod
    def tearDownClass(cls) -> None:
        print('Terminating test suite...')
