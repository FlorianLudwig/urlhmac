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

// echo get_secure_link('/some_path', 'foobar', 60, 0) . "\n";
// echo hash_hmac('sha256', 'test', 'foo') . "\n";


// e = expire
// st = digest
