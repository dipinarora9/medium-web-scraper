import json
from medium_scraper import db


class Post(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    description = db.Column(db.Text, nullable=False)
    medium_url = db.Column(db.Text, unique=True, nullable=False)
    paragraphs = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)
    claps_count = db.Column(db.Integer, nullable=False)
    responses_count = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer,
                           db.ForeignKey('creator.id'),
                           nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.id

    def to_json(self) -> str:
        data = {}
        data["id"] = self.id
        data["title"] = self.title
        data["created_at"] = self.created_at
        data["description"] = self.description
        data["medium_url"] = self.medium_url
        data["paragraphs"] = json.loads(self.paragraphs)
        data["creator"] = self.creator.to_dict()
        data["tags"] = json.loads(self.tags)
        data["claps_count"] = self.claps_count
        data["responses_count"] = self.responses_count
        return json.dumps(data)
