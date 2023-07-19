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
In this, I have made all comments to be the same structure as a normal post, meaning that a comment is really a post just associated to another post. With this, some methods like get a specific comment, edit a comment, and delete comment can be called using the methods dedicated to posts. The only comment specific methods are create comment and get all comments for a user and post

## Running
To run use 
```
flask --app src --debug run
```
in the case the .flaskenv variables do not seem to work

The --debug flag allows for hot deploy during testing, so the server does not have to be restarted while making changes