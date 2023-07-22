USE CS446;

CREATE TABLE user (
    userId char(32) NOT NULL,
    email varchar(200) NOT NULL,
    username varchar(100) NOT NULL,
    userPassword varchar(100),
    PRIMARY KEY(userId),
    UNIQUE (email)
);

CREATE TABLE followers (
    userId char(32) NOT NULL,
    follows char(32) NOT NULL,
    PRIMARY KEY(userId, follows),
    FOREIGN KEY (userId) REFERENCES user(userId) ON DELETE CASCADE,
    FOREIGN KEY (follows) REFERENCES user(userId) ON DELETE CASCADE
);

CREATE TABLE post (
    postId char(32) NOT NULL,
    user char(32) NOT NULL,
    content varchar(500),
    PRIMARY KEY (postId),
    FOREIGN KEY (user) REFERENCES user(userId)
);

CREATE TABLE comments (
    postId char(32) NOT NULL,
    comment char(32),
    PRIMARY KEY (postId, comment),
    FOREIGN KEY (postId) REFERENCES post(postId) ON DELETE CASCADE,
    FOREIGN KEY (comment) REFERENCES post(postId) ON DELETE CASCADE
);

CREATE TABLE routine (
    routineId char(32) NOT NULL,
    author char(32) NOT NULL,
    routine_name varchar(100) NOT NULL,
    description varchar(1000),
    PRIMARY KEY (routineId),
    FOREIGN KEY (author) REFERENCES user(userId)
);

CREATE TABLE exercise (
    routineId char(32) NOT NULL,
    exerciseId char(32) NOT NULL,
    exerciseName varchar(100) NOT NULL,
    calories int,
    sets int,
    reps int,
    weight int,
    weightType varchar(5),
    duration int,
    durationType varchar(10),
    distanct int,
    distanceType varchar(10),
    PRIMARY KEY (routineId, exerciseId),
    FOREIGN KEY (routineId) REFERENCES routine(routineId) ON DELETE CASCADE
);

CREATE TABLE routineComments (
    postId char(32) NOT NULL,
    routineId char(32) NOT NULL,
    PRIMARY KEY (postId, routineId),
    FOREIGN KEY (postId) REFERENCES post(postId) ON DELETE CASCADE,
    FOREIGN KEY (routineId) REFERENCES routine(routineId) ON DELETE CASCADE
);

CREATE TABLE routineLikes (
    routineId char(32) NOT NULL,
    userId char(32) NOT NULL,
    PRIMARY KEY (id, type, userId),
    FOREIGN KEY (routineId) REFERENCES routine(routineId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES user(userId) ON DELETE CASCADE
);

CREATE TABLE postLikes (
    postId char(32) NOT NULL,
    userId char(32) NOT NULL,
    PRIMARY KEY (id, type, userId),
    FOREIGN KEY (postId) REFERENCES post(postId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES user(userId) ON DELETE CASCADE
);

CREATE TABLE tutorials (
    exercise_name varchar(100),
    url varchar(250),
    PRIMARY KEY (exercise_name)
);