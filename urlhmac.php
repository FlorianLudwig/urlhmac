<?php
namespace urlhmac;

/**
 * Sign url or POST data with hmac
 *
 * @param string $url The url to sign
 * @param string $key The shared secret
 * @param int $expire Time in seconds until link expires
 * @param int $t The current timestamp (utc)
 * @return string The signed url
 */
function get_secure_link($url, $key, $expire=60, $t=NULL) {
    if(strpos($url, '?') == null) {
        $url .= '?';
    } else {
        $url .= '&';
    }
    if($t === null) {
        $t = time();
    }
    $expire += $t;
    $url .= 'e=' . $expire;
    $hmac = hash_hmac('sha256', $url, $key, true);
    $encoded = rtrim(base64_encode($hmac), '=');
    // use url safe alphabet for base64
    // as suggeted in rfc4648
    $encoded = strtr($encoded, '+/', '-_');
    return $url . '&s=' . $encoded;
}


/**
 * @param string $url
 * @return boolean
 */
function check_secure_link($url, $key, $t=NULL) {
    if($t === NULL) {
       $t = time();
    }

    $queryStr = parse_url($url, PHP_URL_QUERY);
    parse_str($queryStr, $params);
    if (! isset($params['e']) || ! isset($params['s'])) {
        return false;
    }
    $expiry = $params['e'];
    $signature = $params['s'];
    if ($expiry < $t) {
        return false;
    }

    $pos = strrpos($url, 'e=');
    $base_url = substr($url, 0, $pos-1);
    $signed_url = get_secure_link($base_url, $key, $expiry, 0);
    return $url === $signed_url;
}
