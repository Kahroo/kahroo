""" Tradingview symbol info widget """
import pymysql.cursors
from app_cookie import get_sa_theme
from sa_func import get_broker_affiliate_link

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_tradingview_profile(suid):
    """ Get tradingview symbol info widget """
    return_data = ''
    symbol = ''
    url = get_broker_affiliate_link('Tradingview', 'baseurl')
    label_not_available = 'Indicators are not available for this instrument'
    theme = get_sa_theme()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(suid) +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        symbol = row[0]

    if symbol != '':
        return_data = '' +\
        '<div class="tradingview-widget-container">'+\
        '  <div class="tradingview-widget-container__widget"></div>'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>'+\
        '  {'+\
        '  "symbol": "'+ str(symbol) +'",'+\
        '  "width": "100%",'+\
        '  "height": "100%",'+\
        '  "colorTheme": "'+ str(theme) +'",'+\
        '  "isTransparent": true,'+\
        '  "locale": "en",'+\
        '  "largeChartUrl": "'+ str(url) +'"'+\
        '}'+\
        '  </script>'+\
        '</div>'
    else:
        return_data = label_not_available
    cursor.close()
    connection.close()
    return return_data
