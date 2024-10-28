from asyncio import AbstractEventLoop, get_running_loop

import pytest
import uvloop
from tortoise import connections
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db
from xync_schema import model
from xync_schema.model import Agent, ExAction, TestEx

from cex_clients.loader import DSN
from cex_clients.wallet.web import Private
from cex_clients.wallet.web_p2p import PrivateP2P


@pytest.mark.asyncio(loop_scope="class")
class TestWallet:
    loop: AbstractEventLoop

    @pytest.fixture(scope="class")
    def event_loop_policy(self):
        return uvloop.EventLoopPolicy()

    @pytest.fixture(scope="class", autouse=True)
    async def fx(self) -> PrivateP2P:
        TestWallet.loop = get_running_loop()
        await init_db(DSN, model)
        cn: AsyncpgDBClient = connections.get('default')
        agent = await Agent.get(user_id=1038938370)
        tg = PrivateP2P(agent)
        yield tg
        await tg.close()
        await cn.close()

    # 1 - all_curs
    async def test_all_curs(self, fx):
        curs = await fx.all_curs()
        await TestEx.update_or_create({"ok": bool(curs)}, ex__name="TgWallet", action=ExAction.all_curs_taker)
        assert curs, "No data"

    # 2 - all_coins
    async def test_all_coins(self, fx):
        coins = await fx.all_coins()
        await TestEx.update_or_create({"ok": bool(coins)}, ex__name="TgWallet", action=ExAction.all_coins)
        assert coins, "No data"

    # 3 - all_pms
    async def test_all_pms(self, fx):
        pms = await fx.all_pms()
        await TestEx.update_or_create({"ok": bool(pms)}, ex__name="TgWallet", action=ExAction.all_pms)
        assert pms, "No data"

    # 4 - all_ads
    async def test_cur_filter(self, fx):
        for cur in 'RUB', 'AZN', 'GEL':
            for coin in 'TON', 'USDT', 'BTC':
                for tt in 'SALE', 'PURCHASE':
                    ads = await fx.get_ads(coin, cur, tt)
                    assert len(ads), "No data"
        await TestEx.update_or_create({"ok": bool(ads)}, ex__name="TgWallet", action=ExAction.all_ads)

    # 5 - fiats
    async def test_fiats(self, fx):
        fiats = await fx.fiats()
        await TestEx.update_or_create({"ok": fiats['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.fiats)
        assert fiats['status'] == 'SUCCESS', "Failed to get fiats"

    # 6 - fiat_new
    async def test_fiat_new(self, fx):
        pms = await fx.all_pms()
        add_pm = await fx.fiat_new(pms[0]['code'], 'RUB', pms[0]['name'], '123456789098765')
        await TestEx.update_or_create({"ok": add_pm['status'] == 'SUCCESS'}, ex__name="TgWallet",
                                      action=ExAction.fiat_new)
        assert add_pm['status'] == 'SUCCESS', "Failed to create"

    # 7 - fiat_edit
    async def test_fiat_edit(self, fx):
        editid = await fx.fiats()
        pms = await fx.all_pms()
        add_pm = await fx.fiat_edit(editid['data'][0]['id'], pms[0]['code'], 'RUB', pms[0]['name'], '9876543214442')
        await TestEx.update_or_create({"ok": add_pm['status'] == 'SUCCESS'}, ex__name="TgWallet",
                                      action=ExAction.fiat_upd)
        assert add_pm['status'] == 'SUCCESS', "Failed to edit"

    # 8 - fiat_del
    async def test_fiat_del(self, fx):
        delid = await fx.fiats()
        dl = await fx.fiat_del(delid['data'][0]['id'])
        await TestEx.update_or_create({"ok": dl['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.fiat_del)
        assert dl['status'] == "SUCCESS", "Fiat doesn't delete"

    # 9 - my_ads
    async def test_my_ads(self, fx):
        ads = await fx.my_ads()
        await TestEx.update_or_create({"ok": ads['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.my_ads)
        assert ads['status'] == "SUCCESS", "No data"

    # 10 - ad_new
    async def test_ad_new(self, fx):
        fiats = [(await fx.fiats())['data'][0]['id']]
        ad = await fx.ad_new(fiats=fiats, amount=1000, coin="NOT", cur="EGP", tt="SALE")
        await TestEx.update_or_create({"ok": ad['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.ad_new)
        assert ad['status'] == "SUCCESS", "No data"

    # 11 - ad_upd
    async def test_ad_upd(self, fx):
        fiats = [(await fx.fiats())['data'][0]['id']]
        ad = (await fx.my_ads())['data'][0]
        upd = await fx.ad_upd(ad['type'], ad['id'], fiats, 1000)
        await TestEx.update_or_create({"ok": upd['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.ad_upd)
        assert upd['status'] == "SUCCESS", "No data"

    # 13, 14 - ad_on/ad_off
    async def test_ad_off_on(self, fx):
        ad = (await fx.my_ads())["data"][0]
        if ad['status'] == "ACTIVE":
            resulst_off = await fx.ad_off(ad['type'], ad['id'])
            assert resulst_off['status'] == "SUCCESS", "Inactivate failed"
        resulst_on = await fx.ad_on(ad['type'], ad['id'])
        assert resulst_on['status'] == "SUCCESS", "Activate failed"
        await TestEx.update_or_create({"ok": resulst_on['status'] == 'SUCCESS'}, ex__name="TgWallet",
                                      action=ExAction.ad_on)
        resulst_off = await fx.ad_off(ad['type'], ad['id'])
        await TestEx.update_or_create({"ok": resulst_off['status'] == 'SUCCESS'}, ex__name="TgWallet",
                                      action=ExAction.ad_off)
        assert resulst_off['status'] == "SUCCESS", "Inactivate failed"

    # 12 - ad_del
    async def test_ad_del(self, fx):
        ad = (await fx.my_ads())['data'][0]
        ad_del = await fx.ad_del(ad['type'], ad['id'])
        await TestEx.update_or_create({"ok": ad_del['status'] == 'SUCCESS'}, ex__name="TgWallet",
                                      action=ExAction.ad_del)
        assert ad_del['status'] == "SUCCESS", "No data"

    # 15 - order_approve
    async def test_order_approve(self, fx):
        orders = await fx.my_orders()
        agent = await Agent.get(user_id=2093307892)
        tgw = Private(agent)
        kyc = await tgw.get_kyc()
        if orders['data'][0]['seller']['userId'] == kyc:
            typ = 'SALE'
        elif orders['data'][0]['buyer']['userId'] == kyc:
            typ = 'BUY'
        else:
            typ = None
        approved = await fx.order_approve(orders['data'][0]['id'], typ)
        assert approved['status'] == "SUCCESS", "No approved"

    # 16 - order_reject
    async def test_order_reject(self, fx):
        orders = await fx.my_orders()
        assert len(orders['data']), "No orders. You need create at least one order at first!"
        order_reject = await fx.order_reject(orders['data'][0]['id'])
        await TestEx.update_or_create({"ok": order_reject['status'] == 'SUCCESS'}, ex__name="TgWallet",
                                      action=ExAction.order_reject)
        assert order_reject['status'] == "SUCCESS", "No data"

    # 19 - order_paid
    async def test_upload_file_order_paid(self, fx):
        orders = await fx.my_orders()
        agent = await Agent.get(user_id=1038938370)
        tgw = Private(agent)
        kyc = await tgw.get_kyc()
        if orders['data'][0]['seller']['userId'] == kyc:
            typ = 'SALE'
        elif orders['data'][0]['buyer']['userId'] == kyc:
            typ = 'BUY'
        else:
            typ = None
        order_id = await fx.order_approve(orders['data'][0]['id'], typ)
        upload = await fx.upload_file(order_id, 'Screenshot_788.png')
        assert upload['status'] == "SUCCESS", "No upload"
        paid = await fx.order_paid(orders['data'][0]['id'], upload['data']['file'])
        assert paid['status'] == "SUCCESS", "No data"

    # 20 - order_payment_confirm
    async def test_order_payment_confirm(self, fx):
        orders = await fx.my_orders()
        confirm = await fx.order_payment_confirm(orders['data'][0]['id'])
        assert confirm['status'] == "SUCCESS", "No confirm"
