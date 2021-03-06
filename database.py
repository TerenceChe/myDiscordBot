import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://terence_1:terence_1@cluster0.xnv8m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client["mydatabase"]
balance_collection = database["balance"]
share_collection = database["shares"]


def user_balance(uid):
    ids = balance_collection.find({}, {'uid': 1, 'balance': 1})

    # check if user is in collection
    for n in ids:
        if uid == n.get('uid'):
            return n.get('balance')

    # add user with 1 million balance
    print("adding user")
    new_user = {'uid': uid, 'balance': 1000000}
    balance_collection.insert_one(new_user)
    return 1000000


def add_stock(uid, stock, shares, price):
    balance = user_balance(uid)

    # if the user has enough money, allow them to buy stock
    if balance > (price * shares):

        # if they already have the stock, update the table entry

        share_collection.update_one({'uid': uid, 'stock': stock}, {'$inc': {'amount': shares}})

        # create a new entry if there is none yet
        entry = {"uid": uid, "stock": stock, "amount": shares}
        share_collection.insert_one(entry)

        return True
    else:
        return False
