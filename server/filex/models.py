from . import db

class User(db.Model):
    __tablename__ = 'users'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return '<User #{0} {1}>'.format(self.id, self.name)
