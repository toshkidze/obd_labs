import model

COLUMN_WIDTH = 25


def print_entities(table, data):
    entities = data
    if not entities:
        return

    cols = entities[0].get_columns()
    separator_line = '-' * COLUMN_WIDTH * len(cols)

    print(f'Working with table "{table}"', end='\n\n')
    print(separator_line)
    print(''.join([f'{col}     |'.rjust(COLUMN_WIDTH, ' ') for col in cols]))
    print(separator_line)

    for entity in entities:
        print(''.join([f'{val}     |'.rjust(COLUMN_WIDTH, ' ') for val in entity.get_values()]))
    print(separator_line)


def specified_input(colname=None, msg=None):
    if msg:
        print(msg)
    if colname:
        print(f'{colname}=', end='')
    return input()


def single_input(tname, msg):
    print(msg)
    print('(use format <attribute>=<value>)')
    print(f'({"/".join(model.TABLES[tname])})', end='\n\n')

    while True:
        data = input()
        if not data or data.count('=') != 1:
            print('Invalid input, try one more time')
            continue

        data = data.split('=')
        col, val = data[0].strip(), data[1].strip()
        if col.lower() in [tcol.lower() for tcol in model.TABLES[tname]]:
            return col, val
        else:
            print(f'Invalid column name "{col}" for table "{tname}"')


def multiple_input(tname, msg):
    print(msg)
    print('(use format <attribute>=<value>)')
    print(f'({"/".join(model.TABLES[tname])})', end='\n\n')

    res = {}
    while True:
        data = input()
        if not data:
            break
        if data.count('=') != 1:
            print('Invalid input')
            continue

        data = data.split('=')
        col, val = data[0].strip(), data[1].strip()
        if col.lower() in [tcol.lower() for tcol in model.TABLES[tname]]:
            res[col] = val
        else:
            print(f'Invalid column name "{col}" for table "{tname}"')

    return res


def multiline_input(msg):
    print(msg, end='\n\n')

    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    return '\n'.join(lines)


def press_enter():
    input()