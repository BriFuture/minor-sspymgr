# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

vuefront = Blueprint('vue', __name__, 
    template_folder="../vuetemplates", 
    static_folder="../vuetemplates/vstatic",
    static_url_path="/vstatic" )

@vuefront.route('/home', methods = [ 'GET' ], defaults= { 'path': ''} )
@vuefront.route('/home/<path:path>', methods = [ 'GET' ])
def view_home(path):
    return render_template( 'home.html' )

@vuefront.route('/user', methods = [ 'GET' ], defaults= { 'path': ''} )
@vuefront.route('/user/<path:path>', methods = [ 'GET' ])
def view_user(path):
    return render_template( 'user.html' )

@vuefront.route('/admin', methods = [ 'GET' ], defaults= { 'path': ''} )
@vuefront.route('/admin/<path:path>', methods = [ 'GET' ])
def view_admin(path):
    return render_template( 'admin.html' )

from flask import redirect

def init(app):
    @app.route("/", methods = [ 'GET' ] )
    def app_home_index():
        return redirect( '/home' )
    app.register_blueprint( vuefront )
    app.logger.info("[Plugin VueFront] is Ready")
