def test_home_page(test_client_without_autocomplete):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client_without_autocomplete.get('/')
    assert response.status_code == 200
    assert "its working don't worry!" in response.text


def test_home_page_post(test_client_without_autocomplete):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client_without_autocomplete.post('/')
    assert response.status_code == 405
    assert "its working don't worry!" not in response.text


def test_home_page(test_client_with_autocomplete):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client_with_autocomplete.get('/')
    assert response.status_code == 200
    assert "its working don't worry!" in response.text


def test_home_page_post(test_client_with_autocomplete):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client_with_autocomplete.post('/')
    assert response.status_code == 405
    assert "its working don't worry!" not in response.text
