from medium_scraper.posts.models.creator import Creator


def test_new_creator():
    """
    GIVEN a Creator model
    WHEN a new creator is created
    THEN check that its fields are defined correctly
    """
    creator = Creator(
        profile_url="abc",
        name='name',
        image_url='name',
        bio='bio',
    )
    assert creator.profile_url == 'abc'
    assert creator.name == 'name'
    assert creator.image_url == "name"
    assert creator.bio == 'bio'
