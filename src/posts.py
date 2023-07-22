from src.db import database
import uuid

def createDictOfPostResults(sqlResult):
    postdict = {}
    for post in sqlResult:
        tmpPostDict = {}
        tmpPostDict['postId'] = post[0]
        tmpPostDict['user'] = post[1]
        tmpPostDict['likes'] = post[2]
        tmpPostDict['content'] = post[3]
        postdict[post[0]] = tmpPostDict
    return postdict

def getUserPrimaryComments(user_id):
    try:
        print(user_id)
        db = database()
        print("testing 1")
        query = "SELECT * " +\
                "FROM post c " +\
                "NATURAL JOIN " +\
                "(" +\
                    "SELECT postId " +\
                    "FROM post p " +\
                    "WHERE user = %s" +\
                    "AND user not in ( " +\
                        "SELECT comment " +\
                        "FROM comments " +\
                        "WHERE comment = %s " +\
                    ")" +\
                ") t"
        result = db.execute(query, [user_id, user_id])
        postdict = createDictOfPostResults(result)
        return ({"posts": postdict})
    except Exception as e:
        raise Exception(e)

def createUserPost(user_id, content):
    try:
        post_id = uuid.uuid4().hex
        db = database()
        query = "INSERT INTO post(postId, user, likes, content) VALUES(%s, %s, %s, %s, %s)"
        db.execute(query, [post_id, user_id, 0, content])
        return {'message': 'Post successfully created', 'post_id': post_id}
    except Exception as e:
        raise Exception(e)

def likedPost(user_id, post_id):
    print(user_id)
    print(post_id)
    try:
        db = database()
        query = "UPDATE post SET likes = likes + 1 WHERE postId = %s"
        db.execute(query, [post_id])
        message = f"liked post {post_id}"
        return {"message": message}
    except Exception as e:
        raise Exception(e)

def getSpecificPost(user_id, post_id):
    try:
        db = database()
        query = "SELECT * FROM post WHERE user = %s AND postId = %s"
        result = db.execute(query, [user_id, post_id])
        postDict = createDictOfPostResults(result)
        return postDict[post_id]
    except Exception as e:
        raise Exception(e)

def editUserPost(user_id, post_id, newContent):
    try:
        db = database()
        conditions = ""
        conditionVars = []
        if newContent is not None:
            conditions += "content = %s "
            conditionVars.append(newContent)
        query = "UPDATE post SET " +  conditions + "WHERE postId = %s AND user = %s"
        conditionVars.append(post_id)
        conditionVars.append(user_id)
        db.execute(query, conditionVars)
        return {
            'message': 'Post has been successfully updated',
            'post_id': post_id,
            'user_id': user_id
        }
    except Exception as e:
        raise Exception(e)

def deleteUserPost(user_id, post_id):
    try:
        db = database()
        query = "DELETE FROM post WHERE user = %s AND postId = %s"
        result = db.execute(query, [user_id, post_id])
        print(result)
        message = f"Deleted post {post_id} by {user_id}"
        return {"message": message}
    except Exception as e:
        raise Exception(e)