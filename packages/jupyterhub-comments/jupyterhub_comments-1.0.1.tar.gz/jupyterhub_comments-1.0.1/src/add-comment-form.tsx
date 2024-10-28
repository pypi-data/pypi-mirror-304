import React, { useState } from 'react';
import {
  notebookIcon,
  markdownIcon,
  pythonIcon,
  jsonIcon,
  spreadsheetIcon,
  yamlIcon,
  textEditorIcon,
  html5Icon,
  imageIcon,
  fileIcon,
  pdfIcon
} from '@jupyterlab/ui-components';
import { INotebookTracker } from '@jupyterlab/notebook';
import { IEditorTracker } from '@jupyterlab/fileeditor';
import { TranslationBundle } from '@jupyterlab/translation';
import { updateComment } from './handler';
import { TextAreaButton } from './components/textarea-button';
import { Textarea } from './components/textarea';
import '../style/add-comment-form.css';

/**
 * Menu that displays header of widget, filter and sorting menus
 * and a form to add new comments
 *
 * @param {{
 *   notebookTracker: INotebookTracker;
 *   editorTracker: IEditorTracker;
 *   trans: TranslationBundle;
 *   username: string;
 *   fullUsername: string;
 *   filePath: string;
 *   fileName: string;
 *   updateComments: VoidFunction;
 *   hideResolved: boolean;
 *   setHideResolved: (hideResolved: boolean) => void;
 * }} param0
 * @param {INotebookTracker} param0.notebookTracker an object that tracks notebook events
 * @param {IEditorTracker} param0.editorTracker an object that thacks editor events
 * @param {TranslationBundle} param0.trans translation object
 * @param {string} param0.username username of a user that is currently using jupyter
 * @param {string} param0.fullUsername real username
 * @param {string} param0.filePath full file path to the currently openned file
 * @param {string} param0.fileName name of currenly oppened file
 * @param {VoidFunction} param0.updateComments function that rerenders comments
 * @param {boolean} param0.hideResolved an option that definces if resolved comments should be shown
 * @param {(hideResolved: boolean) => void} param0.setHideResolved a setter for hideResolved
 * @returns {React.JSX.Element}
 */
