from flask import Flask, request

from src.posts import getUserPosts, createUserPost, getSpecificPost, editUserPost, deleteUserPost
from src.user import createUser
import json

def exception_handler(message: str):
    status_code = 400
    print("we are in the exception handler")
    return {
        'statusCode': status_code,
        'body': json.dumps(str(message))
    }

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "hello world"
    
    @app.route("/signup", methods=['POST'])
    def signup():
        payload = request.get_json()
        try:
            username = payload['username']
            password = payload['password']
            email = payload['email']
        except Exception as e:
            return exception_handler("expected fields username, email and password")
        try:
            createUser(username, password, email)
        except Exception as e:
            return exception_handler(e)
        return "success"
        

    # get list of user posts
    @app.route("/post/<user_id>", methods=['GET', 'POST'])
    def posts(user_id):
        try:
            match request.method:
                case 'GET':
                    return getUserPosts(user_id)
                case 'PUT':
                    return createUserPost(user_id)
        except Exception as e:
            return "error has occured"

    @app.route("/post/<user_id>/<post_id>", methods=['GET', 'POST', 'DELETE'])
    def specificPost(user_id, post_id):
        try:
            match request.method:
                case 'GET':
                    return getSpecificPost(user_id, post_id)
                case 'POST':
                    return editUserPost(user_id, post_id)
                case 'DELETE':
                    return deleteUserPost(user_id, post_id)
        except Exception as e:
            return "Error has occured"

    @app.route("/comment/<user_id>", methods=['GET', 'POST'])
    def comment(user_id):
        try:
            match request.method:
                case 'GET':
                    return "something"
                case 'PUT':
                    return "greate"
        except Exception as e:
            return "error has occured"
    
    @app.route("/comment/<user_id>/<post_id>", methods=['GET', 'POST', 'DELETE'])
    def specificComment(user_id, post_id):
        match request.method:
            case 'GET':
                return "hello"
            case 'POST':
                return "hello"
            case 'DELETE':
                return "hellow"

    @app.route("/uploadRoutine", methods=['POST'])
    def uploadRoutine():
        return ""
    # post exercise


    return app