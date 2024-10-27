

import json
import os
from handlebars import Handlebars


def _run_test(template, data, expected_result, helpers={}):
    for helper_key, helper_func in helpers.items():
        Handlebars.registerHelper(helper_key, helper_func)
    template = Handlebars.compile(template)
    actual = template(data)
    assert actual == expected_result

def _test_helper():
    return "test"

def test_helper():
    _run_test(
        "Name: {{name}}, {{testf}}",
        { "name": "Jane" },
        "Name: Jane, test",
        {"testf": _test_helper}
    )

def test_cases():
    directory = os.path.join(
        os.path.dirname(__file__),
        "test_cases"
    )
        
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            with open(os.path.join(directory, file), "rt") as f:
                cases = json.load(f)
                for case in cases:
                    #print(case[0])
                    _run_test(
                        case["template"],
                        case["data"],
                        case["result"]
                    )
            continue
        else:
            continue
