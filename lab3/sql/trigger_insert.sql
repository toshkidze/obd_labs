create or replace function before_insert_question()
returns trigger
language plpgsql
as $$
begin
    if NEW.question_text LIKE '%?' then
        return NEW;
    end if;
    raise exception 'question text should end with `?`';
end;
$$;

drop trigger before_insert on question;

create trigger before_insert before insert on question
    for each row execute procedure before_insert_question();

insert into question(question_text, question_user_id) values ('are you ok', 1);
insert into question(question_text, question_user_id) values ('are you ok?', 1);
