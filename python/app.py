from flask import Flask, jsonify, request
from flask_cors import CORS

import request.request as req
import controller.auth.auth as user
import controller.attraction as attraction
import controller.comments as comments  # You'll need to create this controller


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

# Attraction
@app.post('/attraction')
def addAttraction():
    print("okok", flush=True)
    # Fonction vérif token
    checkToken = user.check_token(request)
    if (checkToken != True):
        return checkToken

    json = request.get_json()
    retour = attraction.add_attraction(json)
    if (retour):
        return jsonify({"message": "Element ajouté.", "result": retour}), 200
    return jsonify({"message": "Erreur lors de l'ajout.", "result": retour}), 500

@app.get('/attraction')
def getAllAttraction():
    result = attraction.get_all_attraction()
    return result, 200

@app.get('/attraction/<int:index>')
def getAttraction(index):
    result = attraction.get_attraction(index)
    return result, 200

@app.delete('/attraction/<int:index>')
def deleteAttraction(index):

    # Fonction vérif token
    checkToken = user.check_token(request)
    if (checkToken != True):
        return checkToken

    json = request.get_json()
    
    if (attraction.delete_attraction(index)):
        return "Element supprimé.", 200
    return jsonify({"message": "Erreur lors de la suppression."}), 500

@app.post('/login')
def login():
    json = request.get_json()

    if (not 'name' in json or not 'password' in json):
        result = jsonify({'messages': ["Nom ou/et mot de passe incorrect"]})
        return result, 400
    
    cur, conn = req.get_db_connection()
    requete = f"SELECT * FROM users WHERE name = '{json['name']}' AND password = '{json['password']}';"
    cur.execute(requete)
    records = cur.fetchall()
    conn.close()

    result = jsonify({"token": user.encode_auth_token(list(records[0])[0]), "name": json['name']})
    return result, 200

# Comments routes
@app.post('/critique')
def addCritique():
    # Fonction vérif token
    checkToken = user.check_token(request)
    if (checkToken != True):
        return checkToken

    json = request.get_json()
    retour = comments.add_critique(json)
    if (retour):
        return jsonify({"message": "Commentaire ajouté.", "result": retour}), 200
    return jsonify({"message": "Erreur lors de l'ajout du commentaire.", "result": retour}), 500

@app.get('/critique')
def getAllCritiques():
    result = comments.get_all_critiques()
    return result, 200

@app.get('/critique/attraction/<int:attraction_id>')
def getCritiquesByAttraction(attraction_id):
    result = comments.get_critiques_by_attraction(attraction_id)
    return result, 200

@app.get('/critique/<int:index>')
def getCritique(index):
    result = comments.get_critique(index)
    return result, 200

@app.delete('/critique/<int:index>')
def deleteCritique(index):
    # Fonction vérif token
    checkToken = user.check_token(request)
    if (checkToken != True):
        return checkToken
    
    if (comments.delete_critique(index)):
        return "Commentaire supprimé.", 200
    return jsonify({"message": "Erreur lors de la suppression du commentaire."}), 500