#!/bin/env python3

import logging
from utils import extract_from_jsonpath, parse_dict_with_extracts
from colorama import init, Fore, Back, Style
import re

def assert_match(config, apicase, assertion, json_obj):
    key = assertion.get('in', 'body')
    exp1 = extract_from_jsonpath(parse_dict_with_extracts(config, assertion['exp1']), json_obj, key)
    exp2 = parse_dict_with_extracts(config, assertion['exp2'])

    result = False
    if exp1 and re.search(exp2, exp1) != None:
        result = True
    
    assertion['result'] = result
    return (result, exp1, exp2)