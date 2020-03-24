from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify, session, g, escape
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum


app = Flask(__name__)
app.secret_key = 'shakhds_1023Sd'


@app.before_request
def get_name():
    g.name = request.args.get('name')


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'zhai')
    response = '<h1>Hello, %s</h1>' %name
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response



@app.route('/hello1')
def hello1():
    #return redirect('http://www.baidu.com')
    return redirect(url_for('hello'))


@app.route('/404')
def not_found():
    abort(404)


# @app.route('/foo')
# def foo():
#     response = make_response('Hello, World')
#     response.mimetype = 'text/plain'
#     return response



@app.route('/foo1')
def foo1():
    data = {
        'name': 'Beck Zhai',
        'gender': 'male'
    }
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response


@app.route('/foo2')
def fool2():
    return jsonify(name = 'Beck Zhai', gender = 'male')


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response



@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))



@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'



@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))



@app.route('/do_something_and_redirect')
def do_something():
    return redirect_back()



@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something')


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something</a>' % url_for('do_something')


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))



def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data) {
                $('.body').append(data);
            }
        })
    })
})
</script>'''  % post_body



@app.route('/more')
def load_post():
    return generate_lorem_ipsum(1)



@app.route('/hello10/<name>')
def hello10(name):
    return '<h1>Hello, %s!</h1>' % escape(name)