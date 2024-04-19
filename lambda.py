import json
import boto3
import requests
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CryptoPrecios')

def lambda_handler(event, context):
    # Obtener precios de BTC y ETH desde CoinMarketCap API
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': 'BTC,ETH'
    }
    headers = {
        'ae927795-11bd-4aca-917f-eef3bc5237fa'
    }
    response = requests.get(url, params=params, headers=headers).json()

    # Formatear datos y almacenarlos en DynamoDB
    for crypto in ['BTC', 'ETH']:
        precio = response['data'][crypto]['quote']['USD']['price']
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item = {
            'CryptoId': crypto,
            'Fecha': fecha,
            'Precio': precio
        }
        table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps('Precios actualizados correctamente')
    }