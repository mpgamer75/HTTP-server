from flask import Flask, request, jsonify
import json
import os 
import logging 
import port_scanner.py


#Initialisation de l'application Flask 

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSONIFY_MIMETYPE'] = 'application/json'

#Serveur HTTP 

@app.route('/api/scan', methods=['POST'])
def scan_ports():
    """Endpoint pour scanner les ports."""
    data = request.get_json()
    host = data.get('host')
    start_port = data.get('start_port')
    end_port = data.get('end_port')

    if not host or not start_port or not end_port:
        return jsonify({"error": "Parametres manquants"}), 400
    
    if not isinstance(start_port, int) or not isinstance(end_port, int):
        return jsonify({"error": "Les ports doivent etre des entiers"}), 400
    
    if start_port < 0 or end_port > 65535 or start_port > end_port:
        return jsonify({"error": "Plage de ports invalide"}), 400
    
    # Appel de la fonction de scan de ports
    open_ports = port_scanner.scan_ports(host, start_port, end_port)
    if open_ports is None:
        return jsonify({"error": "Erreur lors du scan des ports"}), 500
    
    return jsonify({"open_ports": open_ports}), 200

@app.route('/api/close', methods=['POST'])

def close_ports():
    """Endpoint pour fermer les ports."""
    data = request.get_json()
    start_port = data.get('start_port')
    end_port = data.get('end_port')

    if not start_port or not end_port:
        return jsonify({"error": "Parametres manquants"}), 400
    
    if not isinstance(start_port, int) or not isinstance(end_port, int):
        return jsonify({"error": "Les ports doivent etre des entiers"}), 400
    
    if start_port < 0 or end_port > 65535 or start_port > end_port:
        return jsonify({"error": "Plage de ports invalide"}), 400
    
    # Appel de la fonction de fermeture de ports
    closed_ports = port_scanner.close_ports(start_port, end_port)
    if closed_ports is None:
        return jsonify({"error": "Erreur lors de la fermeture des ports"}), 500
    
    return jsonify({"closed_ports": closed_ports}), 200
