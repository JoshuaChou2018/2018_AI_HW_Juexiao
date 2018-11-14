# ghostAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

class MinimaxGhost(GhostAgent):

    """
      Your minimax agent (question 1)

      useage: python2 pacman.py -p ExpectimaxAgent -l smallClassic -g MinimaxGhost -a depth=4
              python2 pacman.py -l smallClassic -g MinimaxGhost

    """
    "*** YOUR CODE HERE ***"
    def __init__(self, index, evalFn = 'betterEvaluationFunctionGhost', depth = '2'):
        self.index = index # Ghosts are always agent index > 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getAction(self, gameState):
        startlayer=1
        ghostindex=self.index#ghost
        # start from the first layer and then traverse all agent
        move=self.MinimaxEvaluationFunction(gameState,startlayer,ghostindex,ghostindex)
        return move

    def MinimaxChoose(self,layer,agentindex,scores,legalMoves):
        if (agentindex!=0)&(layer!=1): #ghost and not the first layer
            return min(scores)
        elif (layer!=1)&(agentindex==0): #pacman not in the first layer
            return max(scores)
        else: #ghost in the first layer
            bestIndices=[]
            for index in range(len(scores)):
                if scores[index]==min(scores):
                    bestIndices.append(index)
            chosenIndex=random.choice(bestIndices)
            return legalMoves[chosenIndex]

    def MinimaxEvaluationFunction(self,gameState,layer,ghostindex,nowindex):
        if (gameState.isLose())|(gameState.isWin()):
            return self.evaluationFunction(gameState)
        if layer>self.depth:
            return self.evaluationFunction(gameState)
        legalMoves=[]
        for x in gameState.getLegalActions(nowindex):
            legalMoves.append(x)
        if nowindex==0:
            scores=[]
            for x in legalMoves:
                scores.append(self.MinimaxEvaluationFunction(gameState.generateSuccessor(nowindex,x),layer+1,ghostindex,ghostindex))
            return self.MinimaxChoose(layer,nowindex,scores,legalMoves)
        else: # ghost layer
            scores=[]
            for x in legalMoves:
                scores.append(self.MinimaxEvaluationFunction(gameState.generateSuccessor(nowindex,x),layer,ghostindex,0))
            return self.MinimaxChoose(layer,nowindex,scores,legalMoves)









def betterEvaluationFunctionGhost(currentGameState):
    """
        Ghost evaluation function
    """

    position = list(currentGameState.getPacmanPosition())
    foodPos = currentGameState.getFood().asList()
    foodList = []

    for food in foodPos:
        pacmanDist = manhattanDistance(position, food)
        foodList.append(pacmanDist)

    if not foodList:
        foodList.append(0)

    nearestPelletDist = min(foodList)
    return currentGameState.getScore() + (-1) * nearestPelletDist

# Abbreviation
ghostEval = betterEvaluationFunctionGhost
