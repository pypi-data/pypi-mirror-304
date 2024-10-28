from enum import IntEnum, StrEnum
from typing import Literal

from cex_clients.wallet.web import Private


class Exceptions(StrEnum):
    PM_KYC = 'OFFER_FIAT_COUNTRY_NOT_SUPPORTED_BY_USER_KYC_COUNTRY'


class PrivateP2P(Private):
    base_url = 'https://p2p.walletbot.me'
    middle_url = '/p2p/'

    # 1: all_curs
    async def all_curs(self):
        coins_curs = await self.post('public-api/v2/currency/all-supported')
        curs = [c['code'] for c in coins_curs['data']['fiat']]
        return curs

    # 2: all_coins
    async def all_coins(self):
        coins_curs = await self.post('public-api/v2/currency/all-supported')
        coins = [c['code'] for c in coins_curs['data']['crypto']]
        return coins

    # 3: all_coins
    async def all_pms(self):
        pms = await self.post('public-api/v3/payment-details/get-methods/by-currency-code', {"currencyCode": "RUB"})
        return pms['data']

    # 4: all_ads
    async def get_ads(self, coin: str = "TON", cur: str = "RUB", tt: str = "SALE", offset: int = 0, limit: int = 100) -> dict:
        params = {"baseCurrencyCode": coin, "quoteCurrencyCode": cur, "offerType": tt, "offset": offset, "limit": limit}  # ,"merchantVerified":"TRUSTED"
        ads = await self.post('public-api/v2/offer/depth-of-market/', params)
        return ads

    # 5: fiats
    async def fiats(self):
        pms = await self.post('public-api/v3/payment-details/get/by-user-id')
        return pms

    # 6: fiat_new
    async def fiat_new(self, code_pms: str, cur: str, name_pms: str, number: str):
        add_fiat = await self.post('public-api/v3/payment-details/create', {
            "paymentMethodCode": code_pms,
            "currencyCode": cur,
            "name": name_pms,
            "attributes": {
                "version": "V1",
                "values": [
                    {
                        "name": "PAYMENT_DETAILS_NUMBER",
                        "value": number
                    }
                ]
            }
        })
        return add_fiat

    # 7 - fiat_edit
    async def fiat_edit(self, fiat_id: int, code_pms: str, cur: str, name_pms: str, number: str):
        edit_fiat = await self.post('public-api/v3/payment-details/edit', {
            "id": fiat_id,
            "paymentMethodCode": code_pms,
            "currencyCode": cur,
            "name": name_pms,
            "attributes": {
                "version": "V1",
                "values": [
                    {
                        "name": "PAYMENT_DETAILS_NUMBER",
                        "value": number
                    }
                ]
            }
        })
        return edit_fiat

    # 8 - fiat_del
    async def fiat_del(self, fiat_id: int):
        del_fiat = await self.post('public-api/v3/payment-details/delete', {"id": fiat_id})
        return del_fiat

    # 9 - my_ads
    async def my_ads(self, status: Literal["INACTIVE", "ACTIVE"] = None):
        ads = await self.post('public-api/v2/offer/user-own/list', {"offset": 0, "limit": 20, "offerType": "SALE"})
        return [ad for ad in ads['data'] if ad['status'] == status] if status else ads

    async def my_orders(self):
        orders = await self.post('public-api/v2/offer/order/history/get-by-user-id', {"offset": 0, "limit": 20, "filter": {"status": "ALL_ACTIVE"}})
        return orders

    # 10 - ad_new
    async def ad_new(self, fiats: list[int], amount: int, coin: str = "TON", cur: str = "RUB", tt: str = "SALE"):
        create = await self.post('public-api/v2/offer/create', {
            "type": tt,
            "initVolume": {
                "currencyCode": coin,
                "amount": f"{amount}"
            },
            "orderRoundingRequired": False,
            "price": {
                "type": "FLOATING",
                "baseCurrencyCode": coin,
                "quoteCurrencyCode": cur,
                "value": "120"
            },
            "orderAmountLimits": {
                "min": "500",
                "max": "2000"
            },
            "paymentConfirmTimeout": "PT15M",
            "comment": "",
            "paymentDetailsIds": fiats
        })
        return create

    # 11 - ad_upd
    async def ad_upd(self, typ: str, offer_id: int, fiats: list[int], amount: int):
        upd = await self.post('public-api/v2/offer/edit', {
            "offerId": offer_id,
            "paymentConfirmTimeout": "PT15M",
            "type": typ,
            "orderRoundingRequired": False,
            "price": {
                "type": "FLOATING",
                "value": "120"
            },
            "orderAmountLimits": {
                "min": "500",
                "max": "2000"
            },
            "comment": "",
            "volume": f"{amount}",
            "paymentDetailsIds": fiats
        })
        return upd

    # 12 - ad_del
    async def ad_del(self, typ: str, offer_id: int):
        ad_del = await self.post('public-api/v2/offer/delete', {"type": typ, "offerId": offer_id})
        return ad_del

    # 13 - ad_on
    async def ad_on(self, typ: str, offer_id: int):
        active = await self.post('public-api/v2/offer/activate', {"type": typ, "offerId": offer_id})
        return active

    # 14 - ad_off
    async def ad_off(self, typ: str, offer_id: int) -> dict[str, str]:
        off = await self.post('public-api/v2/offer/deactivate', {"type": typ, "offerId": offer_id})
        return off

    # 15 - order_approve
    async def order_approve(self, order_id: int, typ: str):
        approve = await self.post('public-api/v2/offer/order/accept', {'orderId': order_id, 'type': typ})
        return approve

    # 16 - order_reject
    async def order_reject(self, order_id: str):
        reject = await self.post('public-api/v2/offer/order/cancel/by-seller', {'orderId': order_id})
        return reject

    async def upload_file(self, order_id: int, path_to_file: str):
        url = f'public-api/v2/file-storage/file/upload?orderId={order_id}&uploadType=UPLOAD_BUYER_PAYMENT_RECEIPT'
        data = {'file': open(path_to_file, 'rb')}
        upload_file = await self.post(url, data)
        return upload_file

    # 19 - order_paid
    async def order_paid(self, order_id: str, file: dict):
        paid = await self.post('public-api/v2/offer/order/confirm-sending-payment', {
            'orderId': order_id,
            'paymentReceipt': file
        })
        return paid

    # 20 - order_payment_confirm
    async def order_payment_confirm(self, order_id: str):
        payment_confirm = await self.post('public-api/v2/payment-details/confirm', {'orderId': order_id})
        return payment_confirm
