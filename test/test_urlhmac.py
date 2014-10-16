import urlhmac

import testcases


def test_check():
    for url in testcases.URLS:
        for key in testcases.KEYS:
            for expire in testcases.EXPIRES:
                for t in testcases.TIMES:
                    signed = urlhmac.get_secure_link(url, key, expire, t)
                    assert urlhmac.check_secure_link(signed, key, t=t)
                    assert urlhmac.check_secure_link(signed, key, expire+t, t)

                    # link is expired
                    assert not urlhmac.check_secure_link(signed, key, t + expire + 1)

                    # wrong key
                    assert not urlhmac.check_secure_link(signed, 'correct key', t=t)

                    # link is manipulated
                    for i in xrange(len(signed)):
                        tempered = signed[:i]
                        tempered += chr(ord(signed[i]) + 1)  # change charackter at pos i
                        tempered += signed[i+1:]
                        assert not urlhmac.check_secure_link(tempered, key, t=t)