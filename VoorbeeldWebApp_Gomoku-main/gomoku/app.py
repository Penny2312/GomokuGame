from flask import Flask, request, json, Response, render_template, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson import json_util

from gomoku_ai_random_webserver import gomoku_random_ai_webServer
import logging
import datetime
from flask_cors import CORS
import os

#setup logging basic configuration for logging to a file
#(if you put this in a route function itself, it won't work)
# De niet zelf gegenereerde errors komen (ook) hier terecht.
logging.basicConfig(filename="mylog.log", level=logging.DEBUG)

app = Flask(__name__)

CORS(app)  # Dit staat CORS toe voor alle domeinen (toegang vanaf browser buiten WSL)

# # Stel een geheime sleutel in voor uw applicatie
# app.secret_key = 'mijn_geheime_gomoku_applicatie_sleutel'

# # MongoDB-clientconfiguratie
# client = MongoClient("mongodb://mongodb:mijn_geheime_mongodb_wachtwoord@mongo:27017/")
# dbGomoku = client.gomoku # selecteert de database 'gomoku' in de Mongo db instance.



# Stel een geheime sleutel in voor uw applicatie vanuit een omgevingsvariabele
app.secret_key = os.environ.get('APP_SECRET_KEY', 'standaard_waarde_als_geen_secret_key')

# MongoDB-clientconfiguratie
mongodb_user = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
mongodb_password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
mongodb_host = os.environ.get('MONGO_HOST', 'mongo')  # 'mongo' is de standaard host die in docker-compose.yml is opgegeven

# Samenstellen van de MongoDB connection string
mongodb_uri = f"mongodb://{mongodb_user}:{mongodb_password}@{mongodb_host}:27017/"# de interne mongodb port: altijd 27017

# Verbind met de MongoDB instance
client = MongoClient(mongodb_uri)
dbGomoku = client.gomoku  # Selecteert de database 'gomoku'




@app.route('/gomoku/')
def hello_world():
    strResult = 'Groetjes van Marius!<br><a href="/gomoku/start">Ga naar gomoku start pagina</a>'
    #raise ValueError("Dit is een testfout!")
    print('bla')
    return strResult

@app.route('/gomoku/testlogging')
def testlogging():
    # logging.basicConfig(filename="mylog.log") Dit is zinloos hier, en moet gebeurd zijn buiten de functie.
    logging.warning('This is a WARNING message 2')
    logging.error('This is an ERROR message 2')
    logging.critical('This is a CRITICAL message 2')

    return Response(response="Log test compleet!",
                    status=200,
                    mimetype='application/json')

@app.route('/gomoku/start', methods=['GET'])
def gmoku_start():
    return render_template('start_gomoku.html') 

def getJsEngineFromSpelerType(spelerType):
    result="unknown"
    if spelerType=="AI Random":
        result="random"
    elif spelerType=="AI Marius TNG":
        result="marius_tng"
    elif spelerType=="Human":
        result="human"
    else:
        logging.append("onbekend spelertype:")
        logging.append(spelerType)
    return result

@app.route('/gomoku/play', methods=['GET', 'POST'])
def gomoku_play():
    if request.method == 'POST':
        data = request.form
        if not data:
            return "Missing form data", 400

        engineBlack = getJsEngineFromSpelerType(data['typeSpeler1'])
        engineWhite = getJsEngineFromSpelerType(data['typeSpeler2'])
        return render_template('play_gomoku.html', engineBlack=engineBlack, engineWhite=engineWhite, nameBlack=data['naamSpeler1'], nameWhite=data['naamSpeler2'])
    
    return render_template('play_gomoku.html')

# Je kunt bovenstaande los testen door bijvoorbeeld in Postman POST naar https://pikido.com/gomoku/make_gomoku_move/ai_marius_tng
# met Body = raw->json:
# {"board": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], "ply": 1, "last_move": null, "max_time_to_move": 400, "winningSeries": 5, "boardSize": 19, "black": true}
# ( dat retourneert: body: {"move": [9, 9]})
#
# Via een curl zou het ook moeten werken. Toch retourneert het in dat geval move(0,0).
# Dat betekent dat uiteindelijk het script in ai_marius_tng niet tevreden is met de input.
# Misschien behandelt curl de null anders dan Postman of javascript en flask, waar het wel goed gaat.
# Moet ik eens uitzoeken...

# kleiner voorbeeld:
# via postman te testen met POST (raw,json) naar:
# https://www.pikido.com/gomoku/make_gomoku_move/ai_marius_tng
# met de volgende content:
#{
#    "board": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0,0, 0, 0, 0, 0,0, 0, 0, 0, 0],
#    "ply": 1,
#    "last_move": null,
#    "max_time_to_move": 600,
#    "winningSeries": 5,
#    "boardSize": 5,
#    "black": true
#}
# BTW: als het niet de eerste move is, is ply>1, en heeft last_move een waarde, zoals [2,3].

