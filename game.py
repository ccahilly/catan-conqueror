from agent import Agent
from board import BeginnerLayout, Board, Edge, Hexagon, Vertex
from collections import Counter
from draw import *
from random import randint


class GameState:
  """
  Class: GameState
  -------------------------------
  A class representing all information about the current state of the game.
  Includes a Board object representing the current state of the game board,
  as well as a list of all agents (players + random agents) in the game.
  -------------------------------
  """

  def __init__(self, prevState = None, layout = BeginnerLayout):
    """
    Method: __init__
    -----------------------------
    Parameters:
      prevState - an optional GameState object to pass in.  If this is passed
        in, this new GameState object will instead be cloned from prevState
      layout - an optional board layout to pass in to define the layout
        of the game board

    Returns: NA

    Initializes the GameState object, either by creating a new one from
    scratch or by cloning an optionally passed-in other GameState object.
    Can also optionally define the board layout if you are creating a new
    GameState object from scratch.
    ------------------------------
    """
    if prevState is not None:
      self.board = prevState.board.deepCopy()
      self.agents = [agent.deepCopy(self.board) for agent in prevState.agents]
    else:
      self.board = Board(layout)
      self.agents = [Agent("Player " + str(i), i) for i in xrange(NUM_PLAYERS)]

  def getLegalActions(self, agentIndex):
    """
    Method: getLegalActions
    ------------------------------
    Parameters:
      agentIndex - the index of the agent to return legal actions for

    Returns: a list of action tuples (ACTION, LOCATION) (e.g. (ACTIONS.SETTLE, *some Vertex object*))
      representing all the valid actions that the given agent/player can take
    ------------------------------
    """
    legalActions = []

    if self.gameOver() >= 0: return legalActions

    agent = self.agents[agentIndex]

    # If they can build a road...
    if agent.canBuildRoad():

      # Look at all unoccupied roads coming from the player's existing settlements
      for settlement in agent.settlements:
        currEdges = self.board.getEdgesOfVertex(settlement)
        for currEdge in currEdges:
          if not currEdge.isOccupied():
            legalActions.append((ACTIONS.ROAD, currEdge))        

    # If they can settle...
    if agent.canSettle():

      # Look at all unoccupied endpoints of the player's existing roads
      for road in agent.roads:
        possibleSettlements = self.board.getVertexEnds(road)
        for possibleSettlement in possibleSettlements:
          if possibleSettlement.canSettle:
            legalActions.append((ACTIONS.SETTLE, settlement))

    # If they can build a city...
    if agent.canBuildCity():

      # All current settlements are valid city locations
      for settlement in agent.settlements:
        legalActions.append((ACTIONS.CITY, settlement))
            
    return legalActions

  def generateSuccessor(self, playerIndex, action):
    """
    Method: generateSuccessor
    ----------------------------
    Parameters:
      playerIndex - the number of the player that is about to take an action
      action - the action that the player is about to take

    Returns: a new GameState object with playerIndex having taken 'action'

    Creates a clone of the current game state, and then performs the
    given action on behalf of the given player.  Returns the resulting
    GameState object.
    ----------------------------
    """
    if self.gameOver() >= 0:
      raise Exception("Can\'t generate a successor of a terminal state!")

    # Create a copy of the current state, and perform the given action
    # for the given player
    state = GameState(self)
    state.agents[playerIndex].applyAction(action)
    state.board.applyAction(playerIndex, action)
    return state

  def getNumAgents(self):
    """
    Method: getNumAgents
    ----------------------------
    Parameters: NA

    Returns: the number of agents in the current game
    ----------------------------
    """
    return len(self.agents)

  def gameOver(self):
    """
    Method: gameOver
    ----------------------------
    Parameters: NA
    Returns: the index of the player that has won, or -1 if the game has not ended
    ----------------------------
    """
    # See if any of the agents have won
    for agent in self.agents:
      if agent.hasWon():
        return agent.agentIndex
    return -1


