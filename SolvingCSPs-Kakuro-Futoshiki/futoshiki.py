from __future__ import print_function
from ortools.sat.python import cp_model

out= open("futoshiki_output.txt","w+")

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    
    def on_solution_callback(self):
        i = 0
        self.__solution_count += 1
        for v in self.__variables:
            if i == 0:
                out.write('%i' % self.Value(v))
                i=i+1
                continue
            elif i % 4 == 0:
                out.write('\n%i' % self.Value(v))
                i=i+1
                continue
            
            out.write(', %i' % self.Value(v))
            i=i+1
 
    def solution_count(self):
        return self.__solution_count

with open("futoshiki_input.txt", 'r') as f:
    lines = f.readlines()

def CPIsFunSat():
    # Constraint programming engine
    model = cp_model.CpModel()

    base = 5

    A1 = model.NewIntVar(1, base - 1,'A1')
    B1 = model.NewIntVar(1, base - 1,'B1')
    C1 = model.NewIntVar(1, base - 1,'C1')
    D1 = model.NewIntVar(1, base - 1,'D1')
    A2 = model.NewIntVar(1, base - 1,'A2')
    B2 = model.NewIntVar(1, base - 1,'B2')
    C2 = model.NewIntVar(1, base - 1,'C2')
    D2 = model.NewIntVar(1, base - 1,'D2')
    A3 = model.NewIntVar(1, base - 1,'A3')
    B3 = model.NewIntVar(1, base - 1,'B3')
    C3 = model.NewIntVar(1, base - 1,'C3')
    D3 = model.NewIntVar(1, base - 1,'D3')
    A4 = model.NewIntVar(1, base - 1,'A4')
    B4 = model.NewIntVar(1, base - 1,'B4')
    C4 = model.NewIntVar(1, base - 1,'C4')
    D4 = model.NewIntVar(1, base - 1,'D4')


    # We need to group variables in lists to use the constraint AllDifferent
    letters = [A1,A2,A3,A4,B1,B2,B3,B4,C1,C2,C3,C4,D1,D2,D3,D4]
    row1 = [A1,A2,A3,A4]
    row2 = [B1,B2,B3,B4]
    row3 = [C1,C2,C3,C4]
    row4 = [D1,D2,D3,D4]
    column1 = [A1,B1,C1,D1]
    column2 = [A2,B2,C2,D2]
    column3 = [A3,B3,C3,D3]
    column4 = [A4,B4,C4,D4]

    # Define constraints
    model.AddAllDifferent(row1)
    model.AddAllDifferent(row2)
    model.AddAllDifferent(row3)
    model.AddAllDifferent(row4)    
    model.AddAllDifferent(column1)
    model.AddAllDifferent(column2)
    model.AddAllDifferent(column3)
    model.AddAllDifferent(column4)

    for line in lines:
        cs = line.split(',')
        cs[1] = cs[1].strip()         # ['B2', '1']     # ['A1', 'A2']

        second = ""
        for letter in letters:
            if cs[0] == str(letter):
                first = letter
            if cs[1] == str(letter):
                second = letter
        
        if str(second) == "":
            model.Add(first == int(cs[1]))
        else:
            model.Add(first > second)

    
    ### Solve model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(letters)
    status = solver.SearchForAllSolutions(model, solution_printer)

if __name__ == '__main__':
    CPIsFunSat()
    out.close()
