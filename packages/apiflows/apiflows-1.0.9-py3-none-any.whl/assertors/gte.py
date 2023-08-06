#!/bin/env python3

import logging
from utils import extract_from_jsonpath, parse_dict_with_extracts
from colorama import init, Fore, Back, Style

def assert_gte(config, apicase, assertion, json_obj):
    key = assertion.get('in', 'body')
    exp1 = extract_from_jsonpath(parse_dict_with_extracts(config, assertion['exp1']), json_obj, key)
    exp2 = extract_from_jsonpath(parse_dict_with_extracts(config, assertion['exp2']), json_obj, key)

    result = False
    if exp1 >= exp2:
        result = True
    
    assertion['result'] = result
    return (result, exp1, exp2)