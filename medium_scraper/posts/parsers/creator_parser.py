from medium_scraper.helpers.constants import *
from medium_scraper.posts.models.creator import Creator


class CreatorParser:

    def __init__(self, user_object):
        self.profile_url = MEDIUM_USER_BASE_URL + user_object["username"]
        self.name = user_object["name"]
        self.image_url = MEDIUM_ASSETS_BASE_URL + user_object["imageId"]
        self.bio = user_object["bio"]

    def to_dict(self) -> dict:
        data = {}
        data["profile_url"] = self.profile_url
        data["name"] = self.name
        data["image_url"] = self.image_url
        data["bio"] = self.bio
        return data

    def to_creator(self) -> Creator:
        creator = Creator()
        creator.profile_url = self.profile_url
        creator.name = self.name
        creator.image_url = self.image_url
        creator.bio = self.bio
        return creator
