import json
import boto3
import urllib3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CryptoPrecios')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CryptoPrecios')

def lambda_handler(event, context):
    try:
        # Obtener precios de BTC y ETH desde CoinMarketCap API
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        params = {
            'symbol': 'BTC,ETH'
        }
        headers = {
            'X-CMC_PRO_API_KEY': 'ae927795-11bd-4aca-917f-eef3bc5237fa'
        }
        http = urllib3.PoolManager()
        response = http.request('GET', url, fields=params, headers=headers)
        data = json.loads(response.data.decode('utf-8'))

        # Formatear datos y almacenarlos en DynamoDB
        for crypto in ['BTC', 'ETH']:
            precio = str(data['data'][crypto]['quote']['USD']['price'])
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
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: ' + str(e))
        }