# a flask webserver that encapsulates a gomoku ai (as example a simple random AI)
from flask import Flask, request, json, Response
from bson import json_util
import logging

import random, time

logging.basicConfig(filename="mylog.log")
app = Flask(__name__)

@app.route('/make_gomoku_move/ai_marius1', methods=['POST'])
def make_gomoku_move_9g3():
    #IncrementalStringDecode

    data = request.json
    ar_error = []

    if data is None or data == {} :
        ar_error.append("data missing")
        strAllErrors=""
        for strError in ar_error:
            strAllErrors += strError
        return Response(response=json.dumps({"Error": strError}),
                        status=400,
                        mimetype='application/json')

    gomoku_ai = gomoku_random_ai_webServer()
    move = gomoku_ai.move(data)

    #dicResponse,ar_error = temptest(data)
    #if(len(ar_error)!=0): return MongoAPI.returnErrors(ar_error)
    dicResponse={}
    dicResponse['move']=move
    return Response(response=json_util.dumps(dicResponse),
                    status=200,
                    mimetype='application/json')

# ******************************************************
# End of Flask part.  Below is the AI part.
# ******************************************************

class GmGameRules():
    winningSeries=5 # global class variable. will be overridden below.
    BOARDWIDTH=19
    BOARDHEIGHT=19

def isValidMove(board, column, row):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    return ((column >= 0) and (column < len(board)) and (row >= 0) and (row < len(board[0])) and (board[column][row] == 0))

def getValidMoves(board,ply):
    # First, make a list of all empty spots
    validMoves = []

    centerX = (len(board)) // 2
    centerY =(len (board[0])) // 2
    firstMove = ( centerX , centerY )

    if ply==1:  #last_move==None:
        # do the first move
        validMoves.append(firstMove)
        return validMoves

    for col in range(0,len(board)):
        for row in range(0,len(board[0])):
            if isValidMove(board, col, row):
                tup=(col,row)
                if tup != firstMove:
                    validMoves.append(tup)

    # if we're the black player, then we cannot move our SECOND move anywhere at a distance of 1 or 2 tiles from the center.
    # .. unless we're testing with a board of size 5 or smaller
    if (ply==3) and (GmGameRules.BOARDWIDTH>7):
        # we're black, and it's our second move.
        # we are not allowed to play our second move near the center.
        centerX = (len(board)) // 2
        centerY =(len (board[0])) // 2
        for y in range(centerY-2,centerY+3):
            for x in range(centerX-2,centerX+3):
                try:
                    validMoves.remove((x,y))
                except:
                    dummy=1;dummy=dummy
    return validMoves

def getRandomMove(board,ply):
    # let's make a random move
    # First, make a list of all empty spots
    validMoves = getValidMoves(board,ply)
    return random.choice(validMoves)

def getRandomMove_obs(board):
    # let's make a random move
    # First, make a list of all empty spots
    validMoves = []
    for col in range(GmGameRules.BOARDWIDTH):
        for row in range(GmGameRules.BOARDHEIGHT):
            if isValidMove(board, col, row):
                validMoves.append((col,row))

    return random.choice(validMoves)

# player gives an implementation the basePlayer cl
class randomPlayer():
    def __init__(self, black_=True):
        self.black = black_

        self.max_move_time_ns   = 0
        self.start_time_ns      = 0

    def new_game(self, black_):
        self.black = black_

    def move(self, gamestate, last_move, max_time_to_move=1000):
        board   = gamestate[0]
        ply     = gamestate[1]

        self.max_move_time_ns   = 0.95 * max_time_to_move * 1000000 # ms to ns
        self.start_time_ns      = time.time_ns()

        return getRandomMove(board,ply)

    def id(self):
        return "Marius_random"

class gomoku_random_ai_webServer():

    def move(self, dic):
        #strData=strUrlEncodedData # urllib.parse.unquote(strUrlEncodedData)

        #dic=json.loads(strData)

        GmGameRules.winningSeries=dic['winningSeries']
        GmGameRules.BOARDWIDTH=dic['boardSize']
        GmGameRules.BOARDHEIGHT=dic['boardSize']

        gamestate = (dic['board'],dic['ply'])
        last_move = dic['last_move']
        # we'll deriver valid_moves ourselves
        player = randomPlayer(dic['black'])

        return player.move(gamestate,last_move,dic['max_time_to_move'])
