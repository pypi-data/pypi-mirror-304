# Table of contents
* [Features](#features)
  * [Add Comments](#add-comments)
  * [Reply to Comments](#reply-to-comments)
  * [Edit Comments](#edit-comments)
  * [Delete Comments](#delete-comments)
  * [Resolve Comments](#resolve-comments)
  * [Comment Indicators](#comment-indicators)
  * [Go to a Comment](#go-to-a-comment)
    * [Notebook](#notebook)
    * [Editor](#document)
* [Installation](#installation)
* [Setup](#setup)
* [Other](#other)
  * [Hotkeys](#hotkeys)
  * [Users](#users)
  * [Full User Names](#full-user-names)

# Features

## Add Comments

In notebooks, comments are linked to the cells that are currently selected, and in documents, they are linked to selected lines.

If a notebook's cell is deleted or a document line's text changes, the comment is linked to the first cell/line by default.

![Image](images/add_comment.gif)

## Reply to Comments

Replies can be added to level 1 comments.

![Image](images/reply.gif)

## Edit Comments

You can edit comments you have authored.

![Image](images/reply.gif)

## Delete Comments

If a parent comment is deleted, the entire thread is deleted.

![Image](images/delete.gif)

## Resolve Comments

Level 1 comments can be resolved, which hides the whole thread by default.

![Image](images/resolve.gif)

## Comment Indicators

If a comment is added to a cell/line, it is indicated by a comment icon next to it. Clicking the icon opens the comments interface and highlights the comment.

![Image](images/focus_notebook.gif)

## Go to a Comment
### Notebook

Clicking a notebook comment in the interface focuses on the cell the comment is linked to.

![Image](images/focus_interface.gif)
### Document

Clicking a document comment in the interface focuses on the line the comment is linked to.

![Image](images/focus_interface_editor.gif)

# Installation

To install the extension, execute:

```bash
pip install jupyterhub_comments
```

# Setup

When jupyterLab is launched with extension installed, a comments.db file is created in the extension directory by default. You can override this behavior by specifying the `JUPYTERHUB_COMMENTS_DB_PATH` environment variable.

It is necessary to provide `JUPYTERHUB_COMMENTS_DB_PATH` in a multi-user environment to ensure all users share the same comments.db file.

The extension will create `JUPYTERHUB_COMMENTS_DB_PATH` directory with 775 permissions for the current user and all users in the `jupyterhub-users` group (this can be changed via `JUPYTERHUB_COMMENTS_DB_GROUP` environment variable) and give 664 permissions to the comments.db file itself.

If the directory is created prior to launching JupyterLab with the installed extension, permissions should be set up manually, or the directory can be deleted so it will be recreated automatically on the next JupyterLab launch.

# Other

## Hotkeys

When the comment text editor is focused, you can press `Ctrl+Enter` to save a comment and `Esc` to cancel

## Users

The system user is used as a comment author. Only the author can edit and delete their comments

## Full user names

You can implement a function that extracts full usernames from the JupyterHub system username by creating `jupyterhub_comments/username.py` with a `try_getting_full_username(username)` function.

For example this function can pull a username from Active Directory or a database. Code that pulls a name from active directory:

```python
def try_getting_full_username(username):
    '''
    try extracting real name of the user from active
    directory
    '''
    if '.' not in username:
        raise(ValueError('username for Active Directory should contain "."'))
    import ldap
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    l = ldap.initialize('ldaps://<hostname>:3269')
    l.simple_bind_s('<username>', '<password>')
    data = l.search_s(
        'dc=<dc>,dc=local',
        scope=ldap.SCOPE_SUBTREE,
        attrlist=['displayName'],
        filterstr=f'(&(userPrincipalName=<ldap-username>)(objectClass=top))'
    )
    name_parts = data[0][1]['displayName'][0].decode('utf-8').split(' ')
    return ' '.join([name_parts[1], name_parts[0]])
```