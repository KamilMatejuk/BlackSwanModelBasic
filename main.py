import connexion
from flask import jsonify
from decouple import Config, RepositoryEnv
from flask_socketio import SocketIO


'''
{
  "price": 100.45,
  "rsi": 24.876,
  "value_account": 75,
  "value_assets": 25
}
'''
def action():
    try:
        data = connexion.request.json
        assert 'value_account' in data, 'Account value is required'
        assert 'value_assets' in data, 'Assets value is required'
        assert 'price' in data, 'Price is required'
        assert 'rsi' in data, 'RSI is required'
    except Exception as ex:
        return jsonify({"error": "Invalid request schema", "details": str(ex)}), 401
    
    can_buy = data['value_account'] > 0
    can_sell = data['value_assets'] > 0
    if can_sell and data['rsi'] > 75: return -1, 200
    if can_buy and data['rsi'] < 25: return 1, 200
    return 0, 200


config = Config(RepositoryEnv('.env.local'))
port = config.get('PORT')
app = connexion.FlaskApp(__name__,
        server='tornado',
        specification_dir='',
        options={'swagger_url': '/swagger-ui'})
app.add_api('openapi.yaml')
print(f' * Checkout SwaggerUI http://127.0.0.1:{port}/swagger-ui/')
socketio = SocketIO(app.app)
socketio.run(app.app, port=port)
