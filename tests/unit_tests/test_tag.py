from medium_scraper.posts.models.tag import Tag


def test_new_tag():
    """
    GIVEN a Tag model
    WHEN a new Tag is created
    THEN check that its fields are defined correctly
    """
    tag = Tag(tag='abc', counter=0)
    assert tag.tag == 'abc'
    assert tag.counter == 0
