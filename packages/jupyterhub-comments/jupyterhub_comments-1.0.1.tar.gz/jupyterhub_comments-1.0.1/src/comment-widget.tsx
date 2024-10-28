import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { ILabShell } from '@jupyterlab/application';
import { INotebookTracker } from '@jupyterlab/notebook';
import { IEditorTracker } from '@jupyterlab/fileeditor';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { LabIcon } from '@jupyterlab/ui-components';
import { TranslationBundle } from '@jupyterlab/translation';
import { PageConfig, IChangedArgs } from '@jupyterlab/coreutils';
import { ICellModel } from '@jupyterlab/cells'
import { requestAPI } from './handler';
import { Panel } from './panel';
import commentSvg from '../style/icons/comment-icon.svg';

/**
 * Icon that is used on the right side menu and to the left of
 * cells / editor lines which contain comments
 *
 * @type {*}
 */
const commentIcon = new LabIcon({
  name: 'CommentIcon',
  svgstr: commentSvg
});

/**
 * Parent element for extension. Listens to user actions outside of
 * extension interface and emits into so interface can act accordingly
 *
 * @export
 * @class CommentWidget
 * @typedef {CommentWidget}
 * @extends {ReactWidget}
 */
export class CommentWidget extends ReactWidget {
  /**
   * Object that tracks if currently openned file was changed, we
   * need this to update current file path and name
   *
   * @private
   * @type {ILabShell}
   */
  private labShell: ILabShell;
  
  /**
   * Object that stores information about oppened files, like their
   * paths and names
   *
   * @private
   * @type {IDocumentManager}
   */
  private docmanager: IDocumentManager;
  
  /**
   * Object that tracks events in notebooks, wee need this to
   * check which cell is currently focused, to link comments
   * to it
   *
   * @private
   * @type {INotebookTracker}
   */
  private notebookTracker: INotebookTracker;
  
  /**
   * Object that tracks events in documents, we need this to
   * check which where user's cursor is placed to link comments
   * to those lines
   *
   * @private
   * @type {IDocumentManager}
   */
  private editorTracker: IEditorTracker;
  
  /**
   * Object trat translated interface text into languages for
   * which translation was provided
   *
   * @private
   * @type {TranslationBundle}
   */
  private trans: TranslationBundle;
  
  /**
   * Parameters about current user, openned file and comments linked to it
   *
   * @type {{ 
   *   comments: [] list of comments linked to a file
   *   rootPath: string full path of directory where user started jupyter
   *   filePath: string path to the currently openned file
   *   fileName: string name of the currently openned file
   *   username: string username of user that interacts with jupyter
   *   fullUsername: string real name of user
   *   commentTimeouts: { [key: string]: NodeJS.Timeout; } timeout that prevents highligh
   *   effect from triggering multiple times
   * }}
   */
  state = {
    comments: [] as any[],
    rootPath: '',
    filePath: '',
    fileName: '',
    username: 'guest',
    fullUsername: '',
    commentTimeouts: {} as { [key: string]: NodeJS.Timeout }
  };
  
  /**
   * Creates an instance of CommentWidget.
   *
   * @constructor
   * @param {ILabShell} labShell
   * @param {IDocumentManager} docmanager
   * @param {INotebookTracker} notebookTracker
   * @param {IEditorTracker} editorTracker
   * @param {TranslationBundle} trans
   */
  constructor(
    labShell: ILabShell,
    docmanager: IDocumentManager,
    notebookTracker: INotebookTracker,
    editorTracker: IEditorTracker,
    trans: TranslationBundle
  ) {
    super();
    this.id = 'comment-widget';
    this.title.icon = commentIcon;

    this.labShell = labShell;
    this.docmanager = docmanager;
    this.notebookTracker = notebookTracker;
    this.editorTracker = editorTracker;
    this.trans = trans;
    
    this.updateComments = this.updateComments.bind(this);
    this.subscribeToCellExecution();
    this.initializeWidget();
  }
  
  /**
   * waits until one of the widgets in the jupyter interface
   * becomes active, loads comments for that file and adds
   * an event handler that listens for active file changes
  */
  initializeWidget() {
    this.setUsername();
    this.setRootPath();
    const interval = setInterval(() => {
      if (this.state.filePath) {
        clearInterval(interval);
        this.subscribeToShellChanges();
        this.updateComments();
        setTimeout(() => {
          this.processCommentLink();
        }, 500);
      } else {
        this.trySettingLocalPath();
      }
    }, 250);
  }
  
