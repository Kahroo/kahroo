""" Trades tab functionalities """
import pymysql.cursors
from sa_func import get_random_str
import datetime
import time
from datetime import timedelta

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_trades_tbl(uid,w,burl,type):
    """ xxx """
    return_data = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)

    selected_symbol = ''
    selected_is_portf = False
    is_user_prf = False
    list_limit = 50
    sql = "SELECT symbol FROM symbol_list WHERE uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: selected_symbol = row[0]
    if not selected_symbol.find( get_portf_suffix() ) == -1: selected_is_portf = True
    if uid == '0' or uid == 0: is_user_prf = True

    user_symbol_selection = ''
    i = 0

    portf_symbol_selection = ''
    i = 0
    if selected_is_portf:
        sql = "SELECT portfolios.symbol, portfolios.portf_symbol FROM symbol_list JOIN portfolios ON symbol_list.symbol = portfolios.portf_symbol WHERE symbol_list.uid = "+ str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        portf_symbol = ''
        for row in rs:
            portf_symbol = row[1]
            if i == 0: portf_symbol_selection = portf_symbol_selection + " AND (trades.symbol = '"+ str(row[0]) +"' "
            else: portf_symbol_selection = portf_symbol_selection + " OR trades.symbol = '"+ str(row[0]) +"' "
            i += 1
        portf_symbol_selection = portf_symbol_selection + ') AND portfolios.portf_symbol ="'+ str(portf_symbol) +'" '

    single_selection = ''
    if not selected_is_portf and not is_user_prf: single_selection = 'AND trades.uid = ' + str(uid)

    dn = datetime.datetime.now(); dnstr = dn.strftime("%Y%m%d"); dn = dn.strftime("%d-%b-%Y")

    if selected_is_portf:
        sql = "SELECT trades.order_type, "+\
            "trades.fullname, "+\
            "trades.entry_date,  "+\
            "trades.entry_price, "+\
            "trades.close_price, "+\
            "trades.expiration_date, "+\
            "trades.pnl_pct,  "+\
            "trades.url,  "+\
            "instruments.unit, "+\
            "portfolios.strategy_order_type, "+\
            "trades.uid "
        sql = sql + "FROM trades JOIN portfolios ON portfolios.symbol = trades.symbol JOIN instruments ON trades.symbol = instruments.symbol WHERE trades.entry_date <=" + dnstr + " AND "
    elif is_user_prf and w != 'today':
        sql = "SELECT trades.order_type, "+\
            "trades.fullname, "+\
            "trades.entry_date, "+\
            "trades.entry_price, "+\
            "trades.close_price, "+\
            "trades.expiration_date, "+\
            "trades.pnl_pct, "+\
            "trades.url, "+\
            "a_alloc.unit, "+\
            "trades.status, "+\
            "trades.uid "+\
            "FROM instruments "+\
            "JOIN portfolios ON instruments.symbol = portfolios.portf_symbol "+\
            "JOIN trades ON trades.symbol = portfolios.symbol "+\
            "JOIN instruments as a_alloc ON a_alloc.symbol =  trades.symbol " +\
            "WHERE instruments.owner = " + str(get_user_numeric_id()) + " "+\
            "AND ((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
            "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
            "OR (portfolios.strategy_order_type = 'long/short') ) AND trades.entry_date <=" + dnstr + " AND "
    elif w == 'today':
        type_status_filter = "" +\
        "((trades.entry_date = " + dnstr + " AND instruments.owner = " + str(get_user_numeric_id()) + " AND status = 'active') OR "+\
        "(trades.expiration_date <= " + dnstr + " AND instruments.owner = "+ str(get_user_numeric_id()) +" AND status = 'active') OR "+\
        "(trades.expiration_date = " + dnstr + " AND instruments.owner = "+ str(get_user_numeric_id()) +" AND status = 'expired')) "

        if type =='expired':
            type_status_filter = "((trades.expiration_date = " + dnstr + " AND instruments.owner = "+ str(get_user_numeric_id()) +")) "

        sql ="SELECT "+\
            "trades.order_type, "+\
            "trades.fullname, "+\
            "trades.entry_date, "+\
            "trades.entry_price, "+\
            "trades.close_price, "+\
            "trades.expiration_date, "+\
            "trades.pnl_pct, "+\
            "trades.url, "+\
            "a_alloc.unit, "+\
            "trades.status, "+\
            "trades.uid "+\
            "FROM trades "+\
            "JOIN portfolios ON portfolios.symbol = trades.symbol "+\
            "JOIN instruments ON instruments.symbol = portfolios.portf_symbol "+\
            "JOIN instruments as a_alloc ON a_alloc.symbol = portfolios.symbol "+\
            "WHERE "+\
            "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
            "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
            "OR (portfolios.strategy_order_type = 'long/short') ) AND "+\
            type_status_filter
    else:
        sql = "SELECT trades.order_type, "+\
            "trades.fullname, "+\
            "trades.entry_date,  "+\
            "trades.entry_price, "+\
            "trades.close_price, "+\
            "trades.expiration_date, "+\
            "trades.pnl_pct,  "+\
            "trades.url,  "+\
            "instruments.unit, "+\
            "trades.status, "+\
            "trades.uid "
        sql = sql + "FROM trades JOIN instruments ON trades.symbol = instruments.symbol WHERE trades.entry_date <=" + dnstr + " AND "

    if w == 'active': sql = sql + " trades.status = 'active' "
    if w == 'expired': sql = sql + " trades.status = 'expired' "

    sql = sql + single_selection
    sql = sql + portf_symbol_selection
    sql = sql + ' order by trades.entry_date DESC'
    cr.execute(sql)
    rs = cr.fetchall()

    l_order = 'Order'
    l_instrument = 'Instrument'
    l_entry_date = 'Entry date'
    l_open_price = 'Open price'
    l_close_price = 'Close price'
    l_expiration_date = 'Expiration date'
    l_pnl = 'PnL'

    return_data = ''+\
    '<table class="table table-hover table-sm sa-table-sm">'+\
    '  <thead>'+\
    '    <tr>'+\
    '      <th scope="col">'+ l_order +'</th>'+\
    '      <th scope="col">'+ l_instrument +'</th>'+\
    '      <th scope="col">'+ l_entry_date +'</th>'+\
    '      <th scope="col">'+ l_open_price +'</th>'
    if w == 'expired': return_data = return_data + '<th scope="col">'+ l_close_price +'</th>'
    return_data = return_data +\
    '      <th scope="col">'+ l_expiration_date +'</th>'+\
    '      <th scope="col">'+ l_pnl +'</th>'+\
    '    </tr>'+\
    '  </thead>'+\
    '  <tbody>'
    i = 0
    for row in rs:
        order_type = row[0]
        fullname = row[1]
        entry_date = row[2].strftime("%d-%b-%Y")
        entry_price = row[3]
        close_price = row[4]
        expiration_date = row[5].strftime("%d-%b-%Y")
        expiration_date_str = str(row[5].strftime("%Y%m%d"))
        pnl_pct = row[6]
        url = row[7]
        unit = row[8]
        alloc_uid = row[10]
        if selected_is_portf: strategy_order_type = row[9]

        if dn == entry_date: badge_today = '&nbsp;&nbsp;<span class="badge badge-primary">open today</span>'
        elif int(dnstr) >= int(expiration_date_str) and (w == 'active' or w == 'today') and (close_price == -1): badge_today = '&nbsp;&nbsp;<span class="badge badge-secondary">close @marketOpen</span>'
        elif int(dnstr) == int(expiration_date_str) and (w == 'expired' or w == 'today'): badge_today = '&nbsp;&nbsp;<span class="badge badge-warning">closed today</span>'
        else: badge_today = ''
        if order_type == 'buy': badge_class = 'badge badge-success'
        else: badge_class = 'badge badge-danger'
        if pnl_pct >= 0: text_class = 'text text-success'
        else: text_class = 'text text-danger'
        if unit == 'pips':
            pnl_pct = round( pnl_pct *10000, 2)
            if pnl_pct > 1: pnl_pct = str( pnl_pct ) + " pips"
            else: pnl_pct = str( pnl_pct ) + " pips"
        else: pnl_pct = str( round( pnl_pct * 100, 2 ) ) + "%"

        if selected_is_portf:
            if (order_type == 'buy' and strategy_order_type == 'long') or (order_type == 'sell' and strategy_order_type == 'short') or (strategy_order_type == 'long/short'):
                return_data = return_data +\
                '    <tr>'+\
                '      <td><span class="'+ badge_class +'">'+ str(order_type) +'</span>'+ badge_today +'</td>'+\
                '      <td><a href="'+ burl + 's/?uid='+ str(alloc_uid) +'">'+ str(fullname) +'</a></td>'+\
                '      <td>'+ str(entry_date) +'</td>'+\
                '      <td>'+ str(entry_price) +'</td>'
                if w == 'expired': return_data = return_data + '<td>'+ str(close_price) +'</td>'
                return_data = return_data +\
                '      <td>'+ str(expiration_date) +'</td>'+\
                '      <td><span class="'+ text_class +'">'+ str(pnl_pct) +'</span></td>'+\
                '    </tr>'
                i += 1
        else:
            return_data = return_data +\
            '    <tr>'+\
            '      <td><span class="'+ badge_class +'">'+ str(order_type) +'</span>'+ badge_today +'</td>'+\
            '      <td><a href="'+ burl + 's/?uid='+ str(alloc_uid) +'">'+ str(fullname) +'</a></td>'+\
            '      <td>'+ str(entry_date) +'</td>'+\
            '      <td>'+ str(entry_price) +'</td>'
            if w == 'expired': return_data = return_data + '<td>'+ str(close_price) +'</td>'
            return_data = return_data +\
            '      <td>'+ str(expiration_date) +'</td>'+\
            '      <td><span class="'+ text_class +'">'+ str(pnl_pct) +'</span></td>'+\
            '    </tr>'
            i += 1
        if i == list_limit: break

    return_data = return_data +\
    '  </tbody>'+\
    '</table>'
    cr.close()
    connection.close()
    return return_data




