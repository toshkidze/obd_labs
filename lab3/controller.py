from consolemenu import SelectionMenu

import model
import view


def display_main_menu(err='', table=None):
    tables = list(model.TABLES.keys())

    menu = SelectionMenu(tables + ['Make commit'], subtitle=err,
                         title="Select a table to work with:")
    menu.show()


    index = menu.selected_option
    if index < len(tables):
        table = tables[index]
        display_secondary_menu(table)
    elif index == len(tables):
        model.commit()
        display_main_menu('Commit was made successful')


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
