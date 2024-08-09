from flask import Flask, jsonify, request, Response, Blueprint
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app

def init_db():
    # create initial table
    cursor = app.get_db().cursor()
    sql_query='CREATE TABLE IF NOT EXISTS IngredientInfo \
        (Ingredient TEXT,kcal REAL, salt REAL, protein REAL, carbohydrate REAL, fat REAL)'
    cursor.execute(sql_query)
    sql_query="INSERT INTO IngredientInfo \
        (Ingredient, kcal, salt, protein, carbohydrate, fat) VALUES ('coke', 1,2,3,4,5)"
    cursor.execute(sql_query)
    app.get_db().commit()
    cursor.close()
    print("db init complete")


db_bp = Blueprint('db_bp', __name__, url_prefix='/')

@db_bp.route('/database')
def home():
  return 'Hello, this is database page!'

def get_nutrients_info(product_name):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT kcal, salt, protein, carbohydrate, fat FROM IngredientInfo WHERE Ingredient=?", (product_name,))
    result = cursor.fetchone()
    cursor.close()
    return result

@db_bp.route('/getNutrients', methods = ['POST'])
def calc_nutrients():
    try:
        data = request.get_json()
        total_kcal = 0
        total_salt = 0
        total_protein = 0
        total_carbo = 0
        total_fat = 0
        for ingredient, volume in data.items():
            nutrient_info = get_nutrients_info(ingredient)
            if nutrient_info:
                kcal, salt, protein, carbohydrate, fat = nutrient_info
                total_kcal += kcal * volume
                total_salt += salt * volume
                total_protein += protein * volume
                total_carbo += carbohydrate * volume
                total_fat += fat * volume

        result = {
            'kcal': total_kcal,
            'salt': total_salt,
            'protein': total_protein,
            'carboHydrate': total_carbo,
            'fat': total_fat
        }   
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)})

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