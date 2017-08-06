import os
import robovest
import unittest
import tempfile

class RobovestTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, robovest.app.config['DATABASE'] = tempfile.mkstemp()
        robovest.app.testing = True
        self.app = robovest.app.test_client()
        with robovest.app.app_context():
            .init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(robovest.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
    ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('robox', 'vest')
        assert b'Invalid username' in rv.data
        rv = self.login('robo', 'vestx')
        assert b'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

    def get_user():
        user = getattr(g, 'user', None)
        if user is None:
            user = fetch_current_user_from_database()
            g.user = user
        return user

# import flask
#
# app = flask.Flask(__name__)
#
# with app.test_request_context('/?name=Peter'):
#     assert flask.request.path == '/'
#     assert flask.request.args['name'] == 'Peter'
#
# app = flask.Flask(__name__)
#
# with app.test_request_context('/?name=Peter'):
#     app.preprocess_request()
#     ...
# app = flask.Flask(__name__)
#
# with app.test_request_context('/?name=Peter'):
#     resp = Response('...')
#     resp = app.process_response(resp)
#     ...
#
# from contextlib import contextmanager
# from flask import appcontext_pushed, g
#
# @contextmanager
# def user_set(app, user):
#     def handler(sender, **kwargs):
#         g.user = user
#     with appcontext_pushed.connected_to(handler, app):
#         yield
#
# from flask import json, jsonify
#
# @app.route('/users/me')
# def users_me():
#     return jsonify(username=g.user.username)
#
# with user_set(app, my_user):
#     with app.test_client() as c:
#         resp = c.get('/users/me')
#         data = json.loads(resp.data)
#         self.assert_equal(data['username'], my_user.username)
#
# app = flask.Flask(__name__)
#
# with app.test_client() as c:
#     rv = c.get('/?tequila=42')
#     assert request.args['tequila'] == '42'
#
# with app.test_client() as c:
#     rv = c.get('/')
#     assert flask.session['foo'] == 42
#
# with app.test_client() as c:
#     with c.session_transaction() as sess:
#         sess['a_key'] = 'a value'


if __name__ == '__main__':
    unittest.main()
