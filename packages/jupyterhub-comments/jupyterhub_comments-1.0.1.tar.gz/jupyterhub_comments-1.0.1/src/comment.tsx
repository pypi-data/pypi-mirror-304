import React, { useState, useRef, useEffect } from 'react';
import { INotebookTracker } from '@jupyterlab/notebook';
import { PageConfig } from '@jupyterlab/coreutils';
import { TranslationBundle } from '@jupyterlab/translation';
import { IEditorTracker } from '@jupyterlab/fileeditor';
import {
  undoIcon,
  ellipsesIcon,
  ToolbarButtonComponent,
  LabIcon
} from '@jupyterlab/ui-components';
import Markdown from 'markdown-to-jsx';
import { requestAPI, updateComment } from './handler';
import { TextAreaButton } from './components/textarea-button';
import { Textarea } from './components/textarea';
import '../style/comment.css';


/**
 * Type defining comment fields
 *
 * @export
 * @interface ICommentType
 * @typedef {ICommentType}
 */
export interface ICommentType {
  id: string;
  file_path: string;
  cell_id: string;
  editor_line: number;
  editor_line_text: string;
  username: string;
  full_username: string;
  text: string;
  timestamp: number;
  updated_timestamp: number;
  resolved: number;
  parent_id: string;
  file_owner: string;
}

/**
 * delete a comment by specified id and then call `updateComments`
 * function to reflect changes in an interface
 *
 * @param {TranslationBundle} trans translation object
 * @param {string} commentId commentId that should be deleted
 * @param {() => void} updateComments function that pulls comments from
 * the database and rerenders interface
 * @returns {void) => void}
 */
const deleteComment = (
  trans: TranslationBundle,
  commentId: string,
  updateComments: () => void
) => {
  if (window.confirm(trans.__('Delete comment?'))){
    requestAPI<any>('comment', {
      method: 'DELETE',
      body: JSON.stringify({ id: commentId })
    })
      .then(reply => {
        if (reply.error) {
          console.error(`Error on DELETE /comment: ${reply.error}`);
        } else {
          updateComments();
        }
      })
      .catch(reason => {
        console.error(
          `Error on DELETE /comment ${commentId}.\n${reason.message}`,
          reason
        );
      });
  }
};

/**
 * Element that tandles updating selected comment text
 *
 * @param {{
 *   trans: TranslationBundle;
 *   text: string;
 *   isEditing: boolean;
 *   editedText: string;
 *   setEditedText: React.Dispatch<React.SetStateAction<string>>;
 *   handleCancelClick: () => void;
 *   handleSaveClick: () => void;
 * }} param0
 * @param {TranslationBundle} param0.trans, translation object
 * @param {string} param0.text, current comment text
 * @param {boolean} param0.isEditing, should text area form be displayed
 * @param {string} param0.editedText, text that user entered into a textarea
 * @param {React.Dispatch<React.SetStateAction<string>>} param0.setEditedText, setter to editedText
 * @param {() => void} param0.handleCancelClick, we should hide textarea and reset editedText on cancel click
 * @param {() => void} param0.handleSaveClick, we should hide textarea and reset editedText, as well as
 * saving updated comment and rerendering interface on save click
 * @returns {React.JSX.Element}
 */
const CommentTextArea = ({
  trans,
  text,
  isEditing,
  editedText,
  setEditedText,
  handleCancelClick,
  handleSaveClick
}: {
  trans: TranslationBundle;
  text: string;
  isEditing: boolean;
  editedText: string;
  setEditedText: React.Dispatch<React.SetStateAction<string>>;
  handleCancelClick: () => void;
  handleSaveClick: () => void;
}): React.JSX.Element => {
  /**
   * should save button be disabled
   *
   * @type {boolean}
   */
  const [disabled, setDisabled] = useState(true);
  
  return isEditing ? (
    <>
      <Textarea
        text={editedText}
        placeholder={trans.__('Comment')}
        setText={setEditedText}
        disabled={disabled}
        setDisabled={setDisabled}
        handleSaveClick={handleSaveClick}
        handleCancelClick={handleCancelClick}
      />
      <div className="jp-comments-jp-comments-comment-buttons">
        <TextAreaButton text={trans.__('Cancel')} onClick={handleCancelClick} />
        <TextAreaButton
          text={trans.__('Save')}
          disabled={disabled}
          onClick={handleSaveClick}
        />
      </div>
    </>
  ) : (
    <div className="jp-comments-comment-text">
      <Markdown
        options={{
          overrides: {
            a: {
              component: ({ href, children }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: '#007bff', textDecoration: 'underline' }}
                >
                  {children}
                </a>
              )
            },
            code: {
              component: ({ children, ...props}) => (
                <code
                  style={{
                    whiteSpace: 'pre-wrap'
                  }}
                  {...props}
                >
                  {children}
                </code>
              )
            }
          }
        }}
      >
        {text}
      </Markdown>
    </div>
  )
};

