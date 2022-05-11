from medium_scraper import db


class Tag(db.Model):
    tag = db.Column(db.Text, primary_key=True)
    counter = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Tag %r>' % self.name
