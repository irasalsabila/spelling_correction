from flask import Flask, request
import datetime, json
import logging
from logging.handlers import RotatingFileHandler
import spelling_correction_function as sf
from collections import Counter
from spellchecker import SpellChecker

# Configure logging
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler = RotatingFileHandler("logs/logs.log", maxBytes=100 * 1024 * 1024, backupCount=5)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
log.addHandler(handler)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    request_data = request.get_json()
    if (not request_data):
        request_data = request.get_data()
        request_data = json.loads(request_data)

    # Get current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract text from request
    text = request_data.get('text')
    language = request_data.get('lang')

    # Log the received request details
    log.info('Receive request for Unscramble Words for "' + text + '" with process date ' + now )

    try:

        spell_corrected = sf.correct_spelling(text, language)
        
        # Check if locations are detected
        if spell_corrected:
            # Return success response with detected locations
            return app.response_class(
                response=json.dumps({
                    # "response": "OK",
                    # "message": "Process completed",
                    "original_sentence": text,
                    "corrected_sentence": spell_corrected
                }),
                status = 200,
                mimetype = 'application/json'
            )
        else:
            # Return success response with message if no locations are detected
            return app.response_class(
                response = json.dumps({"response":"OK", "message":"Words not detected in the text"}),
                status = 201,
                mimetype = 'application/json'
            )
        
    except Exception as Error:
        # Log error and return failure response
        log.error('Process Failed.')
        log.exception(Error)
        return app.response_class(
            response = json.dumps({"response":"FAILED", "message":str(Error).replace("'", "")}),
            status = 403,
            mimetype = 'application/json'
        )

if __name__ == '__main__':
    # Start the Flask application on localhost (127.0.0.1) with debug mode enabled and port 5002.
    app.run(debug=True, host='127.0.0.1', port=5002)