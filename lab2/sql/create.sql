CREATE TABLE "user" (
        user_id SERIAL NOT NULL,
        user_name VARCHAR NOT NULL,
        user_age INTEGER,
        PRIMARY KEY (user_id)
);

CREATE TABLE question (
        question_id SERIAL NOT NULL,
        question_text VARCHAR NOT NULL,
        question_datetime TIMESTAMP WITHOUT TIME ZONE,
        question_user_id INTEGER,
        PRIMARY KEY (question_id),
        FOREIGN KEY(question_user_id) REFERENCES "user" (user_id)
);

CREATE TABLE answer (
        answer_id SERIAL NOT NULL,
        answer_text VARCHAR NOT NULL,
        answer_is_valid BOOLEAN,
        answer_user_id INTEGER,
        answer_question_id INTEGER,
        PRIMARY KEY (answer_id),
        FOREIGN KEY(answer_user_id) REFERENCES "user" (user_id),
        FOREIGN KEY(answer_question_id) REFERENCES question (question_id)
);

INSERT INTO "user"(user_name, user_age) VALUES
    ('lolkek', 20),
    ('user', 20),
    ('user1234', 15),
    ('nagibator', 30),
    ('pro100', 12),
    ('sample', 11);

INSERT INTO question(question_text, question_datetime, question_user_id) VALUES
    ('Who are you?', '01/01/2015 01:00:00', 1),
    ('Is sky blue?', '01/01/2016 01:00:00', 2),
    ('Are you ok?', '01/01/2017 01:00:00', 2),
    ('How are you?', '01/01/2018 01:00:00', 3),
    ('Are you hungry?', '01/01/2019 01:00:00', 4);

INSERT INTO answer(answer_text, answer_is_valid, answer_user_id, answer_question_id) VALUES
    ('Human', True, 5, 1),
    ('No', False, 4, 2),
    ('Yep', True, 1, 2),
    ('Sure', True, 1, 3),
    ('I`m fine', False, 5, 4),
    ('I feel sad', True, 6, 4);