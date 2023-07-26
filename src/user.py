from src.db import database
import hashlib
from src.logger import logger
import uuid
import boto3
from botocore.exceptions import ClientError

def createUser(username, password, email, name, pfpId):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        log = logger()
        emailQuery = ("SELECT * FROM user WHERE email = %s")
        result = db.execute(emailQuery, [email])
        print(result)
        emailExists = True if result != [] else False
        usernameQuery = ("SELECT * FROM user WHERE username = %s")
        result = db.execute(usernameQuery, [username])
        usernameExists = True if result != [] else False
        if usernameExists and emailExists:
            raise Exception("Username and Email already exist")
        elif usernameExists:
            raise Exception("Username already exists")
        elif emailExists:
            raise Exception("Email already exists")
        user_id = uuid.uuid4().hex
        print(f"uuid is {user_id} with len {len(user_id)}")
        log.debug(f"Creating user with username {username}, name {name} and email {email} with uuid {user_id}")
        query = "INSERT into user(userId, email, username, userPassword, preferredName, profilePictureId) VALUES(%s, %s, %s, %s, %s, %s)"
        db.execute(query, [user_id, email, username, password, name, pfpId])
        return {"message": "User Successfully registered", 'user_id': user_id}
    except Exception as e:
        raise Exception(e)

def verifyUser(user, password):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        log = logger()
        print(user)
        query = ("SELECT userId, userPassword, preferredName, username, email FROM user WHERE email = %s OR username = %s")
        result = db.execute(query, [user, user])
        if result == []:
            raise Exception("Invalid password or username")
        foundUser = result[0] # There should only be one user since we prevent registering of the same email
        user_id = foundUser[0]
        correct_password = foundUser[1]
        name = foundUser[2]
        username = foundUser[3]
        email = foundUser[4]
        log.debug(f"User {user} was found, checking if valid")
        print(user_id)
        print(correct_password)
        print(password)
        if correct_password == password:
            log.debug("the passwords are the same for user {user}")
            return {"message": "User Successfully verified", 'user_id': user_id, 'name': name, 'username': username, 'email': email}
        else:
            raise Exception("Invalid password or username")
    except Exception as e:
        raise Exception(e)
    
def editProfile(user_id, bio, username, preferred_name):
    try:
        db = database()
        if username is not None:
            checkuser = "SELECT * FROM user WHERE username = %s"
            result = db.execute(checkuser, [username])
            if result != []:
                raise Exception("Username already taken")
        updateProfileQuery = "UPDATE user SET"
        vars = []
        if bio is not None:
            updateProfileQuery += " bio = %s,"
            vars.append(bio)
        if username is not None:
            updateProfileQuery += " username = %s,"
            vars.append(username)
        if preferred_name is not None:
            updateProfileQuery += " preferredName = %s,"
            vars.append(preferred_name)
        updateProfileQuery = updateProfileQuery[:-1]
        updateProfileQuery += " WHERE userId = %s"
        vars.append(user_id)
        result = db.execute(updateProfileQuery, vars)
        return ({"message": "updated profile successfully"})
    except Exception as e:
        raise Exception(e)

def updateProfilePicture(user_id, pfpId):
    if pfpId is None:
        raise Exception("Expected a pfpId")
    try:
        db = database()
        query = "UPDATE user SET profilePictureId = %s WHERE user.userId = %s"
        db.execute(query, [user_id, pfpId])
        return({"message": f"Successfully update pfp for userId {user_id} to {pfpId}"})
    except Exception as e:
        raise Exception(e)
    
def get_presigned_access_url(object_name):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    bucket_name = '446-backend'
    s3_client = boto3.client('s3')
    # print(object_name)
    object_name += '.jpg'
    try:
        doesKeyExist = s3_client.head_object(
            Bucket=bucket_name,
            Key=object_name,
        )
        # if it does not raise an error
        response = 'https://446-backend.s3.amazonaws.com/' + object_name
        # response = s3_client.generate_presigned_url('get_object',
        #                                             Params={'Bucket': bucket_name,
        #                                                     'Key': object_name},
        #                                             ExpiresIn=3600)
    except s3_client.exceptions.NoSuchKey as e:
        print("user profile not found")
        response = 'https://446-backend.s3.amazonaws.com/stockUser.jpg'
    except ClientError as e:
        response = 'https://446-backend.s3.amazonaws.com/stockUser.jpg'

    # The response contains the presigned URL
    # print(response)
    return response