/**
 * Element that defines a comment thread, which has parentComment
 * and any number of children comments
 *
 * @param {{
 *   notebookTracker: INotebookTracker;
 *   editorTracker: IEditorTracker;
 *   trans: TranslationBundle;
 *   parentComment: ICommentType;
 *   childrenComments: ICommentType[];
 *   fullUsername: string;
 *   username: string;
 *   hideResolved: boolean;
 *   updateComments: () => void;
 * }} param0
 * @param {INotebookTracker} param0.notebookTracker, object that tracks changes in notebooks
 * @param {IEditorTracker} param0.editorTracker, object that tracks changes in editors
 * @param {TranslationBundle} param0.trans, translation object
 * @param {ICommentType} param0.parentComment, comment that thread is based on
 * @param {{}} param0.childrenComments, comment that are replies to parentComment
 * @param {string} param0.fullUsername, real name of a user
 * @param {string} param0.username, system username of user interacting with jupyter
 * @param {boolean} param0.hideResolved, if resolved parentComments should be hidden
 * @param {() => void} param0.updateComments, function to pull comments and rerender inteface
 * @returns {React.JSX.Element}
 */
export const CommentThread = ({
  notebookTracker,
  editorTracker,
  trans,
  parentComment,
  childrenComments,
  fullUsername,
  username,
  hideResolved,
  updateComments
}: {
  notebookTracker: INotebookTracker;
  editorTracker: IEditorTracker;
  trans: TranslationBundle;
  parentComment: ICommentType;
  childrenComments: ICommentType[];
  fullUsername: string;
  username: string;
  hideResolved: boolean;
  updateComments: () => void;
}): React.JSX.Element => {
  /**
   * textarea value when replying to thread
   *
   * @type {string}
   */
  const [text, setText] = useState('');
  
  /**
   * is reply form visible
   *
   * @type {boolean}
   */
  const [visible, setVisible] = useState(false);
  
  /**
   * is add comment button in reply form disabled
   *
   * @type {boolean}
   */
  const [disabled, setDisabled] = useState(true);
  
  /**
   * uncovers interface to change comment text prevents propagation
   * in order to stop comment highlighting (which is undesirable on
   * actions that interact with interface buttons)
   *
   * @param {React.MouseEvent<HTMLDivElement>} event
   */
  const handleReplyClick = (event: React.MouseEvent<HTMLDivElement>): void => {
    setVisible(!visible);
    setDisabled(true);
    event.stopPropagation();
  };
  
  /**
   * needed to pass somethin to child comments reply function which
   * does not exist, since replies are added to parent comments
   *
   * @param {React.MouseEvent<HTMLDivElement>} event
   */
  const dummyTextClick = (event: React.MouseEvent<HTMLDivElement>): void => {
  };
  
  /** creates new comment in reply to parentOne */
  const handleAddCommentClick = () => {
    updateComment(
      '', parentComment.file_path, parentComment.cell_id, parentComment.editor_line,
      parentComment.editor_line_text, username, text, 0, parentComment.id,
      updateComments
    );
    setText('');
    setDisabled(true);
    setVisible(false);
  };
  
  /** cancel replying to parentComment */
  const handleCancelButtonClick = () => {
    setText('');
    setVisible(false);
  };
  
  /**
   * hightlights comment in notebook / editor interface on click
   * in any uninteractable area of a comment
   *
   * @param {React.MouseEvent<HTMLDivElement>} event
   */
  const handleThreadClick = (event: React.MouseEvent<HTMLDivElement>) => {
    // prevent function call when user clicks on interactable elements
    const elementTag = (event.target as HTMLElement).tagName.toLowerCase();
    if (['button', 'textarea'].indexOf(elementTag) < 0) {
      handleThreadLinkedToCellClick(event);
      handleThreadLinkedToLineClick(event);
    }
  };
  
  /**
   * If a comment is linked to a cell, on click event focus that cell
   * and scroll to it
   *
   * @param {React.MouseEvent<HTMLDivElement>} event
   */
  const handleThreadLinkedToCellClick = (
    event: React.MouseEvent<HTMLDivElement>
  ) => {
    const cell_id = parentComment.cell_id;
    if (!cell_id) {
      return;
    }
    const panel = notebookTracker.currentWidget?.content;
    let found = false;
    panel?.widgets.map(w => {
      if (w.model.id === cell_id) {
        found = true;
        if (cell_id !== panel.activeCell?.model.id) {
          w.node.scrollIntoView({ behavior: 'smooth', block: 'start' });
          w.editor?.focus();
        }
      }
    });
    if (!found) {
      // couldn't find comment cell, delete comment?
    }
  };
  
  /**
   * If a comment is linked to a cell, on click event focus
   * that cell and scroll to it
   *
   * @param {React.MouseEvent<HTMLDivElement>} event
   */
  const handleThreadLinkedToLineClick = (
    event: React.MouseEvent<HTMLDivElement>
  ) => {
    const editorLine = parentComment.editor_line;
    const editor = editorTracker.currentWidget?.content.editor;
    if (editor) {
      editor.focus();
      const line = editor.getLine(editorLine);
      if (!line) {
        // line not found in the document, delete comment?
        return;
      }
      editor.setCursorPosition({
        line: editorLine,
        column: 0
      });
      editor.setSelection({
        start: { line: editorLine, column: 0 },
        end: { line: editorLine, column: line.length }
      });
    }
  };

  if (hideResolved && parentComment.resolved) {
    return <></>;
  } else {
    return (
      <div
        className="jp-comments-thread-container"
        data-comment-id={parentComment.id}
      >
        <div onClick={handleThreadClick}>
          <Comment
            trans={trans}
            comment={parentComment}
            currentUsername={username}
            updateComments={updateComments}
            handleReplyClick={event => handleReplyClick(event)}
          ></Comment>
          {childrenComments.map(comment => (
            <Comment
              key={comment.id}
              trans={trans}
              comment={comment}
              currentUsername={username}
              updateComments={updateComments}
              handleReplyClick={event => dummyTextClick(event)}
            ></Comment>
          ))}
        </div>
        {visible && (
          <div>
            <Textarea
              text={text}
              placeholder={trans.__('Reply')}
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
        )}
      </div>
    );
  }
};


