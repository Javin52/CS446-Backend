from src.db import database
import uuid

def createDictOfPostResults(sqlResult):
    postdict = {}
    for post in sqlResult:
        tmpPostDict = {}
        tmpPostDict['postId'] = post[0]
        tmpPostDict['user'] = post[1]
        tmpPostDict['category'] = post[2]
        tmpPostDict['likes'] = post[3]
        tmpPostDict['content'] = post[4]
        postdict[post[0]] = tmpPostDict
    return postdict

def getUserPosts(user_id):
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

def createUserPost(user_id, category, content):
    try:
        post_id = uuid.uuid4().hex
        db = database()
        query = "INSERT INTO post(postId, user, category, likes, content) VALUES(%s, %s, %s, %s, %s)"
        db.execute(query, [post_id, user_id, category, 0, content])
        return {'message': 'Post successfully create', 'post_id': post_id}
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

def editUserPost(user_id, post_id, newContent, Category):
    try:
        db = database()
        conditions = ""
        conditionVars = []
        if newContent is None and Category is None: 
            return "this should not have been passed"
        if newContent is not None:
            conditions += "content = %s "
            conditionVars.append(newContent)
        if Category is not None:
            conditions += "category = %s "
            conditionVars.append(Category)
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