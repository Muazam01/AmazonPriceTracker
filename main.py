from bs4 import BeautifulSoup
import requests
from smtplib import SMTP
import json

with open("details.json", "r") as fd:
    details =json.load(fd)

################################################################################################################

my_email=details["email"]
my_password=details["mypassword"]

RECIPIENT_EMAIL="RECIPIENT's EMAIL"

################################################################################################################

headers={
    "User-Agent":"Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language":"en-GB,en;q=0.6",
    "Connection":"keep-alive",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Request Line":"GET / HTTP/1.1",
}

with open("my_dict.json", "r") as f:
    my_dict =json.load(f)



def function1(URL,ask):

    try:
        response = requests.get(url=URL, headers=headers)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    soup = BeautifulSoup(response.text, "html.parser")
    price_ = soup.find(name="span", class_="a-offscreen").get_text()
    split = price_.split('₹')[1]
    price = int(float(split.replace(',', '')))

    if price < ask:
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email, to_addrs=RECIPIENT_EMAIL,
                                msg=f"Subject:Price Alert\n\n The price is below the {ask} price..Buy now")


for key in my_dict:
    URL=my_dict[key]["URL"]
    ask=int(my_dict[key]["target"])
    function1(URL,ask)

