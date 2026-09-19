import copy
import time
from collections import Counter

class Node:
    def __init__(self, parent, matrix, arrCompleted, n, m, ntubes, lastMove, depth, evaluatedValue):
        self.parent = parent
        self.matrix = matrix
        self.arrCompleted = arrCompleted
        self.lastMove = lastMove
        self.depth = depth
        self.evaluatedValue = evaluatedValue
        self.n = n
        self.m = m
        self.ntubes = ntubes

    def getMatrix(self):
        return self.matrix
    
    def getArrCompleted(self):
        return self.arrCompleted
    
    def getLastMove(self):
        return self.lastMove
    
    def getDepth(self):
        return self.depth
    
    def getEvaluatedValue(self):
        return self.evaluatedValue
    
    def getParent(self):
        return self.parent
    
    def moveBall(self, fromCol, toCol):
        num = self.matrix[fromCol].pop(-1)
        self.matrix[toCol].append(num)
        if self.checkCompleted(self.matrix, toCol):
            self.arrCompleted[toCol] = 1
        self.lastMove = (fromCol, toCol)

    def evaluateState(self):
        for column in self.matrix:
            numCount = Counter(column)
            if len(column) > 1:
                for common in numCount.most_common(1):
                    commonNumber = common[0]
                for i in range(0, len(column)):
                    if column[i] == commonNumber:
                        continue
                    else:
                        self.evaluatedValue += (len(column) - i)
                        break
            elif len(column) == 1:
                self.evaluatedValue += 1

    def evaluateState2(self):
        for column in self.matrix:
            if len(column) == 0:
                continue
            else:
                num = column[0]
            for i in range(0, len(column)):
                if column[i] == num:
                    self.evaluatedValue += 1
                else:
                    break

    def gameOver(self):
        return self.getArrCompleted().count(1) == self.n

    def checkCompleted(self, matrix, col):
        return len(set(matrix[col])) == 1 and len(matrix[col]) == self.m

    def validMove(self, fromCol, toCol):
        if len(self.matrix[fromCol]) > 0 and len(self.matrix[toCol]) < self.m and fromCol != toCol and not (
        self.arrCompleted[fromCol]):
            if len(self.matrix[toCol]) == 0:
                return True
            elif self.matrix[fromCol][-1] == self.matrix[toCol][-1]:
                return True
            else:
                return False
        else:
            return False

    def generateChilds(self, heuristic):
        childs = []
        for i in range(0, self.ntubes):
            for j in range(0, self.ntubes):
                y = self.getLastMove()
                if self.validMove(i, j) and i != y[1]:
                    newstate = Node(self, copy.deepcopy(self.getMatrix()), copy.deepcopy(self.getArrCompleted()),
                                    self.n, self.m, self.ntubes, (i, j), self.getDepth() + 1, 0)
                    newstate.moveBall(i, j)
                    if heuristic == 1:
                        newstate.evaluateState()
                    elif heuristic == 2:
                        newstate.evaluateState2()
                    childs.append(newstate)
        return childs


