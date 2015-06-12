import os
import subprocess
import json

import urlhmac
import testcases

DIR_PATH = os.path.dirname(__file__)
DIR_PATH = DIR_PATH if DIR_PATH else '.'
BASE_PATH = os.path.abspath(DIR_PATH + '/..')
BASE_CODE = """<?php

set_include_path({PATH});

require_once('urlhmac.php');

$re = {code}

echo json_encode($re) . "\\n";
"""


def exec_php(code):

    code = BASE_CODE.format(
        PATH=repr(BASE_PATH),
        code=code
    )
    try:
        proc = subprocess.Popen(['php'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        proc.stdin.write(code)
        proc.stdin.close()
        result = proc.stdout.read()
        proc.wait()

        return json.loads(result)
    except:
        print code
        raise


def get_secure_link(url, key, expire, t):
    return exec_php(
        '\urlhmac\get_secure_link(' + repr(url) + ', '
                                     + repr(key) + ', '
                                     + str(expire) + ', '
                                     + str(t) + ');')


def check_secure_link(url, key, t=None):
    return exec_php(
        '\urlhmac\check_secure_link(' + json.dumps(url) + ', '
                                      + json.dumps(key) + ', '
                                      + json.dumps(t) + ');')

def test_compare_to_py():
    for url in testcases.URLS:
        for key in testcases.KEYS:
            for expire in testcases.EXPIRES:
                for t in testcases.TIMES:
                    php = php_get_secure_link(url, key, expire, t)
                    py = urlhmac.get_secure_link(url, key, expire, t)
                    assert php == py
