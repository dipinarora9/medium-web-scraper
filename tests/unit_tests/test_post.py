from medium_scraper.posts.models.post import Post


def test_new_post():
    """
    GIVEN a Post model
    WHEN a new Post is created
    THEN check that its fields are defined correctly
    """
    post = Post(
        id='abc',
        title='Post',
        created_at=1234654789,
        description='description',
        medium_url='https://abc.com',
        paragraphs='["fas","a"]',
        tags="['tags']",
        claps_count=0,
        responses_count=0,
        creator_id='abc',
    )
    assert post.id == 'abc'
    assert post.title == 'Post'
    assert post.created_at == 1234654789
    assert post.description == 'description'
    assert post.medium_url == 'https://abc.com'
    assert post.paragraphs == '["fas","a"]'
    assert post.tags == "['tags']"
    assert post.claps_count == 0
    assert post.responses_count == 0
    assert post.creator_id == 'abc'
    assert post.time_taken_to_crawl == 0
