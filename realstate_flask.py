from flask import Flask, flash, request, redirect, send_from_directory, render_template
import time


app = Flask(__name__)


count = 0


def check_realstates():
    while(True):
        if(count<10):
            time.sleep(2)
            print(count)
            count+=1
        else:
            print("Doing ....")
            count=0

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            pw = request.form.get("pw")
            print(pw)
            if(not pw=="123"):
                return "Wrong Password"
            url_content = request.form.get("urls")
            raw_urls = url_content.strip().split("\n")
            urls=[]
            file=open("urls","w")
            for i in range(0, len(raw_urls)):
                url=raw_urls[i].replace("\r","")
                urls.append(url)
                file.write(url+"\n")
            file.close()
            print(urls)
            global count
            count = 10
            return "Urls are submitted"
        return render_template('inputurl.html')
    except:
        return "Bad request"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)