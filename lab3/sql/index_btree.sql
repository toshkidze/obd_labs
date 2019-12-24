create index btree_index on question using btree(question_id);

drop index btree_index;

explain select * from question;
explain select * from question where question_id = 1000;

select count(*) from question;