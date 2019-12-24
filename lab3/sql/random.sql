INSERT INTO question(question_text, question_datetime, question_user_id)
SELECT
       md5(g :: text),
       CURRENT_TIMESTAMP + ( g || 'minute' ) :: interval,
       1
FROM generate_series(1, 10000) as g;
