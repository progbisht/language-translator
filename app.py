from flask import Flask, jsonify, request
from happytransformer import HappyTextToText
from happytransformer import TTSettings
from langdetect import detect

app = Flask(__name__)

# Initializing the model to be used for language translation
happy_tt = HappyTextToText("MARIAN", 'Helsinki-NLP/opus-mt-en-fr')

# method for language detection
def detect_language(text):
    try:
        lang_code = detect(text)
        return lang_code
    except:
        return "Unknown"


# method POST for accepting text and translating it to french
@app.route('/translate', methods=['POST'])
def translation():
    data = request.get_json()
    text = data['text']

    if text == "":
        result = {
            "status" : 400,
            "message" : "No Content Received."
        }

    else:
        language = detect_language(text)
    
        if language == 'en':
            # happy_tt = HappyTextToText("MARIAN", 'Helsinki-NLP/opus-mt-en-fr')
            length = len(text)
            args = TTSettings(max_length=length)
            translated = happy_tt.generate_text(text, args=args)
            result = {
                "status" : 200,
                "translated_from" : language,
                "translation" : translated.text
            }
        else:
            result = {
                "status" : 406,
                "message" : "Not Acceptable"
                }


    return jsonify(result)


# main section starts here
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')