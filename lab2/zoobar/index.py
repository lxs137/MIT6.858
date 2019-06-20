from flask import g, render_template, request
from login import requirelogin
from debug import *
import pcode_client 

@catch_err
@requirelogin
def index():
    if 'profile_update' in request.form:
        pcode_client.update_pcode(g.user.person.username, g.user.token, request.form['profile_update'])
    return render_template('index.html')
