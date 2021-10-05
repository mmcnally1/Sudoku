import sys
from collections import deque
import copy

def readInput(randomAssignment):
    assignment = sys.stdin.readline().strip()
    assignment = assignment.replace(' ', '')
    if len(assignment) != 81:
        return randomAssignment
    return assignment

class SudokuSolver:
    def __init__(self):
        self.assignment = [[0 for i in range(9)] for i in range(9)]
        self.domains = {}
        self.arcs = {}

    def display(self):
        for i in range(9):
            print(self.assignment[i])
        print("\n")
    
    def createDomains(self):
        for i in range(9):
            for j in range(9):
                self.domains[(i,j)] = []
                for k in range(9):
                    self.domains[(i,j)].append(k + 1)
    
    def createArcs(self):
        for i in range(9):
            for j in range(9):
                self.arcs[(i,j)] = []
        for arc in self.arcs:
            for i in range(9):
                if i != arc[1]:
                    self.arcs[arc].append((arc[0], i))
            for i in range(9):
                if i != arc[0]:
                    self.arcs[arc].append((i, arc[1]))
                    
            x = (arc[0] // 3) * 3
            y = (arc[1] // 3) * 3
            for i in range(3):
               for j in range(3):
                    if (x + i, y + j) != arc:
                        if (x + i, y + j) not in self.arcs[arc]:
                            self.arcs[arc].append((x + i, y + j))
    
    def createAssignment(self, assignment):
        pos = 0
        for i in range(9):
            for j in range(9):
                self.assignment[i][j] = int(assignment[pos])
                if int(assignment[pos]) != 0:
                    self.domains[(i,j)] = []
                    self.domains[(i,j)].append(int(assignment[pos]))
                pos += 1

    def AC3(self):
        q = deque()
        for arc in self.arcs:
            for var in self.arcs[arc]:
                q.append((arc, var))
        while q:
            (Xi, Xj) = q.popleft()
            if self.revise(Xi, Xj):
                if len(self.domains[Xi]) == 0:
                    return False
                for Xk in self.arcs[Xi]:
                    if Xk != Xj:
                        q.append((Xk, Xi))
        return True
        

    def revise(self, Xi, Xj):
        revised = False
        for x in self.domains[Xi]:
            needToRevise = True
            for y in self.domains[Xj]:
                if y != x:
                    needToRevise = False
            if needToRevise:
                self.domains[Xi].remove(x)
                revised = True
        return revised


    def backtrackSearch(self):
        if self.backtrack() != "failure":
            self.display()
        else:
            print("Could not solve")

    def backtrack(self):
        if self.isAssignmentComplete():
            return self.assignment
        var = self.selectUnassignedVariable()
        for value in self.orderDomainValues(var):
            if self.isAssignmentConsistent(var, value):
                self.assignment[var[0]][var[1]] = value
                result = self.backtrack()
                if result != "failure":
                    return result
                self.assignment[var[0]][var[1]] = 0
        return "failure"

    def isAssignmentComplete(self):
        for i in range(9):
            for j in range(9):
                if self.assignment[i][j] == 0:
                    return False
        return True

    def isAssignmentConsistent(self, Xi, x):
        assignment = copy.deepcopy(self.assignment)
        assignment[Xi[0]][Xi[1]] = x
        isConsistent = True
        if not self.isNodeConsistent(assignment, Xi):
            isConsistent = False
        for Xj in self.arcs[Xi]:
            if not self.isArcConsistent(assignment, Xi, Xj):
                isConsistent = False
        return isConsistent
    
    def isNodeConsistent(self, assignment, Xi):
        if (assignment[Xi[0]][Xi[1]] >= 0 and 
            assignment[Xi[0]][Xi[1]] <= 9):
            return True
        else:
            return False

    def isArcConsistent(self, assignment, Xi, Xj):
        if assignment[Xi[0]][Xi[1]] != self.assignment[Xj[0]][Xj[1]]:
            return True
        else:
            return False

    def selectUnassignedVariable(self):
        for i in range(9):
            for j in range(9):
                if self.assignment[i][j] == 0:
                    return (i,j)

    def orderDomainValues(self, var):
        return self.domains[var]

if __name__ == "__main__":
    easy1 = "060000230305090416200604009100800604090000070708006001500901003836050102014000060"
    assignment = readInput(easy1)
    solver = SudokuSolver()
    solver.createDomains()
    solver.createArcs()
    solver.createAssignment(assignment)
    solver.display()
    solver.AC3()
    solver.backtrackSearch()
