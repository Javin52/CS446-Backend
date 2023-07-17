from flask import Flask, request

from src.posts import getUserPosts, createUserPost, getSpecificPost, editUserPost, deleteUserPost, likedPost
from src.user import createUser, verifyUser
import json

def exception_handler(message):
    status_code = 400
    print("we are in the exception handler")
    return {
        'statusCode': status_code,
        'body': json.dumps(str(message))
    }

def success_handler(infoDict: dict):
    status_code = 200
    return {
        'statusCode': status_code,
        'body': json.dumps(infoDict)
    }

def create_app():
    app = Flask(__name__)

    # I believe that flask checks the method types for each route but just in case
    # there are case statements
    @app.route("/hello")
    def testBasic():
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
            match request.method:
                case 'POST':
                    result = createUser(username, password, email)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected POST")
        except Exception as e:
            return exception_handler(e)
    
    @app.route("/login", methods=['POST'])
    def login():
        payload = request.get_json()
        try:
            password = payload['password']
            email = payload['email']
        except Exception as e:
            return exception_handler("expected fields email and password")
        try:
            match request.method:
                case 'POST':
                    result = verifyUser(email, password)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected POST")
        except Exception as e:
            return exception_handler(e)
        

    # get list of posts by a user or create a post by a user
    @app.route("/post/<user_id>", methods=['GET', 'POST'])
    def posts(user_id):
        print("why hellow there")
        try:
            match request.method:
                case 'GET':
                    result = getUserPosts(user_id)
                    return success_handler(result)
                case 'POST':
                    payload = request.get_json()
                    category = payload.get('category', None)
                    try:
                        content = payload['content']
                    except Exception as e:
                        return exception_handler("expected at least content in request")
                    result = createUserPost(user_id, category, content)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    # Get, edit or delete a specific post from a user
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
                case _:
                    raise Exception("Invalid request method, expected GET, POST or DELETE")
        except Exception as e:
            return "Error has occured"
    
    # Get all comments or create a comment by a user
    @app.route("/comment/<user_id>", methods=['GET', 'POST'])
    def comment(user_id):
        try:
            match request.method:
                case 'GET':
                    return "something"
                case 'POST':
                    return "greate"
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return "error has occured"
    
    # get, edit or delete a specific comment by a user
    @app.route("/comment/<user_id>/<post_id>", methods=['GET', 'POST', 'DELETE'])
    def specificComment(user_id, post_id):
        match request.method:
            case 'GET':
                return "hello"
            case 'POST':
                return "hello"
            case 'DELETE':
                return "hellow"
            case _:
                raise Exception("Invalid request method, expected GET, POST or DELETE")

    @app.route("/likeComment/<user_id>/<post_id>", methods=['POST'])
    def likeComment(user_id, post_id):
        match request.method:
            case 'POST':
                result = likedPost(user_id, post_id)
                return success_handler(result)
            case _:
                raise Exception("Invalid request method, expected POST")

    @app.route("/uploadRoutine", methods=['POST'])
    def uploadRoutine():
        return ""
    # post exercise


    return app