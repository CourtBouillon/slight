from html import escape
from os import getenv
from pathlib import Path
from shutil import rmtree

from flask import (
    Flask, abort, redirect, render_template, request, send_from_directory,
    url_for)
from flask_weasyprint import HTML, render_pdf
from weasyprint.urls import URLFetchingError

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


@app.route('/slideshow/add', methods=('get', 'post'))
def add_slideshow():
    themes = tuple(paths('themes'))
    folders = app.config['slideshows']
    if request.method.lower() == 'post':
        folder = folders[int(request.form['folder'])]
        name = Path(request.form['name']).name
        html_name = escape(name)
        slideshow_folder = folder / name
        slideshow_folder.mkdir()
        content = f'<section><h1>{html_name}</h1><p>Text</p></section>\n'
        (slideshow_folder / 'slides.html').write_text(content)
        content = f'<title>{html_name}</title>\n'
        if 'theme' in request.form:
            theme = themes[int(request.form['theme'])]
            content += (
                '<link rel="stylesheet" '
                f'href="/themes/{theme.name}/style.css" />\n')
        (slideshow_folder / 'meta.html').write_text(content)
        return redirect(url_for('slideshow', name=name))
    return render_template(
        'add_slideshow.html.jinja2', themes=themes, folders=folders)


@app.route('/slideshow/<name>/delete', methods=('get', 'post'))
def delete_slideshow(name):
    for root in paths('slideshows'):
        if root.name != name:
            continue
        if request.method.lower() == 'post':
            if request.form['action'].lower() == 'delete':
                rmtree(root)
                return redirect(url_for('index'))
            else:
                return redirect(url_for('slideshow', name=name))
        return render_template('delete_slideshow.html.jinja2', name=name)
    return abort(404)


@app.route('/slideshow/<name>/rename', methods=('get', 'post'))
def rename_slideshow(name):
    for root in paths('slideshows'):
        if root.name != name:
            continue
        if request.method.lower() == 'post':
            name = Path(request.form['name']).name
            root.rename(root.parent / name)
            return redirect(url_for('slideshow', name=name))
        return render_template('rename_slideshow.html.jinja2', name=name)
    return abort(404)


@app.route('/slideshow/<name>.pdf')
def print_slideshow(name):
    try:
        html = HTML(url_for('slideshow', name=name), media_type='weasyprint')
    except URLFetchingError:
        return abort(404)
    return render_pdf(html)


@app.route('/slideshow/<name>/save', methods=('post',))
def save_slideshow(name):
    for root in paths('slideshows'):
        if root.name != name:
            continue
        (root / 'slides.html').write_text(request.form['sections'])
        return 'OK'
    return abort(404)


@app.route('/slideshow/<name>/static/<path:path>')
def slideshow_static(name, path):
    return custom_static('slideshows', name, Path('static') / path)


@app.route('/themes/<name>/<path:path>')
def theme_static(name, path):
    return custom_static('themes', name, Path(path))


def custom_static(variable, name, path):
    for root in paths(variable):
        if root.name != name:
            continue
        if (root / path).is_file():
            try:
                return send_from_directory(root, path)
            except Exception:  # pragma: no cover
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
