import os
import json
import tornado
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from pathlib import Path
import sqlite3

try:
    DB_PATH = os.path.join(
        os.environ['JUPYTERHUB_COMMENTS_DB_PATH'],
        'comments.db'
    )
except KeyError:
    path = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(path, 'comments.db')

def init_comments_table():
    '''
    creates comments table if it does not exist yet,
    updates db file permissions to make it accessible
    '''
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = '''
        create table if not exists comments (
            id text primary key,
            file_path text not null,
            cell_id text not null,
            editor_line number null,
            editor_line_text text null,
            username text not null,
            text text not null,
            timestamp integer not null,
            updated_timestamp integer not null,
            resolved boolean not null,
            parent_id text null,
            file_owner not null
        );
        '''
        cursor.execute(query)
        cursor.execute('create index if not exists idx_file_path on comments (file_path);')
        cursor.execute('create index if not exists idx_ids on comments (id, parent_id);')
    set_db_permissions()

def set_db_permissions():
    '''
    sets permissions on comments.db file to make in
    writable by users in jupyterhub-users group
    '''
    from shutil import chown
    os.chmod(DB_PATH, 0o664)
    try:
        chown(DB_PATH, group='jupyterhub-users')
    except LookupError:
        pass

def init_users_table():
    '''
    creates table with full user names if it
    does not exist
    '''
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = '''
        create table if not exists users(
            username text primary key,
            full_username text not null
        );
        '''
        cursor.execute(query)

def get_comments(file_path):
    '''
    returns all comments for specified file path
    '''
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cols = [
            'c.id', 'c.file_path', 'c.cell_id', 'c.editor_line',
            'c.editor_line_text', 'c.username', 'u.full_username',
            'c.text', 'c.timestamp', 'c.updated_timestamp',
            'c.resolved', 'c.parent_id', 'c.file_owner'
        ]
        query = f'''
        select
            {','.join(cols)}
        from comments as c
        left join users as u on
            u.username = c.username
        where
            file_path = '{resolve_path(file_path)}'
        '''
        cursor.execute(query)
        comments = [
            {c.split('.')[1] : comment[i] for i,c in enumerate(cols)}
            for comment in cursor.fetchall()
        ]
        return comments

def upsert_comment(comment):
    '''
    creates comment if it does not exist, otherwise
    updates its properties
    '''
    id = comment['id']
    file_path = resolve_path(comment['file_path'])
    cell_id = comment['cell_id']
    editor_line = comment['editor_line']
    editor_line_text = comment['editor_line_text']
    username = comment['username']
    text = comment['text']
    timestamp = comment['timestamp']
    resolved = comment['resolved']
    parent_id = comment['parent_id']
    file_owner = get_file_owner(file_path)
    
    assert resolved in [0,1]
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f'''
        insert into comments (
            id, file_path, cell_id, editor_line, editor_line_text,
            username, text, timestamp, updated_timestamp, resolved,
            parent_id, file_owner
        )
        values (
            (?), (?), (?), (?), (?), (?),
            (?), (?), (?), (?), (?), (?)
        )
        on conflict(id) do update set
            file_path = excluded.file_path,
            cell_id = excluded.cell_id,
            editor_line = excluded.editor_line,
            editor_line_text = excluded.editor_line_text,
            username = excluded.username,
            text = excluded.text,
            updated_timestamp = excluded.timestamp,
            resolved = excluded.resolved,
            parent_id = excluded.parent_id,
            file_owner = excluded.file_owner
        '''
        cursor.execute(query, (
            id, file_path, cell_id, editor_line, editor_line_text,
            username, text, timestamp, timestamp, resolved, parent_id,
            file_owner
        ))

def delete_comment(comment):
    '''
    deletes comment with specified id
    '''
    id = comment['id']
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        query = f'''
        delete from comments
        where
            id = '{id}'
            or parent_id = '{id}'
        '''
        cursor.execute(query)

def get_username():
    '''
    extract system username of current jupyterlab user
    as well as real username
    '''
    import getpass
    username = getpass.getuser().replace('jupyter-', '')
    if username == 'vadim':
        username = 'v.arnold'
    full_username = get_full_username(username)
    return {
        'username' : username,
        'full_username' : full_username
    }

def resolve_path(path):
    '''
    returns resolved path
    '''
    return str(Path(path).expanduser().resolve())

