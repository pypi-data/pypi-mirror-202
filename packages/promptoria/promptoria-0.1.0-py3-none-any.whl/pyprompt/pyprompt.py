#!/usr/bin/env python3
import os
import json
import sys
import openai
from pprint import pprint,pformat

__version__ = '0.1.0'

# This script is meant to be imported and used as a module.
# It is not supposed to be called directly.
# If you want to use it, import it in your code and call the functions you need.

# First, we need a __init__ function that will set the API key, among other defaults.

# Example usage by user:
# from pyprompt import gptPrompt
# arrayGpt = gptPrompt(lang='Spanish', temperature=0.6, max_tokens='100', return_as='array')
# for element in arrayGpt('most used programming languages in the world'):
#     print(element)

class gptPrompt:
    VALID_RETURN_AS = ['string', 'list', 'dict', 'json']
    def __init__(self, lang=None, temperature=0.5, max_tokens=1024, return_as='string', openai_key=None, n=None, debug=False):
        self.debug = debug
        self.lang = lang
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.return_as = return_as
        if openai_key is None:
            openai_key = os.environ['OPENAI_API_KEY']
        openai.api_key = openai_key

        if lang is not None:
            lang_prompt = f'Respond in {lang}.'
        else:
            lang_prompt = ''

        if n is not None:
            n_prompt = f'Limit the result to {n} first-order items.'
        else:
            n_prompt = ''

        if return_as == 'string':
            return_as_prompt = ''
        elif return_as == 'list':
            return_as_prompt = 'Reply one JSON string list. '
        elif return_as == 'dict':
            return_as_prompt = 'Reply one JSON string dictionary.'
        elif return_as == 'json':            
            return_as_prompt = "Response format: JSON string. Response string object must represent JSON."
        else:
            raise ValueError(f"return_as must be one of {gptPrompt.VALID_RETURN_AS}. Defaults to 'string'.")

        self.prompt_extras = f"- MUST ALWAYS: {lang_prompt} {return_as_prompt} {n_prompt}"
        if self.debug:
            print(f'[DEBUG] prompt_extras = "{self.prompt_extras}"',file=sys.stderr)

    def rungpt(self, final_prompt):
        if self.debug:
            print(f'[DEBUG] final_prompt = "{final_prompt}"',file=sys.stderr)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=final_prompt,
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=self.temperature,)
        raw_response = response.choices[0].text.strip()
        if self.debug:
            print(f'[DEBUG] raw_response:\n{raw_response}\n[DEBUG] --- END raw_response ---\n',file=sys.stderr)
        return(raw_response)

    def __call__(self, prompt):
        ret = self.rungpt(f"{prompt} {self.prompt_extras}").strip()
        if self.return_as == 'string':
            retObj = ret
        if self.return_as == 'list' or self.return_as == 'dict' or self.return_as == 'json':
            retObj = json.loads(ret.replace('\n',''))
        if self.debug:
            print('[DEBUG] json.loads(ret) result:',file=sys.stderr)
            print(pformat(retObj),file=sys.stderr)
            print('[DEBUG] END json.loads(ret) result.',file=sys.stderr)
        return(retObj)






if __name__ == '__main__':
    print('pyprompt.py is not supposed to be called directly. use import pyprompt in your code. cheers, Buanzo.', file=sys.stderr)
