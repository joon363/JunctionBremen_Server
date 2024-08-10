from flask import Flask, jsonify, request, Response, Blueprint, send_file
import requests
import os
import sys
import json
from datetime import datetime, timedelta
import app

def init_db():
    # create initial table
    cursor = app.get_db().cursor()
    sql_query='CREATE TABLE IF NOT EXISTS IngredientInfo (Ingredient TEXT,kcal REAL, salt REAL, protein REAL, carbohydrate REAL, fat REAL)'
    cursor.execute(sql_query)
    sql_query='CREATE TABLE IF NOT EXISTS MenuInfo (storeName TEXT,menuName TEXT,optionName TEXT,description TEXT,menuType TEXT,kcal INTEGER,salt INTEGER,protein INTEGER,carbohydrate INTEGER,fat INTEGER,menuImageURL TEXT, price INTEGER)'
    cursor.execute(sql_query)
    sql_query='CREATE TABLE IF NOT EXISTS MenuOptionInfo (storeName TEXT, menuName TEXT, optionName TEXT, groupName TEXT)'
    cursor.execute(sql_query)
    sql_query='CREATE TABLE IF NOT EXISTS GroupInfo (storeName TEXT, menuName TEXT, groupName TEXT, groupType TEXT, groupMin INTEGER, groupMax INTEGER)'
    cursor.execute(sql_query)
    sql_query='CREATE TABLE IF NOT EXISTS StoreInfo (storeName TEXT, description TEXT, storeImageURL TEXT, latitude REAL, longitude REAL, preference REAL)'
    cursor.execute(sql_query)
    sql_query='CREATE TABLE IF NOT EXISTS OrderInfo (dateTime TEXT, userID INTEGER, storeName TEXT, menuName TEXT, stars INTEGER, isReviewed INTEGER, reviewImageURL TEXT, reviewText TEXT)'
    cursor.execute(sql_query)
    app.get_db().commit()
    cursor.close()
    print("db init complete")

db_bp = Blueprint('db_bp', __name__, url_prefix='/')

# get all stores in db
@db_bp.route('/storeInfo/', methods = ['GET'])
def get_all_stores():
    cursor = app.get_db().cursor()
    cursor.execute("SELECT storeName FROM StoreInfo")
    result = cursor.fetchall()
    cursor.close()
    store_names = [row[0] for row in result]
    json_data = json.dumps(store_names)
    return json_data

# store Text
@db_bp.route('/storeInfo/<storeName>/text', methods = ['GET'])
def get_store_text(storeName):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT description FROM StoreInfo WHERE storeName=?", (storeName,))
    result = cursor.fetchone()
    cursor.close()
    return jsonify(result)

# store Image
@db_bp.route('/storeInfo/<storeName>/image', methods = ['GET'])
def get_store_image(storeName):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT storeImageURL FROM StoreInfo WHERE storeName=?", (storeName,))
    result = cursor.fetchone()
    cursor.close()
    storeImageURL = result[0]
    imagePath = os.path.join(os.path.dirname(__file__), 'static', 'staticdata_stores',storeImageURL)
    return send_file(imagePath, mimetype='image/jpeg')

# get all menu names from a store
@db_bp.route('/menuInfo/<storeName>', methods = ['GET'])
def get_all_menu(storeName):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT menuName FROM MenuInfo WHERE storeName=?", (storeName,))
    result = cursor.fetchall()
    cursor.close()
    menu_names = [row[0] for row in result]
    json_data = json.dumps(menu_names)
    return json_data

# menu info
@db_bp.route('/menuInfo/<storeName>/<menuName>/text', methods = ['GET'])
def get_menu_text(storeName, menuName):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT menuName, description, kcal, salt, protein, carbohydrate, fat, price FROM MenuInfo WHERE storeName=? AND menuName=? AND optionName='default'", (storeName,menuName,))
    result = cursor.fetchone()
    cursor.close()
    return jsonify(result)

# menu image
@db_bp.route('/menuInfo/<storeName>/<menuName>/image', methods = ['GET'])
def get_menu_image(storeName, menuName):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT menuImageURL FROM MenuInfo WHERE storeName=? AND menuName=?", (storeName,menuName,))
    result = cursor.fetchone()
    cursor.close()
    menuImageURL = result[0]
    imagePath = os.path.join(os.path.dirname(__file__), 'static', 'staticdata_stores',menuImageURL)
    return send_file(imagePath, mimetype='image/jpeg')

