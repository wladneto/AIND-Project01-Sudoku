
from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
cols_rev = cols[::-1] #Inverse Cols
diagonal_1_units = [[rows[i]+cols[i] for i in range(len(rows))]] # Diagonal1 Like A1, B2, C3, D4...
diagonal_2_units = [[rows[i]+cols_rev[i] for i in range(len(rows))]] #Diagonal2 Like A9, B8, C7, D6...

unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units 
unitlist = unitlist + diagonal_1_units + diagonal_2_units #Add Diagnonals

# Must be called after all units (including diagonals) are added to the unitlist
#units = extract_units(unitlist, boxes) #old
#peers = extract_peers(units, boxes) #old
units = dict((s, [u for u in unitlist if s in u]) for s in boxes) #newunits with diagonals
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) #newunits with diagonals

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # TODO: Implement this function!
    # Passo 1 Selecionar os Boxes com 2 entradas 
    # New Box with 2 entrances
    naked_twin_dic = {}
    for unit in unitlist:
        pairdict = {} #Dicionario de possíveis pares # dict with possible pairs
        for box in unit:
            # Pssiveis canditados aos twins #Possible candidates for a naked twin (2)   
            if len(values[box]) == 2:
                if not values[box] in pairdict:
                    pairdict[values[box]] = [box] 
                else:
                    pairdict[values[box]].append(box)
        # Examinar os pares para substituilos
        for key in pairdict:
            # Se possui 2 keys é um nakedTwins
            if len(pairdict[key]) == 2:
                if not key in naked_twin_dic:
                    naked_twin_dic[key] = [unit]
                else:
                    naked_twin_dic[key].append(unit)
    # Remover os itens iguais para posibilidade de pares # Remove nakedtwins in pairs(peers)
    for key in naked_twin_dic:
        for unit in naked_twin_dic[key]:
            for box in unit:
                if values[box] != key:
                    assign_value(values, box, values[box].replace(key[0], ''))
                    assign_value(values, box, values[box].replace(key[1], ''))
    return values

def eliminate(values):
    # TODO: Copy your code from the classroom to complete this function
    # Wlad - OK
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for solved_val in solved_values:
        digit = values[solved_val]
        peers_solv = peers[solved_val]
        for peer in peers_solv:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    # TODO: Copy your code from the classroom to complete this function
    # Wlad - OK
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
                #values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = False
        while not stalled:
            solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
            values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
            values = only_choice(values)  
       # Wlad - OK (Call Naked Twins)
            values = naked_twins(values)        
        # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
            stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
            if len([box for box in values.keys() if len(values[box]) == 0]):
                return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
