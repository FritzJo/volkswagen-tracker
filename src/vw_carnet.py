#!/usr/bin/python
# Thanks to Rene Boer and Stefan Rehlegger for the inital code


import re
import requests
import json
import sys

request_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; D5803 Build/23.5.A.1.291; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36'
}


def remove_newline_chars(string: str) -> str:
    return string.replace('\n', '').replace('\r', '')


def extract_csrf(string: str) -> str:
    csrf_re = re.compile('<meta name="_csrf" content="(.*?)"/>')
    return csrf_re.search(string).group(1)


def extract_login_relay_state_token(string: str) -> str:
    regex = re.compile('<input.*?id="input_relayState".*?value="(.*?)"/>')
    return regex.search(string).group(1)


def extract_login_hmac(string: str) -> str:
    regex = re.compile('<input.*?id="hmac".*?value="(.*?)"/>')
    return regex.search(string).group(1)


def extract_login_csrf(string: str) -> str:
    regex = re.compile('<input.*?id="csrf".*?value="(.*?)"/>')
    return regex.search(string).group(1)


def CarNetLogin(session, email, password):
    base_url = 'https://www.portal.volkswagen-we.com'
    auth_base_url = 'https://identity.vwgroup.io'

    # Get initial CSRF
    landing_page_url = base_url + '/portal/en_GB/web/guest/home'
    landing_page_response = session.get(landing_page_url)
    if landing_page_response.status_code != 200:
        return ''
    csrf = extract_csrf(landing_page_response.text)

    # Get login page url
    auth_request_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; D5803 Build/23.5.A.1.291; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36'
    }
    auth_request_headers['Referer'] = base_url + '/portal'
    auth_request_headers['X-CSRF-Token'] = csrf
    get_login_url = base_url + \
                    '/portal/en_GB/web/guest/home/-/csrftokenhandling/get-login-url'
    login_page_response = session.post(
        get_login_url, headers=auth_request_headers)
    if login_page_response.status_code != 200:
        return ''
    login_url = json.loads(login_page_response.content).get(
        'loginURL').get('path')

    # Get login form url
    login_url_response = session.get(
        login_url, allow_redirects=False, headers=auth_request_headers)
    if login_url_response.status_code != 302:
        return ''
    login_form_url = login_url_response.headers.get('location')

    # Get login action url, relay state and hmac tokens, and login CSRF
    login_form_location_response = session.get(
        login_form_url, headers=auth_request_headers)
    if login_form_location_response.status_code != 200:
        return ''
    login_action_url_re = re.compile(
        '<form.*?id="emailPasswordForm".*?action="(.*?)">')
    login_form_location_response_data = remove_newline_chars(
        login_form_location_response.text)
    login_action_url = auth_base_url + \
                       login_action_url_re.search(login_form_location_response_data).group(1)
    login_relay_state_token1 = extract_login_relay_state_token(
        login_form_location_response_data)
    hmac_token1 = extract_login_hmac(login_form_location_response_data)
    login_csrf1 = extract_login_csrf(login_form_location_response_data)

    # Post initial login data
    del auth_request_headers['X-CSRF-Token']
    auth_request_headers['Referer'] = login_form_url
    auth_request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    post_data = {
        'email': email,
        'relayState': login_relay_state_token1,
        'hmac': hmac_token1,
        '_csrf': login_csrf1,
    }
    login_action_url_response = session.post(login_action_url, data=post_data,
                                             headers=auth_request_headers, allow_redirects=True)
    if login_action_url_response.status_code != 200:
        return ''
    auth_request_headers['Referer'] = login_action_url
    auth_request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    login_action2_url_re = re.compile(
        '<form.*?id="credentialsForm".*?action="(.*?)">')
    login_action_url_response_data = remove_newline_chars(
        login_action_url_response.text)
    login_action2_url = auth_base_url + \
                        login_action2_url_re.search(login_action_url_response_data).group(1)
    login_relay_state_token2 = extract_login_relay_state_token(
        login_action_url_response_data)
    hmac_token2 = extract_login_hmac(login_action_url_response_data)
    login_csrf2 = extract_login_csrf(login_action_url_response_data)

    # Post login data to "login action 2" url
    login_data = {
        'email': email,
        'password': password,
        'relayState': login_relay_state_token2,
        'hmac': hmac_token2,
        '_csrf': login_csrf2,
        'login': 'true'
    }
    login_post_response = session.post(login_action2_url, data=login_data,
                                       headers=auth_request_headers, allow_redirects=True)
    if login_post_response.status_code != 200:
        return ''
    ref2_url = login_post_response.headers.get('location')
    authcode_re = re.compile('&code=([^"]*)')
    portlet_code = authcode_re.search(login_post_response.url).group(1)
    state = extract_csrf(login_post_response.text)

    # Post login data to complete login url
    auth_request_headers['Referer'] = ref2_url
    portlet_data = {'_33_WAR_cored5portlet_code': portlet_code}
    final_login_url = base_url + '/portal/web/guest/complete-login' + '?p_auth=' + state + \
                      '&p_p_id=33_WAR_cored5portlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_33_WAR_cored5portlet_javax.portlet.action=getLoginStatus'
    complete_login_response = session.post(final_login_url, data=portlet_data,
                                           allow_redirects=False, headers=auth_request_headers)
    if complete_login_response.status_code != 302:
        return ''

    # Get base JSON url
    base_json_url = complete_login_response.headers.get('location')
    base_json_response = session.get(
        base_json_url, headers=auth_request_headers)
    csrf = extract_csrf(base_json_response.text)
    request_headers['Referer'] = base_json_url
    request_headers['X-CSRF-Token'] = csrf
    return base_json_url


def CarNetPost(session, url_base, command):
    print(command)
    r = session.post(url_base + command, headers=request_headers)
    return r.text


def CarNetPostAction(session, url_base, command, data):
    print(command)
    r = session.post(url_base + command, json=data, headers=request_headers)
    return r.text


def retrieveCarNetInfo(session, url_base):
    print(CarNetPost(session, url_base, '/-/msgc/get-new-messages'))
    print(CarNetPost(session, url_base, '/-/vsr/request-vsr'))
    print(CarNetPost(session, url_base, '/-/vsr/get-vsr'))
    print(CarNetPost(session, url_base, '/-/cf/get-location'))
    print(CarNetPost(session, url_base, '/-/vehicle-info/get-vehicle-details'))
    print(CarNetPost(session, url_base, '/-/emanager/get-emanager'))
    return 0


def getMileage(s, url_base):
    info = CarNetPost(s, url_base, '/-/vehicle-info/get-vehicle-details')
    json_info = json.loads(info)
    distance_covered = json_info['vehicleDetails']['distanceCovered']
    return distance_covered


def getRange(s, url_base):
    info = CarNetPost(s, url_base, '/-/vehicle-info/get-vehicle-details')
    json_info = json.loads(info)
    current_range = json_info['vehicleDetails']['range']
    return current_range
