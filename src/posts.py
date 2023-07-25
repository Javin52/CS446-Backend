from src.db import database
import uuid

def createDictOfPostResults(sqlResult):
    postdict = {}
    for post in sqlResult:
        tmpPostDict = {}
        postId = post[0]
        tmpPostDict['postId'] = postId
        tmpPostDict['user'] = post[1]
        tmpPostDict['content'] = post[3]
        try:
            tmpPostDict['likes'] = countLikesInPost(postId)
        except Exception as e:
            tmpPostDict['likes'] = "-1"
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
        query = "INSERT INTO post(postId, user, content) VALUES(%s, %s, %s)"
        db.execute(query, [post_id, user_id, content])
        return {'message': 'Post successfully created', 'post_id': post_id}
    except Exception as e:
        raise Exception(e)

def likedPost(user_id, post_id):
    print(user_id)
    print(post_id)
    try:
        db = database()
        hasLikedQuery = "SELECT * FROM postLikes WHERE postId = %s AND userId = %s"
        result = db.execute(hasLikedQuery, [post_id, user_id])
        if result != []:
            query = "DELETE FROM postLikes WHERE postId = %s AND userId = %s"
            db.execute(query, [post_id, user_id])
            message = f"{user_id} disliked post {post_id}"
        else:
            query = "INSERT INTO postLikes(postId, userId) VALUES(%s, %s)"
            db.execute(query, [post_id, user_id])
            message = f"{user_id} liked post {post_id}"
        return {"message": message}
    except Exception as e:
        raise Exception(e)
    
# This should be a private method
def countLikesInPost(post_id):
    try:
        db = database()
        query = "SELECT COUNT(*) FROM postLikes WHERE postId = %s"
        result = db.execute(query, [post_id])
        return result[0]
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