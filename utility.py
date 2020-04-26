"""
Conatins all the utilities used across all the modules.
"""
import os
from flask import request, send_from_directory, render_template,\
                  make_response, redirect, session
import pandas as pd
from werkzeug.utils import secure_filename
from app_settings import APP

LOG = APP.logger

class ApiUtils:
    """
    Utlitiy methods for REST Endoints
    """
    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    def get_execute_params(self):
        input_file = request.files.get('input_file')
        build_file = request.files.get('build_file')
        drop_down = True
        if build_file:
            build_name = build_file.filename
            build_file.save(os.path.join(APP.config['BUILD_FOLDER'], secure_filename(build_name)))
            drop_down = False
        else:
            build_name = request.form.get('build_files')
        build_no = request.form.get('build_no')
        input_file.save(os.path.join(APP.config['INPUT_FOLDER'], secure_filename(input_file.filename)))
        LOG.info("%s & %s uploaded."%(input_file.filename, build_file))
        input_file_path = os.path.join(APP.config['INPUT_FOLDER'], input_file.filename)
        build_file_path = os.path.join(APP.config['BUILD_FOLDER'], build_name)
        execute_params = dict(input_file_path=input_file_path, build_file_path=build_file_path,
                              build_no=build_no, drop_down=drop_down)
        LOG.debug(execute_params)
        return execute_params

    def download_file(self):
        filename = request.args.get('filename')
        file = send_from_directory(APP.config['OUTPUT_FOLDER'], filename, as_attachment=True)
        LOG.info(f'Attaching {filename} in response')
        return file

    def render_download(self):
        output_files = os.listdir(APP.config['OUTPUT_FOLDER'])
        return make_response(render_template('downloads.html', output=output_files), 200, self.headers)
    
    def delete_file(self):
        file_name = request.args.get('filename')
        os.remove(os.path.join(APP.config['OUTPUT_FOLDER'], file_name))
        return redirect(request.referrer)
    
    def get_stored_builds(self):
        #Todo only 3 latest builds
        return os.listdir(APP.config['BUILD_FOLDER'])

    def home(self):
        if not session.get('logged_in'):
            return redirect('/login')
        builds = self.get_stored_builds()
        if builds:
            return make_response(render_template('main.html', stored_builds=builds), 200, self.headers)
        return make_response(render_template('main.html'))    

    def user_login(self):
        username = request.form.get('username') 
        password = request.form.get('password')
        if password == APP.config['USERS'].get(username):
            session['logged_in'] = True
            return redirect('/')
        failed_reponse = 'Incorrect Usename or Password'
        return make_response(render_template('login.html', auth_reponse=failed_reponse))
    
    def user_logout(self):
        session.pop('logged_in', None)
        return redirect('/login')

    def generate_report(self, option):
        if not session.get('logged_in'):
            return redirect('/login')
        if option == 'download':
            return self.download_file()
        output = os.listdir(APP.config['OUTPUT_FOLDER'])
        if output:
            file_path = os.path.join(APP.config['OUTPUT_FOLDER'], output[0])
            df = pd.read_csv(file_path, na_values='-')
            return make_response(render_template('report.html',\
                 excel=df.to_html(classes="table table-hover table-striped w-auto", index=False), \
                                  filename=output[0]), 200, self.headers)
        return make_response(render_template('report.html'), \
                                              200, self.headers)