  /**
   * if comment-id is in url, open comment widget
   * and highlight a comment with requested id
   */
  processCommentLink() {
    const urlParams = new URLSearchParams(window.location.search);
    const commentId = urlParams.get('comment-id');
    const filePath = window.location.pathname.split('lab/tree/')[1];
    if (commentId && filePath) {
      this.docmanager.openOrReveal(filePath);
      this.focusComment(commentId);
    }
  }
  
  /**
   * checks if any widget is active, if it is, extracts its path
   * and sets according state variables
   */
  trySettingLocalPath() {
    const currentWidget = this.labShell.currentWidget;
    if (currentWidget) {
      const localPath =
        this.docmanager.contextForWidget(currentWidget)?.localPath;
      if (localPath) {
        this.state.filePath = this.state.rootPath + '/' + localPath;
        this.state.fileName = localPath.split('/').slice(-1)[0];
      }
    }
  }
  
  /**
   * triggers when user selects another widget (file) in
   * the interface, loads comments for that widget
   */
  subscribeToShellChanges() {
    this.labShell.currentChanged.connect((sender, args) => {
      const currentWidget = args.newValue;
      if (!currentWidget) {
        return;
      }
      const localPath =
        this.docmanager.contextForWidget(currentWidget)?.localPath;
      if (localPath) {
        this.state.filePath = this.state.rootPath + '/' + localPath;
        this.state.fileName = localPath.split('/').slice(-1)[0];
        this.updateComments();
      } else {
        this.state.filePath = '';
        this.updateComments();
      }
    });
  }
  
  /**
   * opens comments widget if is is collapsed
   * searches for a comment with specified id
   * if search is successfull, focuses that comment
   * and adds a glow animation to highlight it
   * 
   * @param {string} commentId
   */
  focusComment(commentId: string) {
    const container = document.querySelector('.jp-comments-comments-container');
    const comment = container?.querySelector(
      '[data-comment-id="' + commentId + '"]'
    );
    if (comment) {
      comment.scrollIntoView({ behavior: 'smooth', block: 'start' });
      comment.classList.add('jp-comments-glowing-border');
      this.labShell.activateById('comment-widget');
      this.labShell.expandRight();
      if (commentId in this.state.commentTimeouts) {
        clearTimeout(this.state.commentTimeouts[commentId]);
      }
      const timeoutId = setTimeout(() => {
        comment.classList.remove('jp-comments-glowing-border');
      }, 3000);
      this.state.commentTimeouts[commentId] = timeoutId;
    }
  }
  
  /**
   * returns a container with comment icon, that should be inserted
   * into editor / notebook as an indicator that there is a comment there
   *
   * @param {string} commentId
   * @param {string} containerElement tag of an element that should contain indicator icon
   * @param {string} className class name of an icon container
   * @returns {*}
   */
  getIconContainer(
    commentId: string,
    containerElement: string,
    className: string
  ) {
    const iconContainer = document.createElement(containerElement);
    iconContainer.className = className;
    iconContainer.dataset.commentId = commentId;
    iconContainer.onclick = (ev: MouseEvent) => {
      const target = ev.target as HTMLElement;
      const targetDiv = target.closest('[data-comment-id]') as HTMLElement;
      const commentId = targetDiv?.dataset.commentId;
      if (commentId) {
        this.focusComment(commentId);
      }
    };
    commentIcon.element({
      container: iconContainer
    });
    return iconContainer;
  }
  
  /** Rerenders cell comment icons on cell execution */
  subscribeToCellExecution() {
    const onExecutionCountChanged = (_: ICellModel, changed: IChangedArgs<any>): void => {
      if (changed.name === 'executionCount' && changed.newValue) {
        this.addCommentIconsToCells();
      }
    }
    this.notebookTracker.activeCellChanged.connect((_, newActiveCell) => {
      newActiveCell?.model.stateChanged.connect(onExecutionCountChanged);
    });
  }
  
  /**
   * If comments are linked to current notebook widget
   * add icons that indicate which cells were commented on
   */
  addCommentIconsToCells() {
    const className = 'jp-comments-cell-icon';
    const panel = this.notebookTracker.currentWidget?.content;
    if (!panel) {
      return;
    }
    const commentIds: { [key: string]: string } = {};
    this.state.comments.map(c => {
      const cellId = c.cell_id;
      const commentId = c.id;
      if (cellId && !c.parent_id && !c.resolved) {
        commentIds[cellId] = commentId;
      }
    });

    panel?.widgets.map(w => {
      w.node.querySelector('.' + className)?.remove();
      const cellId = w.model.id;
      if (cellId in commentIds) {
        // if icon already exists remove it
        const commentId = commentIds[cellId];
        const cell = w.node.querySelector('.jp-InputArea-prompt');
        const iconContainer = this.getIconContainer(
          commentId,
          'div',
          className
        );
        cell?.appendChild(iconContainer);
      }
    });
  }
  
