def test_trending_tags(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/trending_tags' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client_without_autocomplete.get('/trending_tags')
    assert response.status_code == 200


def test_trending_tags_post(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/trending_tags' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client_without_autocomplete.post('/trending_tags')
    assert response.status_code == 405


def test_load_more_posts(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/load_more_posts/blue/1' page is requested (GET)
    WHEN the '/load_more_posts/blue/2' page is requested (GET)
    THEN check that the responses are valid
    """
    response = test_client_without_autocomplete.get('/load_more_posts/blue/1')
    assert response.status_code == 200
    response = test_client_without_autocomplete.get('/load_more_posts/blue/2')
    assert response.status_code == 200


def test_load_more_posts_post(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/load_more_posts/blue/1' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client_without_autocomplete.post('/load_more_posts/blue/1')
    assert response.status_code == 405


def test_search(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/search/blue' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client_without_autocomplete.get('/search/blue')
    assert response.status_code == 200


def test_search_post(test_client_without_autocomplete):
    """
    GIVEN Without autocomplete client
    WHEN the '/search/blue' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client_without_autocomplete.post('/search/blue')
    assert response.status_code == 405
