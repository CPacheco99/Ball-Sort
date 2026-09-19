import pygame
import copy
from pathlib import Path
from solver import Node, Graph
from pygame.locals import (
    K_ESCAPE, K_h, K_1, K_2, K_3, K_4, K_5, K_s, K_d, K_a, K_u, K_r, KEYDOWN, QUIT, K_6, K_7
)

WHITE = (236, 239, 241)
BLACK = (38, 50, 56)
GREY = (144, 164, 174)
RED = (244, 67, 54)
GREEN = (76, 175, 80)
BLUE = (33, 150, 243)
ORANGE = (255, 152, 0)
PINK = (240, 98, 146)
PURPLE = (156, 39, 176)


class Game:
    def __init__(self, levels_data, level_index):
        self.levels_data = levels_data
        self.level_index = level_index
        self.n = levels_data[level_index][0]
        self.m = levels_data[level_index][1]
        self.ntubes = levels_data[level_index][2]
        self.initialState = copy.deepcopy(levels_data[level_index][3])
        self.arrTotal = copy.deepcopy(self.initialState)
        self.completed = [0] * self.ntubes
        self.tubesArray = [0] * self.ntubes
        self.nMoves = 0
        self.history = []

    def fillCompleted(self, col):
        if self.checkCompleted(col):
            self.completed[col] = 1
        else:
            self.completed[col] = 0

    def checkCompleted(self, col):
        return len(set(self.arrTotal[col])) == 1 and len(self.arrTotal[col]) == self.m

    def validMove(self, fromCol, toCol):
        if len(self.arrTotal[fromCol]) > 0 and len(self.arrTotal[toCol]) < self.m and fromCol != toCol and not (
        self.completed[fromCol]):
            if len(self.arrTotal[toCol]) == 0:
                return True
            elif self.arrTotal[fromCol][-1] == self.arrTotal[toCol][-1]:
                return True
            else:
                return False
        else:
            return False

    def moveBall(self, fromCol, toCol):
        if self.validMove(fromCol, toCol):
            num = self.arrTotal[fromCol].pop(-1)
            self.arrTotal[toCol].append(num)
            self.fillCompleted(toCol)
            self.fillCompleted(fromCol)
            self.nMoves += 1
            self.history.append((fromCol, toCol))

    def undoMove(self):
        """Devuelve el último movimiento realizado"""
        if len(self.history) > 0:
            fromCol, toCol = self.history.pop()
            num = self.arrTotal[toCol].pop(-1)
            self.arrTotal[fromCol].append(num)
            self.fillCompleted(fromCol)
            self.fillCompleted(toCol)
            self.nMoves -= 1

    def resetLevel(self):
        """Reinicia el nivel a su estado inicial"""
        self.arrTotal = copy.deepcopy(self.initialState)
        self.completed = [0] * self.ntubes
        self.nMoves = 0
        self.history = []

    def gameOver(self):
        return self.completed.count(1) == self.n


