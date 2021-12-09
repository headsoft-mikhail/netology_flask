from sqlalchemy import exc, sql, inspect
import errors
from app import db
from config import SALT
import hashlib


class BaseModelMixin:
    @classmethod
    def get_by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    @classmethod
    def get_all(cls):
        obj_list = cls.query.all()
        if len(obj_list) > 0:
            return obj_list
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
            return {'status': 'created',
                    'object': self.to_dict()}
        except exc.IntegrityError:
            raise errors.BadLuck

    @classmethod
    def update(cls, obj_id, data):
        obj = cls.get_by_id(obj_id)
        for key in data.keys():
            setattr(obj, key, data[key])
        try:
            db.session.commit()
            return {'status': 'updated',
                    'object': obj.to_dict()}
        except exc.IntegrityError:
            raise errors.BadLuck

    @classmethod
    def delete_by_id(cls, obj_id):
        obj = cls.get_by_id(obj_id)
        try:
            db.session.delete(obj)
            db.session.commit()
            return {'status': 'deleted',
                    'object': obj.to_dict()}
        except exc.IntegrityError:
            raise errors.BadLuck


class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128), index=True)
    name = db.Column(db.String(50))

    def __str__(self):
        return f'User {self.email} ({self.name})'

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def hash_password(self, raw_password):
        raw_password = f'{raw_password}{SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def verify_password(self, raw_password):
        raw_password = f'{raw_password}{SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    @classmethod
    def get_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user is not None:
            return user
        else:
            raise errors.BadLuck

    @classmethod
    def add(cls, email, password, name='NoName'):
        if cls.query.filter_by(email=email).first() is not None:
            raise errors.BadLuck
        else:
            new_user = User()
            new_user.email = email
            new_user.name = name
            new_user.hash_password(password)
            db.session.add(new_user)
            try:
                db.session.commit()
                return {'status': 'created',
                        'object': new_user.to_dict()}
            except exc.IntegrityError:
                raise errors.BadLuck


class Post(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), index=True)
    text = db.Column(db.String(1000), index=True)
    created_at = db.Column(db.DateTime, server_default=sql.func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

    def __str__(self):
        return f'Post {self.title} ({self.created_at})'

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'created_at': self.created_at,
            'owner_id': self.owner_id,
            'owner': str(self.owner)
        }






