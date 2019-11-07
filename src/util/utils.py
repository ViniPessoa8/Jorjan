from itertools import groupby
from operator import itemgetter

def format_history_result(result):
    grouper = itemgetter('id', 'date', 'seller_id', 'observation', 'status')
    history = [{
        'id': key[0],
        'date': key[1],
        'seller_id': key[2],
        'observation': key[3],
        'status': key[4],
        'products': [{
            'id': p['product_id'],
            'name': p['product_name'],
            'category_id': p['product_category'],
            'description': p['product_description'],
            'price': p['product_price'],
            'quantity': p['product_quantity'],
        } for p in list(group) if p['product_id'] != None]
    } for key, group in groupby(result, key=grouper)]

    return history