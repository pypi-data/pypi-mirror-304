import json
from json import dumps

from erp_apis.apis.afterSales import AftersaleRequest

from xiaobu.xiaobu_erp import ErpRequest


class WaveCheckErpRequest(ErpRequest):
    def __init__(self, data: dict, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.url = '/app/wms/outcheck/WaveCheckout_Checkout.aspx'
        self.data.update(data)
        self.method = 'POST'
        self.callback = callback


# 出库校验
def check_out(lid: str):
    """
    出库
    """
    return WaveCheckErpRequest(data={
        'l_id_checkout': lid,
        'wave_id_checkout': '',
        'sku_id_checkout': '',
        'dewu_box_no': '',
        'scaned_order_code': '',
        'ExpressNum': '',
        'isAppendSub': 'true',
        'isAddRemark': 'true',
        'lc_id': '',
        'print': '',
        'keep_last_checkinfo': '',
        '__CALLBACKID': 'ACall1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "LoadOrderByLidData",
                "Args": [
                    dumps({"Lid": lid,
                           "LcId": "",
                           "ShowDisplayPicker": False,
                           "IsCheckOnlyLid": True})
                ],
                "CallControl": "{page}"
            }
        ),
    },
        callback=lambda res: check_out_callback(res)
    )


# 响应体回调
def check_out_callback(res):
    resp_text = res.text
    resp_data = json.loads(resp_text[resp_text.find('{'):])

    if not resp_data.get('IsSuccess'):
        return False, resp_data.get('ExceptionMessage')
    if resp_data['ReturnValue']:
        return_value = json.loads(resp_data['ReturnValue'])
        return True, return_value.get('Data').get('lc_name')
    return False, None