def get_trades_box(uid,burl,is_dashboard):
    """ xxx """
    box_content = ''
    if not uid == 0 or len(get_user()) > 1:
        l_tab_today_title = 'Today`s order execution'; tab_today_id = 'today_orders'
        l_tab_active_title = 'Active trade(s)'; tab_active_id = 'active_trades'
        l_tab_expired_title = 'Closed trade(s)'; tab_expired_id = 'expired_trades'
        l_box_user_profile_title = ''
        if uid == 0 : l_box_user_profile_title = '<i class="fas fa-piggy-bank"></i>&nbsp;Your tradebook'

        div_placement = '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'
        tab_style_overflow = ''
        tab_active_trade = 'active'
        tab_today_orders = ''
        tab_today_orders_content = ''
        if is_dashboard == str(1):
            div_placement = '<div class="col-lg-6 col-md-12 col-sm-12 col-xs-12">'
            tab_style_overflow ='overflow-y: scroll; max-height: 600px; min-height: 600px;'
            tab_active_trade = ''
            tab_today_orders = '<li class="nav-item"><a class="nav-link active" data-toggle="pill" href="#'+ tab_today_id +'">'+ l_tab_today_title +'</a></li>'
            tab_today_orders_content = '<div id="'+ tab_today_id +'" class="tab-pane active" style="'+ tab_style_overflow +'"><div>&nbsp;</div>'+ get_trades_tbl(uid,'today',burl,'') +'</div>'

        box_content = '' +\
        div_placement +\
        '<div class="box-part rounded">' +\
        '               <span class="sectiont">'+ l_box_user_profile_title +'</span>'+\
        '               <ul id="sa-tab-sm" class="nav nav-tabs" role="tablist">'+\
        tab_today_orders +\
        '                   <li class="nav-item">'+\
        '                       <a class="nav-link '+ tab_active_trade +'" data-toggle="pill" href="#'+ tab_active_id +'">'+ l_tab_active_title +'</a>'+\
        '                   </li>'+\
        '                   <li class="nav-item">'+\
        '                       <a class="nav-link" data-toggle="pill" href="#'+ tab_expired_id +'">'+ l_tab_expired_title +'</a>'+\
        '                   </li>'+\
        '               </ul>'+\
        '               <div class="tab-content">'+\
        tab_today_orders_content +\
        '                   <div id="'+ tab_active_id +'" class="tab-pane '+ tab_active_trade +'" style="'+ tab_style_overflow +'"><div>&nbsp;</div>'+ get_trades_tbl(uid,'active',burl,'') +'</div>'+\
        '                   <div id="'+ tab_expired_id +'" class="tab-pane fade" style="'+ tab_style_overflow +'"><div>&nbsp;</div>'+ get_trades_tbl(uid,'expired',burl,'') +'</div>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'
    return box_content
