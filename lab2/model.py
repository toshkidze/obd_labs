import psycopg2

conn = psycopg2.connect("dbname='labs' user='anton'"
                        "host='localhost' password='password'")
cursor = conn.cursor()

TABLES = {
    'user': ('user_id', 'user_name', 'user_age'),
    'question': ('question_id', 'question_text', 'question_datetime', 'question_user_id'),
    'answer': ('answer_id', 'answer_text', 'answer_is_valid', 'answer_user_id', 'answer_question_id')
}


def insert(table_name, opts):
    try:
        cols = opts.keys()
        vals = [f"'{val}'" for val in opts.values()]
        command = f'insert into "{table_name}" ({", ".join(cols)}) ' + \
            f'values ({", ".join(vals)})'
        cursor.execute(command)
    finally:
        conn.commit()


def get(table_name, opts=None):
    command = f'select * from "{table_name}"'

    if opts:
        conditions = [f"{col}='{opts[col]}'" for col in opts]
        command = f'{command} where {" and ".join(conditions)}'

    cursor.execute(command)
    return cursor.fetchall(), TABLES[table_name]


def update(table_name, condition, opts):
    try:
        column, value = condition
        updates = ', '.join([f"{col} = '{opts[col]}'" for col in opts])
        command = f'update "{table_name}" set {updates} where {column}=\'{value}\''

        cursor.execute(command)
        conn.commit()
    finally:
        conn.commit()


def delete(table_name, opts):
    try:
        conditions = [f"{col}='{opts[col]}'" for col in opts]
        command = f'delete from "{table_name}" where {" and ".join(conditions)}'
        cursor.execute(command)
    finally:
        conn.commit()


def search_questions_by_answer_is_valid(is_valid):
    command = f'''
    select question_id, question_text, question_datetime, question_user_id from question
    join answer a on question.question_id = a.answer_question_id
    where answer_is_valid={is_valid}
    group by question_id;'''

    cursor.execute(command)
    return cursor.fetchall(), TABLES['question']


def search_users_by_question_date(dates):
    start, end = dates
    command = f"""
    select "user".user_id, user_name, user_age from "user"
    join question q on "user".user_id = q.question_user_id
    where question_datetime between '{start}' and '{end}'
    group by user_id;"""

    cursor.execute(command)
    return cursor.fetchall(), TABLES['user']


def full_text_search_without_word(word):
    command = f"""
    select question_text, answer_text from question
    join answer a on question.question_id = a.answer_question_id
    where to_tsvector(question_text) || to_tsvector(answer_text) @@ to_tsquery('!{word}');"""
    cursor.execute(command)
    return cursor.fetchall(), ('question_text', 'answer_text')


def full_text_search_by_phrase(phrase):
    command = f"""
    select ts_headline(question_text, phraseto_tsquery('{phrase}'), 'StartSel=\033[91m, StopSel=\033[0m'),
           ts_headline(answer_text, phraseto_tsquery('{phrase}'), 'StartSel=\033[91m, StopSel=\033[0m')
    from question join answer a on question.question_id = a.answer_question_id
    where to_tsvector(question_text) || to_tsvector(answer_text) @@ phraseto_tsquery('{phrase}');"""
    cursor.execute(command)
    return cursor.fetchall(), ('question_text', 'answer_text')


def create_random_questions():
    try:
        with open('sql/random.sql', 'r') as file:
            sql = file.read()
            cursor.execute(sql)
    finally:
        conn.commit()

