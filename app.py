from flask import Flask
from flask.cli import load_dotenv
from src.apis.itemApis import items_apis
from src.apis.cartApis import cart_apis
from src.apis.checkoutApi import checkout_apis
app = Flask(__name__)

app.register_blueprint(items_apis)
app.register_blueprint(cart_apis)
app.register_blueprint(checkout_apis)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port=5000)
