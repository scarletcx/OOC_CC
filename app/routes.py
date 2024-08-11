from flask import request, jsonify
from app import app, mongo

@app.route('/buyBait/<uid>/<int:baitNumber>/<int:coins>', methods=['GET'])
def buy_bait(uid, baitNumber, coins):
    result = mongo.db.users.update_one(
        { "UserID": uid },  # 查询条件
        { "$inc": { "baitNumber": baitNumber,"GMCNumber": -coins  }, }  # 增减
        
    )
    GMCNumberNow = mongo.db.users.find_one({'UserID': uid})['GMCNumber']
    baitNumberNow = mongo.db.users.find_one({'UserID': uid})['baitNumber']
    buyResult = {
        "code": 0,
        "message": "success",
        "data": {
        "uid": uid,
        "coinsNow": GMCNumberNow,
        "baitNumberNow": baitNumberNow
        }
    }
    if result.modified_count > 0:
        return jsonify(buyResult), 200
    else:
        return jsonify({"message": "No document found or data unchanged"}), 404

@app.route('/sellFish/<uid>/<int:fishPrice>', methods=['GET'])
def sell_fish(uid, fishPrice):
    result = mongo.db.users.update_one(
        { "UserID": uid },  # 查询条件
        { "$inc": { "GMCNumber": fishPrice } }  # 增加 fishPrice
    )

    GMCNumber = mongo.db.users.find_one({'UserID': uid})['GMCNumber']
    sellResult = {
        "code": 0,
        "message": "success",
        "data": {
        "uid": uid,
        "coinsNow": GMCNumber
        }
    }
    if result.modified_count > 0:
        return jsonify(sellResult), 200
    else:
        return jsonify({"message": "No document found or data unchanged"}), 404
