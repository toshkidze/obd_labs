from consolemenu import SelectionMenu

import model
import view


def display_main_menu(err='', table=None):
    tables = list(model.TABLES.keys())

    menu = SelectionMenu(tables + ['Search users by question.question_datetime',
                                   'Search questions by answer.answer_is_valid',
                                   'Create 10_000 random questions',
                                   'Full Text Search without word',
                                   'Full Text Search by phrase'], subtitle=err,
                         title="Select a table to work with:")
    menu.show()

    index = menu.selected_option
    if index < len(tables):
        table = tables[index]
        display_secondary_menu(table)
    elif index == len(tables):
        search_users_by_question_date()
    elif index == len(tables) + 1:
        search_questions_by_answer_is_valid()
    elif index == len(tables) + 2:
        create_random_questions()
    elif index == len(tables) + 3:
        full_text_search_without_word()
    elif index == len(tables) + 4:
        full_text_search_by_phrase()
    else:
        print('Bye! Have a nice day!')


def display_secondary_menu(table, subtitle=''):
    opts = ['Select', 'Insert', 'Update', 'Delete']
    steps = [select, insert, update, delete, display_main_menu]

    menu = SelectionMenu(
        opts, subtitle=subtitle,
        title=f'Selected table "{table}"', exit_option_text='Go back',)
    menu.show()
    index = menu.selected_option
    steps[index](table=table)


def select(table):
    query = view.multiple_input(table, 'Enter requested fields:')
    data = model.get(table, query)
    view.print_entities(table, data)
    view.press_enter()
    display_secondary_menu(table)


def insert(table):
    data = view.multiple_input(table, 'Enter new fields values:')
    model.insert(table, data)
    display_secondary_menu(table, 'Insertion was made successfully')


def update(table):
    condition = view.single_input(
        table, 'Enter requirement of row to be changed:')
    query = view.multiple_input(table, 'Enter new fields values:')

    model.update(table, condition, query)
    display_secondary_menu(table, 'Update was made successfully')


def delete(table):
    query = view.multiple_input(
        table, 'Enter requirement of row to be deleted:')

    model.delete(table, query)
    display_secondary_menu(table, 'Deletion was made successfully')


def search_users_by_question_date():
    dates = view.specified_input(msg='Enter datetime range divided in format <dd/mm/yyyy hh:mm:ss>-<dd/mm/yyyy hh:mm:ss>:').split('-')
    data = model.search_users_by_question_date(dates)
    view.print_entities(f'User who wrote questions in date range={dates}', data)
    view.press_enter()
    display_main_menu()


def search_questions_by_answer_is_valid():
    query = view.specified_input(
        'is_valid', 'Enter answer.is_valid value:'
    ).lower() in ['true', 't', 'yes', 'y', '+']

    data = model.search_questions_by_answer_is_valid(query)
    view.print_entities(
        f'Questions which where answered with answer.is_valid={query}:', data)
    view.press_enter()
    display_main_menu()


def full_text_search_without_word():
    query = view.specified_input(
        'word', 'Enter your word to be absent in the document:')
    data = model.full_text_search_without_word(query)
    view.print_entities(
        f'Documents without word=`{query}`', data)
    view.press_enter()
    display_main_menu()


def full_text_search_by_phrase():
    query = view.specified_input(
        'phrase', 'Enter your phrase to be found in document:')
    data = model.full_text_search_by_phrase(query)
    view.print_entities(
        f'Documents with phrase=`{query}`', data)
    view.press_enter()
    display_main_menu()


def create_random_questions():
    model.create_random_questions()
    display_main_menu('10_000 random questions were successfully added')
