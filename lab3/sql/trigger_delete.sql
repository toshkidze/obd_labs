create or replace function before_delete_question()
returns trigger
language plpgsql
as $$
declare
    all_questions cursor is select * from question;
    question_count integer = 0;
begin
        for q in all_questions loop
        question_count := question_count + 1;
    end loop;
    if question_count <= 10 then
        raise exception 'At least 10 questions should be in table';
    end if;
    return old;
end;
$$;

drop trigger before_delete on question;

create trigger before_delete before delete on question
    for each row execute procedure before_delete_question();

select * from question;


select count(*) from question;
delete from question where question_id = 1780013;
select count(*) from question;
delete from question where question_id = 1780014;
select count(*) from question;
