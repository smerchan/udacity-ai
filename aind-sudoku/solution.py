assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in  A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#
# Add diagonal boxes to the peer list
# Box on the left or right diagonal should have unique value 
# i.e constraint propogation should check for box having unique
# value within the row, column, square and additionally if the box
# is on the diagonal, it should check for uniqueness along the diagonal
#
diagonal1 = [rd+cols[i] for i, rd in enumerate(rows)]
diagonal2 = [rd+cols[8-i] for i, rd in enumerate(rows)]
diag_unitlist = unitlist + [diagonal1, diagonal2]

diag_units = dict((s, [u for u in diag_unitlist if s in u]) for s in boxes)
diag_peers = dict((s, set(sum(diag_units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

#
# Naked Twin Problem
#
def match_and_eliminate_twin_box_in_row(values, box):
    """
    Look for twin boxes in a row. i.e. find a pair of boxes
    with identical 2 digit values.
    Eliminate twin box values from all other boxes within the row
    """
    match_list = []
    eliminated = False

    # Find all matching boxes in the row 
    for elem in cross(box[0], cols):
        if values[elem] == values[box]:
            match_list.append(elem)

    # If this is a twin match, eliminate twin digits from 
    # any other boxes in the row that has these twin digits
    if len(match_list) == 2:
        for elem in cross(box[0], cols):
            if elem not in match_list:
               for digit in values[box]:
                   if len(values[elem]) >= 2:
                        before_value = values[elem]
                        values[elem] = values[elem].replace(digit, '')
                        if values[elem] != before_value:
                            eliminated = True
    return eliminated

def match_and_eliminate_twin_box_in_col(values, box):
    """
    Look for twin boxes in a column. i.e. find a pair of boxes
    with identical 2 digit values.
    Eliminate twin box values from all other boxes within the column
    """
    match_list = []
    eliminated = False

    # Find all matching boxes in the row 
    for elem in cross(rows, box[1]):
        if values[elem] == values[box]:
            match_list.append(elem)

    # If this is a twin match, eliminate twin digits from 
    # any other boxes in the col that has these twin digits
    if len(match_list) == 2:
        for elem in cross(rows, box[1]):
            if elem not in match_list:
               for digit in values[box]:
                   if len(values[elem]) >= 2:
                        before_value = values[elem]
                        values[elem] = values[elem].replace(digit, '')
                        if values[elem] != before_value:
                            eliminated = True
    return eliminated

def match_and_eliminate_twin_box_in_square(values, box):
    """
    Look for twin boxes in a square. i.e. find a pair of boxes
    with identical 2 digit values.
    Eliminate twin box values from all other boxes within the square
    """
    match_list = []
    eliminated = False

    for rs in ('ABC', 'DEF', 'GHI'):
        if box[0] in rs:
            box_rs = rs

    for cs in ('123', '456', '789'):
        if box[1] in cs:
            box_cs = cs

    box_square_units = [cross(rs, cs) for rs in box_rs for cs in box_cs]
    # Find all matching boxes in the square
    for elem_list in box_square_units:
        for elem in elem_list:
            if values[elem] == values[box]:
                match_list.append(elem)

    # If this is a twin match, eliminate twin digits from 
    # any other boxes in the squre that has these twin digits
    if len(match_list) == 2:
       for elem_list in box_square_units:
            for elem in elem_list:
                if elem not in match_list:
                   for digit in values[box]:
                       if len(values[elem]) >= 2:
                            before_value = values[elem]
                            values[elem] = values[elem].replace(digit, '')
                            if values[elem] != before_value:
                                eliminated = True
    return eliminated

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    no_more_twins = False
    while not no_more_twins:
        # Scan through the board looking for boxes with 2 digit values
        eliminated_count = 0
        for box, value in values.items():
            if len(value) == 2:
                if match_and_eliminate_twin_box_in_row(values, box):
                    eliminated_count += 1
                if match_and_eliminate_twin_box_in_col(values, box):
                    eliminated_count += 1
                if match_and_eliminate_twin_box_in_square(values, box):
                    eliminated_count += 1
        if eliminated_count == 0:
           no_more_twins = True
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    if len(grid) != 81:
        print("Invalig grid: %r" % grid)
        return {}

    values = dict(zip(cross(rows, cols), grid))
    for k, v in values.items():
        if v == '.':
            values[k] = '123456789'
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    new_values = values.copy()
    solved_values = [box for box in new_values.keys() if len(new_values[box]) == 1]
    for box in solved_values:
        digit = new_values[box]
        for peer in diag_peers[box]:
            new_values[peer] = new_values[peer].replace(digit,'')
            assign_value(new_values, peer, new_values[peer])
    return new_values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a
    value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    new_values = values.copy()
    for unit in diag_unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in new_values[box]]
            if len(dplaces) == 1:
                new_values[dplaces[0]] = digit
                assign_value(new_values, dplaces[0], digit)
    return new_values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point,
    there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same,
    return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    new_values = values.copy()
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    stalled = False
    while not stalled:
        # keep track of boxes that have been solved so far
        solved_values_before = len([box for box in new_values.keys() if len(new_values[box]) == 1])

        # Eliminate values through constraint propogation 
        new_values = eliminate(new_values)

        # Identify digits that can be placed in only one box
        # within a row, a column, a square or a diagonal 
        new_values = only_choice(new_values)

        # Check if we solved any new boxes 
        solved_values_after = len([box for box in new_values.keys() if len(new_values[box]) == 1])

        # if new new boxes were solved - no further elimination 
        # can be done through constraint propogation 
        stalled = solved_values_before == solved_values_after

        if len([box for box in new_values.keys() if len(new_values[box]) == 0]):
            return False

    return new_values

def search(values):
    """
    Using depth-first search and propagation,
    create a search tree and solve the sudoku.
    """
    # First, reduce the puzzle using the previous function
    new_values = reduce_puzzle(values.copy())

    if new_values is False:
        return False

    # Return if puzzle is solved
    if all(len(new_values[s]) == 1 for s in boxes):
        return new_values

    # Use naked twin rule to go further 
    #values = naked_twins(values)

    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(new_values[s]), s) for s in boxes if len(new_values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, 
    # and if one returns a value (not False), return that answer
    for digit in new_values[s]:
        copy_values = new_values.copy()
        copy_values[s] = digit
        solution = search(copy_values)
        if solution:
            return solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid = grid_values(grid)
    solution = search(grid)
    if solution:
        return solution

if __name__ == '__main__':
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    #diag_sudoku_grid  = '..9.8.....5..3914..4...1..5.38......61..9..52......89.5..3...1..7491..8.....5.7..'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
