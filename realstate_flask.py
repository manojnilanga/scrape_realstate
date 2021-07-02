from flask import Flask, flash, request, redirect, send_from_directory, render_template
import time
from threading import Thread
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import smtplib, ssl

app = Flask(__name__)

def scrape_data(checking_urls):
    final_onmarket = []
    final_offmarket = []

    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)

    # driver = webdriver.Chrome()

    for m in range(0, len(checking_urls)):
        print("Start scraping ..")

        driver.get(checking_urls[m])
        agent = checking_urls[m].split("/")[-1]

        # listings arrow down
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="review"]/div[2]/i')))
        driver.find_element_by_xpath('//*[@id="review"]/div[2]/i').click()
        time.sleep(2)

        # on market
        onmarket_url_list = []
        print("scraping on market")
        for i in range(1, 5):
            try:
                driver.find_element_by_xpath(
                    '//*[@id="collapseOne5"]/div[2]/div/div[2]/div[' + str(i) + ']/div/div[1]/div').click()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])
                print(driver.current_url)
                onmarket_url_list.append(agent+" - "+driver.current_url)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
            except:
                break

        final_onmarket+=onmarket_url_list
        # off market
        offmarket_url_list = []
        print("scraping off market")
        for i in range(1, 5):
            try:
                driver.find_element_by_xpath(
                    '//*[@id="collapseOne5"]/div[3]/div/div[2]/div[' + str(i) + ']/div/div[1]/div').click()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])
                print(driver.current_url)
                offmarket_url_list.append(agent+" - "+driver.current_url)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
            except:
                break

        final_offmarket += offmarket_url_list
        time.sleep(4)
    driver.close()

    #checking old data with new for send email
    file_off = open("off_market.txt")
    old_off = file_off.read().strip().split("\n")
    print("old_off")
    print(old_off)
    file_off.close()

    file_on = open("on_market.txt")
    old_on = file_on.read().strip().split("\n")
    print("old_on")
    print(old_on)
    file_on.close()

    print("final_onmarket")
    print(final_onmarket)

    print("final_offmarket")
    print(final_offmarket)

    print(len(old_off))
    if(len(old_off)>1):
        newly_added_realstate = []
        for p in range(0, len(final_onmarket)):
            if(not final_onmarket[p] in old_on):
                newly_added_realstate.append(final_onmarket[p])

        newly_sold_realstate = []
        for q in range(0, len(final_offmarket)):
            if(final_offmarket[q] in old_on):
                newly_sold_realstate.append(final_offmarket[q])

        send_mail(newly_added_realstate, newly_sold_realstate)

    #writing new data to files
    file_off = open("off_market.txt","w")
    for a in range(0 ,len(final_offmarket)):
        file_off.write(final_offmarket[a]+"\n")
    file_off.close()
    file_on = open("on_market.txt", "w")
    for a in range(0, len(final_onmarket)):
        file_on.write(final_onmarket[a] + "\n")
    file_on.close()

def send_mail(newly_added_realstate , newly_sold_realstate):
    message = ""
    print("newly_added_realstate")
    print(newly_added_realstate)
    print("newly_sold_realstate")
    print(newly_sold_realstate)
    sender_mail = "agentlistingupdates@gmail.com"
    password = "Testacc101"
    receiver_mail = "ray@infiniteviewsllc.com"
    gmail_server = "smtp.gmail.com"
    gmail_port = 465
    context = ssl.create_default_context()
    if(len(newly_added_realstate)>0 or len(newly_sold_realstate)>0 ):
        if(len(newly_added_realstate)!=0):
            message+="newly added realstate --->\n\n"
            for k in range(0, len(newly_added_realstate)):
                message+=newly_added_realstate[k]+"\n"
        message+="\n"
        if (len(newly_sold_realstate) != 0):
            message += "newly sold realstate --->\n\n"
            for k in range(0, len(newly_sold_realstate)):
                message += newly_sold_realstate[k] + "\n"
        print("Message content for the mail :")
        print(message)
    else:
        message = "No new real state data"
    try:
        with smtplib.SMTP_SSL(gmail_server, gmail_port, context=context) as server:
            server.login(sender_mail, password)
            server.sendmail(sender_mail, receiver_mail, message)
            print("Mail sent from " + sender_mail + " to " + receiver_mail)
    except:
        print("Fail sending mail from " + sender_mail + " to " + receiver_mail)

count = 0
def check_realstates():
    global count
    while(True):
        #720
        if(count<720):
            time.sleep(60)
            # time.sleep(2)
            print(count)
            count+=1
        else:
            check_file = open("urls")
            checking_urls = check_file.read().strip().split("\n")
            print(checking_urls)
            scrape_data(checking_urls)
            count=0


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            pw = request.form.get("pw")
            if(not pw=="6589"):
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
            global count
            count = 720
            # count = 10
            return "Urls are submitted"
        return render_template('inputurl.html')
    except:
        return "Bad request"


if __name__ == "__main__":
    t = Thread(target=check_realstates)
    t.start()
    app.run(host='0.0.0.0',port=80)