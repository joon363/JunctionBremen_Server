from flask import jsonify, request, Blueprint, send_file
import os
import json
from datetime import datetime, timedelta
import app

def insert_dummy():
    c = app.get_db().cursor()
    menu_info_data = [
        ('청담동김밥', '김밥', 'default', '기본적인 김밥', '일반', 250, 2, 8, 40, 5, 'basic_kimbab.jpg', 5000),
        ('청담동김밥', '김밥', '마요네즈', '마요네즈를 추가한 참치김밥', '일반', 300, 3, 12, 35, 7, 'tuna_kimbab.jpg', 6000),
        ('블루커피', '아메리카노', 'default', '클래식 아메리카노', '음료', 10, 0, 0, 2, 0, 'americano.jpg', 4000),
        ('블루커피', '아메리카노', '시럽 추가', '바닐라 시럽 추가', '음료', 50, 0, 0, 8, 0, 'americano_syrup.jpg', 4500),
        ('블루커피', '라떼', 'default', '부드러운 라떼', '음료', 150, 0.5, 6, 15, 7, 'latte.jpg', 5000)
    ]

    menu_options_data = [
        ('청담동김밥', '김밥', 'default', '기본 옵션'),
        ('청담동김밥', '김밥', '마요네즈', '추가 옵션'),
        ('블루커피', '아메리카노', 'default', '시럽'),
        ('블루커피', '아메리카노', '시럽 추가', '시럽')
    ]

    menu_groups_data = [
        ('청담동김밥', '김밥', '기본 옵션', 'radiobutton', 1, 1),
        ('청담동김밥', '김밥', '추가 옵션', 'checkbox', 0, 1),
        ('블루커피', '아메리카노', '시럽 추가', 'radiobutton', 0, 1)
    ]

    store_details_data = [
        ('청담동김밥', '서울의 유명한 김밥집', 'kimbab.jpg', 37.5234, 127.0248, 4.5),
        ('블루커피', '신선한 원두를 사용하는 커피숍', 'coffee.jpg', 37.5111, 127.0983, 4.2)
    ]

    reviews_data = [
        ('2024-08-05 14:30', 101, '청담동김밥', '김밥', 5, 1, 'review1.jpg', '정말 맛있어요!'),
        ('2024-08-06 16:45', 101, '청담동김밥', '김밥', 4, 1, 'review2.jpg', '참치가 신선하네요!'),
        ('2024-08-07 18:00', 103, '블루커피', '아메리카노', 3, 0, None, '조금 싱거운 편이에요.'),
        ('2024-08-08 19:30', 103, '블루커피', '라떼', 4, 1, 'review4.jpg', '부드럽고 크리미해요.')
    ]

    ingredients_data = [
        ('김치', 30, 1.2, 2.0, 4.0, 0.3),
        ('참치', 184, 0.7, 25.0, 0, 8.0),
        ('커피', 2, 0, 0.3, 0, 0),
        ('우유', 42, 0.1, 3.4, 4.9, 1.0)
    ]
    tables = ['MenuInfo', 'MenuOptionInfo', 'GroupInfo', 'StoreInfo', 'OrderInfo', 'IngredientInfo']
    empty_tables = []
    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        if count == 0:
            empty_tables.append(table)

    # 모든 테이블이 비어 있는지 확인
    if len(empty_tables) != len(tables):
        return
    
    # 데이터베이스에 데이터 삽입
    c.executemany('INSERT INTO MenuInfo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', menu_info_data)
    c.executemany('INSERT INTO MenuOptionInfo VALUES (?, ?, ?, ?)', menu_options_data)
    c.executemany('INSERT INTO GroupInfo VALUES (?, ?, ?, ?, ?, ?)', menu_groups_data)
    c.executemany('INSERT INTO StoreInfo VALUES (?, ?, ?, ?, ?, ?)', store_details_data)
    c.executemany('INSERT INTO OrderInfo VALUES (?, ?, ?, ?, ?, ?, ?, ?)', reviews_data)
    c.executemany('INSERT INTO IngredientInfo VALUES (?, ?, ?, ?, ?, ?)', ingredients_data)

    # 커밋 및 연결 종료

    app.get_db().commit()
    c.close()
    print("dummy insert complete")
    return