import unittest
from practice.从入门到实践.test.language import AnonymousSurvey

class TestAnonmyousSurvey(unittest.TestCase):

    def test_score_single_response(self):
        question = "What language did you first learn to speak?"

        my_survey = AnonymousSurvey(question)
        responses = ['English', 'Spanish', 'Mandarin']
        for response in responses:
            my_survey.store_response(response)
        for response in responses:
             self.assertIn(response, my_survey.responses)

unittest.main()
