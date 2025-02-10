import request.request as req
from flask import jsonify

def add_critique(json):
    try:
        cur, conn = req.get_db_connection()
        requete = """
            INSERT INTO critiques (note, commentaire, attraction_id, users_id) 
            VALUES (%s, %s, %s, %s)
        """
        values = (json['note'], json['commentaire'], json['attraction_id'], json['users_id'])
        cur.execute(requete, values)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return False

def get_all_critiques():
    try:
        cur, conn = req.get_db_connection()
        requete = "SELECT * FROM critiques;"
        cur.execute(requete)
        records = cur.fetchall()
        conn.close()
        return jsonify(records)
    except Exception as e:
        print(e, flush=True)
        return jsonify([])

def get_critiques_by_attraction(attraction_id):
    try:
        cur, conn = req.get_db_connection()
        requete = "SELECT * FROM critiques WHERE attraction_id = %s;"
        cur.execute(requete, (attraction_id,))
        records = cur.fetchall()
        conn.close()
        return jsonify(records)
    except Exception as e:
        print(e, flush=True)
        return jsonify([])

def get_critique(index):
    try:
        cur, conn = req.get_db_connection()
        requete = "SELECT * FROM critiques WHERE critique_id = %s;"
        cur.execute(requete, (index,))
        records = cur.fetchall()
        conn.close()
        return jsonify(records[0] if records else None)
    except Exception as e:
        print(e, flush=True)
        return jsonify(None)

def delete_critique(index):
    try:
        cur, conn = req.get_db_connection()
        requete = "DELETE FROM critiques WHERE critique_id = %s;"
        cur.execute(requete, (index,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e, flush=True)
        return False