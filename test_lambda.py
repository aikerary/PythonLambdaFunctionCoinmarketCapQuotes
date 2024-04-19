import unittest
from unittest.mock import patch, MagicMock
import lambda_function

class TestLambdaFunction(unittest.TestCase):

    @patch('lambda_function.requests.get')
    @patch('lambda_function.boto3.resource')
    def test_lambda_handler(self, mock_boto3_resource, mock_requests_get):
        # Simular la respuesta de la API de CoinMarketCap
        mock_response = {
            "data": {
                "BTC": {
                    "quote": {
                        "USD": {
                            "price": 60000
                        }
                    }
                },
                "ETH": {
                    "quote": {
                        "USD": {
                            "price": 2000
                        }
                    }
                }
            }
        }
        mock_requests_get.return_value.json.return_value = mock_response

        # Simular la tabla de DynamoDB
        mock_table = MagicMock()
        mock_boto3_resource.return_value.Table.return_value = mock_table

        # Llamar a la función Lambda
        event = {}
        context = {}
        response = lambda_function.lambda_handler(event, context)

        # Verificar que se almacenaron los datos correctamente en DynamoDB
        mock_table.put_item.assert_any_call(Item={'CryptoId': 'BTC', 'Fecha': mock.ANY, 'Precio': 60000})
        mock_table.put_item.assert_any_call(Item={'CryptoId': 'ETH', 'Fecha': mock.ANY, 'Precio': 2000})

        # Verificar que la respuesta de la función Lambda es correcta
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '{"statusCode": 200, "body": "Precios actualizados correctamente"}')

if __name__ == '__main__':
    unittest.main()