from src.db import database
from src.logger import logger
from src.comments import createUserComment
import uuid

def createDictOfRoutineInfo(routine_result):
    postList = []
    for routine in routine_result:
        tmp = {}
        routine_id = routine[0]
        tmp['routine_id'] = routine_id
        tmp['author'] = routine[1]
        tmp['routine_name'] = routine[2]
        tmp['description'] = routine[3]
        try:
            tmp['likes'] = countLikesInRoutine(routine_id)
        except Exception as e:
            tmp['likes'] = "-1"
        postList.append(tmp)
    return postList

def createDictOfExercises(sqlResult):
    postList = []
    for exercise in sqlResult:
        tmp = {}
        tmp['exercise_id'] = exercise[1]
        tmp['exercise_name'] = exercise[2]
        tmp['sets'] = exercise[3]
        tmp['reps'] = exercise[4]
        tmp['weight'] = exercise[5]
        tmp['weightType'] = exercise[6]
        tmp['duration'] = exercise[7]
        tmp['durationType'] = exercise[8]
        tmp['distanct'] = exercise[9]
        tmp['distanceType'] = exercise[10]
        postList.append(tmp)
    return postList

def getListofRoutines(user_id):
    try:
        db = database()
        query = "SELECT * " +\
                "FROM routine r " +\
                "WHERE r.author = %s"
        result = db.execute(query, [user_id])
        postdict = createDictOfRoutineInfo(result)
        return ({"routines": postdict})
    except Exception as e:
        raise Exception(e)
    
def getListofCommunityRoutines(index):
    try:
        db = database()
        log = logger()
        index = int(index) * 100
        query = "SELECT * FROM routine r LIMIT %s,%s"
        result = db.execute(query, [index, 100])
        postdict = createDictOfRoutineInfo(result)
        return ({"routines": postdict})
    except Exception as e:
        raise Exception(e)

def searchRoutineeByName(name):
    try:
        db = database()
        log = logger()
        searchQuery = "SELECT * FROM routine WHERE routine_name LIKE '%%s%'"
        result = db.execute(searchQuery, [name])
        postDict = createDictOfRoutineInfo(result)
        return ({'routines': postDict})
    except Exception as e:
        raise Exception(e)

def uploadRoutine(user_id, routine_name, exercises, description):
    if routine_name is None:
        raise Exception("Expected a routine name for the routine")
    elif exercises is None:
        raise Exception("Expected exercises for the routine")
    try:
        db = database()
        routine_id = uuid.uuid4().hex
        insertRoutineQuery = "INSERT INTO routine(routineId, author, routine_name, description) VALUES(%s, %s, %s, %s)"
        db.execute(insertRoutineQuery, [routine_id, user_id, routine_name, description])
        exerciseErrors = {}
        exercise_ids = []
        count = 1
        for exercise in exercises:
            try:
                exercise_id = uuid.uuid4().hex
                exercise_ids.append(exercise_id)
                listOfVals = [routine_id, exercise_id]
                # This might be able to be shorter with list comprehension of the dict and mult var decalration
                # not too sure maybe ill try it later if there is time
                listOfVals.append(exercise.get('exerciseName', None))
                listOfVals.append(exercise.get('sets', None))
                listOfVals.append(exercise.get('reps', None))
                listOfVals.append(exercise.get('weight', None))
                listOfVals.append(exercise.get('weightType', None))
                listOfVals.append(exercise.get('duration', None))
                listOfVals.append(exercise.get('durationType', None))
                listOfVals.append(exercise.get('distanct', None))
                listOfVals.append(exercise.get('distanceType', None))
                exericseQuery = "INSERT INTO exercise(routineId, exerciseId, exerciseName, sets, reps, "+\
                    "weight, weightType, duration, durationType, distanct, distanceType) "+\
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                db.execute(exericseQuery, listOfVals)
                count += 1
            except Exception as e:
                exerciseErrors[count] = e
        return {
            'message': 'routine successfuly created',
            'routine_id': routine_id,
            'exercise_ids': exercise_ids,
            'errorMessages': exerciseErrors 
            }
    except Exception as e:
        raise Exception(e)

def getSpecificRoutine(routine_id):
    try:
        db = database()
        routine_query = "SELECT * FROM routine WHERE routineId = %s"
        routine = db.execute(routine_query, [routine_id])
        routine_info = createDictOfRoutineInfo(routine)[routine_id]
        exercise_query = "SELECT * FROM exercise WHERE routineId = %s"
        exercises = db.execute(exercise_query, [routine_info['routine_id']])
        exercise_info = createDictOfExercises(exercises)
        return {
            'routine_info': routine_info,
            'exercise_info': exercise_info
        }
    except Exception as e:
        raise Exception(e)

# TODO
def editRoutine():
    return "TODO"

def deleteRoutine(routine_id):
    try:
        db = database()
        query = "DELETE FROM routine WHERE routineId = %s"
        db.execute(query, [routine_id])
        message = f"Deleted routine id: {routine_id}"
        return {"message": message}
    except Exception as e:
        raise Exception(e)

def commentRoutine(user_id, content, routine_id):
    if routine_id is None:
        raise Exception("Expected a routine id of the routine being commented")
    elif content is None:
        raise Exception("Expected content of the comment")
    try:
        post_result = createUserComment(user_id=user_id, content=content)
        post_result = post_result['post_id']
        db = database()
        query = "INSERT INTO postExercise(postId, routineId) VALUES(%s, %s)"
        db.execute(query, [post_result, routine_id])
        return {
            'message': 'Routine Comment Successfuly Created',
            'post_id': post_result,
            'routine_id': routine_id 
            }
    except Exception as e:
        raise Exception(e)

# This should be a private method
def countLikesInRoutine(routine_id):
    try:
        db = database()
        query = "SELECT COUNT(*) FROM routineLikes WHERE routineId = %s"
        result = db.execute(query, [routine_id])
        return result[0]
    except Exception as e:
        raise Exception(e)

def likeRoutine(user_id, routine_id):
    print(user_id)
    print(routine_id)
    try:
        db = database()
        hasLikedQuery = "SELECT * FROM routineLikes WHERE routineId = %s AND userId = %s"
        result = db.execute(hasLikedQuery, [routine_id, user_id])
        if result == []:
            query = "INSERT INTO routineLikes(routineId, userId) VALUES(%s, %s)"
            db.execute(query, [routine_id, user_id])
            message = f"{user_id} liked post {routine_id}"
        else:
            query = "DELETE FROM routineLikes WHERE routineId = %s AND userId = %s"
            db.execute(query, [routine_id, user_id])
            message = f"{user_id} disliked post {routine_id}"
        return {"message": message}
    except Exception as e:
        raise Exception(e)

# def postRoutine(user_id, category, content, routine_id):
#     if routine_id is None:
#         raise Exception("Expected a routine id of the routine being commented")
#     elif content is None:
#         raise Exception("Expected content of the comment")
#     try:
#         post_result = createUserComment(user_id=user_id, content=content, category=category)
#         post_result = post_result['post_id']
#         db = database()
#         query = "INSERT INTO postExercise(postId, routineId) VALUES(%s, %s)"
#         db.execute(query, [post_result, routine_id])
#         return {
#             'message': 'Routine Post successfuly created',
#             'post_id': post_result,
#             'routine_id': routine_id 
#             }
#     except Exception as e:
#         raise Exception(e)