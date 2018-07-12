import flaskml
import unittest
import json

from flask import g, session, Response
from flaskml import create_app, medlp
from unittest.mock import patch
import flaskml.medlp as medlp

class FlaskBookshelfTests(unittest.TestCase):

    def setUp(self):
        # creates a test client
        test_config = {'SECRET_KEY':'dev',
                       'TESTING':True,

        }
        self.app = create_app(test_config).test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

        self.INPUT_TEXT = "the quick brown fox jumped over the lazy dog"


    def tearDown(self):
        pass


    def make_json_post_to_endpoint(self, endpoint, dict_to_jsonify):
        return self.app.post(endpoint,
                               data=json.dumps(dict_to_jsonify),
                               content_type='application/json'
                               )


    def test_annotate_no_entity_text(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.post('/medlp/annotate/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 400)


    def test_annotate_empty_entity_text(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.make_json_post_to_endpoint('/medlp/annotate/',
                                                 dict())

        # assert the status code of the response
        self.assertEqual(result.status_code, 400)


    @patch('flaskml.medlpInterface.get_entities')
    def test_get_entities_happy_case(self, mockMedLPInterface):

        entity_response_json = [{'fox': 'PHI'}, {'dog': 'PHI'}]
        mockMedLPInterface.return_value = entity_response_json
        expected_result = Response(entity_response_json, mimetype=u'application/json')
        result = medlp._get_entities(self.INPUT_TEXT, entityTypes="all")

        mockMedLPInterface.assert_called_with(self.INPUT_TEXT, entityTypes="all")



    @patch('flaskml.medlpInterface.get_entities')
    def test_annotate_no_specified_types(self, mockMedLPInterface):
        entity_response_json = [{'fox': 'PHI'}, {'dog': 'PHI'}]
        mockMedLPInterface.return_value = entity_response_json

        result = self.make_json_post_to_endpoint('/medlp/annotate/',
                                                 dict(extract_text=self.INPUT_TEXT))


        mockMedLPInterface.assert_called_with(self.INPUT_TEXT)


if __name__ == '__main__':
    unittest.main()