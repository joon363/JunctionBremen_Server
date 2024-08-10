from flask import jsonify, request, Blueprint, send_file
import app
import dummydata
def init_db():
    # create initial table
    cursor = app.get_db().cursor()
    sql_query='''
    CREATE TABLE IF NOT EXISTS IngredientInfo (
        Ingredient TEXT,
        kcal REAL, 
        salt REAL, 
        protein REAL, 
        carbohydrate REAL, 
        fat REAL
    )'''
    cursor.execute(sql_query)
    sql_query='''
    CREATE TABLE IF NOT EXISTS MenuInfo (
        storeName TEXT,
        menuName TEXT,
        optionName TEXT,
        description TEXT,
        menuType TEXT,
        kcal INTEGER,
        salt INTEGER,
        protein INTEGER,
        carbohydrate INTEGER,
        fat INTEGER,
        menuImageURL TEXT, 
        price INTEGER
    )'''
    cursor.execute(sql_query)
    sql_query='''CREATE TABLE IF NOT EXISTS MenuOptionInfo (
        storeName TEXT, 
        menuName TEXT, 
        optionName TEXT, 
        groupName TEXT
    )'''
    cursor.execute(sql_query)
    sql_query='''CREATE TABLE IF NOT EXISTS GroupInfo (
        storeName TEXT, 
        menuName TEXT, 
        groupName TEXT, 
        groupType TEXT, 
        groupMin INTEGER, 
        groupMax INTEGER
    )'''
    cursor.execute(sql_query)
    sql_query='''CREATE TABLE IF NOT EXISTS StoreInfo (
        storeName TEXT, 
        description TEXT, 
        storeImageURL TEXT, 
        latitude REAL, 
        longitude REAL, 
        preference REAL
    )'''
    cursor.execute(sql_query)
    sql_query='''CREATE TABLE IF NOT EXISTS OrderInfo (
        dateTime TEXT, 
        userID INTEGER, 
        storeName TEXT, 
        menuName TEXT, 
        stars INTEGER, 
        isReviewed INTEGER, 
        reviewImageURL TEXT, 
        reviewText TEXT
    )'''
    cursor.execute(sql_query)
    app.get_db().commit()
    cursor.close()
    dummydata.insert_dummy()
    print("db init complete")