class Graph:
    def __init__(self, root):
        self.root = root
        self.statesCounter = 1
        self.startTime = 0
        self.endTime = 0

    def breadthFirst(self, node):
        visited = []
        states = [node]
        visited.append(node.getMatrix())
        self.statesCounter = 1
        while states:
            state = states.pop(0)
            children = state.generateChilds(None)
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append(child)

    def depthFirst(self, initState):
        visited = []
        states = [initState]
        self.statesCounter = 1
        self.startTime = time.time()

        while len(states) != 0:
            visited.append(states[-1].getMatrix())
            children = states[-1].generateChilds(None)
            children.reverse()
            states.pop()

            for child in children:
                if child.gameOver():
                    self.endTime = time.time()
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter += 1
                    states.append(child)

    def limitedDepthSearch(self, initState, limit):
        visited = []
        states = [[initState, 0]]
        self.statesCounter = 1
        self.startTime = time.time()

        while len(states) != 0:
            value = states[-1][1] + 1
            if value > limit:
                states.pop()
                continue

            visited.append(states[-1][0].getMatrix())
            children = states[-1][0].generateChilds(None)
            children.reverse()
            states.pop()

            for child in children:
                if child.gameOver():
                    self.endTime = time.time()
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter += 1
                    states.append([child, value])

    def progressiveDeepening(self, initState, progress):
        currentProgress = progress
        visited = []
        toBeChecked = []
        states = [[initState, 0]]
        self.statesCounter = 1
        self.startTime = time.time()

        while True:
            if len(states) == 0:
                currentProgress += progress
                toBeChecked.reverse()
                for i in toBeChecked:
                    states.append(i)
                toBeChecked = []
            if not states:
                return None
            if states[-1][1] == currentProgress and states[-1][1] != 0:
                toBeChecked.append(states[-1])
                states.pop()
                continue

            visited.append(states[-1][0].getMatrix())
            children = states[-1][0].generateChilds(None)
            children.reverse()
            value = states[-1][1] + 1
            states.pop()

            for child in children:
                if child.gameOver():
                    self.endTime = time.time()
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter += 1
                    states.append([child, value])

    def uniformCostSearch(self, initState):
        visited = []
        states = [[initState, initState.getEvaluatedValue()]]
        visited.append(initState.getMatrix())
        self.statesCounter = 1
        self.startTime = time.time()

        while states:
            states.sort(key=lambda x: x[1])
            state = states.pop(0)
            children = state[0].generateChilds(None)
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append([child, child.getDepth()])

    def greedySearch(self, initState, heuristic):
        visited = []
        states = [[initState, initState.getEvaluatedValue()]]
        visited.append(initState.getMatrix())
        self.statesCounter = 1
        self.startTime = time.time()

        while states:
            states.sort(key=lambda x: x[1])
            if heuristic == 2:
                states.reverse()

            state = states.pop(0)
            children = state[0].generateChilds(heuristic)

            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append([child, child.getEvaluatedValue()])

    def aStarSearch(self, initState, heuristic):
        visited = []
        states = [[initState, initState.getEvaluatedValue() + initState.getDepth()]]
        visited.append(initState.getMatrix())
        self.statesCounter = 1
        self.startTime = time.time()

        while states:
            states.sort(key=lambda x: x[1])
            if heuristic == 2:
                states.reverse()
            state = states.pop(0)

            children = state[0].generateChilds(heuristic)
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append([child, (child.getEvaluatedValue() * 5) + child.getDepth()])

    def solve(self, rootnode, solver):
        if solver == 1:
            return self.aStarSearch(rootnode, 1)
        elif solver == 2:
            return self.greedySearch(rootnode, 1)
        elif solver == 3:
            return self.depthFirst(rootnode)
        elif solver == 4:
            return self.breadthFirst(rootnode)
        elif solver == 5:
            return self.uniformCostSearch(rootnode)
        elif solver == 6:
            return self.progressiveDeepening(rootnode, 5)
        elif solver == 7:
            return self.limitedDepthSearch(rootnode, 30)
        else:
            return self.aStarSearch(rootnode, 1)

    def getHint(self, rootnode, solver):
        node = self.solve(rootnode, solver)
        if not node:
            return -1
        solution = [(node.getMatrix(), "Final Solution")]
        currNode = node
        while True:
            if not currNode:
                return -1
            parent = currNode.getParent()
            if parent is not None:
                solution.append((parent.getMatrix(), currNode.getLastMove()))
                currNode = parent
            else:
                break
        return solution[-1][1]

    def getAutoSolve(self, rootnode, solver):
        node = self.solve(rootnode, solver)
        solution = []
        currNode = node
        while True:
            if not currNode:
                return []
            parent = currNode.getParent()
            if parent is not None:
                solution.append((parent.getMatrix(), currNode.getLastMove()))
                currNode = parent
            else:
                break
        return solution

