from behave import given, when, then, step
import requests


api_endpoints = {}
request_headers = {}
response_codes ={}
response_texts={}
request_bodies = {}
api_url=None


@given(u'I set api url to list zones "{endpoint}"')
def step_impl(context, endpoint):
    global api_url
    api_url = endpoint


@given(u'I set GET posts api endpoint to list zones "{after_slash_url}"')
def step_impl(context, after_slash_url):
    api_endpoints['GET_URL'] = api_url + after_slash_url
    print('url: ' + api_endpoints['GET_URL'])


@when(u'I set HEADER param request content to list zones type as "{header_content_type}"')
def step_impl(context, header_content_type):
    response = requests.get(url=api_endpoints['GET_URL'], headers=request_headers)
    response_texts['GET'] = response.text 
    response_codes['GET'] = response.status_code


@then(u'I receive valid HTTP response code "{response_code}" for "{request_name}" to list zones')
def step_impl(context, response_code, request_name):
    print('Get rep code for '+request_name+':'+ str(response_codes[request_name]))

    assert response_codes[request_name] == int(response_code)


@then(u'Response BODY "{request_name}" is non-empty to list zones')
def step_impl(context, request_name):
    print('request_name: '+request_name)
    print(response_texts)

    assert response_texts[request_name] is not None
