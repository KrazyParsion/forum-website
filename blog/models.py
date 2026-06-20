from datetime import datetime
from blog import db
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(120),
        unique=False,
        nullable=False
    )

    posts = db.relationship(
        'Post',
        backref='author',
        lazy=True
    )

    def __repr__(self):
        return f"{self.username}"



class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    date_updated = db.Column(
        db.DateTime, 
        nullable=True,
        default=datetime.utcnow
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
        # default=User.id.data
        # default=1 #delete when implementing sessions
        )
    
    upvotes = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    downvotes = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )



    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(
        db.Text,
        nullable=False
    )

    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    date_updated = db.Column(
        db.DateTime, 
        nullable=True,
        default=datetime.utcnow
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
        # default=User.id.data
        # default=1 #delete when implementing sessions
        )
    
    author = db.relationship(
        'User',
        backref='comments'
        )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        nullable=False
    )

    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"
