import os
import unittest
import json
from dummy_extractor.DX_DummyExtractor import DX_DummyExtractor
from dummy_extractor.rest_extractor import app
from fastapi.testclient import TestClient
from dummy_extractor.extractor import DummyExtractor


class TestPreBuild(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print('Setting up test suite...')
        os.environ['SERVICE_DATA_BUCKET'] = "barmoach-ocr-production"
        # os.environ['SERVICE_DATA_BUCKET'] = "vatbox-deploy-env-stag-env-ds-env"
        os.environ['SERVICE_DATA_ROOT_FOLDER'] = "NexusData"
        os.environ['ROOT_LOG_LEVEL'] = "DEBUG"
        os.environ['USE_REDIS_CACHE'] = "False"
        os.environ['MODE'] = "local"
        cls.client = TestClient(app)

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

    # make sure to modify request body to accomodate expected structure by the extractor
    def test_worker_basic_scenario(self):
        request_body = {"GoogleOcrDataFormatted": {"text": ['hello', 'world'], "bboxes": {'x': 1, 'y': 2, 'height': 3, 'width': 4}}, "imaginary_id": "mock-imaginary-id"}
        response = self.client.post('/extract', json=request_body)
        print(f'Status code is: {response.status_code}')
        print(f'Response body is: {response.json()}')
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json() is not None and response.json()['conclusion'] == 'dummy_conclusion')

    @classmethod
    def tearDownClass(cls) -> None:
        print('Terminating test suite...')
