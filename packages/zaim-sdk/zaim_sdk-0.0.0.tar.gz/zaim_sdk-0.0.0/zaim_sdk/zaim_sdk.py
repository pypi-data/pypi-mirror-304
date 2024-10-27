from requests_oauthlib import OAuth1Session


class ZaimSDK:
    VERIFY_URL = "https://api.zaim.net/v2/home/user/verify"
    MONEY_URL = "https://api.zaim.net/v2/home/money"
    PAYMENT_URL = "https://api.zaim.net/v2/home/money/payment"
    INCOME_URL = "https://api.zaim.net/v2/home/money/income"
    TRANSFER_URL = "https://api.zaim.net/v2/home/money/transfer"
    CATEGORY_URL = "https://api.zaim.net/v2/home/category"
    GENRE_URL = "https://api.zaim.net/v2/home/genre"
    ACCOUNT_URL = "https://api.zaim.net/v2/home/account"
    CURRENCY_URL = "https://api.zaim.net/v2/currency"

    def __init__(
        self,
        consumer_id,
        consumer_secret,
        access_token,
        access_token_secret,
    ):
        self.consumer_id = consumer_id
        self.consumer_secret = consumer_secret

        self.auth = OAuth1Session(
            client_key=self.consumer_id,
            client_secret=self.consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )
        self._verify()
        self._build_id_table()

    def get_data(self, params=None):
        return self.auth.get(self.MONEY_URL, params=params).json()["money"]

    def insert_payment_simple(
        self,
        date,
        amount,
        genre,
        from_account=None,
        comment=None,
        name=None,
        place=None,
        receipt_id=None,
    ):
        genre_id = self.genre_stoi[genre]
        category_id = self.genre_to_category[genre_id]
        if from_account is not None:
            from_account_id = self.account_stoi[from_account]
        else:
            from_account_id = None
        return self.insert_payment(
            date, amount, category_id, genre_id, from_account_id, comment, name, place, receipt_id
        )

    def insert_payment(
        self,
        date,
        amount,
        category_id,
        genre_id,
        from_account_id=None,
        comment=None,
        name=None,
        place=None,
        receipt_id=None,
    ):
        data = {
            "mapping": 1,
            "category_id": category_id,
            "genre_id": genre_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if from_account_id is not None:
            data["from_account_id"] = from_account_id
        if comment is not None:
            data["comment"] = comment
        if name is not None:
            data["name"] = name
        if place is not None:
            data["place"] = place
        if receipt_id is not None:
            data["receipt_id"] = receipt_id
        return self.auth.post(self.PAYMENT_URL, data=data)

    def update_payment_simple(
        self,
        data_id,
        date,
        genre,
        amount,
        from_account=None,
        comment=None,
        name=None,
        place=None,
        receipt_id=None,
    ):
        genre_id = self.genre_stoi[genre]
        category_id = self.genre_to_category[genre_id]
        if from_account is not None:
            from_account_id = self.account_stoi[from_account]
        else:
            from_account_id = None
        return self.update_payment(
            data_id,
            date,
            amount,
            category_id,
            genre_id,
            from_account_id,
            comment,
            name,
            place,
            receipt_id,
        )

    def update_payment(
        self,
        data_id,
        date,
        amount,
        category_id,
        genre_id,
        from_account_id=None,
        comment=None,
        name=None,
        place=None,
        receipt_id=None,
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "category_id": category_id,
            "genre_id": genre_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if from_account_id is not None:
            data["from_account_id"] = from_account_id
        if comment is not None:
            data["comment"] = comment
        if name is not None:
            data["name"] = name
        if place is not None:
            data["place"] = place
        if receipt_id is not None:
            data["receipt_id"] = receipt_id
        return self.auth.put("{}/{}".format(self.PAYMENT_URL, data_id), data=data)

    def delete_payment(self, data_id):
        return self.auth.delete("{}/{}".format(self.PAYMENT_URL, data_id))

    def insert_income_simple(self, date, category, amount, to_account=None, comment=None, place=None):
        category_id = self.category_stoi[category]
        if to_account is not None:
            to_account_id = self.account_stoi[to_account]
        else:
            to_account_id = None
        return self.insert_income(date, category_id, amount, to_account_id, comment, place)

    def insert_income(self, date, category_id, amount, to_account_id=None, comment=None, place=None):
        data = {
            "mapping": 1,
            "category_id": category_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if to_account_id is not None:
            data["to_account_id"] = to_account_id
        if comment is not None:
            data["comment"] = comment
        if place is not None:
            data["place"] = place
        return self.auth.post(self.INCOME_URL, data=data)

    def update_income_simple(self, data_id, date, category, amount, to_account=None, comment=None, place=None):
        category_id = self.category_stoi[category]
        if to_account is not None:
            to_account_id = self.account_stoi[to_account]
        else:
            to_account_id = None
        return self.update_income(data_id, date, category_id, amount, to_account_id, comment, place)

    def update_income(
        self,
        data_id,
        date,
        category_id,
        amount,
        to_account_id=None,
        comment=None,
        place=None,
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "category_id": category_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if to_account_id is not None:
            data["to_account_id"] = to_account_id
        if comment is not None:
            data["comment"] = comment
        if place is not None:
            data["place"] = place
        return self.auth.put("{}/{}".format(self.INCOME_URL, data_id), data=data)

    def delete_income(self, data_id):
        return self.auth.delete("{}/{}".format(self.INCOME_URL, data_id))

    def insert_transfer_simple(self, date, amount, from_account, to_account, comment=None):
        from_account_id = self.account_stoi[from_account]
        to_account_id = self.account_stoi[to_account]
        return self.insert_transfer(date, amount, from_account_id, to_account_id, comment)

    def insert_transfer(self, date, amount, from_account_id, to_account_id, comment=None):
        data = {
            "mapping": 1,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
        }
        if comment is not None:
            data["comment"] = comment
        return self.auth.post(self.TRANSFER_URL, data=data)

    def update_transfer_simple(self, data_id, date, amount, from_account, to_account, comment=None):
        from_account_id = self.account_stoi[from_account]
        to_account_id = self.account_stoi[to_account]
        return self.update_transfer(data_id, date, amount, from_account_id, to_account_id, comment)

    def update_transfer(self, data_id, date, amount, from_account_id, to_account_id, comment=None):
        data = {
            "mapping": 1,
            "id": data_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
        }
        if comment is not None:
            data["comment"] = comment
        return self.auth.put("{}/{}".format(self.TRANSFER_URL, data_id), data=data)

    def delete_transfer(self, data_id):
        return self.auth.delete("{}/{}".format(self.TRANSFER_URL, data_id))

    def _build_id_table(self):
        self.genre_itos = {}
        self.genre_stoi = {}
        self.genre_to_category = {}
        genre = self._get_genre()["genres"]
        for g in genre:
            self.genre_itos[g["id"]] = g["name"]
            self.genre_stoi[g["name"]] = g["id"]
            self.genre_to_category[g["id"]] = g["category_id"]
        self.category_itos = {}
        self.category_stoi = {}
        category = self._get_category()["categories"]
        for c in category:
            self.category_itos[c["id"]] = c["name"]
            self.category_stoi[c["name"]] = c["id"]
        self.account_stoi = {}
        self.account_itos = {}
        account = self._get_account()["accounts"]
        for a in account:
            self.account_itos[a["id"]] = a["name"]
            self.account_stoi[a["name"]] = a["id"]

    def _get_account(self):
        return self.auth.get(self.ACCOUNT_URL).json()

    def _get_category(self):
        return self.auth.get(self.CATEGORY_URL).json()

    def _get_genre(self):
        return self.auth.get(self.GENRE_URL).json()

    def _verify(self):
        res = self.auth.get(self.VERIFY_URL)
        if res.status_code != 200:
            raise Exception("認証エラー: キーを確認してください")
