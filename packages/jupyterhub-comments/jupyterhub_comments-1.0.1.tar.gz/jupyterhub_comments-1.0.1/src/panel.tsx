import React, { useState } from 'react';
import { INotebookTracker } from '@jupyterlab/notebook';
import { IEditorTracker } from '@jupyterlab/fileeditor';
import { TranslationBundle } from '@jupyterlab/translation';
import { CommentThread, ICommentType } from './comment';
import { AddCommentForm } from './add-comment-form';


/**
 * List of comment tuples, where first element is parent comment
 * and second one is any number of children comments
 *
 * @typedef {CommentTuple}
 */
type CommentTuple = [ICommentType, ICommentType[]];

/**
 * Element that shores whole comments widget interface, which consists of:
 * add new comment form, any number of comment threads
 *
 * @param {{
 *   notebookTracker: INotebookTracker;
 *   editorTracker: IEditorTracker;
 *   trans: TranslationBundle;
 *   username: string;
 *   fullUsername: string;
 *   filePath: string;
 *   fileName: string;
 *   comments: ICommentType[];
 *   updateComments: () => void;
 * }} param0
 * @param {INotebookTracker} param0.notebookTracker, object that tracks changes in notebooks
 * @param {IEditorTracker} param0.editorTracker, object that tracks changes in editors
 * @param {TranslationBundle} param0.trans, interface translation object
 * @param {string} param0.username, system username
 * @param {string} param0.fullUsername, real username
 * @param {string} param0.filePath, full path of currently openned file
 * @param {string} param0.fileName, name of currently openned file
 * @param {{}} param0.comments, list of comments liked to currently openned file
 * @param {() => void} param0.updateComments, function that pulls comments from db and rerenders interface
 * @returns {React.JSX.Element}
 */
export const Panel = ({
  notebookTracker,
  editorTracker,
  trans,
  username,
  fullUsername,
  filePath,
  fileName,
  comments,
  updateComments
} : {
  notebookTracker: INotebookTracker;
  editorTracker: IEditorTracker;
  trans: TranslationBundle;
  username: string;
  fullUsername: string;
  filePath: string;
  fileName: string;
  comments: ICommentType[];
  updateComments: () => void;
}): React.JSX.Element => {
  /**
   * if comment thread is resolved or not
   *
   * @type {boolean}
   */
  const [hideResolved, setHideResolved] = useState(true);
  
  /**
   * Iterates over plain comment list and groups them into a 
   * structure where there is parentComments and children 
   * comments linked to them
   *
   * @param {ICommentType[]} comments, list of comments
   * @returns {CommentTuple[]}
   */
  const groupCommentsIntoThreads = (
    comments: ICommentType[]
  ): CommentTuple[] => {
    const commentDict: { [id: string]: CommentTuple } = {};
    comments.map(comment => {
      if (!comment.parent_id) {
        commentDict[comment.id] = [comment, []];
      }
    });
    comments.map(comment => {
      if (comment.parent_id) {
        try {
          commentDict[comment.parent_id][1].push(comment);
        } catch (exception) {
          commentDict[comment.id] = [comment, []];
        }
      }
    });
    
    let commentTuples = Object.values(commentDict);
    // sort to show oldest comments first
    commentTuples = commentTuples.sort((a, b) => {
      return a[0].timestamp - b[0].timestamp;
    });
    // sort to show oldest replies first
    const sortedCommentTuples: CommentTuple[] = [];
    commentTuples.map(c => {
      sortedCommentTuples.push([
        c[0],
        c[1].sort((a, b) => {
          return a.timestamp - b.timestamp;
        })
      ]);
    });
    return sortedCommentTuples;
  };

  return (
    <div className="jp-comments-comments-container">
      <AddCommentForm
        notebookTracker={notebookTracker}
        editorTracker={editorTracker}
        trans={trans}
        username={username}
        fullUsername={fullUsername}
        filePath={filePath}
        fileName={fileName}
        updateComments={updateComments}
        hideResolved={hideResolved}
        setHideResolved={setHideResolved}
      />
      <div className="comments-block-container">
        {groupCommentsIntoThreads(comments).map(commentTuple => (
          <CommentThread
            key={commentTuple[0].id}
            notebookTracker={notebookTracker}
            editorTracker={editorTracker}
            trans={trans}
            parentComment={commentTuple[0]}
            childrenComments={commentTuple[1]}
            fullUsername={fullUsername}
            username={username}
            hideResolved={hideResolved}
            updateComments={updateComments}
          />
        ))}
      </div>
    </div>
  );
};
