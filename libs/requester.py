import requests
import json


class RequesterLib:

    def __init__(self):
        self.url = "https://1c22eh3aj8.execute-api.us-east-1.amazonaws.com/challenge/quotes"
        self.len_of_quotes = 0

    def get_quotes(self):
        get_quotes = requests.get(url=self.url)
        if get_quotes.status_code == 200:
            json_data = json.loads(get_quotes.text)
            self.len_of_quotes = len(json_data["quotes"])
            self.len_of_quotes = self.len_of_quotes - 1
            print(json_data)
            return json_data
        return {"error": get_quotes.status_code}

    def get_quote(self, quote_number):
        if not isinstance(quote_number, int):
            print("number format error")
            return {"error": "input must be integer"}

        url_num = self.url + "/{}".format(quote_number)
        get_quote_number = requests.get(url=url_num)

        if quote_number > self.len_of_quotes:
            print("index error")
            return {"error": "index out of range, {}".format(self.len_of_quotes)}
        if get_quote_number.status_code == 200:
            json_data = json.loads(get_quote_number.text)
            print(json_data)
            return json_data
        print(get_quote_number.status_code)
        return {"error": get_quote_number.status_code}


classObj = RequesterLib()
classObj.get_quotes()
classObj.get_quote(31)