from src.db import database
import hashlib
from src.logger import logger
import uuid


def createUser(username, password, email):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        log = logger()
        query = ("SELECT * FROM user WHERE email = %s")
        result = db.execute(query, [email])
        print(result)
        if result != []:
            raise Exception("Email already exists")
        user_id = uuid.uuid4().hex
        print(f"uuid is {user_id} with len {len(user_id)}")
        log.debug(f"Creating user with username {username} and email {email} with uuid {user_id}")
        query = "INSERT into user(userId, email, username, userPassword) VALUES(%s, %s, %s, %s)"
        db.execute(query, [user_id, email, username, password])
        return {"message": "User Successfully registered", 'user_id': user_id}
    except Exception as e:
        raise Exception(e)

def verifyUser(email, password):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        log = logger()
        print(email)
        query = ("SELECT userId, userPassword FROM user WHERE email = %s")
        result = db.execute(query, [email])
        if result == []:
            raise Exception("Invalid password or username")
        foundUser = result[0] # There should only be one user since we prevent registering of the same email
        user_id = foundUser[0]
        correct_password = foundUser[1]
        log.debug(f"email {email} was found, checking if valid")
        print(user_id)
        print(correct_password)
        print(password)
        if correct_password == password:
            log.debug("the passwords are the same for email {email}")
            return {"message": "User Successfully verified", 'user_id': user_id}
        else:
            raise Exception("Invalid password or username")
    except Exception as e:
        raise Exception(e)