import os
import subprocess

import urlhmac
import testcases

BASE_PATH = os.path.abspath(os.path.dirname(__file__) + '/..')
BASE_CODE = """<?php

set_include_path({PATH});

require_once('urlhmac.php');

{code}
"""


def exec_php(code):
    code = BASE_CODE.format(
        PATH=repr(BASE_PATH),
        code=code
    )
    proc = subprocess.Popen(['php'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(code)
    proc.stdin.close()
    proc.wait()
    return proc.stdout.read()


def php_get_secure_link(url, key, expire, t):
    return exec_php(
        'echo \urlhmac\get_secure_link(' + repr(url) + ', '
                                         + repr(key) + ', '
                                         + str(expire) + ', '
                                         + str(t) + ');')


def test_compare_to_py():
    for url in testcases.URLS:
        for key in testcases.KEYS:
            for expire in testcases.EXPIRES:
                for t in testcases.TIMES:
                    php = php_get_secure_link(url, key, expire, t)
                    py = urlhmac.get_secure_link(url, key, expire, t)
                    assert php == py
