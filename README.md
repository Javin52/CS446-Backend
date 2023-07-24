## Quick Description ##
This is the backend code for CS 446 fitness app.
The main content for the back end code is related to the social component of the application. 

## Endpoints supported ##
- upload routine
- get list of user posts
- create/edit/delete post
- create/edit/delete comment
- like comment
- follow user
- search tutorial

## Notes:
- In this, I have made all comments to be the same structure as a normal post, meaning that a comment is really a post just associated to another post. With this, some methods like get a specific comment, edit a comment, and delete comment can be called using the methods dedicated to posts. The only comment specific methods are create comment and get all comments for a user and post
- I dont think there would ever be a use case where we would want to just remove the routine from a post, so that method does not exist, but you can delete the post to stop sharing the routine.

# Getting Started

To run locally, first start your MySQL server and in your MySQL Command Line Client, run the following

```
CREATE DATABASE CS446
```

Then, run the following in your terminal under this directory to instantiate the database, replacing user, password and host with your MySQL credentials

```
mysql -u {user} --password={password} -h {host} < CreateTables.sql
```

Finally, create an env.py file in this directory with the following lines, replacing the values with your corresponding details

```
DB_USER = {DB User}
DB_NAME = {DB Name}
DB_PASSWORD = {MySQL Password}
DB_HOST = {MySQL Host}
DB_PORT = {MySQL Port Number}
```

## Running
To run use 
```
flask --app src --debug run
```
in the case the .flaskenv variables do not seem to work

The --debug flag allows for hot deploy during testing, so the server does not have to be restarted while making changes

## Running in Ubuntu
https://medium.com/@prithvishetty/deploying-multiple-python-3-flask-apps-to-aws-using-nginx-d78e9477f96d

For reference

sudo service CS446-Backend restart


## API Reference

Note that there are two types of "comments", one is a direct comment of a routine, which we will call a primary comment, and the other is a nested comment, or comments of a primary comemnt, which we will call secondary comments.

|URL| Method | Description|
|------------|-------------|-------------------------------------|
| /hello | GET | Test if server is working |
| /signup | POST | Sign up a new user (register) |
| /login | POST | Validate returning user (sign/log in) |
| /commentRoutine/<routine_id> | GET | Gets all primary comments of the specified routine id |
| /commentRoutine/<routine_id> | POST | Creates a primary comment |
| /pimaryComments/<user_id> | GET | Returns all primary comments made by a user |
| /comment/<user_id>/<post_id> | GET | Return information about specific post_id (can be either a primary or secondary comment) |
| /comment/<user_id>/<post_id> | POST | edits the content of the specified primary or secondary comment | 
| /comment/<user_id>/<post_id> | DELETE | DELETE specific primary or secondary | 
| /user_comment/<user_id> | GET | Return all secondary comments of a user (If we want, this can be merged with /pimaryComments/<user_id>)|
| /user_comment/<user_id> | POST | create a seondary comment of a primary comment (this is the method called for nested comments) |
| /post_comment/<post_id> | GET | Returns all direct comments of a comment |
| /likeComment/<user_id>/<post_id> | POST | Likes a user's comment (works for both primary and secondary comments). If the user already liked the comment, it will then unlike it. |
| /likeRoutine/<user_id>/<routine_id> | POST | Likes a routine. Similar to likeComment, If the user has already liked the routine, then they will unlike it |
| communityRoutines/<index> | GET | Returns a list of community routines. The index acts like "a page in a book" so index 0 returns the first 100 routines, index 1 returns the second 100 routines (100-200) etc. |
| /routine/<user_id> | GET | gets the list of routine_ids created by the specified user_id |
| /routine/<user_id> | POST | create a routine, this can also be interpreted as sharing a routine to the community |
| /specificRoutine/<routine_id> | GET | Get details of a specific routine id |
| /specificRoutine/<routine_id> | POST | Edit a routine |
| /specificRoutine/<routine_id> | DELETE | Delete a routine |