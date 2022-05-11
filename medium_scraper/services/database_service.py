from medium_scraper.posts.models.creator import Creator
from medium_scraper.posts.models.tag import Tag
from medium_scraper.posts.models.post import Post
from medium_scraper import db


class DatabaseService:

    @staticmethod
    def get_trending_tags():
        t = Tag.query.order_by(Tag.counter.desc()).limit(5).all()
        tags = []
        for tag in t:
            tags.append(tag.tag)
        return tags

    @staticmethod
    def get_tag(tag):
        return Tag.query.filter_by(tag=tag).first()

    @staticmethod
    def update_tag_counter(tag):
        tag_model = DatabaseService.get_tag(tag)
        if tag_model is None:
            db.session.add(Tag(tag=tag, counter=1))
        else:
            tag_model.counter = Tag.counter + 1
        db.session.commit()

    @staticmethod
    def get_creator(creator_profile_url):
        return Creator.query.filter_by(profile_url=creator_profile_url).first()

    @staticmethod
    def add_post_and_creator_to_db(post: Post):
        creator = DatabaseService.get_creator(post.creator.profile_url)
        if creator is not None:
            creator = post.creator
            creator.posts.append(post)
            del post.creator
            post.creator_id = creator.profile_url
            db.session.add(post)
        else:
            creator = post.creator
            del post.creator
            creator.posts.append(post)
            db.session.add(creator)
            db.session.add(post)
        db.session.commit()

    @staticmethod
    def get_post_from_post_id(post_id):
        return Post.query.filter_by(id=post_id).first()

    @staticmethod
    def get_post_from_post_url(post_url):
        post_id = post_url.split('-')[-1]
        return DatabaseService.get_post_from_post_id(post_id)
