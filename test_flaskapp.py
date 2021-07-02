from flask import Flask, flash, request, redirect, send_from_directory, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return "testing ..."

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)