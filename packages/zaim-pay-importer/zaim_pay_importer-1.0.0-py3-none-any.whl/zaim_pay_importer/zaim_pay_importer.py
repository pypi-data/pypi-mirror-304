from dataclasses import dataclass
from datetime import datetime

from PayGmailScraper import PayGmailScraper, PaymentInformation
from zaim_sdk import ZaimSDK


@dataclass
class PaymentInformationsList:
    """支払い情報リスト"""

    ana_pay: list[PaymentInformation]
    rakuten_pay: list[PaymentInformation]
    others: list[PaymentInformation]


class ZaimPayImporter:
    def __init__(
        self,
        consumer_id: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
        exclude_set: set[str],
        app_type: str = "desktop",
        credentials_path: str | None = None,
        token_path: str = "token.json",
    ):
        if credentials_path is None and app_type == "desktop":
            raise ValueError("credentials_path is required when app_type is desktop")
        self.zaim_sdk = ZaimSDK(consumer_id, consumer_secret, access_token, access_token_secret)
        self.pay_gmail_scraper = PayGmailScraper(app_type, credentials_path, token_path)
        self.zaim_payments_list = self._get_zaim_payment_list()
        self.exclude_set = exclude_set

    def _diff_payment(
        self, gmail_payments: list[PaymentInformation], zaim_payments: list[PaymentInformation]
    ) -> list[PaymentInformation]:
        # gmail_paymentsにあってzaim_paymentsにないものを返す
        payment_info_zaim_set = {(p.payment_date.strftime("%Y-%m-%d"), p.price, p.store) for p in zaim_payments}
        new_payment_info = []
        for p in gmail_payments:
            if (p.payment_date.strftime("%Y-%m-%d"), p.price, p.store) not in payment_info_zaim_set:
                new_payment_info.append(p)
        return new_payment_info

    def _get_zaim_payment_list(self) -> PaymentInformationsList:
        page = 1
        ana_pay_list = []
        rakuten_pay_list = []
        others_list = []
        while True:
            params = {"page": page, "limit": 100}
            response = self.zaim_sdk.get_data(params=params)
            if not response:
                break
            for r in response:
                payment_info = PaymentInformation(
                    payment_date=datetime.strptime(r.get("date"), "%Y-%m-%d"),
                    price=r.get("amount"),
                    store=r.get("place"),
                    payment_method=r.get("comment"),
                )
                if r.get("comment") == "ANA Pay":
                    ana_pay_list.append(payment_info)
                elif r.get("comment") == "楽天ペイ":
                    rakuten_pay_list.append(payment_info)
                else:
                    others_list.append(payment_info)
            page += 1
        return PaymentInformationsList(ana_pay=ana_pay_list, rakuten_pay=rakuten_pay_list, others=others_list)

    def _add_payments_to_zaim(self, new_payments: list[PaymentInformation]):
        for p in new_payments:
            print(p.values())
            self.zaim_sdk.insert_payment_simple(
                date=p.payment_date,
                amount=p.price,
                genre="Uncategorized",
                place=p.store,
                comment=p.payment_method,
            )

    # 除外する支払い情報を省く
    def _exclude_payment(self, payments: list[PaymentInformation], exclude_set: set[str]) -> list[PaymentInformation]:
        new_payments = []
        for p in payments:
            if p.store and not any([word in p.store.lower() for word in exclude_set]):
                new_payments.append(p)
        return new_payments

    def import_ana_pay(self):
        gmail_payments = self.pay_gmail_scraper.get_payments_ana_pay()
        new_payments = self._diff_payment(gmail_payments, self.zaim_payments_list.ana_pay)
        new_payments = self._exclude_payment(new_payments, self.exclude_set)
        self._add_payments_to_zaim(new_payments)
        print("ANA Pay import finished")

    def import_rakuten_pay(self):
        gmail_payments = self.pay_gmail_scraper.get_payments_rakuten_pay()
        new_payments = self._diff_payment(gmail_payments, self.zaim_payments_list.rakuten_pay)
        new_payments = self._exclude_payment(new_payments, self.exclude_set)
        self._add_payments_to_zaim(new_payments)
        print("Rakuten Pay import finished")