class Game:
  """
  Class: Game
  ------------------------
  Represents all information about a game, and controls game flow.
  In addition to containing a GameState object to keep track of all game
  state, a Game object also contains the game's move history as a list
  of (AGENTNAME, ACTION) tuples.
  ------------------------
  """

  def __init__(self, gameState = GameState()):
    """
    Method: __init__
    ----------------------
    Parameters:
      gameState - an optional pre-defined GameState object to use for the game.
        If one isn't passed in, the Game begins with a newly-created GameState object.

    Returns: NA

    Initializes the Game object by initializing the move history list
    and the internal GameState object.
    ----------------------
    """
    self.moveHistory = []
    self.gameState = gameState
    self.draw = Draw(self.gameState.board.tiles)

  def drawGame(self):
    """
    Method: drawGame
    ----------------------
    Parameters: NA
    Returns: NA

    Draws the graphics for displaying the board
    tiles.
    ----------------------
    """
    self.draw.drawBG()
    # draw.drawTitle()  
    self.draw.drawBoard()
    # draw.drawDiceRoll()
    # draw.drawPlayer(self.curPlayer)
    #draw.drawKey(self)
    # draw.drawRoads(self.roads, self.vertices)
    # draw.drawSettlements(self.vertices)
    # else: #gameOver is true
    #     draw.drawWinner(self) #draw winning screen
    #     self.hideButtons()          #hide all buttons 
    #     self.f.place(x=20, y=565)   #except for New Game button

  def run(self):    
    """
    Method: run
    ----------------------
    Parameters: NA
    Returns: NA

    Runs the main game loop.  Initializes all the players' resources
    and settlements, prints out the game state, and then begins the main loop.
    Each turn, the dice are rolled, and all players get resources.  Then, the
    player whose turn it is can take 1 action, and the game state is updated
    accordingly.  The game continues until 1 player wins by reaching
    VICTORY_POINTS_TO_WIN victory points.
    ----------------------
    """
    # --- PLAYER INITIALIZATION --- #

    # Each player starts with 2 settlements
    initialSettlements = [self.gameState.board.getVertex(2,2), 
      self.gameState.board.getVertex(4,4), 
      self.gameState.board.getVertex(3,1)]

    # Use % to essentially loop through and assign a settlement to each agent until
    # there are no more settlements to assign
    # ASSUMPTION: len(initialSettlements) is a clean multiple of # agents
    for i, settlement in enumerate(self.gameState.agents):
      agent = self.gameState.agents[i % self.gameState.getNumAgents()]
      agent.settlements.append(initialSettlements[i])
      self.gameState.board.applyAction(agent.agentIndex, (ACTIONS.SETTLE, initialSettlements[i]))

    # Each player starts with resources for each of their settlements
    for agent in self.gameState.agents:
      agent.collectInitialResources(self.gameState.board)

    # --- END PLAYER INITIALIZATION --- #

    # --- GAME START --- #

    # Welcome message
    print "WELCOME TO SETTLERS OF CATAN!"
    print "-----------------------------"
    DEBUG = True if raw_input("DEBUG mode? (y/n) ") == "y" else False

    # Turn tracking
    turnNumber = 1
    currentAgentIndex = 0

    # Main game loop
    while (self.gameState.gameOver() < 0):

      # Draw the gameboard
      self.drawGame()

      # Initial information
      currentAgent = self.gameState.agents[currentAgentIndex]
      print "---------- TURN " + str(turnNumber) + " --------------"
      print "It's " + str(currentAgent.name) + "'s turn!"

      # Print player info
      if DEBUG:
        print "PLAYER INFO:"
        for a in self.gameState.agents:
          print a

      raw_input("Press ENTER to proceed:")
      
      # Dice roll + resource distribution
      dieRoll = randint(1,6) + randint(1,6)
      if DEBUG:
        print "Rolled a " + str(dieRoll)

      for agent in self.gameState.agents:
        gainedResources = agent.updateResources(dieRoll, self.gameState.board)
        if DEBUG:
          print str(agent.name) + " received: " + str(gainedResources)
          print str(agent.name) + " now has: " + str(agent.resources)

      # The current player performs 1 action
      action = currentAgent.getAction(self.gameState)
      currentAgent.applyAction(action)
      self.gameState.board.applyAction(currentAgent.agentIndex, action)

      # Print out the updated game state
      print str(currentAgent.name) + " took action " + str(action[0]) + " at " + str(action[1]) + "\n"
      print currentAgent

      # Track the game's move history
      self.moveHistory.append((currentAgent.name, action))
      
      # Go to the next player/turn
      currentAgentIndex = (currentAgentIndex+1) % self.gameState.getNumAgents()
      turnNumber += 1

    print self.gameState.agents[self.gameState.gameOver()], " won the game"


game = Game()
game.run()
