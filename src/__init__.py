from flask import Flask, request
from src.comments import createUserComment, getAllCommentsUser, getAllCommentsofPost, getAllCommentsofRoutine

from src.posts import getUserPosts, createUserPost, getSpecificPost, editUserPost, deleteUserPost, getUserPrimaryComments, likedPost
from src.routine import commentRoutine, deleteRoutine, editRoutine, getListofCommunityRoutines, getListofRoutines, getSpecificRoutine, postRoutine, uploadRoutine
from src.user import createUser, verifyUser
import json
from src.logger import logger

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
    log = logger()

    # I believe that flask checks the method types for each route but just in case
    # there are case statements
    @app.route("/")
    def start():
        return "start api link of pages or something"

    @app.route("/hello")
    def testBasic():
        log.debug("test hello")
        return "hello world"
    
    @app.route("/signup", methods=['POST'])
    def signup():
        payload = request.get_json()
        try:
            username = payload['username']
            password = payload['password']
            email = payload['email']
        except Exception as e:
            log.debug(e)
            return exception_handler("expected fields username, email and password")
        try:
            match request.method:
                case 'POST':
                    result = createUser(username, password, email)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected POST")
        except Exception as e:
            log.debug(e)
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
        
    # adds a comment to a routine (this creates a primary comment)
    @app.route("/commentRoutine/<routine_id>", methods=['POST'])
    def postRoutineOnline(routine_id):
        try:
            match request.method:
                case 'GET':
                    result = getAllCommentsofRoutine(routine_id)
                    return success_handler(routine_id)
                case 'POST':
                    payload = request.get_json()
                    user_id = payload.get('post_id', None)
                    content = payload.get('content', None)
                    result = commentRoutine(user_id, content, routine_id)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    # get list of primary comments of a user
    @app.route("/pimaryComments/<user_id>", methods=['GET'])
    def posts(user_id):
        print("why hellow there")
        try:
            match request.method:
                case 'GET':
                    result = getUserPrimaryComments(user_id)
                    return success_handler(result)
                # case 'POST':
                #     payload = request.get_json()
                #     try:
                #         content = payload['content']
                #     except Exception as e:
                #         return exception_handler("expected at least content in request")
                #     result = createUserPost(user_id, content)
                #     return success_handler(result)
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
                    return editUserPost(user_id, post_id, content)
                case 'DELETE':
                    result = deleteUserPost(user_id, post_id)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET, POST or DELETE")
        except Exception as e:
            return exception_handler(e)
    
    # Get all secondary comments by a user or create a secondarycomment
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

    # Get all secondary comments of a specific secondary or primary comment
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
        
    #  TODO
    @app.route("/likeRoutine/<user_id>/<routine_id>", methods=['POST'])
    def likeRoutine(user_id, routine_id):
        try:
            match request.method:
                case 'POST':
                    # result = likedPost(user_id, routine_id)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected POST")
        except Exception as e:
            return exception_handler(e)

    @app.route("communityRoutines/<index>", methods=['GET'])
    def commuinityRoutines(idx):
        try:
            match request.method:
                case 'GET':
                    result = getListofCommunityRoutines(idx)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    # get ids of all routines created by a user and create/share a routine
    @app.route("/routine/<user_id>", methods=['GET', 'POST'])
    def routine(user_id):
        try:
            match request.method:
                case 'GET':
                    result = getListofRoutines(user_id)
                    return success_handler(result)
                case 'POST':
                    payload = request.get_json()
                    routine_name = payload.get('routine_name', None)
                    exercises = payload.get('exercises', None)
                    result = uploadRoutine(user_id, routine_name, exercises)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)
    
    # get a specific routine, edit a specific routine, and delete a routine
    @app.route("/specificRoutine/<routine_id>", methods=['GET', 'POST', 'DELETE'])
    def rmeoveRoutine(routine_id):
        try:
            match request.method:
                case 'GET':
                    result = getSpecificRoutine(routine_id)
                    return success_handler(result)
                case 'POST':
                    # TO DO
                    payload = request.get_json()
                    # post_id = payload.get('post_id', None)
                    # content = payload.get('content', None)
                    result = editRoutine()
                    return success_handler(result)
                case 'DELETE':
                    result = deleteRoutine(routine_id)
                    return success_handler(result)
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    return app