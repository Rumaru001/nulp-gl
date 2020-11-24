INSERT INTO user_status (name) VALUES ('user');

SELECT user_status.id AS user_status_id, user_status.name AS user_status_name 
FROM user_status WHERE user_status.name = 'user' LIMIT 1 OFFSET 0;

INSERT INTO tag (name) VALUES ('tag1');

INSERT INTO user (username, email, password, status_id) VALUES 
('tester2', 'tester2@gmail.com', 'pass2', 1);

INSERT INTO user (username, email, password, status_id) VALUES 
('tester1', 'tester1@gmail.com', 'pass1', 1);

INSERT INTO note (name, text, number_of_moderators, owner_id) VALUES 
('Second note', 'This is only a second note', 1, 1);

INSERT INTO note (name, text, number_of_moderators, owner_id) VALUES 
 ('Fisrt note', 'This is a very first note', 0, 2);

INSERT INTO tag_to_note (note_id, tag_id) VALUES (1, 1);
INSERT INTO note_to_user (note_id, user_id) VALUES (1, 2);