# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
from sa_func import *
access_obj = sa_db_access()
import pymysql.cursors
import datetime
import time
from user_dashboard_count import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def gen_aggregate_perf_graph():
    r = ''
    try:

        l_aggregate_perf_series_name = 'Aggregate Portfolio Performance'

        portf_owner = get_user_numeric_id()

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = ' '+\
        'SELECT DISTINCT chart_data.date, s.nav '+\
        'FROM chart_data '+\
        'JOIN instruments ON instruments.symbol = chart_data.symbol '+\
        'JOIN (SELECT sum(chart_data.price_close) as nav, chart_data.date FROM chart_data '+\
        'JOIN instruments ON instruments.symbol = chart_data.symbol '+\
        'WHERE instruments.owner = '+ str(portf_owner) +' GROUP BY chart_data.date) AS s ON s.date = chart_data.date '+\
        'WHERE instruments.owner = '+ str(portf_owner) +' ORDER BY chart_data.date'
        cr.execute(sql)
        rs = cr.fetchall()
        i = 0
        chart_rows = ''
        for row in rs:
            date = row[0].strftime("%d-%m-%Y")
            nav = row[1]
            if i == 0:
                chart_rows = "['"+ str(date) +"',  "+ str(nav) +"]"
            else:
                chart_rows = chart_rows + ",['"+ str(date) +"',  "+ str(nav) +"]"
            i += 1

        r = "<script>"+\
        "google.charts.load('current', {'packages':['corechart']}); "+\
        "google.charts.setOnLoadCallback(drawChart); "+\
        "function drawChart() { "+\
        "  var data = google.visualization.arrayToDataTable([ "+\
        "    ['text', '"+ l_aggregate_perf_series_name +"'], "+\
        chart_rows +\
        "  ]); "+\
        "  var options = { "+\
        "    title: '"+ l_aggregate_perf_series_name +"', "+\
        "    hAxis: {title: 'Year',  titleTextStyle: {color: '#333'}}, "+\
        "    chartArea:{width:'80%',height:'80%'}, "+\
        "    vAxis: {minValue: 600} "+\
        "  }; "+\
        "  var chart = new google.visualization.AreaChart(document.getElementById('aggr_perf_chart_div')); "+\
        "  chart.draw(data, options); "+\
        "} "+\
        "</script>"+\
        "<div id='aggr_perf_chart_div'></div>"

        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r

def get_aggregate_perf():

    box_content = ''

    try:

        l_title_aggregate_perf = 'Your Performance'

        box_content = '' +\
        '            <div class="box-part rounded" style="height: 465px;">'+\
        '               <span class="sectiont"><i class="fas fa-chart-area"></i>&nbsp;'+ l_title_aggregate_perf +'</span>'+\
        gen_aggregate_perf_graph() +\
        '            </div>'

        '''
        cr.close()
        connection.close()
        '''

    except Exception as e: print(e)

    return box_content

def get_control_center(burl):

    box_content = ''

    try:

        l_control_center_open_trade = 'You have {#} trade(s) to open today.'
        l_control_center_close_trade = 'You have to close {#} trade(s) at the best available price.'
        l_control_center_pending_trade = 'You have {#} trade(s) that you have to get ready to close at market open.'

        num_open_trades = get_num_orders('open')
        num_close_trades =  get_num_orders('close')
        num_pending_trades = get_num_orders('pending')

        l_control_center_open_trade = l_control_center_open_trade.replace('{#}', str(num_open_trades) )
        l_control_center_close_trade = l_control_center_close_trade.replace('{#}', str(num_close_trades) )
        l_control_center_pending_trade = l_control_center_pending_trade.replace('{#}', str(num_close_trades) )

        open_trades = ''
        close_trades = ''
        pending_trades = ''

        if num_open_trades != 0:
            open_trades = ' '+\
            '  <li class="list-group-item d-flex justify-content-between align-items-center">'+\
            '<span style="font-size: small;">' + l_control_center_open_trade +'</span>'+\
            '    <span class="badge badge-primary badge-pill">'+ str(num_open_trades) +'</span>'+\
            '  </li>'
        if num_close_trades != 0:
            close_trades = ' '+\
            '  <li class="list-group-item d-flex justify-content-between align-items-center">'+\
            '<span style="font-size: small;">' + l_control_center_close_trade +'</span>' +\
            '    <span class="badge badge-warning badge-pill">'+ str( num_close_trades ) +'</span>'+\
            '  </li>'
        if num_pending_trades != 0:
            pending_trades = ' '+\
            '  <li class="list-group-item d-flex justify-content-between align-items-center">'+\
            '<span style="font-size: small;">' + l_control_center_pending_trade +'</span>' +\
            '    <span class="badge badge-secondary badge-pill">'+ str( num_pending_trades ) +'</span>'+\
            '  </li>'

        control_center_content = ' '+\
        '<ul class="list-group">'+\
        open_trades +\
        close_trades +\
        pending_trades +\
        '</ul>'

        l_title_control_center = 'Control Center'

        box_content = '' +\
        '            <div class="box-part rounded" style="height: 250px;">'+\
        '               <span class="sectiont"><i class="fas fa-tasks"></i>&nbsp;'+ l_title_control_center +'</span>'+\
        control_center_content+\
        '            </div>'

    except Exception as e: print(e)

    return box_content


def get_control_center_aggregate_perf(burl):
    r = ''
    try:
        r = '<div class="col-lg-6 col-md-12 col-sm-12 col-xs-12">'+\
        get_control_center(burl)+\
        get_aggregate_perf()+\
        '</div>'

    except Exception as e: print(e)
    return r