from flask import Flask, send_from_directory
from config import APP_NAME, DEBUG, PORT, HOST, SWAGGER_API_URL, SWAGGER_ENDPOINT, SWAGGER_CONFIG
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from mainApp.gui.views import bp_gui
from mainApp.api.routes import bp_api
from mainApp.authentication.routes import bp_auth

app = Flask(__name__)
CORS(app)
app.json.sort_keys = False
app.register_blueprint(bp_gui)
app.register_blueprint(bp_api)
app.register_blueprint(bp_auth)

swagger_document = get_swaggerui_blueprint(SWAGGER_ENDPOINT, SWAGGER_API_URL, config=SWAGGER_CONFIG)
app.register_blueprint(swagger_document, url_prefix=SWAGGER_ENDPOINT)


@app.route("/swagger.json")
def send_swagger():
    return send_from_directory("mainApp/doc/static", "swagger.json")


if __name__ == "__main__":
    print(f"{APP_NAME} started running on {HOST}:{PORT} - Debug mode is {'on' if DEBUG else 'off'}")
    app.run(debug=DEBUG, port=PORT, host=HOST)

