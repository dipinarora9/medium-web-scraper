def test_typo_check(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/typo_check/clokc' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client_without_autocomplete.get('/typo_check/clokc')
    assert response.status_code == 200


def test_typo_check_post(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/typo_check/clokc' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client_without_autocomplete.post('/typo_check/clokc')
    assert response.status_code == 405
    assert "clock" not in response.text


def test_insert_autocomplete_word(test_client_with_autocomplete):
    """
    GIVEN With autocomplete client
    WHEN the '/insert_autocomplete_word/blue' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client_with_autocomplete.get(
        '/insert_autocomplete_word/blue')
    assert response.status_code == 200
    assert "" in response.text


def test_insert_autocomplete_word_post(test_client_with_autocomplete):
    """
    GIVEN With autocomplete client
    WHEN the '/insert_autocomplete_word/blue' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client_with_autocomplete.post(
        '/insert_autocomplete_word/blue')
    assert response.status_code == 405
