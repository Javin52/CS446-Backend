from src.db import database
from src.posts import countLikesInPost, createDictOfPostResults, createUserPost


def createDictOfCommentResults(sqlResult):
    postdict = {}
    for post in sqlResult:
        tmpPostDict = {}
        postId = post[0]
        tmpPostDict['postId'] = postId
        tmpPostDict['user'] = post[1]
        tmpPostDict['content'] = post[2]
        tmpPostDict['comment'] = post[3]
        try:
            tmpPostDict['likes'] = countLikesInPost(postId)
        except Exception as e:
            tmpPostDict['likes'] = "-1"
        postdict[post[0]] = tmpPostDict
    return postdict

def createDictOfPostRoutine(sqlResult):
    postdict = {}
    for post in sqlResult:
        tmpPostDict = {}
        postId = post[0]
        tmpPostDict['postId'] = postId
        tmpPostDict['routineId'] = post[1]
        tmpPostDict['user'] = post[2]
        tmpPostDict['content'] = post[3]
        try:
            tmpPostDict['likes'] = countLikesInPost(postId)
        except Exception as e:
            tmpPostDict['likes'] = "-1"
        postdict[post[0]] = tmpPostDict
    return postdict

def getAllCommentsUser(user_id):
    try:
        db = database()
        query = "SELECT * " +\
                "FROM post p " +\
                "NATURAL JOIN " +\
                "comments c" +\
                "WHERE p.user = %s"
        result = db.execute(query, [user_id])
        postdict = createDictOfCommentResults(result)
        return ({"posts": postdict})
    except Exception as e:
        raise Exception(e)

def getAllCommentsofPost(post_id):
    try:
        db = database()
        query = "SELECT * " +\
                "FROM post p " +\
                "NATURAL JOIN " +\
                "comments c" +\
                "WHERE c.postId = %s"
        result = db.execute(query, [post_id])
        postdict = createDictOfCommentResults(result)
        return ({"posts": postdict})
    except Exception as e:
        raise Exception(e)
    

def getAllCommentsofRoutine(routine_id):
    try:
        db = database()
        query = "SELECT * " +\
                "FROM routineComments r " +\
                "NATURAL JOIN " +\
                "post p " +\
                "WHERE r.routineId = %s"
        result = db.execute(query, [routine_id])
        postdict = createDictOfPostRoutine(result)
        return ({"posts": postdict})
    except Exception as e:
        raise Exception(e)

def createUserComment(user_id, post_id, content):
    if post_id is None:
        raise Exception("Expected a post id of the post being commented")
    elif content is None:
        raise Exception("Expected content of the comment")
    try:
        post_result = createUserPost(user_id=user_id, content=content)
        post_result = post_result['post_id']
        db = database()
        query = "INSERT INTO comments(postId, comment) VALUES(%s, %s)"
        db.execute(query, [post_id, post_result])
        return {
            'message': 'comment successfuly created',
            'post_id': post_id,
            'comment_id': post_result 
            }
    except Exception as e:
        raise Exception(e)
