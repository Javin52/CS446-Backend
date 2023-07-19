from flask import Flask, request
from src.comments import createUserComment, getAllCommentsUser, getAllCommentsofPost

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
                    result = getSpecificPost(user_id, post_id)
                    return success_handler(result)
                case 'POST':
                    payload = request.get_json()
                    content = payload.get('content', None)
                    category = payload.get('category', None)
                    if content is None and category is None:
                        return exception_handler("Post was not updated since there was nothing to update")
                    return editUserPost(user_id, post_id, content, category)
                case 'DELETE':
                    result = deleteUserPost(user_id, post_id)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET, POST or DELETE")
        except Exception as e:
            return exception_handler(e)
    
    # Get all comments or create a comment by a user
    @app.route("/user_comment/<user_id>", methods=['GET', 'POST'])
    def comment_users(user_id):
        try:
            match request.method:
                case 'GET':
                    result = getAllCommentsUser(user_id)
                    return success_handler(result)
                case 'POST':
                    payload = request.get_json()
                    post_id = payload.get('post_id', None)
                    content = payload.get('content', None)
                    result = createUserComment(user_id, post_id, content)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    # Get all comments for a specific post/comment
    @app.route("/post_comment/<post_id>", methods=['GET'])
    def comment_posts(post_id):
        try:
            match request.method:
                case 'GET':
                    result = getAllCommentsofPost(post_id)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    @app.route("/likeComment/<user_id>/<post_id>", methods=['POST'])
    def likeComment(user_id, post_id):
        try:
            match request.method:
                case 'POST':
                    result = likedPost(user_id, post_id)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected POST")
        except Exception as e:
            return exception_handler(e)

    # post exercise
    @app.route("/uploadRoutine", methods=['POST'])
    def uploadRoutine():
        return ""
    
    @app.route("/removeRoutine", methods=['POST'])
    def rmeoveRoutine():
        return ""


    return app