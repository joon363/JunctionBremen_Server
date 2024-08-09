from flask import Flask, jsonify, request, Response, Blueprint
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app

def init_db():
    
    # create initial table
    cursor = app.get_db().cursor()
    sql_query='CREATE TABLE IF NOT EXISTS Company \
        (Employee TEXT,Department TEXT, Salary INTEGER, Gender TEXT)'
    cursor.execute(sql_query)
    # ex.
    sql_query='INSERT INTO Company \
        (Employee, Department, Salary, Gender) \
        VALUES (?,?,?,?)'
    cursor.execute(sql_query,('John','sales',5000,'M'))
    app.get_db().commit()
    print("db init complete")


db_bp = Blueprint('db_bp', __name__, url_prefix='/')

@db_bp.route('/database')
def home():
  return 'Hello, this is database page!'


@db_bp.route('/execute_sql', methods = ['GET'])
def execute_sql():
    
    # 기본 순서
    # cursor = app.get_db().cursor()
    # cursor.execute("SELECT * FROM Company")
    # results = cursor.fetchall()
    # cursor.close()
    # return jsonify(results)

    try:
        data = request.get_json()
        sql_query = data['query']
        if sql_query is None:
            return jsonify({"no query error"})
        cursor = app.get_db().cursor()
        cursor.execute(sql_query)
        app.get_db().commit()
        
        # 결과 가져오기 (예: SELECT 문일 경우)
        if sql_query.strip().lower().startswith('select'):
            results = cursor.fetchall()
            cursor.close()
            return jsonify(results)
        
        cursor.close()
        return jsonify({"message": "Query executed successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})