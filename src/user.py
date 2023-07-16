from src.db import database
import hashlib
import uuid


def createUser(username, password, email):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        query = ("SELECT * FROM user WHERE email = %s")
        result = db.execute(query, [email])
        print(result)
        if result != []:
            raise Exception("Email already exists")
        user_id = uuid.uuid4().hex
        print(f"uuid is {user_id} with len {len(user_id)}")
        query = "INSERT into user(userId, email, username, userPassword) VALUES(%s, %s, %s, %s)"
        db.execute(query, [user_id, email, username, password])
        return "User Successfully registered"        
    except Exception as e:
        raise Exception(e)

def verifyUser(email, password):
    password = (hashlib.sha256(password.encode('utf-8'))).hexdigest()
    try:
        db = database()
        query = ("SELECT userPassword FROM user WHERE email = %s")
        result = db.execute(query, [email])
        print(result)
        foundUser = result[0] # There should only be one user since we prevent registering of the same email
        print(foundUser)
        if result != []:
            raise Exception("Email already exists")
    except Exception as e:
        raise Exception(e)
    return "valid"