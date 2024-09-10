import os
#kis_api module 을 찾을 수 없다는 에러가 나는 경우 sys.path에 kis_api.py 가 있는 폴더를 추가해준다.
import sys
from datetime import datetime, timedelta

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'kis_api')))
from rest_framework import viewsets, status
from rest_framework.response import Response

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(os.path.join(project_root, 'gtp_backend', 'kis_trading', 'controller'))

from kis_trading.controller import kis_api as ka
import pandas as pd



class TradingView(viewsets.ViewSet):

    def order_stock(self, request):
        ka.auth()
        stock_code = request.data.get('stock_code')
        qty = request.data.get('qty')
        price = request.data.get('price')
        order_type = request.data.get('order_type')

        if order_type == 'buy':
            response = ka.do_buy(stock_code, qty, price)
        elif order_type == 'sell':
            response = ka.do_sell(stock_code, qty, price)

        msg = response.getBody().msg1 if response else 'No message available'

        return Response({'status': 'success', 'msg': msg}, status=status.HTTP_200_OK)




    def get_my_complete(self, request):
        ka.auth()
        sdt = datetime.now().strftime('%Y%m%d')
        df_complete = ka.get_my_complete(sdt, sdt)
        print('sdfsdfsdf', df_complete.to_dict(orient='records'))
        return Response(df_complete.to_dict(orient='records'), status=status.HTTP_200_OK)



