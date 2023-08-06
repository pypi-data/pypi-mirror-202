import os
import sys
from pprint import pprint
# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from promptoria import gptPrompt

class TestGptPrompt(unittest.TestCase):
    def test_return_as_string(self):
        print('\033[1;33m---------[ test_return_as_string ]--------------\033[0;37m\n')
        gpt = gptPrompt(lang='spanish', temperature=0.7, max_tokens=1024, return_as='string', debug=True)
        prompt = "What is the name of Argentina's most beloved author?"
        response = gpt(prompt)
        self.assertIsInstance(response, str)

    def test_return_as_list(self):
        print('\033[1;33m---------[ test_return_as_list ]--------------\033[0;37m\n')
        gpt = gptPrompt(lang='spanish', temperature=0.7, max_tokens=1024, return_as='list', debug=True)
        prompt = 'Give me a list of animals.'
        response = gpt(prompt)
        pprint(response)
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 0)

    def test_return_as_list_five_items(self):
        print('\033[1;33m---------[ test_return_as_list_five_items ]--------------\033[0;37m\n')
        gpt = gptPrompt(lang='spanish', temperature=0.7, max_tokens=1024, return_as='list', n=5, debug=True)
        prompt = 'Give me a list of cat names created by combining a Vulcan name with a Klingon name'
        response = gpt(prompt)
        pprint(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 5)

    def test_return_as_dict(self):
        print('\033[1;33m---------[ test_return_as_dict ]--------------\033[0;37m\n')
        gpt = gptPrompt(lang='spanish', temperature=0.7, max_tokens=1024, return_as='dict', debug=True)
        prompt = 'Capital cities of the world. Group by continent.'
        response = gpt(prompt)
        self.assertIsInstance(response, dict)
        self.assertGreater(len(response), 0)

if __name__ == '__main__':
    unittest.main()
