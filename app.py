from flask import Flask
from src.apis.itemApis import items_apis
from src.apis.cartApis import cart_apis

app = Flask(__name__)

app.register_blueprint(items_apis)
app.register_blueprint(cart_apis)
# app.register_blueprint(checkout_bp, url_prefix='/checkout')
# app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
