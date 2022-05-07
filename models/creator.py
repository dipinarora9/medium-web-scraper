from models.constants import MEDIUM_ASSETS_BASE_URL, MEDIUM_USER_BASE_URL


class Creator:

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