# we need to add another field for the url of the s3 link for the profile picture
def createDictOfProfileInfo(profile_result):
    postList = []
    for profile in profile_result:
        tmp = {}
        userId = profile[0]
        tmp['userId'] = userId
        tmp['email'] = profile[1]
        tmp['username'] = profile[2]
        tmp['name'] = profile[3]
        # tmp['pfp_url'] = get_presigned_access_url(userId)
        tmp['bio'] = profile[5]
        tmp['pfpId'] = profile[6]
        postList.append(tmp)
    return postList

def getProfileList(index):
    try:
        db = database()
        log = logger()
        index = int(index) * 100
        query = "SELECT * FROM user LIMIT %s,%s"
        result = db.execute(query, [index, 100])
        postdict = createDictOfProfileInfo(result)
        return ({"profiles": postdict})
    except Exception as e:
        raise Exception(e)
    
def searchProfileByName(name):
    try:
        db = database()
        log = logger()
        name = '%' + name + '%'
        print(name)
        searchQuery = "SELECT * FROM user WHERE username LIKE %s"
        result = db.execute(searchQuery, [name])
        postDict = createDictOfProfileInfo(result)
        return ({'profiles': postDict})
    except Exception as e:
        raise Exception(e)
    
def searchProfileById(profile_id):
    try:
        db = database()
        log = logger()
        searchQuery = "SELECT * FROM user WHERE userId = %s"
        result = db.execute(searchQuery, [profile_id])
        postDict = createDictOfProfileInfo(result)
        return ({'profiles': postDict})
    except Exception as e:
        raise Exception(e)

def getFollowing(user_id):
    try:
        db = database()
        log = logger()
        searchQuery = "SELECT * FROM user WHERE userId in (select follows from followers WHERE userId = %s)"
        result = db.execute(searchQuery, [user_id])
        postDict = createDictOfProfileInfo(result)
        return ({'profiles': postDict})
    except Exception as e:
        raise Exception(e)

def getFollowers(user_id):
    try:
        db = database()
        log = logger()
        searchQuery = "SELECT * FROM user WHERE userId in (select userId from followers WHERE follows = %s)"
        result = db.execute(searchQuery, [user_id])
        postDict = createDictOfProfileInfo(result)
        return ({'profiles': postDict})
    except Exception as e:
        raise Exception(e)

def getNumFollowingMethod(user_id):
    try:
        db = database()
        log = logger()
        searchQuery = "SELECT count(userId) from followers WHERE userId = %s"
        result = db.execute(searchQuery, [user_id])

        return str(result[0][0])
    except Exception as e:
        raise Exception(e)

def getNumFollowersMethod(user_id):
    try:
        db = database()
        log = logger()

        searchQuery = "SELECT count(userId) from followers WHERE follows = %s"
        result = db.execute(searchQuery, [user_id])
        return str(result[0][0])
    except Exception as e:
        raise Exception(e)

def followUser(user_id, following_id):
    try:
        db = database()
        hasLikedQuery = "SELECT * FROM followers WHERE userId = %s AND follows = %s"
        result = db.execute(hasLikedQuery, [user_id, following_id])
        if result == []:
            query = "INSERT INTO followers(userId, follows) VALUES(%s, %s)"
            db.execute(query, [user_id, following_id])
            message = f"{user_id} follows {following_id}"
        else:
            query = "DELETE FROM followers WHERE userId = %s AND follows = %s"
            db.execute(query, [user_id, following_id])
            message = f"{user_id} has unfollowed user {following_id}"
        return {"message": message}
    except Exception as e:
        raise Exception(e)