def get_resolved_path(root_path):
    '''
    resolves absoute root path where
    jupyter started for a user
    '''
    return {
        'resolved_path' : resolve_path(root_path)
    }

def get_file_owner(file_path):
    '''
    extracts owner of a file at specified path
    '''
    try:
        username = Path(file_path).owner()
    except FileNotFoundError:
        username = ''
    if username == 'vadim':
        username = 'v.arnold'
    return username

def get_full_username(username):
    '''
    if real username exists in users table return it
    otherwise try extracting it from active directory
    and storing in users table for future use
    '''
    try:
        '''
        optional function that handles extracting
        real user name from Active Directory / DB /
        so on, should be defined manually
        '''
        from .username import try_getting_full_username
    except ModuleNotFoundError:
        def try_getting_full_username(username):
            raise ValueError
    
    full_username = ''
    with sqlite3.connect(DB_PATH) as connection:
        query = f'''
        select
            full_username
        from users
        where
            username = '{username}'
        '''
        cursor = connection.cursor()
        cursor.execute(query)
        try:
            full_username = cursor.fetchone()[0]
        except TypeError:
            try:
                full_username = try_getting_full_username(username)
                insert_full_username(username, full_username)
            except Exception as ex:
                pass
    return full_username

def insert_full_username(username, full_username):
    '''
    stores real username in users table for future use
    (to not access active directory each time since in
    can be somewhat unstable, digger is the example)
    '''
    query = f'''
    insert into users (username, full_username)
    values ('{username}', '{full_username}')
    on conflict(username) do update set
        full_username = excluded.full_username
    '''
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(query)

class RouteHandler(APIHandler):
    '''
    The following decorator should be present on all verb methods (head, get, post,
    patch, put, delete, options) to ensure only authorized user can request the
    Jupyter server

    those methods define how different request types (GET, POST, DELETE) should
    be handled by API service
    '''

    @tornado.web.authenticated
    def post(self):
        endpoint = self.request.path.split('/')[-1]
        input_data = self.get_json_body()
        if endpoint == 'comment':
            return self.finish(json.dumps(self.comment(input_data)))
        elif endpoint == 'comments':
            return self.finish(json.dumps(self.comments(input_data)))
        elif endpoint == 'resolve-path':
            return self.finish(json.dumps(self.get_resolved_path(input_data)))
    
    @tornado.web.authenticated
    def delete(self):
        endpoint = self.request.path.split('/')[-1]
        input_data = self.get_json_body()
        if endpoint == 'comment':
            return self.finish(json.dumps(self.delete_comment(input_data)))
        
    @tornado.web.authenticated
    def get(self):
        endpoint = self.request.path.split('/')[-1]
        input_data = self.get_json_body()
        if endpoint == 'username':
            return self.finish(json.dumps(self.get_username(input_data)))

    def comment(self, data):
        try:
            upsert_comment(data)
            return {'status' : 'ok'}
        except Exception as ex:
            return {'error' : str(ex)}

    def comments(self, data):
        try:
            return {'comments' : get_comments(data['file_path'])}
        except Exception as ex:
            return {'error' : str(ex)}

    def delete_comment(self, data):
        try:
            delete_comment(data)
            return {'status' : 'ok'}
        except Exception as ex:
            return {'error' : str(ex)}
        
    def get_username(self, data):
        try:
            return get_username()
        except Exception as ex:
            return {'error' : str(ex)}
        
    def get_resolved_path(self, data):
        try:
            return get_resolved_path(data['root_path'])
        except Exception as ex:
            return {'error' : str(ex)}

def setup_handlers(web_app):
    '''
    initialized api service
    '''
    init_comments_table()
    init_users_table()
    host_pattern = '.*$'

    base_url = web_app.settings['base_url']
    # Prepend the base_url so that it works in a JupyterHub setting
    handlers = [
        (url_path_join(base_url, 'jupyterhub-comments-server', 'comment'), RouteHandler),
        (url_path_join(base_url, 'jupyterhub-comments-server', 'comments'), RouteHandler),
        (url_path_join(base_url, 'jupyterhub-comments-server', 'username'), RouteHandler),
        (url_path_join(base_url, 'jupyterhub-comments-server', 'resolve-path'), RouteHandler)
    ]
    web_app.add_handlers(host_pattern, handlers)