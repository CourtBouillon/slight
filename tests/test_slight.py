import pytest


def test_index(test_app):
    html = test_app.get('/').data.decode('utf8')
    for i in range(1, 4):
        assert f'slideshow-{i}' in html


@pytest.mark.parametrize('i', range(1, 4))
def test_slideshow(test_app, i):
    html = test_app.get(f'/slideshow/slideshow-{i}/').data.decode('utf8')
    assert 'bars' in html
    assert f'<title>slideshow {i}</title>' in html
    assert f'<section>slideshow {i}</section>' in html


def test_slideshow_404(test_app):
    assert test_app.get('/slideshow/slideshow-5/').status_code == 404


def test_save_slideshow(test_app):
    base_url = '/slideshow/slideshow-1/'
    for value in ('test', 'slideshow 1'):
        content = f'<section>{value}</section>'
        post = test_app.post(f'{base_url}save', data={'sections': content})
        assert post.status_code == 200
        html = test_app.get(base_url).data.decode('utf8')
        assert content in html


def test_save_slideshow_404(test_app):
    post = test_app.post('/slideshow/slideshow-5/save', data={'sections': ''})
    assert post.status_code == 404


def test_slideshow_static(test_app):
    url = '/slideshow/slideshow-1/static/test'
    content = test_app.get(url).data.decode('utf8')
    assert 'slideshow 1' in content


@pytest.mark.parametrize('i', range(1, 5))
def test_slideshow_static_404(test_app, i):
    url = f'/slideshow/slideshow-{i}/static/nothing'
    assert test_app.get(url).status_code == 404


def test_static(test_app):
    css = test_app.get('/static/index.css').data.decode('utf8')
    assert '{' in css


def test_static_404(test_app):
    assert test_app.get('/static/nothing').status_code == 404


@pytest.mark.parametrize('i', range(1, 4))
def test_theme_static(test_app, i):
    css = test_app.get(f'/themes/theme-{i}/style.css').data.decode('utf8')
    assert f'theme {i}' in css


@pytest.mark.parametrize('i', range(1, 5))
def test_theme_static_404(test_app, i):
    assert test_app.get(f'/themes/theme-{i}/nothing').status_code == 404


def test_theme_static_ignored(test_app):
    assert test_app.get('/themes/.ignored/style.css').status_code == 404


def test_pdf(test_app):
    pdf = test_app.get('/slideshow/slideshow-1.pdf').data
    assert pdf.startswith(b'%PDF')


def test_pdf_404(test_app):
    assert test_app.get('/slideshow/slideshow-5.pdf').status_code == 404


def test_add_delete(test_app):
    assert 'Add' in test_app.get('/slideshow/add').data.decode('utf8')
    data = {'name': 'name', 'folder': 0, 'theme': 0}
    post = test_app.post('/slideshow/add', data=data)
    assert post.status_code < 400
    assert 'name' in test_app.get('/slideshow/name/').data.decode('utf8')
    assert 'Delete' in test_app.get(
        '/slideshow/name/delete').data.decode('utf8')
    data = {'action': 'Delete'}
    post = test_app.post('/slideshow/name/delete', data=data)
    assert post.status_code < 400
    assert test_app.get('/slideshow/name/').status_code == 404


def test_add_delete_no_theme(test_app):
    assert 'Add' in test_app.get('/slideshow/add').data.decode('utf8')
    data = {'name': 'name', 'folder': 0}
    post = test_app.post('/slideshow/add', data=data)
    assert post.status_code < 400
    assert 'name' in test_app.get('/slideshow/name/').data.decode('utf8')
    assert 'Delete' in test_app.get(
        '/slideshow/name/delete').data.decode('utf8')
    data = {'action': 'Delete'}
    post = test_app.post('/slideshow/name/delete', data=data)
    assert post.status_code < 400
    assert test_app.get('/slideshow/name/').status_code == 404


def test_delete_404(test_app):
    assert test_app.get('/slideshow/unknown/delete').status_code == 404
    data = {'action': 'Delete'}
    post = test_app.post('/slideshow/unknown/delete', data=data)
    assert post.status_code == 404


def test_delete_cancel(test_app):
    data = {'action': 'Cancel'}
    post = test_app.post('/slideshow/slideshow-1/delete', data=data)
    assert post.status_code < 400
    html = test_app.get('/slideshow/slideshow-1/').data.decode('utf8')
    assert 'slideshow-1' in html


def test_rename(test_app):
    html = test_app.get('/slideshow/slideshow-1/rename').data.decode('utf8')
    assert 'slideshow-1' in html
    data = {'name': 'name'}
    post = test_app.post('/slideshow/slideshow-1/rename', data=data)
    assert post.status_code < 400
    html = test_app.get('/slideshow/name/').data.decode('utf8')
    assert 'slideshow 1' in html
    data = {'name': 'slideshow-1'}
    post = test_app.post('/slideshow/name/rename', data=data)
    assert test_app.get('/slideshow/name/').status_code == 404
    html = test_app.get('/slideshow/slideshow-1/').data.decode('utf8')
    assert 'slideshow 1' in html


def test_rename_404(test_app):
    assert test_app.get('/slideshow/unknown/rename').status_code == 404
    data = {'action': 'Rename'}
    post = test_app.post('/slideshow/unknown/rename', data=data)
    assert post.status_code == 404
