# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request, redirect
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_instr_fullname(uid):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            symbol = row[0]

    except Exception as e:
        print(e)
    return r

def get_portf_table_rows():
    r = ''
    try:
        for i in range(5):

            strategy_order_type = request.cookies.get('portf_s_' + str(i+1) + '_type' )
            strategy_conviction = request.cookies.get('portf_s_' + str(i+1) + '_conv' )
            instr_selection = ''
            uid = request.cookies.get('portf_s_' + str(i+1) )

            if not uid is None or uid == '':
                connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
                cr = connection.cursor(pymysql.cursors.SSCursor)
                sql = "SELECT instruments.fullname, instruments.symbol FROM instruments JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
                "WHERE symbol_list.uid=" + str(uid)
                cr.execute(sql)
                rs = cr.fetchall()
                for row in rs: instr_selection = row[0] + '('+ row[1] +')'
                cr.close()


            r = r + ''+\
            '    <tr>'+\
            '      <th scope="row">'+\
            '       <div class="dropdown">'+\
            '           <button class="btn btn-secondary dropdown-toggle" type="button" id="strategy_order_type_'+ str(i+1) +'" name="strategy_order_type_'+ str(i+1) +'" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
            strategy_order_type +\
            '           </button>'+\
            '           <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'+\
            '               <a class="dropdown-item" href="#">Buy and Sell (Long/Short)</a>'+\
            '               <a class="dropdown-item" href="#">Buy Only (Long)</a>'+\
            '               <a class="dropdown-item" href="#">Sell Only (Short)</a>'+\
            '           </div>'+\
            '       </div>'+\
            '       </th>'+\
            '       <td>'+\
            '       <div class="dropdown">'+\
            '           <button class="btn btn-secondary dropdown-toggle" type="button" id="strategy_conviction_'+ str(i+1) +'" name="strategy_conviction_'+ str(i+1) +'" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
            strategy_conviction +\
            '           </button>'+\
            '           <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'+\
            '               <a class="dropdown-item" href="#">Weak</a>'+\
            '               <a class="dropdown-item" href="#">Strong</a>'+\
            '               <a class="dropdown-item" href="#">Neutral</a>'+\
            '           </div>'+\
            '       </div>'+\
            '      </td>'+\
            '      <td width="100%">'+ instr_selection +'</td>'+\
            '    </tr>'
    except Exception as e:
        print(e)
    return r

def get_list_portf_alloc(burl):
    r = ''
    try:
        l_conviction = 'What is your conviction?'
        l_buttonSave = 'Save and generate portfolio'
        r = '' +\
        '<table class="table table-hover">'+\
        '  <thead>'+\
        '    <tr>'+\
        '      <th scope="col" colspan="3">'+ l_conviction +'</th>'+\
        '    </tr>'+\
        '  </thead>'+\
        '  <tbody>'+\
        get_portf_table_rows() +\
        '  </tbody>'+\
        '</table>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<form method="GET" action="'+ burl +'p/?ins=4">'+\
        '   <button type="submit" class="btn btn-info btn-lg form-signin-btn"><i class="fas fa-save"></i>&nbsp;'+ l_buttonSave +'</button>'+\
        '</form>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'
    except Exception as e:
        print(e)
    return r

def get_box_portf_save(burl):

    box_content = ''

    try:

        box_content = '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-center-content sa-instr-n-portf-list">'+\
        get_list_portf_alloc(burl)+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


        #cr.close()
        #connection.close()

    except Exception as e: print(e)

    return box_content
