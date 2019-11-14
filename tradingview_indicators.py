""" Tradingview Indicators """
from app_cookie import theme_return_this, get_sa_theme
from sa_func import get_broker_affiliate_link
import pymysql.cursors

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_tradingview_indicators(suid,width,height):
    """ Get Tradingview Indicators """
    return_data = ''
    url = get_broker_affiliate_link('Tradingview','baseurl')
    symbol = ''
    label_not_available = 'Indicators are not available for this instrument'
    theme = get_sa_theme()
    
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT tradingview_ta FROM symbol_list WHERE uid ='"+ str(suid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: symbol = row[0]

    if symbol != '':
        return_data = '' +\
        '<div class="tradingview-widget-container">'+\
        '  <div class="tradingview-widget-container__widget"></div>'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>'+\
        '  {'+\
        '  "showIntervalTabs": true,'+\
        '  "width": "'+ width +'",'+\
        '  "colorTheme": "'+ theme +'",'+\
        '  "isTransparent": true,'+\
        '  "locale": "en",'+\
        '  "symbol": "'+ symbol +'",'+\
        '  "interval": "1h",'+\
        '  "height": "'+ height +'",'+\
        '  "largeChartUrl": "'+ url +'"'+\
        '}'+\
        '  </script>'+\
        '</div>'
    else:
        return_data = label_not_available

    cr.close()
    connection.close()
    return return_data
