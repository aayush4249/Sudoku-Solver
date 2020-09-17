import random
import sys

# prints the board in a readable format
def print_board(board):
    row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    print ("\n   1 2 3 4 5 6 7 8 9\n")
    for x in range(0,9):
        word = row_labels[x] + '  '
        for y in range(0, 9):
            if(str(board[9 * x + y]) == '0'):
                word += '- '
            else:
                word += str(board[9 * x + y]) + ' '
        print(word)

# checks if the board is solved
def solved(domains, grids, variables):
    for e in variables:
        for neigh in grids:
            answers = list(range(1,10))
            for xi in neigh:
                if(int(domains[xi][0]) in answers): 
                    answers.remove(int(domains[xi][0]))
                else: 
                    return False
    return True

# checks to make sure the number is valid
def valid_choice(xi, constraints, assignment):

    for neigh in constraints[xi]:
        answers = list(range(1,10))
        if(int(assignment[xi][0]) != 0): 
            answers.remove(int(assignment[xi][0]))
        
        for value in neigh:
            complete = False
            for p_val in assignment[value]:
    
                if(complete == False and int(p_val) != 0 and p_val in answers): 
                    answers.remove(int(p_val)) 
                    complete = True
    
                if(complete == False and int(p_val) == 0): 
                    complete = True
     
            if(complete == False):
                return False  
    
    return True
 
# recursing backtracking algorithm
def backtracking(val, assignment, variables, constraints, orig_domains, grids):
    if(solved(assignment,grids,variables)):
        return True
    
    for x in orig_domains[val]:
        assignment[val] = [x]
        if(valid_choice(val, constraints, assignment)):

            passed = 0
            next_val = 0
            for var in variables:
                if(passed == 1 and len(orig_domains[var]) > 1): 
                    next_val = var
                    break
                if(var == val): 
                    passed = 1 
    
            if(next_val != 0):   
                if(backtracking(next_val, assignment, variables, constraints, orig_domains, grids)):
                    return True
            else:
                if(solved(assignment, grids, variables)): 
                    return True

    assignment[val] = [0]
    return False

# initialize the arcs
def initialize_arcs(variables, constraints):
    arcs = []
    for xi in variables:
        for neigh in constraints[xi]:
            for xj in neigh:
                arcs.append((xi,xj))
    return arcs

# create sudoku cell variables
def create_variables(column_letters):
    variables = []

    for letters in column_letters:
        for numbers in range(0, 9):
            variables.append(str(letters) + str(numbers))
    return variables

# creates the grids
def create_grids():
    return [
        ['A0', 'A1', 'A2', 'B0', 'B1', 'B2', 'C0', 'C1', 'C2'],
        ['A3', 'A4', 'A5', 'B3', 'B4', 'B5', 'C3', 'C4', 'C5'],
        ['A6', 'A7', 'A8', 'B6', 'B7', 'B8', 'C6', 'C7', 'C8'],
        ['D0', 'D1', 'D2', 'E0', 'E1', 'E2', 'F0', 'F1', 'F2'],
        ['D3', 'D4', 'D5', 'E3', 'E4', 'E5', 'F3', 'F4', 'F5'],
        ['D6', 'D7', 'D8', 'E6', 'E7', 'E8', 'F6', 'F7', 'F8'],
        ['G0', 'G1', 'G2', 'H0', 'H1', 'H2', 'I0', 'I1', 'I2'],
        ['G3', 'G4', 'G5', 'H3', 'H4', 'H5', 'I3', 'I4', 'I5'],
        ['G6', 'G7', 'G8', 'H6', 'H7', 'H8', 'I6', 'I7', 'I8']
    ]

# create the constraints for each cell
def create_constraints(grids, variables, column_letters):
    constraints = {}

    for letters in column_letters:
        row = []
        for numbers in range(0,9): 
            row.append(str(letters) + str(numbers))
        grids.append(row)
    
    # add columns to grids
    for numbers in range(0,9):
        row = []
        for letters in ['A','B','C','D','E','F','G','H','I']:
            row.append(str(letters) + str(numbers))
        grids.append(row)
    
    # add empty lists for our variables
    for xi in variables: 
        constraints[xi] = []
    
    # filling in the constraints
    for rows in grids:
        for xi in rows:
            index = rows.index(xi)
            constraints[xi].append(rows[:index] + rows[index + 1:]) 

    return constraints
   
# create cell domains
def create_domains(variables, sudoku_input):
    domains = {}
    filled_cells = 0
    for index, xi in enumerate(variables):
        if(int(sudoku_input[index]) == 0):
            domains[xi] = [1,2,3,4,5,6,7,8,9]
        else:
            domains[xi] = [int(sudoku_input[index])]
            filled_cells += 1
    return domains, filled_cells

# main function
def main():
    sudoku_input = input('Input an unsolved 9x9 unsolved sudoku: \n')
    sudoku_input = sudoku_input[:81]
    print("\nInput Board:\n")
    print_board(sudoku_input)

    # initialize variables
    column_letters = ['A','B','C','D','E','F','G','H','I']
    variables = create_variables(column_letters)

    # get our grid constraints
    grids = create_grids()
    constraints = create_constraints(grids, variables, column_letters)
    
    # create domains
    domains, filled_cells = create_domains(variables, sudoku_input)
    
    # any sudoku with less than 17 clues is not solvable
    if filled_cells < 17:
        print ("\nError! This board is not Solvable!!")
        return

    arcs = initialize_arcs(variables, constraints)

    Solution = True
    ac3_xis = 0

    # ac3 implementation
    while arcs:
        xi, xj = arcs.pop(0)

        # Revised Func
        revised = False
        for xi_sol in domains[xi]:
            passed = False
            for xj_sol in domains[xj]:
                if(xi_sol != xj_sol): 
                    passed = True
  
            if(passed == False): 
                #print("Domain Before Revision:", domains[xi])
                domains[xi].remove(xi_sol)
                #print("Domain Before Revision:", domains[xi])
                revised = True 
                ac3_xis += 1
 
        if revised:
            if (len(domains[xi]) == 0): 
                Solution = False
            for neigh in constraints[xi]:
                for xi3 in neigh:
                    if(xi3 != xj): 
                        arcs.append((xi3, xi))   

    selected = []
    answer_dict = dict()

    next_val = 0
    assignment = dict()

    # assign values
    for var in variables:
        if(len(domains[var]) == 1): 
            assignment[var] = domains[var]
        else: 
            assignment[var] = [0] 

    for var in variables:
        if(len(domains[var]) > 1): 
            next_val = var 
            break

    if(next_val != 0):
        backtracking(next_val, assignment, variables, constraints, domains, grids)
        answer_dict = assignment
    else:
        answer_dict = domains
 
    answer = ''
    solution_found = True

    for index, xi in enumerate(variables):
        try:
            answer = answer + str(answer_dict[xi][0])
        except IndexError:
            solution_found = False
  
    if(solution_found):
        print("\n")
        print ("Output Board:")
        print_board(answer)
    else:
        print ("Err: Board not solvable")
    return

main()