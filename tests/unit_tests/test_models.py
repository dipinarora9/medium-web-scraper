from medium_scraper.posts.models.post import Post
from medium_scraper.word_checker.models.trie import Trie
from medium_scraper.posts.models.creator import Creator
from medium_scraper.posts.models.tag import Tag


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


def test_new_tag():
    """
    GIVEN a Tag model
    WHEN a new Tag is created
    THEN check that its fields are defined correctly
    """
    tag = Tag(tag='abc', counter=0)
    assert tag.tag == 'abc'
    assert tag.counter == 0


def test_new_trie():
    """
    GIVEN a Trie model
    WHEN a new Trie is created
    THEN check that its fields are defined correctly
    """
    trie = Trie()
    trie.insert("abc")
    assert trie.search("abc") == True
    assert trie.search("ab") == False
    assert trie.suggest_next_word("a") == ["abc"]
    assert trie.suggest_next_word("ab") == ["abc"]
    assert trie.suggest_next_word("c") == []


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
