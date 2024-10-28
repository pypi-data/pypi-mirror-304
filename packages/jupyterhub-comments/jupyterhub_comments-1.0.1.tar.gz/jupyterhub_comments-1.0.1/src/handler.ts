import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { v4 as uuidv4 } from 'uuid';


/**
 * Makes request to Jupyter Comments API
 *
 * @export
 * @async
 * @template T
 * @param {string} [endPoint=''] API endpoint
 * @param {RequestInit} [init={}]
 * @returns {Promise<T>}
 */
export async function requestAPI<T>(
  endPoint = '',
  init: RequestInit = {}
): Promise<T> {
  const settings = ServerConnection.makeSettings();
  const requestUrl = URLExt.join(
    settings.baseUrl,
    'jupyterhub-comments-server',
    endPoint
  );

  let response: Response;
  try {
    response = await ServerConnection.makeRequest(requestUrl, init, settings);
  } catch (error) {
    throw new ServerConnection.NetworkError(error as any);
  }

  let data: any = await response.text();

  if (data.length > 0) {
    try {
      data = JSON.parse(data);
    } catch (error) {
      console.log('Not a JSON response body.', response);
    }
  }

  if (!response.ok) {
    throw new ServerConnection.ResponseError(response, data.message || data);
  }

  return data;
}

/**
 * Function to send new comment data to the API and calls
 * a function that updates interface on a successfull call
 *
 * @param {string} commentId, id of a comment, '' if it is a new comment
 * @param {string} filePath, full path of a file that was commented on
 * @param {string} cellId, id of a cell if comment is linked to a notebook, '' otherwise
 * @param {number} editorLine, line number if comment is lined to an editor, '' otherwise
 * @param {string} editorLineText, text for the line commented in an editor, '' otherwise
 * @param {string} username, system username of user that created a comment
 * @param {string} text, comment text
 * @param {number} resolved, is comment resolved
 * @param {string} parentId, comment parentId if it is a reply, '' otherwise
 * @param {() => void} updateComments, function that pulls comments from db and rerenders inteface
 * @returns {void) => void}
 */
export const updateComment = (
  commentId: string,
  filePath: string,
  cellId: string,
  editorLine: number,
  editorLineText: string,
  username: string,
  text: string,
  resolved: number,
  parentId: string,
  updateComments: () => void
) => {
  const comment = {
    id: commentId ? commentId : uuidv4(),
    file_path: filePath,
    cell_id: cellId,
    editor_line: editorLine,
    editor_line_text: editorLineText,
    username: username,
    timestamp: Date.now(),
    text: text,
    resolved: resolved,
    parent_id: parentId
  };

  requestAPI<any>('comment', {
    body: JSON.stringify(comment),
    method: 'POST'
  })
    .then(reply => {
      if (reply.error) {
        console.error(`Error on POST /comment: ${reply.error}`);
      } else {
        updateComments();
      }
    })
    .catch(reason => {
      console.error(
        `Error on POST /jupyterhub-comments-server/comment ${comment}.\n${reason.message.error}`
      );
    });
};
