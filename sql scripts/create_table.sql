CREATE TABLE user_status (
        id INTEGER NOT NULL, 
        name VARCHAR(30), 
        PRIMARY KEY (id)
);

CREATE TABLE tag (
        id INTEGER NOT NULL, 
        name VARCHAR(20), 
        PRIMARY KEY (id), 
        UNIQUE (name)
);

CREATE TABLE user (
        id INTEGER NOT NULL, 
        username VARCHAR(30), 
        email VARCHAR(60), 
        password VARCHAR(128), 
        status_id INTEGER, 
        PRIMARY KEY (id), 
        UNIQUE (username), 
        UNIQUE (email), 
        FOREIGN KEY(status_id) REFERENCES user_status (id)
);

CREATE TABLE note (
        id INTEGER NOT NULL, 
        name VARCHAR(50), 
        text VARCHAR(404), 
        number_of_moderators SMALLINT, 
        owner_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(owner_id) REFERENCES user (id) ON DELETE CASCADE
);


CREATE TABLE note_to_user (
        note_id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        PRIMARY KEY (note_id, user_id), 
        FOREIGN KEY(note_id) REFERENCES note (id), 
        FOREIGN KEY(user_id) REFERENCES user (id)
);

CREATE TABLE modifications (
        note_id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        date_of_modification DATETIME, 
        PRIMARY KEY (note_id, user_id), 
        FOREIGN KEY(note_id) REFERENCES note (id), 
        FOREIGN KEY(user_id) REFERENCES user (id)
);

CREATE TABLE tag_to_note (
        note_id INTEGER NOT NULL, 
        tag_id INTEGER NOT NULL, 
        PRIMARY KEY (note_id, tag_id), 
        FOREIGN KEY(note_id) REFERENCES note (id), 
        FOREIGN KEY(tag_id) REFERENCES tag (id)
);