@app.route('/gomoku/post-game-result', methods=['POST'])
def post_game_result():

    # try:
    #     data = request.get_json()  # Ontvang de JSON-data
    #     logging.debug("Received data: %s", data)  # Gebruik logging om de data te loggen
    #     # Verwerk de data hier
    #     return {"status": "success"}, 200
    # except Exception as e:
    #     logging.error(f"Error processing game result: {str(e)}")  # Log de fout met logging.error
    #     return {"status": "error", "message": str(e)}, 500

    try:
        data = request.get_json()
        # app.logger.debug(f"Received data: {data}")  # Gedetailleerde logging van ontvangen data
        logging.debug("Received data: %s", data)  # Gebruik logging om de data te loggen

        # Verifieer de ontvangen data
        if not data:
            raise ValueError("No data received")
        
        # Controleer of alle benodigde velden aanwezig zijn
        required_fields = ["winner", "engineBlack", "engineWhite", "nameBlack", "nameWhite", "plies"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        logging.debug("fields ok")

        # We slaan de json op as-is, in onze mongodb:
        mongo_data = {
            "winner": data.get('winner'),
            "engineBlack": data.get('engineBlack'),
            "engineWhite": data.get('engineWhite'),
            "nameBlack": data.get('nameBlack'),
            "nameWhite": data.get('nameWhite'),
            "plies": data.get('plies'),
            "insertedAt": datetime.datetime.utcnow()  # Voeg een timestamp toe voor debugging
        }

        # Toevoegen of updaten van een document in de collectie genaamd "games"
        result = dbGomoku.games.insert_one(mongo_data)

        # Log het resultaat van de MongoDB operatie
        # app.logger.debug(f"Inserted document ID: {result.inserted_id}")
        logging.debug(f"Inserted document ID: {result.inserted_id}")
        # Controleer of het document daadwerkelijk is ingevoegd
        inserted_document = dbGomoku.games.find_one({"_id": result.inserted_id})

        logging.debug(f"Inserted document: {inserted_document}")
        # app.logger.debug(f"Inserted document: {inserted_document}")

        # Succesvolle response terugsturen
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        # app.logger.error(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")
        # Stuur een foutmelding terug als er iets misgaat
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/gomoku/statistics')
def gomoku():
    return render_template('statistics_gomoku.html')

def convert_objectid_to_str(document):
    """ Converteer ObjectId-velden naar strings in een document """
    if '_id' in document:
        document['_id'] = str(document['_id'])
    if 'insertedAt' in document:
        document['insertedAt'] = document['insertedAt'].isoformat()
    return document

@app.route('/gomoku/results')
def get_results():
    try:
        black_player = request.args.get('blackPlayer')
        black_player_name = request.args.get('blackPlayerName')
        white_player = request.args.get('whitePlayer')
        white_player_name = request.args.get('whitePlayerName')
        filter_type = request.args.get('filterType', 'AND')
        page = int(request.args.get('page', 0))
        page_size = 10

        black_query = {}
        white_query = {}

        if black_player != 'All':
            if black_player == 'Human':
                black_query['engineBlack'] = 'human'
                if black_player_name:
                    black_query['nameBlack'] = black_player_name
            elif black_player == "AI Random":
                black_query['engineBlack'] = 'random'
            elif black_player == "AI Marius TNG":
                black_query['engineBlack'] = 'marius_tng'
        if white_player != 'All':
            if white_player == 'Human':
                white_query['engineWhite'] = 'human'
                if white_player_name:
                    white_query['nameWhite'] = white_player_name
            elif white_player == "AI Random":
                white_query['engineWhite'] = 'random'
            elif white_player == "AI Marius TNG":
                white_query['engineWhite'] = 'marius_tng'

        app.logger.debug(f"Black Query: {black_query}")
        app.logger.debug(f"White Query: {white_query}")

        if filter_type == 'AND':
            query = {'$and':[black_query, white_query]}
        else:  # OR
            query = {'$or': [black_query, white_query]}

        app.logger.debug(f"Final Query: {query}")

        total_results = dbGomoku.games.count_documents(query)
        results_cursor = dbGomoku.games.find(query).sort('insertedAt', -1).skip(page * page_size).limit(page_size)
        results = [convert_objectid_to_str(doc) for doc in results_cursor]

        app.logger.debug(f"Total results: {total_results}, Fetched results: {results}")

        has_prev = page > 0
        has_next = (page + 1) * page_size < total_results

        return jsonify({
            'results': results,
            'hasPrev': has_prev,
            'hasNext': has_next
        })
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/gomoku/make_gomoku_move/ai_random', methods=['POST'])
def make_gomoku_move_random():
    data = request.json
    player = gomoku_random_ai_webServer()
    return make_gomoku_move(player,data)

def make_gomoku_move(player,data):
    ar_error = []

    logging.warning('bla1')
    if data is None or data == {} :
        ar_error.append("data missing")
        strAllErrors=""
        for strError in ar_error:
            strAllErrors += strError
        logging.warning('bla2')
        return Response(response=json.dumps({"Error": strError}),
                        status=400,
                        mimetype='application/json')

    logging.warning('bla3')
    move = player.move(data)
    move_ints = (int(move[0]) ,int(move[1]))
    logging.warning('bla4')

    dicResponse={}
    dicResponse['move']=move_ints
    logging.warning('bla5')
    return Response(response=json_util.dumps(dicResponse),
                    status=200,
                    mimetype='application/json')

port = 5000 # Er is geen reden om intern, binnen deze flask container een andere port dan de standaard
            # port voor flask applicaties te gebruiken: port 5000.

# Haal de waarde van FLASK_ENV op en stel debug in op basis van de omgeving
flask_env = os.environ.get('FLASK_ENV', 'production')  # Standaard naar 'production'
debug_mode = flask_env == 'development'  # Debug modus is True als FLASK_ENV 'development' is

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
