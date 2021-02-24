from flask import Flask, jsonify, request
from wrapper import Classifier
app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
classifier = Classifier("models/tfidf_vectorizer.pkl", "models/svc.sav",
                        "models/full_uni_sg_300_twitter.mdl", "models/bi_lstm.best.hdf5")


def generic_error_response(code, message, headers=None):
    """
    generic error response function to handle the internals error in micro-service api.
    Args:
        code(int): the code of the errors eg:- 400, 500.
        message(str): the message that will appear to the user when you raise the error.
        headers: default api header
    Returns:
        response (dict): dictionary contains the status which is fail and the error message.
        code(int): the code of the errors eg:- 400, 500.
        headers: default api header
    """

    return jsonify({"status": "fail", "results": message}), code, headers


@app.route("/classify", methods=["GET", "POST"])
def classify():
    if request.method == 'GET':
        text = request.args["text"]
    else:
        payload = request.get_json()
        text = payload.get('text', '')

    return jsonify({"status": "success", "results": classifier.classify(text)}), 200


@app.route("/dl_classify", methods=["GET", "POST"])
def dl_classify():
    if request.method == 'GET':
        text = request.args["text"]
    else:
        payload = request.get_json()
        text = payload.get('text', '')
    return jsonify({"status": "success", "results": classifier.dl_model_classify(text)}), 200


@app.errorhandler(404)
def not_found(e):
    """Page not found."""
    return generic_error_response(404, "page not found")


@app.errorhandler(400)
def bad_request(e):
    """Bad request."""
    return generic_error_response(400, "bad request")


@app.errorhandler(500)
def server_error(e):
    """Internal server error."""
    return generic_error_response(500, "internal server error")


def launch_the_app():
    app.run(host='0.0.0.0', debug=True)
