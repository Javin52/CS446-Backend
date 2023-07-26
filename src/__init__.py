from flask import Flask, request, Response
from src.comments import createUserComment, getAllCommentsUser, getAllCommentsofPost, getAllCommentsofRoutine

from src.posts import getSpecificPost, editUserPost, deleteUserPost, getUserPrimaryComments, likedPost
from src.routine import commentRoutine, deleteRoutine, editRoutine, getListofCommunityRoutines, getListofRoutines, getMostLikedRoutines, getSpecificRoutine, searchRoutineeByName, uploadRoutine
from src.user import createUser, editProfile, searchProfileById, verifyUser, updateProfilePicture, getProfileList, getFollowers, getFollowing, searchProfileByName, followUser, get_presigned_access_url, getNumFollowingMethod, getNumFollowersMethod
import json
from src.logger import logger

def exception_handler(message):
    status_code = 400
    print("we are in the exception handler")
    return Response(str(message), status_code)

def success_handler(infoDict: dict):
    status_code = 200
    return {
        'statusCode': status_code,
        'body': infoDict
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
            name = payload['name']
            email = payload['email']
        except Exception as e:
            log.debug(e)
            return exception_handler("expected fields username, name, email and password")
        try:
            match request.method:
                case 'POST':
                    result = createUser(username, password, email, name)
                    return result
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
            user = payload['user']
        except Exception as e:
            return exception_handler("expected fields username or email and password")
        try:
            match request.method:
                case 'POST':
                    result = verifyUser(user, password)
                    return result
                case _:
                    raise Exception("Invalid request method, expected POST")
        except Exception as e:
            return exception_handler(e)
        
    @app.route("/editProfile/<user_id>", methods=['POST'])
    def editUserProfile(user_id):
        try:
            match request.method:
                case 'POST':
                    payload = request.get_json()
                    bio = payload.get('bio', None)
                    username = payload.get('username', None)
                    preferred_name = payload.get('preferred_name', None)
                    result = editProfile(user_id, bio, username, preferred_name)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)
        
    @app.route("/testProfile/<user_id>", methods=['GET'])
    def testProfilePicture(user_id):
        return get_presigned_access_url(user_id)
    
    # not sure if we want a get request and send a s3 signed url using the user_id
    # for the name to make it identifiable. 
    @app.route("/updateProfilePic", methods=['POST'])
    def uploadProfilePicture():
        try:
            match request.method:
                case 'GET':
                    result = updateProfilePicture()
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    @app.route("/getNumFollowing/<userId>", methods=['GET'])
    def getNumFollowing(userId):
        try:
            match request.method:
                case 'GET':
                    result = getNumFollowingMethod(userId)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    @app.route("/getNumFollowers/<userId>", methods=['GET'])
    def getNumFollowers(userId):
        try:
            match request.method:
                case 'GET':
                    result = getNumFollowersMethod(userId)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    # Get method returns a list of profiles by index,
    # index is every 100 profiles
    @app.route("/getProfileList/<index>", methods=['GET'])
    def profile(index):
        try:
            match request.method:
                case 'GET':
                    result = getProfileList(index)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)
    
    # Get method returns a list of usernames like the provided name
    @app.route("/searchProfile/<name>", methods=['GET'])
    def searchProfile(name):
        try:
            match request.method:
                case 'GET':
                    result = searchProfileByName(name)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)
    
    @app.route("/searchProfileId/<profile_id>", methods=['GET'])
    def searchProfileId(profile_id):
        try:
            match request.method:
                case 'GET':
                    result = searchProfileById(profile_id)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    # Get provides list of people following the specified user_id
    # Post method when a user_id will be following someone else
    @app.route("/follow/<user_id>", methods=['GET', 'POST'])
    def follows(user_id):
        try:
            match request.method:
                case 'GET':
                    result = getFollowing(user_id)
                    return result
                case 'POST':
                    payload = request.get_json()
                    follow_id = payload.get('follow_id', None)
                    result = followUser(user_id, follow_id)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    # Get method returns a list of people you follow
    @app.route("/followers/<user_id>", methods=['GET'])
    def followers(user_id):
        try:
            match request.method:
                case 'GET':
                    result = getFollowers(user_id)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    @app.route("/searchRoutineName/<name>", methods=['GET'])
    def searchRoutineName(name):
        try:
            match request.method:
                case 'GET':
                    result = searchRoutineeByName(name)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    # adds a comment to a routine (this creates a primary comment)
    @app.route("/commentRoutine/<routine_id>", methods=['GET', 'POST'])
    def postRoutineOnline(routine_id):
        try:
            match request.method:
                case 'GET':
                    result = getAllCommentsofRoutine(routine_id)
                    return result
                case 'POST':
                    payload = request.get_json()
                    user_id = payload.get('user_id', None)
                    content = payload.get('content', None)
                    result = commentRoutine(user_id, content, routine_id)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    # get list of primary comments of a user
    @app.route("/primaryComments/<user_id>", methods=['GET'])
    def posts(user_id):
        print("why hellow there")
        try:
            match request.method:
                case 'GET':
                    result = getUserPrimaryComments(user_id)
                    return result
                # case 'POST':
                #     payload = request.get_json()
                #     try:
                #         content = payload['content']
                #     except Exception as e:
                #         return exception_handler("expected at least content in request")
                #     result = createUserPost(user_id, content)
                #     return result
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    # Get, edit or delete a specific post from a user
    @app.route("/comment/<user_id>/<post_id>", methods=['GET', 'POST', 'DELETE'])
    def specificPost(user_id, post_id):
        try:
            match request.method:
                case 'GET':
                    result = getSpecificPost(user_id, post_id)
                    return result
                case 'POST':
                    payload = request.get_json()
                    content = payload.get('content', None)
                    return editUserPost(user_id, post_id, content)
                case 'DELETE':
                    result = deleteUserPost(user_id, post_id)
                    return result
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
                    return result
                case 'POST':
                    payload = request.get_json()
                    post_id = payload.get('post_id', None)
                    content = payload.get('content', None)
                    result = createUserComment(user_id, post_id, content)
                    return result
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
                    return result
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
                    return result
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
                    result = likeRoutine(user_id, routine_id)
                    return result
                case _:
                    raise Exception("Invalid request method, expected POST")
        except Exception as e:
            return exception_handler(e)

    @app.route("/communityRoutines/<index>", methods=['GET'])
    def commuinityRoutines(index):
        try:
            match request.method:
                case 'GET':
                    result = getListofCommunityRoutines(index)
                    return result
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
                    return result
                case 'POST':
                    payload = request.get_json()
                    routine_name = payload.get('routine_name', None)
                    exercises = payload.get('exercises', None)
                    description = payload.get('description', None)
                    result = uploadRoutine(user_id, routine_name, exercises, description)
                    return result
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
                    return result
                case 'POST':
                    # TO DO
                    payload = request.get_json()
                    # post_id = payload.get('post_id', None)
                    # content = payload.get('content', None)
                    result = editRoutine()
                    return result
                case 'DELETE':
                    result = deleteRoutine(routine_id)
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET or POST")
        except Exception as e:
            return exception_handler(e)

    @app.route("/mostLikedRoutines", methods=['GET'])
    def mostLiked():
        try:
            match request.method:
                case 'GET':
                    result = getMostLikedRoutines()
                    return result
                case _:
                    raise Exception("Invalid request method, expected GET")
        except Exception as e:
            return exception_handler(e)

    return app