/**
 * Element that represents a single comment either parent or child one
 *
 * @param {{
 *   trans: TranslationBundle;
 *   comment: ICommentType;
 *   currentUsername: string;
 *   updateComments: () => void;
 *   handleReplyClick: (event: React.MouseEvent<HTMLDivElement>) => void;
 * }} param0
 * @param {TranslationBundle} param0.trans, translation object
 * @param {ICommentType} param0.comment, comment object
 * @param {string} param0.currentUsername, username of a user that started jupyter
 * @param {() => void} param0.updateComments, function to pull comments and rerender inteface
 * @param {(event: React.MouseEvent<HTMLDivElement>) => void} param0.handleReplyClick, function
 * that shows add comment form when reply button is clicked on parent comment
 * @returns {JSX.Element}
 */
export const Comment = ({
  trans,
  comment,
  currentUsername,
  updateComments,
  handleReplyClick
}: {
  trans: TranslationBundle;
  comment: ICommentType;
  currentUsername: string;
  updateComments: () => void;
  handleReplyClick: (event: React.MouseEvent<HTMLDivElement>) => void;
}): JSX.Element => {
  /**
   * are we editing current comment text
   *
   * @type {boolean}
   */
  const [isEditing, setIsEditing] = useState(false);
  
  /**
   * edited comment text
   *
   * @type {string}
   */
  const [editedText, setEditedText] = useState(comment.text);
  
  /**
   * is comment context menu with edit/delete and so on visible
   *
   * @type {boolean}
   */
  const [menuVisible, setMenuVisible] = useState(false);
  
  /**
   * reference to context menu element, needed to check
   * if user clicked outside of it
   *
   * @type {*}
   */
  const menuRef = useRef<HTMLDivElement>(null);
  
  /**
   * reference to particular button of a context menu,
   * needed to check if user clicked it
   *
   * @type {*}
   */
  const contextMenuButtonRef = useRef<HTMLDivElement>(null);
  
  /**
   * should edit button be shown to user based on wheather current
   * user created the comment
   *
   * @type {boolean}
   */
  const editDisabled = comment.username !== currentUsername;

  
  /**
   * takes date timestamp and formats in as 'yyyy-MM-dd HH:mm'
   *
   * @param {number} timestamp
   * @returns {string}
   */
  const getFormattedDate = (timestamp: number): string => {
    const dateTime = new Date(timestamp);
    const {year, month, day, hour, minute} = {
      year: dateTime.getFullYear(),
      month: dateTime.getMonth(),
      day: dateTime.getDate(),
      hour: dateTime.getHours(),
      minute: dateTime.getMinutes()
    };
    const formattedDate = (
      year.toString()
      + '-'
      + (month >= 10 ? month.toString() : '0' + month)
      + '-'
      + (day >= 10 ? day.toString() : '0' + day)
      + ', '
      + (hour >= 10 ? hour.toString() : '0' + hour)
      + ':'
      + (minute >= 10 ? minute.toString() : '0' + minute)
    );
    return formattedDate;
  }
  
  /**
   * show / hide context menu upon button press
   *
   * @param {React.MouseEvent<HTMLDivElement>} event
   */
  const handleContextMenuToggle = (event: React.MouseEvent<HTMLDivElement>) => {
    setMenuVisible(!menuVisible);
    event.stopPropagation();
  };

  /**
   * needed to listen for clicks outside of context menu
   */
  useEffect(() => {
    /**
     * hides context menu when user clicks outside of menu area
     *
     * @param {MouseEvent} event
     */
    const handleClickOutside = (event: MouseEvent) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target as Node) &&
        contextMenuButtonRef.current &&
        !contextMenuButtonRef.current.contains(event.target as Node)
      ) {
        setMenuVisible(false);
      }
    };

    document.addEventListener('click', handleClickOutside, true);
    return () => {
      document.removeEventListener('click', handleClickOutside, true);
    };
  }, []);
  
  /** start comment editing */
  const handleEditClick = () => {
    setIsEditing(true);
    setEditedText(comment.text);
    setMenuVisible(false);
  };
  
  /** cancel comment text editing */
  const handleCancelClick = () => {
    setIsEditing(false);
    setMenuVisible(false);
    setEditedText(comment.text);
  };
  
  /** save a comment that was edited */
  const handleSaveClick = () => {
    if (comment.text !== editedText) {
      updateComment(
        comment.id, comment.file_path, comment.cell_id, comment.editor_line,
        comment.editor_line_text, comment.username, editedText, comment.resolved,
        comment.parent_id, updateComments
      );
    }
    setIsEditing(false);
    setMenuVisible(false);
  };
  
  /**
   * on delete button click show a menu to confirm an
   * action an delete comment if user agrees to it
   * 
   */
  const handleDeleteClick = () => {
    setIsEditing(false);
    deleteComment(trans, comment.id, updateComments);
    setMenuVisible(false);
  };
  
  /**
   * copies a direct link to a particular comment into clipboard
   */
  const handleCopyShareableLinkClick = () => {
    setMenuVisible(false);
    const baseUrl = PageConfig.getTreeShareUrl();
    const shareableLink =
      baseUrl + '/' + comment.file_path + '?comment-id=' + comment.id;
    navigator.clipboard.writeText(shareableLink);
  };

  
  /**
   * updates a comment when it was resolved / unresolved
   *
   * @param {number} newResolvedState
   */
  const handleResolveClick = (newResolvedState: number) => {
    updateComment(
      comment.id, comment.file_path, comment.cell_id, comment.editor_line,
      comment.editor_line_text, comment.username, comment.text, newResolvedState,
      comment.parent_id, updateComments
    );
    setIsEditing(false);
    setMenuVisible(false);
  };

  return (
    <div className="jp-comments-comment-container">
      <div className="jp-comments-comment-header">
        <div>
          <div className="jp-comments-comment-username">
            {comment.full_username ? comment.full_username : comment.username}
          </div>
          <div className="jp-comments-comment-timestamp">{getFormattedDate(comment.timestamp)}</div>
        </div>
        <div>
          {!comment.parent_id && (
            <>
              <IconWithTooltip
                tooltip={trans.__('Reply')}
                icon={undoIcon}
                contextMenuButtonRef={contextMenuButtonRef}
                onClick={event => handleReplyClick(event)}
              />
            </>
          )}
          <IconWithTooltip
            tooltip={trans.__('More')}
            icon={ellipsesIcon}
            contextMenuButtonRef={contextMenuButtonRef}
            onClick={event => handleContextMenuToggle(event)}
          />
        </div>
        {menuVisible && (
          <div
            ref={menuRef}
            className="jp-comments-comment-context-menu-container"
          >
            {!editDisabled && (
              <button
                onClick={handleEditClick}
                className="jp-comments-comment-context-menu-item"
              >
                {trans.__('Edit')}
              </button>
            )}
            {!editDisabled && (
              <button
                onClick={handleDeleteClick}
                className="jp-comments-comment-context-menu-item"
              >
                {trans.__('Delete')}
              </button>
            )}
            {!editDisabled && (
              <button
                style={{
                  display: 'none'
                }}
                onClick={handleCopyShareableLinkClick}
                className="jp-comments-comment-context-menu-item"
              >
                {trans.__('Copy link')}
              </button>
            )}
            {!comment.parent_id && (
              <button
                onClick={() =>
                  handleResolveClick(comment.resolved === 0 ? 1 : 0)
                }
                className="jp-comments-comment-context-menu-item"
              >
                {comment.resolved === 0
                  ? trans.__('Mark as resolved')
                  : trans.__('Re-open')}
              </button>
            )}
          </div>
        )}
      </div>
      <CommentTextArea
        trans={trans}
        text={comment.text}
        isEditing={isEditing}
        editedText={editedText}
        setEditedText={setEditedText}
        handleCancelClick={handleCancelClick}
        handleSaveClick={handleSaveClick}
      ></CommentTextArea>
    </div>
  );
};


