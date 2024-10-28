# jupyterhub_comments

A JupyterLab extension that allows adding comments to notebooks and documents in a multiuser environment, where files are shared between users, wher the main goal is the review process

![Image](https://github.com/SausageLion/jupyterhub-comments/blob/main/docs/images/add_comment.gif?raw=true)

# Features

* Add comments to specific cells of jupyter notebooks or lines of text documents
* Edit, delete, resolve and reply to comments
* Icons indicate when comments are added to a document and highlight the comment upon clicking
* Clicking a comment text in an interface focuses notebook cell / line where comment was placed

[Examples and more detailed documentation](https://github.com/SausageLion/jupyterhub-comments/blob/main/docs/README.md)

## Requirements

- JupyterLab >= 4.0.0,<5

## Install

To install the extension, execute:

```bash
pip install jupyterhub_comments
```

To enable comment sharing among users, set the JUPYTERHUB_COMMENTS_DB_PATH environment variable to specify the directory where the comments.db file should be stored. By default, the comments are saved in the directory where the extension is installed, which may vary between users or be non-writable if the extension is installed globally, thus preventing comment sharing.

Ensure that Jupyter users have read, write, and execute permissions for the directory where the comments.db file is located, and read and write permissions for the file itself.

The library will attempt to configure these permissions automatically by creating the specified directory from JUPYTERHUB_COMMENTS_DB_PATH with 775 permissions for the current user and the jupyterhub-users group, and setting 664 permissions on the comments.db file. You can change the default jupyterhub-users group by using the JUPYTERHUB_COMMENTS_DB_GROUP environment variable.

## Uninstall

To remove the extension, execute:

```bash
pip uninstall jupyterhub_comments
```
