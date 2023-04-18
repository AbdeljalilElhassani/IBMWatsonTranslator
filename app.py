from flask import Flask, render_template, request
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)
languages = [
    'ar', 'en', 'es', 'fr', 'de', 'it', 'ja', 'ko', 'pt', 'ru', 'zh'
]
apikey = 'J8lEybAXTwOLqYhL_06IZTbsr8G8pBsYo6233nWo_WPH'
url = 'https://api.au-syd.language-translator.watson.cloud.ibm.com/instances/c2094ccb-e797-4d44-94e6-c8028defd1e9'

authenticator = IAMAuthenticator(apikey)
lt = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)
lt.set_service_url(url)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        text = request.form['text']
        source = request.form['source']
        target = request.form['target']
        authenticator = IAMAuthenticator(apikey)
        lt = LanguageTranslatorV3(
            version='2018-05-01',
            authenticator=authenticator
        )
        lt.set_service_url(url)
        if source == "Automatic":
            lang = lt.identify(text).get_result()['languages'][0]['language']
            translation = lt.translate(
                text=text,
                source=lang,
                target=target
            ).get_result()['translations'][0]['translation']
        else:
            lang = source
            translation = lt.translate(
                text=text,
                source=lang,
                target=target
            ).get_result()['translations'][0]['translation']
        return render_template('home.html', translation=translation, languages=languages)
    else:
        return render_template('home.html', languages=languages)


@app.route('/translateFile')
def file():
    return render_template('file.html')


@app.route('/translateFile', methods=['GET', 'POST'])
def translateFile():
    # Get the uploaded file
    file = request.files['file']
    source = request.form['source_language']
    target = request.form['target_language']
    if source == "Automatic":
        contents = file.read()
        contents = contents.decode('utf-8')
        lang = lt.identify(contents).get_result()['languages'][0]['language']
    else:
        contents = file.read()
        contents = contents.decode('utf-8')
        lang = source

    # Translate the text to English
    translation = lt.translate(text=contents, source=lang, target=target).get_result()[
        'translations'][0]['translation']

    # Return the translated text as part of the HTML
    return render_template('file.html', translation=translation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
