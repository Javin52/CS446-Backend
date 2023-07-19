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


## Running
To run use 
```
flask --app src --debug run
```
in the case the .flaskenv variables do not seem to work

The --debug flag allows for hot deploy during testing, so the server does not have to be restarted while making changes