from enum import unique
from medium_scraper import db


class Creator(db.Model):
    profile_url = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    posts = db.relationship('Post', backref=db.backref('creator', lazy=True))

    def __repr__(self):
        return '<Creator %r>' % self.name

    def to_dict(self) -> dict:
        data = {}
        data["profile_url"] = self.profile_url
        data["name"] = self.name
        data["image_url"] = self.image_url
        data["bio"] = self.bio
        return data