export const AddCommentForm = ({
  notebookTracker,
  editorTracker,
  trans,
  username,
  fullUsername,
  filePath,
  fileName,
  updateComments,
  hideResolved,
  setHideResolved
}: {
  notebookTracker: INotebookTracker;
  editorTracker: IEditorTracker;
  trans: TranslationBundle;
  username: string;
  fullUsername: string;
  filePath: string;
  fileName: string;
  updateComments: VoidFunction;
  hideResolved: boolean;
  setHideResolved: (hideResolved: boolean) => void;
}): React.JSX.Element => {
  /**
   * is add comment button disabled
   *
   * @type {*}
   */
  const [disabled, setDisabled] = useState(true);
  /**
   * is add comment block visible
   *
   * @type {*}
   */
  const [visible, setVisible] = useState(false);
  /**
   * // text in add comment textarea
   *
   * @type {*}
   */
  const [text, setText] = useState('');
  /**
   * should we show a button that unravels add comment form
   *
   * @type {boolean}
   */
  const showForm = filePath !== '';

  /**
   * Decide what jupyter icon should be shown based on currently
   * oppened file
   *
   * @returns {JSX.Element}
   */
  const chooseFileIcon = (): JSX.Element => {
    switch (fileName.split('.').splice(-1)[0]) {
      case 'ipynb':
        return (
          <notebookIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'md':
        return (
          <markdownIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'py':
        return (
          <pythonIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'json':
        return (
          <jsonIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'csv':
        return (
          <spreadsheetIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'xlsx':
        return (
          <spreadsheetIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'xls':
        return (
          <spreadsheetIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'yaml':
        return (
          <yamlIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'yml':
        return (
          <yamlIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'txt':
        return (
          <textEditorIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'html':
        return (
          <html5Icon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'png':
        return (
          <imageIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'jpg':
        return (
          <imageIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'jpeg':
        return (
          <imageIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'git':
        return (
          <imageIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      case 'pdf':
        return (
          <pdfIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
      default:
        return (
          <fileIcon.react className="jp-comments-add-comment-form-file-icon" />
        );
    }
  };

  /**
   * Try getting cellId of currently selected cell
   * in a notebook. If no cell is active returns ''
   *
   * @returns {*}
   */
  const getCurrentCellId = () => {
    const panel = notebookTracker.currentWidget?.content;
    const activeCellId = panel?.activeCell?.model.id;
    return activeCellId ? activeCellId : '';
  };

  /**
   * If current widget is an editor, extracts currenly
   * selected line and its text, otherwise returns '' and 0
   *
   * @returns {{
   *     editorLine: number;
   *     editorLineText: string;
   *   }}
   */
  const getCurrentEditorSelection = (): {
    editorLine: number;
    editorLineText: string;
  } => {
    const editor = editorTracker.currentWidget?.content.editor;
    if (editor) {
      const selection = editor.getSelection();
      if (selection) {
        const offset = editor.getOffsetAt({
          line: selection?.start.line,
          column: 0
        });
        const editorText = editor.getTokenAt(offset)?.value;
        const editorLine = selection.start.line;
        return {
          editorLine: editorLine,
          editorLineText: editorText
        };
      }
    }
    return {
      editorLine: 0,
      editorLineText: ''
    };
  };

  
  /** When add comment button is clicked show add comment form */
  const handlePlusButtonClick = () => {
    setVisible(true);
  };

  
  /** When cancel button is clicked, hide add comment form and reset its text */
  const handleCancelButtonClick = () => {
    setText('');
    setVisible(false);
  };

  /** When hide resolved checkbox in toggled hide/show resolved comments */
  const handleHideResolvedChanged = () => {
    setHideResolved(!hideResolved);
  };

  /** Adds a comment for selected notebook cell/editor line */
  const handleAddCommentClick = () => {
    const { editorLine, editorLineText } = getCurrentEditorSelection();
    const cellId = getCurrentCellId();
    updateComment(
      '', filePath, cellId, editorLine, editorLineText,
      username, text, 0, '', updateComments
    );
    setText('');
    setDisabled(true);
    setVisible(false);
  };

  if (showForm) {
    return (
      <>
        <div className="jp-comments-add-comment-form-header-container">
          <div className="jp-comments-add-comment-form-file-name-container">
            {chooseFileIcon()}
            {fileName}
          </div>
          <div className="checkbox">
            <label>
              <input
                type="checkbox"
                checked={hideResolved}
                onChange={handleHideResolvedChanged}
              ></input>
              <span>{trans.__('Hide resolved')}</span>
            </label>
          </div>
        </div>
        {visible ? (
          <div className="jp-comments-add-comment-form-container">
            <div className="jp-comments-add-comment-form-username">
              {fullUsername ? fullUsername : username}
            </div>
            <Textarea
              text={text}
              placeholder={trans.__('Comment')}
              setText={setText}
              disabled={disabled}
              setDisabled={setDisabled}
              handleSaveClick={handleAddCommentClick}
              handleCancelClick={handleCancelButtonClick}
            />
            <div className="jp-comments-jp-comments-add-comment-form-button-container">
              <TextAreaButton text={trans.__('Cancel')} onClick={handleCancelButtonClick} />
              <TextAreaButton
                text={trans.__('Add')}
                disabled={disabled}
                onClick={handleAddCommentClick}
              />
            </div>
          </div>
        ) : (
          <div className="jp-comments-show-comment-form-button-container">
            <TextAreaButton
              text={trans.__('Add comment')}
              onClick={handlePlusButtonClick}
            />
          </div>
        )}
      </>
    );
  } else {
    return (
      <div className="jp-comments-cannot-add-comment-block">
        {trans.__('Comments are added to selected notebooks / files')}
      </div>
    );
  }
};
