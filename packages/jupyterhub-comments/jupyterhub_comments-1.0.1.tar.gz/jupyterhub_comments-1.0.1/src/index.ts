import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILabShell
} from '@jupyterlab/application';
import { INotebookTracker } from '@jupyterlab/notebook';
import { IEditorTracker } from '@jupyterlab/fileeditor';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { CommentWidget } from './comment-widget';
import { ITranslator } from '@jupyterlab/translation'


/**
 * Entrypoint to an extension
 *
 * @type {JupyterFrontEndPlugin<void>}
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterhub-comments:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [
    ILabShell,
    IDocumentManager,
    INotebookTracker,
    IEditorTracker,
    ITranslator
  ],
  activate: (
    app: JupyterFrontEnd,
    labShell: ILabShell,
    docmanager: IDocumentManager,
    notebookTracker: INotebookTracker,
    editorTracker: IEditorTracker,
    translator: ITranslator
  ) => {
    const { shell } = app;
    const trans = translator.load('jupyterhub_comments');
    
    const commentWidget = new CommentWidget(
      labShell,
      docmanager,
      notebookTracker,
      editorTracker,
      trans
    );
    shell.add(commentWidget, 'right');
  }
};

export default plugin;