class GameLoop:
    def __init__(self, screen, width=1280, height=720):
        self.screen = screen
        self.width = width
        self.height = height
        self.levels = [
            # Nivel 1 (Tutorial básico - 2 colores)
            [2, 4, 3, [[2, 2, 2, 1], [1, 1, 1, 2], []]],
            
            # Nivel 2 (3 colores)
            [3, 4, 4, [[2, 1, 2, 3], [3, 1, 3, 2], [1, 3, 2, 1], []]],
            
            # Nivel 3
            [3, 4, 5, [[6, 5, 6], [5, 5, 6, 4], [6, 4, 5, 4], [4], []]],
            
            # Nivel 4
            [3, 4, 5, [[1, 2, 3, 1], [2, 2, 3, 1], [3, 1, 2, 3], [], []]],
            
            # Nivel 5
            [3, 4, 5, [[1, 2, 3, 3], [1, 2, 1, 2], [3, 1, 2, 3], [], []]],
            
            # Nivel 6 (4 colores)
            [4, 4, 5, [[3, 2, 1, 3], [2, 1, 1, 2], [1, 2, 3, 4], [4, 4], [3, 4]]],
            
            # Nivel 7
            [4, 4, 6, [[1, 3, 2, 4], [4, 2, 1, 3], [3, 4, 1, 2], [2, 1, 4, 3], [], []]],
            
            # Nivel 8
            [4, 4, 6, [[4, 1, 2, 3], [3, 2, 4, 1], [1, 4, 3, 2], [2, 3, 1, 4], [], []]],
            
            # Nivel 9 (Introducción a 5 colores)
            [5, 4, 6, [[3, 2, 1, 3], [2, 1, 1, 2], [1, 2, 3, 4], [4, 4], [3, 5, 5, 4], [5, 5]]],
            
            # Nivel 10
            [5, 4, 7, [[1, 5, 2, 3], [4, 2, 5, 1], [3, 1, 4, 5], [2, 3, 1, 4], [5, 4, 3, 2], [], []]],
            
            # Nivel 11
            [5, 4, 7, [[5, 1, 3, 2], [2, 4, 1, 5], [3, 2, 5, 4], [1, 3, 4, 2], [4, 5, 2, 3], [], []]],
            
            # Nivel 12
            [5, 4, 7, [[2, 3, 5, 1], [1, 4, 2, 5], [5, 1, 3, 4], [4, 2, 1, 3], [3, 5, 4, 2], [], []]],
            
            # Nivel 13 (Introducción a 6 colores)
            [6, 4, 7, [[1, 2, 3, 4], [6, 6], [2, 1, 1, 2], [4, 4, 6], [3, 2, 1, 3], [3, 5, 5], [5, 5, 4, 6]]],
            
            # Nivel 14
            [6, 4, 8, [[1, 2, 3, 4], [5, 6, 1, 2], [3, 4, 5, 6], [6, 5, 4, 3], [2, 1, 6, 5], [4, 3, 2, 1], [], []]],
            
            # Nivel 15
            [6, 4, 8, [[6, 1, 5, 2], [3, 4, 2, 6], [1, 5, 3, 4], [2, 6, 4, 1], [5, 3, 1, 5], [4, 2, 6, 3], [], []]],
            
            # Nivel 16
            [6, 4, 8, [[2, 4, 6, 1], [5, 3, 1, 4], [6, 2, 5, 3], [1, 6, 3, 2], [4, 5, 2, 6], [3, 1, 4, 5], [], []]],
            
            # Nivel 17
            [6, 4, 8, [[4, 3, 1, 6], [2, 5, 6, 3], [1, 2, 4, 5], [6, 1, 3, 2], [5, 4, 2, 1], [3, 6, 5, 4], [], []]],
            
            # Nivel 18
            [6, 4, 8, [[3, 6, 2, 5], [1, 4, 5, 2], [6, 3, 1, 4], [2, 5, 4, 6], [5, 1, 3, 2], [4, 2, 6, 3], [], []]],
            
            # Nivel 19
            [6, 4, 8, [[5, 2, 4, 1], [6, 3, 1, 5], [2, 6, 3, 4], [1, 4, 5, 2], [3, 1, 2, 6], [4, 5, 6, 3], [], []]],
            
            # Nivel 20 (Nivel Final Avanzado)
            [6, 4, 8, [[1, 6, 2, 5], [3, 4, 6, 1], [5, 2, 1, 4], [6, 3, 5, 2], [4, 1, 3, 6], [2, 5, 4, 3], [], []]]
        ]
        self.currentLevel = 0
        self.game = Game(self.levels, self.currentLevel)
        self.tubeSelected = False
        self.fromTube = -1
        self.toTube = -1
        self.hint = [0, 0]
        self.showHint = False
        self.showAuto = False
        self.solver = 1
        self.clickable_buttons = {}
        self.noSols = False
        self.currAlg = ""

    def loadNextLevel(self):
        if self.currentLevel < len(self.levels) - 1:
            self.currentLevel += 1
            self.game = Game(self.levels, self.currentLevel)
            self.resetSelection()

    def resetSelection(self):
        self.tubeSelected = False
        self.fromTube = -1
        self.toTube = -1
        self.showHint = False

    def color(self, number):
        colors = {1: RED, 2: GREEN, 3: BLUE, 4: ORANGE, 5: PINK, 6: PURPLE}
        return colors.get(number, BLACK)

    def drawTube(self, number):
        center = self.width / (self.game.ntubes + 1)
        tube = pygame.Surface((60, 300))
        font = pygame.font.Font('freesansbold.ttf', 40)
        tube.fill(BLACK)
        if number == self.fromTube:
            tube.fill(GREY)
        tube_center = ((center * (number + 1) - tube.get_width() / 2), (self.height - tube.get_height()) / 2 + 30)
        pygame.draw.rect(tube, WHITE, pygame.Rect(5, 0, 50, 215))
        pygame.draw.rect(tube, WHITE, pygame.Rect(0, 220, 60, 80))
        text = font.render("%d" % number, True, BLACK, WHITE)
        tube.blit(text, (20, 240))
        currentBall = 1
        for x in self.game.arrTotal[number]:
            pygame.draw.circle(tube, self.color(x), (30, 215 - (25 * currentBall)), 20)
            currentBall += 2
        tubeClickable = self.screen.blit(tube, tube_center)
        self.game.tubesArray[number] = tubeClickable

    def drawGame(self):
        font = pygame.font.Font('freesansbold.ttf', 24)
        self.screen.fill(WHITE)
        
        # Información
        levelText = font.render(f"Nivel: {self.currentLevel + 1}", True, BLACK)
        self.screen.blit(levelText, (40, 30))
        
        movesText = font.render(f"Movs: {self.game.nMoves}", True, BLACK)
        self.screen.blit(movesText, (180, 30))

        # Botones de la barra superior
        self.clickable_buttons = {}

        btn_hint_surf = font.render("[Pista]", True, BLUE)
        btn_hint = self.screen.blit(btn_hint_surf, (340, 30))
        self.clickable_buttons['hint'] = btn_hint

        btn_undo_surf = font.render("[Deshacer]", True, ORANGE)
        btn_undo = self.screen.blit(btn_undo_surf, (450, 30))
        self.clickable_buttons['undo'] = btn_undo

        btn_reset_surf = font.render("[Reiniciar]", True, RED)
        btn_reset = self.screen.blit(btn_reset_surf, (610, 30))
        self.clickable_buttons['reset'] = btn_reset

        btn_menu_surf = font.render("[Menú]", True, BLACK)
        btn_menu = self.screen.blit(btn_menu_surf, (760, 30))
        self.clickable_buttons['menu'] = btn_menu

        if self.showHint:
            hintText = font.render("Sugerencia: %d -> %d" % tuple(self.hint), True, BLACK)
            self.screen.blit(hintText, (340, 70))
            
        if self.showAuto:
            autoText = font.render("Auto Solving: " + self.currAlg, True, BLACK)
            self.screen.blit(autoText, (170, 650))

        if self.noSols:
            noSolution = font.render('No Solution', True, RED)
            self.screen.blit(noSolution, (500, 650))

        for x in range(0, self.game.ntubes):
            self.drawTube(x)

    def handleMouseClick(self):
        pos = pygame.mouse.get_pos()

        # Interacción con botones superiores
        if self.clickable_buttons.get('hint') and self.clickable_buttons['hint'].collidepoint(pos):
            self.updateHint()
            return "CONTINUE"
        elif self.clickable_buttons.get('undo') and self.clickable_buttons['undo'].collidepoint(pos):
            self.game.undoMove()
            self.resetSelection()
            return "CONTINUE"
        elif self.clickable_buttons.get('reset') and self.clickable_buttons['reset'].collidepoint(pos):
            self.game.resetLevel()
            self.resetSelection()
            return "CONTINUE"
        elif self.clickable_buttons.get('menu') and self.clickable_buttons['menu'].collidepoint(pos):
            return "GO_MENU"

        # Interacción con los tubos
        for tube in self.game.tubesArray:
            if tube.collidepoint(pos):
                if not self.tubeSelected:
                    self.fromTube = self.game.tubesArray.index(tube)
                    self.tubeSelected = True
                else:
                    self.toTube = self.game.tubesArray.index(tube)
                    self.game.moveBall(self.fromTube, self.toTube)
                    self.resetSelection()
        return "CONTINUE"

    def updateHint(self):
        self.showHint = True
        root = Node(None, self.game.arrTotal, self.game.completed, self.game.n, self.game.m, self.game.ntubes, (-1, -1), 0, 0)
        graph1 = Graph(root)
        hint = graph1.getHint(root, self.solver)
        if hint == -1:
            self.noSols = True
        else:
            self.hint = hint

    def autoSolve(self, solver):
        self.showAuto = True
        self.noSols = False
        root = Node(None, self.game.arrTotal, self.game.completed, self.game.n, self.game.m, self.game.ntubes, (-1, -1), 0, 0)
        graph1 = Graph(root)
        solution = graph1.getAutoSolve(root, solver)
        if len(solution) == 0:
            self.noSols = True
            self.showAuto = False
            return
        solution.reverse()
        for x in solution:
            pygame.time.wait(150)
            self.game.moveBall(x[-1][0], x[-1][1])
            self.update()
            pygame.time.wait(150)
        self.showAuto = False

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                res = self.handleMouseClick()
                if res == "GO_MENU":
                    return "GO_MENU"

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "GO_MENU"
                elif event.key == K_h:
                    self.updateHint()
                elif event.key == K_u:
                    self.game.undoMove()
                    self.resetSelection()
                elif event.key == K_r:
                    self.game.resetLevel()
                    self.resetSelection()
                elif event.key == K_a or event.key == K_1:
                    self.currAlg = "A*"
                    self.autoSolve(1)
                elif event.key == K_2:
                    self.currAlg = "Greedy"
                    self.autoSolve(2)
                elif event.key == K_3:
                    self.currAlg = "DFS"
                    self.autoSolve(3)
                elif event.key == K_4:
                    self.currAlg = "BFS"
                    self.autoSolve(4)
                elif event.key == K_5:
                    self.currAlg = "Uniform Cost"
                    self.autoSolve(5)
                elif event.key == K_6:
                    self.currAlg = "Iterative Deepening"
                    self.autoSolve(6)
                elif event.key == K_7:
                    self.currAlg = "Limited Depth"
                    self.autoSolve(7)
                elif event.key == K_d:
                    self.noSols = False
                    self.loadNextLevel()

            elif event.type == QUIT:
                return "EXIT_GAME"
        return "CONTINUE"

    def update(self):
        self.drawGame()
        pygame.display.flip()
        if self.game.gameOver():
            pygame.time.wait(300)
            if self.currentLevel < len(self.levels) - 1:
                self.loadNextLevel()
            else:
                return "GO_MENU"
        return "CONTINUE"
