import time
import hmac
import hashlib
import base64

try:
    from urllib import parse as urlparse
except ImportError:
    from urlparse import urlparse

def check_secure_link(url, key, t=None):
    """check given url's signature with provided key

    :param url:
    :param key:
    :param t:
    """
    print(url)
    if u'&s=' not in url:
        return False
        # raise AttributeError('{} is not a singed url'.format(
        #     repr(url)
        # ))

    query = urlparse.urlparse(url).query
    query = urlparse.parse_qs(query)

    if not u'e' in query:
        return False
        # raise AttributeError('{} is not a singed url'.format(
        #     repr(url)
        # ))
    expire = query[u'e'][-1]
    if not expire.isdigit():
        return False
    expire = int(expire)

    if t is None:
        t = int(time.time())

    if expire < t:
        # link is expired
        return False

    signed_url, e = url.rsplit(u'&s=', 1)
    # remove expire-param from url
    base_url = signed_url[:signed_url.rfind(u'e=') - 1]

    # replace url-unsafe charackters in signature
    e = e.replace(u' ', u'-')  # + signs are spaces in urls
    e = e.replace(u'+', u'-')  # + signs might have been urlencoded
    e = e.replace(u'/', u'_')

    check = get_secure_link(base_url, key, expire, 0)
    return check == signed_url + u'&s=' + e


def get_secure_link(url, key, expire=60, t=None):
    """Sign url or POST data with hmac

    :param str url: The url to sign
    :param str key: The shared secret
    :param int expire: Time in seconds until link expires
    :param int t: The current timestamp (utc)
    :rtype: str
    """
    if u'?' in url:
        url += u'&'
    else:
        url += u'?'
    if t is None:
        t = int(time.time())

    expire += t
    url += u'e=' + str(expire)
    s = hmac.new(key.encode(), url.encode(), hashlib.sha256).digest()
    return url + u'&s=' + base64.b64encode(s, b'-_').decode().rstrip(u'=')
