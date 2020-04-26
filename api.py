"""
API module for CARE
"""
import os
from flask_restful import Resource
from flask import render_template, make_response, redirect, session
from app_settings import APP, API
from utility import ApiUtils
from execute import run

LOG = APP.logger

class Operations(Resource, ApiUtils):
    """
    Endpoint : /execute
    Supported Methods : get, post
    """
    def post(self):
        """
        Upload file to input directory, Params-> file (Attach file in client request)
        """        
        execute_params = self.get_execute_params()
        run(execute_params)
        return redirect("/report/show")


class Home(Resource, ApiUtils):
    def get(self):
        return self.home()

class Report(Resource, ApiUtils):
    def get(self, option):
        return self.generate_report(option)

class Login(Resource, ApiUtils):
    def get(self):
        if session.get('logged_in'):
            return redirect('/')
        return make_response(render_template('login.html'))
        
    def post(self):
        return self.user_login()

class Logout(Resource, ApiUtils):
    def get(self):
        return self.user_logout()


API.add_resource(Home, '/', endpoint='/')
API.add_resource(Login, '/login', endpoint='/login')
API.add_resource(Logout, '/logout', endpoint='/logout')
API.add_resource(Operations, '/execute', endpoint='/execute')
API.add_resource(Report, '/report/<option>', endpoint='/report/show')
API.add_resource(Report, '/report/<option>', endpoint='/report/download')

if __name__ == "__main__":
    APP.run(debug=True, port=7000)
