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
        print(email)
        query = ("SELECT userId, userPassword FROM user WHERE email = %s")
        result = db.execute(query, [email])
        if result == []:
            raise Exception("Invalid password or username")
        foundUser = result[0] # There should only be one user since we prevent registering of the same email
        user_id = foundUser[0]
        correct_password = foundUser[1]
        print(user_id)
        print(correct_password)
        print(password)
        if correct_password == password:
            return ["Successful login", user_id]
        else:
            raise Exception("Invalid password or username")
    except Exception as e:
        raise Exception(e)