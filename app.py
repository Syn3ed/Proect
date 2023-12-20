from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import speech_recognition as sr

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создаем объект распознавания
recognizer = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audioFile' in request.files:
        audio_file = request.files['audioFile']

        if audio_file.filename != '':
            # Создаем безопасное имя файла
            filename = secure_filename(audio_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Сохраняем файл
            audio_file.save(file_path)

            print('Файл успешно загружен и сохранен в:', file_path)

            # Распознавание речи
            try:
                with sr.AudioFile(file_path) as source:
                    audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='ru-RU')
                print("Распознанный текст: " + text)

                # Возвращаем распознанный текст как ответ на запрос
                return 'Распознаный текст: {}'.format(text)

            except sr.UnknownValueError:
                print("Речь не распознана")
                return 'Ошибка: Речь не распознана'
            except sr.RequestError as e:
                print("Ошибка при запросе к сервису распознавания: {0}".format(e))
                return 'Ошибка при распознавании речи'

        else:
            print('Ошибка: Файл не выбран')
            return 'Ошибка: Файл не выбран'
    else:
        print('Ошибка: Файл не отправлен')
        return 'Ошибка: Файл не отправлен'

if __name__ == '__main__':
    app.run(debug=True)
