create index brin_index on question using brin(question_datetime);

drop index brin_index;

select count(*) from question;

explain select * from question;
explain select * from question where question_datetime between '2005-01-01 00:00:00' and '2015-01-01 00:00:00';