# option group info
# example output
"""
{
    "groupName1": {
        "options": ["option1", "option2", "option3"],
        "prices" : [0, 1000, 2000]
        "kcal": [10, 20, 30],
        "salt": [10, 20, 30],
        "protein": [1, 2, 3],
        "carbohydrate": [5, 6, 7],
        "fat": [8, 9, 10],
        "groupType": "checkbox"
        "groupText": "최소 1개부터 3개까지 선택해 주세요",
        "groupMin":1,
        "groupMax":3
    },
    "groupName2": {
        "options": ["option4", "option5"],
        "prices" : [0, 1000, 2000]
        ...
        "groupType": "radiobutton"
        "groupText": "하나를 선택해 주세요",
        "groupMin": 1,
        "groupMax": 1
    }
}
"""
@db_bp.route('/menuInfo/<storeName>/<menuName>/options', methods = ['GET'])
def get_menu_options(storeName, menuName):
    cursor = app.get_db().cursor()
    cursor.execute("""
        SELECT 
            g.groupName, 
            g.groupType, 
            g.groupMin, 
            g.groupMax,
            o.optionName, 
            m.price,
            m.kcal,
            m.salt,
            m.protein,
            m.carbohydrate,
            m.fat
        FROM 
            GroupInfo g
        JOIN 
            MenuOptionInfo o ON g.groupName = o.groupName AND g.storeName = o.storeName AND g.menuName = o.menuName
        JOIN 
            MenuInfo m ON g.storeName = m.storeName AND g.menuName = m.menuName AND o.optionName = m.optionName
        WHERE 
            g.storeName = ? AND g.menuName = ?;
        """, (storeName, menuName))
    groups = cursor.fetchall()
    cursor.close()
    group_dict = {}
    for group in groups:
        groupName, groupType, groupMin, groupMax, optionName, price, kcal, salt, protein, carbohydrate, fat = group

        group_text = ""
        if groupType=="checkbox":
            group_text='최소 {0}개부터 {1}개까지 선택해 주세요'.format(groupMin,groupMax)
        else:
            group_text='하나를 선택해 주세요'

        if groupName not in group_dict:
            group_dict[groupName] = {
                "options": [],
                "prices" : [],
                "kcal": [],
                "salt": [],
                "protein": [],
                "carbohydrate": [],
                "fat": [],
                "groupType": groupType,
                "groupText":group_text,
                "groupMin": groupMin,
                "groupMax": groupMax
            }
        
        group_dict[groupName]["options"].append(optionName)
        group_dict[groupName]["prices"].append(price)
        group_dict[groupName]["kcal"].append(kcal)
        group_dict[groupName]["salt"].append(salt)
        group_dict[groupName]["protein"].append(protein)
        group_dict[groupName]["carbohydrate"].append(carbohydrate)
        group_dict[groupName]["fat"].append(fat)

    # JSON으로 반환
    return jsonify(group_dict)


# 재현ai적용
@db_bp.route('/imageAI/processImage', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'No image part', 400

    image = request.files['image']

    if image.filename == '':
        return 'No selected file', 400
    return run_ai(image)

def run_ai(image):
    # python code
    # ai 들어가는곳
    data={"coke":13.2, "suka":123.0}
    return calc_nutrients(data)


# 음식의 구성 성분에 따른 영양성분 얻어오기
# input: "토마토 파스타"
# output: kcal, salt, protein, carbohydrate, fat
def get_nutrients_info(product_name):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT kcal, salt, protein, carbohydrate, fat FROM IngredientInfo WHERE Ingredient=?", (product_name,))
    result = cursor.fetchone()
    cursor.close()
    return result

# 음식의 구성 성분 부피 목록에 따른 총 영양성분 얻어오기
# input: "토마토 파스타":100, "콜라":150
# output: kcal, salt, protein, carbohydrate, fat
def calc_nutrients(data):
    try:
        # data = request.get_json()
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


# 유저 리뷰 모아보기
@db_bp.route('/menuInfo/<storeName>/reviews/text', methods = ['GET'])
def get_all_reviews_text(storeName, menuName):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT * FROM OrderInfo WHERE storeName=? AND menuName=?", (storeName,menuName,))
    reviews = cursor.fetchall()
    cursor.close()
    
    dateTimes= []
    userIDs = []
    menuNames= []
    starss=[]
    reviewImageURLs=[]
    reviewTexts= []
    for review in reviews:
        dateTime, userID, storeName, menuName, stars, isReviewed, reviewImageURL, reviewText = review
        
        if stars == 0 or isReviewed == 0:
            continue
        else:
            dateTimes.append(dateTime)
            userIDs.append(userID)
            menuNames.append(menuName)
            starss.append(stars)
            reviewImageURLs.append(reviewImageURL)
            reviewTexts.append(reviewText)

    result = {
        "dateTimes": dateTimes,
        "userIDs": userIDs,
        "menuNames": menuNames,
        "stars": starss,
        "reviewImageURLs": reviewImageURLs,
        "reviewTexts": reviewTexts
    }
    
    return jsonify(result)

# 유저 리뷰 사진 불러오기
@db_bp.route('/menuInfo/<storeName>/reviews/<reviewImageURL>', methods = ['GET'])
def get_review_image(reviewImageURL):
    reviewImage = reviewImageURL
    imagePath = os.path.join(os.path.dirname(__file__), 'static', 'staticdata_reviews',reviewImage)
    return send_file(imagePath, mimetype='image/jpeg')

# 유저 기록 조회하기
@db_bp.route('/orderInfo/<userID>', methods = ['GET'])
def get_order_info(userID):
    cursor = app.get_db().cursor()
    cursor.execute("SELECT dateTime, storeName,	menuName, stars FROM OrderInfo WHERE userID=?",(userID,))
    result = cursor.fetchall()
    cursor.close()
    record = []
    for row in result:
        dateTime, storeName, menuName, stars = row
        result.append({
            "dateTime": dateTime,
            "storeName": storeName,
            "menuName": menuName,
            "stars": stars
        })

    # JSON으로 반환
    return jsonify(record)

# 유저 최근 30일 개수 조회하기
@db_bp.route('/orderInfo/<userID>/oneMonthCount', methods = ['GET'])
def get_one_month_count(userID):
    cursor = app.get_db().cursor()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("SELECT COUNT(*) FROM OrderInfo WHERE dateTime >= ?", (thirty_days_ago_str,))
    count = cursor.fetchone()[0]
    cursor.close()
    return jsonify({"count": count})