# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *
from app_stylesheet import *
from app_cookie import *
import pymysql.cursors
from sa_db import *
from sa_func import *

access_obj = sa_db_access()
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_settings_content(burl):
    box_content = ''
    try:
        l_profile_section = 'Profile Settings'
        l_fullname = 'Fullname'
        l_nickname = 'Displayed Nickname'
        l_email = 'Email address'
        l_market_ac = 'What market or asset class do you trade?'

        box_content = ' '+\
        '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        '               <form name="settingsForm" id="settingsForm" method="post" action="'+ burl +'settings/?step=2" >'+\
        '                   <span class="sectiont">'+ l_profile_section +'</span>'+\
        '                   <!--------------------- Name --------------------->'+\
        '                   <div class="input-group input-group-lg">'+\
        '                       <span>'+ l_fullname +'</span>'+\
        '                       <div class="input-group-prepend">'+\
        '                           <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-user-alt" style="font-size: large;"></i></span>'+\
        '                       </div>'+\
        '                           <input type="text" id="name" name="name" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_fullname +'" required autofocus>'+\
        '                   </div>'+\
        '                   <!--------------------- Nickname ----------------->'+\
        '                   <div class="input-group input-group-lg">'+\
        '                       <span>'+ l_nickname +'</span>'+\
        '                       <div class="input-group-prepend">'+\
        '                           <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-user-alt" style="font-size: large;"></i></span>'+\
        '                       </div>'+\
        '                           <input type="text" id="name" name="name" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_nickname +'" required autofocus>'+\
        '                   </div>'+\
        '                   <!--------------------- Email -------------------->'+\
        '                   <div class="input-group input-group-lg">'+\
        '                       <span>'+ l_email +'</span>'+\
        '                       <div class="input-group-prepend">'+\
        '                           <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-at" style="font-size: large;"></i></span>'+\
        '                       </div>'+\
        '                           <input type="email" id="email" name="email" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_email +'" required autofocus>'+\
        '                   </div>'+\
        '                   <!---------------- Trader: Market ---------------->'+\
        '                   <div class="input-group input-group-lg">'+\
        '                       <span>'+ l_market_ac +'</span>'+\
        get_radio_button_Trader_prf()+\
        '                   </div>'+\
        '               </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'
    except Exception as e: print(e)
    return box_content

def get_radio_button_Trader_prf():
    r = ''
    try:
        l_market = 'market'
        l_radioBtn_name = 'tradingProfile'
        value =''; label =''
        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT market_id, market_label FROM market ORDER market_label'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            value = row[0]
            label = row[1]
            r = r + '<input type="radio" name="'+ l_radioBtn_name +'" value="'+ str(value) +'">&nbsp;'+ str(label) +'&nbsp;'+ l_market +'<br>'
        sql = 'SELECT asset_class_id, asset_class_name FROM asset_class ORDER BY asset_class_name'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            value = row[0]
            label = row[1]
            r = r + '<input type="radio" name="'+ l_radioBtn_name +'" value="'+ str(value) +'">&nbsp;'+ str(label)+'<br>'
        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r

def get_settings_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + get_settings_content(burl) + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
