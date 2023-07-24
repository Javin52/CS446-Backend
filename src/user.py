from src.db import database
import hashlib
from src.logger import logger
import uuid


def createUser(user_id, username, password, email):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        log = logger()
        # See if email already exists
        query = ("SELECT * FROM user WHERE email = %s")
        result = db.execute(query, [email])
        print(result)
        emailExists = True if result != [] else False
        # See if user Id already exists
        query = ("SELECT * FROM user WHERE userId = %s")
        result = db.execute(query, [user_id])
        print(result)
        userIdExists = True if result != [] else False
        # Raise exceptions if either UserID or Email already exist
        # This is for frontend to handle error properly
        if userIdExists and emailExists:
            raise Exception("User ID and Email already exist")
        elif userIdExists:
            raise Exception("User ID already exists")
        elif emailExists:
            raise Exception("Email already exists")
        # Create user if no exceptions
        log.debug(f"Creating user with username {username} and email {email} with user ID {user_id}")
        query = "INSERT into user(userId, email, username, userPassword) VALUES(%s, %s, %s, %s)"
        db.execute(query, [user_id, email, username, password])
        return {"message": "User Successfully registered", 'user_id': user_id}
    except Exception as e:
        raise Exception(e)

def verifyUser(user, password):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        log = logger()
        print(user)
        query = ("SELECT userId, userPassword FROM user WHERE email = %s OR userId = %s")
        result = db.execute(query, [user, user])
        if result == []:
            raise Exception("Invalid password or username")
        foundUser = result[0] # There should only be one user since we prevent registering of the same email
        user_id = foundUser[0]
        correct_password = foundUser[1]
        log.debug(f"User {user} was found, checking if valid")
        print(user_id)
        print(correct_password)
        print(password)
        if correct_password == password:
            log.debug("the passwords are the same for user {user}")
            return {"message": "User Successfully verified", 'user_id': user_id}
        else:
            raise Exception("Invalid password or username")
    except Exception as e:
        raise Exception(e)