  /**
   * If comments are linked to current editor widget
   * add icons that indicate which lines were commented on
   */
  addCommentIconsToEditorLines() {
    const className = 'jp-comments-editor-line-icon';
    const editorContainer = this.editorTracker.currentWidget?.content;
    const editor = editorContainer?.editor;
    if (!editor) {
      return;
    }

    const elements = editorContainer?.node.querySelectorAll('.' + className);
    // removes existing comment icons
    if (elements) {
      for (let i = 0; i < elements?.length; i++) {
        elements[i].remove();
      }
    }
    // places new icons
    const commentIds: { [key: number]: string[] } = {};
    this.state.comments.map(c => {
      const editorLine = c.editor_line;
      const editorLineText = c.editor_line_text;
      const commentId = c.id;
      if (!c.parent_id && !c.resolved) {
        commentIds[editorLine] = [commentId, editorLineText];
      }
    });
    Object.keys(commentIds).map(line => {
      const editorLine = Number(line);
      const commentId = commentIds[editorLine][0];
      const editorLineText = commentIds[editorLine][1];
      try {
        const offset = editor.getOffsetAt({ line: editorLine, column: 0 });
        const editorText = editor.getTokenAt(offset).value;
        if (editorLineText === editorText) {
          const editorLineEl = editorContainer.node.querySelectorAll(
            '.cm-lineNumbers .cm-gutterElement'
          )[editorLine + 1];
          const iconContainer = this.getIconContainer(
            commentId,
            'span',
            className
          );
          editorLineEl?.prepend(iconContainer);
        } else {
          //text at commentLine has changed, reset comment to line 0
        }
      } catch (ex) {
        if (ex instanceof RangeError) {
          // line doesn't exist anymore, delete comment?
        } else {
          throw ex;
        }
      }
    });
  }
  
  /**
   * extracts and sets username for current user, it defines new comment author as well
   * as which actions current user can perform on existing comments
   */
  setUsername() {
    requestAPI<any>('username', { method: 'GET' })
      .then(reply => {
        if (reply.error) {
          console.error(`Error on GET /username: ${reply.error}`);
        } else {
          this.state.username = reply.username;
          this.state.fullUsername = reply.full_username;
        }
      })
      .catch(reason => {
        console.log(reason.response);
        console.error(
          `Error on GET /jupyterhub-comments-server/username.\n${reason.message.error}`
        );
      });
  }
  
  /** Sets where user started jupyter, to resolve full path of files */
  setRootPath() {
    requestAPI<any>('resolve-path', {
      method: 'POST',
      body: JSON.stringify({'root_path' : PageConfig.getOption('serverRoot')})
    })
      .then(reply => {
        if (reply.error) {
          console.error(`Error on POST /resolve-path: ${reply.error}`);
        } else {
          this.state.rootPath = reply.resolved_path;
        }
      })
      .catch(reason => {
        console.log(reason.response);
        console.error(
          `Error on POST /jupyterhub-comments-server/resolve-path.\n${reason.message.error}`
        );
      });
  }
  
  /** loads comments for current widget, updates them in the interface */
  updateComments() {
    if (!this.state.filePath) {
      this.trySettingLocalPath();
    }
    const dataToSend = {
      file_path: this.state.filePath
    };
    requestAPI<any>('comments', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    })
      .then(reply => {
        if (reply.error) {
          console.error(`Error on POST /comments: ${reply.error}`);
          return [];
        } else {
          this.state.comments = reply.comments || [];
          this.update();
          setTimeout(() => {
            this.addCommentIconsToCells();
            this.addCommentIconsToEditorLines();
          }, 50);
        }
      })
      .catch(reason => {
        console.log(reason.response);
        console.error(
          `Error on POST /jupyterhub-comments-server/comments ${dataToSend}.\n${reason.message.error}`
        );
      });
  }

  render() {
    return (
      <Panel
        notebookTracker={this.notebookTracker}
        editorTracker={this.editorTracker}
        trans={this.trans}
        username={this.state.username}
        fullUsername={this.state.fullUsername}
        filePath={this.state.filePath}
        fileName={this.state.fileName}
        comments={this.state.comments}
        updateComments={this.updateComments}
      ></Panel>
    );
  }
}