/**
 * Element that stores jupyterlab icon and its tooltip
 *
 * @param {{
 *   tooltip: string;
 *   icon: LabIcon;
 *   contextMenuButtonRef: React.RefObject<HTMLDivElement>;
 *   onClick: (event: React.MouseEvent<HTMLDivElement>) => void;
 * }} param0
 * @param {string} param0.tooltip, text that is shown on icon hover
 * @param {LabIcon} param0.icon, icon object that should be displayed
 * @param {React.RefObject<HTMLDivElement>} param0.contextMenuButtonRef, ref to context menu
 * since clicking on it should not trigger comment focusing
 * @param {(event: React.MouseEvent<HTMLDivElement>) => void} param0.onClick, function that
 * focuses a comment on icon click
 * @returns {React.JSX.Element}
 */
const IconWithTooltip = ({
  tooltip,
  icon,
  contextMenuButtonRef,
  onClick
}: {
  tooltip: string;
  icon: LabIcon;
  contextMenuButtonRef: React.RefObject<HTMLDivElement>;
  onClick: (event: React.MouseEvent<HTMLDivElement>) => void;
}): React.JSX.Element => {
  return (
    <div
      className="jp-comments-comment-context-menu-element-container"
      onClick={event => onClick(event)}
      ref={contextMenuButtonRef}
      title={tooltip}
    >
      <ToolbarButtonComponent icon={icon} />
    </div>
  );
};
