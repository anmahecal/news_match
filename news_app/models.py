from news_app import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    base_url = db.Column(db.String(100), unique=True)
    html_element = db.Column(db.String(20), nullable=False)
    element_class = db.Column(db.String(50))
    html_label = db.Column(db.String(20))
    label_class = db.Column(db.String(50))
    news = db.relationship('News', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f'Company({self.name}, {self.base_url})'


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(30))
    relevance = db.Column(db.Integer)
    url = db.Column(db.String(200))
    posted_at = db.Column(db.DateTime(), default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'company.id'), nullable=False)

    def __repr__(self) -> str:
        return f'News({self.title}, {self.posted_at})'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def get_reset_token(self, expired_seconds=1800):
        s = Serializer(app.config['SECRET_KEY'], expired_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
            return User.query.get(user_id)
        except:
            return None

    def __repr__(self) -> str:
        return f'User({self.username}, {self.email})'
