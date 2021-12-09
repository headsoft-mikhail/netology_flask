from app import app
from flask import request, jsonify
from flask.views import MethodView
from validator import validate
from models import Post, User
from schema import POST_CREATE, POST_UPDATE, USER_CREATE
from authorization import multi_auth, create_token, check_owner


@app.route('/', methods=['GET', ])
def test():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})
    return {'status': 'OK'}


class PostView(MethodView):
    @staticmethod
    def get(obj_id):
        if obj_id is not None:
            return jsonify(Post.get_by_id(obj_id).to_dict())
        else:
            return jsonify([post.to_dict() for post in Post.get_all()])

    @staticmethod
    @validate('json', POST_CREATE)
    @multi_auth.login_required
    def post():
        post = Post(**request.json)
        post.owner = User.get_by_email(multi_auth.current_user())
        post.owner_id = post.owner.id
        post.add()
        return jsonify(post.to_dict())

    @staticmethod
    @validate('json', POST_UPDATE)
    @multi_auth.login_required
    @check_owner(obj_class='Post')
    def put(obj_id):
        return jsonify(Post(**request.json).update(obj_id, request.json))

    @staticmethod
    @multi_auth.login_required
    @check_owner(obj_class='Post')
    def delete(obj_id):
        return jsonify(Post.delete_by_id(obj_id))


class UserView(MethodView):
    @validate('json', USER_CREATE)
    def post(self):
        if request.json.get('name'):
            user = User.add(
                request.json.get('email'),
                request.json.get('password'),
                name=request.json.get('name')
            )
        else:
            user = User.add(
                request.json.get('email'),
                request.json.get('password')
            )
        create_token(request.json.get('email'))
        return jsonify(user)

    @staticmethod
    @multi_auth.login_required
    def get():
        user = User.get_by_email(multi_auth.current_user())
        return jsonify(user.to_dict())


get_posts_view = PostView.as_view('posts_get')
app.add_url_rule('/posts/', defaults={'obj_id': None}, view_func=get_posts_view, methods=['GET', ])
app.add_url_rule('/posts/<int:obj_id>', view_func=get_posts_view, methods=['GET', ])
app.add_url_rule('/posts/<int:obj_id>', view_func=PostView.as_view('posts_update'), methods=['PUT', ])
app.add_url_rule('/posts/<int:obj_id>', view_func=PostView.as_view('posts_delete'), methods=['DELETE', ])
app.add_url_rule('/posts/', view_func=PostView.as_view('posts_post'), methods=['POST', ])

app.add_url_rule('/user/', view_func=UserView.as_view('users_get'), methods=['GET', ])
app.add_url_rule('/user/', view_func=UserView.as_view('users_post'), methods=['POST', ])
