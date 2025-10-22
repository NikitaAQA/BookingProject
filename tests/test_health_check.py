import allure
import pytest
import requests


@allure.feature('Test ping')
@allure.story('Test connection')
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expected status 201 but god {status_code}"

@allure.feature('Test ping')
@allure.story('Test server unavailability')
def test_ping_server_unavailability(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception("Server unavailability"))
    with pytest.raises(Exception, match="Server unavailability"):
        api_client.ping()

@allure.feature('Test ping')
@allure.story('Test wrong HTTP method')
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but god 405"):
        api_client.ping()

@allure.feature('Test ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but god 500"):
        api_client.ping()

@allure.feature('Test ping')
@allure.story('Test wrong URL')
def test_ping_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but god 404"):
        api_client.ping()

@allure.feature('Test ping')
@allure.story('Test connection with different success code')
def test_ping_not_success_different_code(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but god 200"):
        api_client.ping()

@allure.feature('Test ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session,'get', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()
