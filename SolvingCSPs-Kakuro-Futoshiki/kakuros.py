from __future__ import print_function

from ortools.sat.python import cp_model

with open("kakuro_input.txt", 'r') as f:
    lines = f.readlines()

values = []
for line in lines:
    cs = line.split(',')          # ['22', ' 18', ' 7\n']
    for value in cs:
        value = value.strip()
        if "\n" in value:
            value = value[:-2]
            values.append(value)
            continue 
        values.append(value)

out= open("kakuro_output.txt","w+")

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):

        self.__solution_count += 1
        
        out.write("x, " + values[0] + ", " + values[1] + ", " + values[2])
        out.write("\n" + values[3])
        i=0
        for v in self.__variables:
            if i < 3:
                out.write(", %i" % (self.Value(v)))
                i = i+1
                continue
            elif i == 3:
                out.write("\n" + values[4])
                i = i + 1
            elif i == 7:
                out.write("\n" + values[5])
                i = i+1

            if i < 7:
                out.write(", %i" % (self.Value(v)))
                i = i+1
                continue
            elif i < 11:
                out.write(", %i" % (self.Value(v)))
                i = i+1
                continue
        

    def solution_count(self):
        return self.__solution_count


def CPIsFunSat():
    """Solve the CP+IS+FUN==TRUE cryptarithm."""
    # Constraint programming engine
    model = cp_model.CpModel()

    base = 10

    x1 = model.NewIntVar(1, base - 1,'x1')
    x2 = model.NewIntVar(1, base - 1,'x2')
    x3 = model.NewIntVar(1, base - 1,'x3')
    y1 = model.NewIntVar(1, base - 1,'y1')
    y2 = model.NewIntVar(1, base - 1,'y2')
    y3 = model.NewIntVar(1, base - 1,'y3')
    z1 = model.NewIntVar(1, base - 1,'z1')
    z2 = model.NewIntVar(1, base - 1,'z2')
    z3 = model.NewIntVar(1, base - 1,'z3')

    # We need to group variables in lists to use the constraint AllDifferent.
    letters = [x1, x2, x3, y1, y2, y3, z1, z2, z3]
    row1 = [x1, x2, x3]
    row2 = [y1, y2, y3]
    row3 = [z1, z2, z3]
    column1 = [x1, y1, z1]
    column2 = [x2, y2, z2]
    column3 = [x3, y3, z3]

    # Define constraints
    model.AddAllDifferent(row1)
    model.AddAllDifferent(row2)
    model.AddAllDifferent(row3)
    model.AddAllDifferent(column1)
    model.AddAllDifferent(column2)
    model.AddAllDifferent(column3)

    model.Add(x1 + x2 + x3 == int(values[3]))
    model.Add(y1 + y2 + y3 == int(values[4]))
    model.Add(z1 + z2 + z3 == int(values[5]))
    model.Add(x1 + y1 + z1 == int(values[0]))
    model.Add(x2 + y2 + z2 == int(values[1]))
    model.Add(x3 + y3 + z3 == int(values[2]))

    ### Solve model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(letters)
    status = solver.SearchForAllSolutions(model, solution_printer)

if __name__ == '__main__':
    CPIsFunSat()
    out.close()
