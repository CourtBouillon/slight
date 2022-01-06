from os import getenv
from pathlib import Path

from flask import (
    Flask, abort, render_template, request, send_from_directory, url_for)
from flask_weasyprint import HTML, render_pdf

__version__ = '0.0.0'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html.jinja2', slideshows=paths('slideshows'))


@app.route('/slideshow/<name>/')
def slideshow(name):
    for root in paths('slideshows'):
        if root.name != name:
            continue
        slideshow = (root / 'slides.html').read_text()
        meta = (root / 'meta.html').read_text()
        return render_template(
            'slideshow.html.jinja2', slideshow=slideshow, meta=meta, name=name)
    return abort(404)


@app.route('/slideshow/<name>/save', methods=('POST',))
def save_slideshow(name):
    for root in paths('slideshows'):
        if root.name != name:
            continue
        (root / 'slides.html').write_text(request.form['sections'])
        return 'OK'


@app.route('/slideshow/<name>/static/<path:path>')
def slideshow_static(name, path):
    return custom_static('slideshows', name, Path('static') / path)


@app.route('/themes/<name>/<path:path>')
def theme_static(name, path):
    return custom_static('themes', name, Path(path))


@app.route('/slideshow/<name>.pdf')
def print_slideshow(name):
    html = HTML(url_for('slideshow', name=name), media_type='weasyprint')
    return render_pdf(html)


def custom_static(variable, name, path):
    for root in paths(variable):
        if root.name != name:
            continue
        if (root / path).is_file():
            try:
                return send_from_directory(root, path)
            except Exception:
                break
    return abort(404)


def paths(variable):
    for path in app.config[variable]:
        for child in path.iterdir():
            if child.is_dir() and child.name[0] != '.':
                yield child


for variable in ('slideshows', 'themes'):
    folders = getenv(f'SLIGHT_{variable.upper()}', '').split(':')
    app.config[variable] = [Path(folder) for folder in folders if folder]
