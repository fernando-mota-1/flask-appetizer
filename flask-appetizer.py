from flask import Flask, Blueprint, render_template, abort, Response, send_file, send_from_directory
from jinja2 import TemplateNotFound, UndefinedError
import os

appName = os.path.basename(__file__).split('.')[0]
baseDir = os.path.abspath(os.path.dirname(__file__))
fileServeDir = os.path.join(baseDir, 'file-server')
bp = Blueprint(appName, __name__, template_folder='templates')


@bp.route('/', defaults={'req_path': ''})
@bp.route('/<path:req_path>', methods=['GET'])
def dir_listing(req_path):

    # Joining the base and the requested path
    #abs_path = os.path.join(fileServeDir, req_path)
    abs_path = os.path.join('/', req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {f: '/' if os.path.isdir(os.path.join(abs_path,f)) else '' for f in os.listdir(abs_path, )}

    return render_template('files.html', files=files)

def main():
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix='/')
    app.run(port=1919)

if __name__ == "__main__":
    main()