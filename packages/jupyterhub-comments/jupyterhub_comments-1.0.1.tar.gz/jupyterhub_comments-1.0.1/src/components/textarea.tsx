import React, { useEffect, useRef } from 'react';
import '../../style/components.css';


/**
 * textarea element that is used in add/edit comment form
 *
 * @param {{
 *   text: string;
 *   setText: React.Dispatch<React.SetStateAction<string>>;
 *   isEditing?: boolean;
 *   placeholder?: string;
 *   disabled: boolean;
 *   setDisabled: (value: boolean) => void;
 *   handleSaveClick: () => void;
 *   handleCancelClick: () => void;
 * }} param0
 * @param {string} param0.text initial text of textarea
 * @param {React.Dispatch<React.SetStateAction<string>>} param0.setText function that sets text
 * @param {boolean} param0.isEditing should textarea be shown
 * @param {string} param0.placeholder placeholder parameter
 * @param {boolean} param0.disabled should adding comment be disabled (when text is empty)
 * @param {(value: boolean) => void} param0.setDisabled setter for disabled
 * @param {() => void} param0.handleSaveClick function that should be called on textarea on save button click
 * @param {() => void} param0.handleCancelClick function that should be called on textarea on cancel button click
 * @returns {React.JSX.Element}
 */
export const Textarea = ({
  text,
  setText,
  isEditing,
  placeholder,
  disabled,
  setDisabled,
  handleSaveClick,
  handleCancelClick
}: {
  text: string;
  setText: React.Dispatch<React.SetStateAction<string>>;
  isEditing?: boolean;
  placeholder?: string;
  disabled: boolean;
  setDisabled: (value: boolean) => void;
  handleSaveClick: () => void;
  handleCancelClick: () => void;
}): React.JSX.Element => {

  
  /**
   * a reference to textarea
   *
   * @type {*}
   */
  const textAreaRef = useRef<HTMLTextAreaElement>(null);  
  /**
   * A comment cam be added only if it is longer than minCommentLen
   *
   * @type {1}
   */
  const minCommentLen = 1;
  
  /**
   * Change height of a textarea based on real text height, adds/
   * removes new rows on new line insertions / deletions
   *
   * @param {HTMLTextAreaElement} textarea
   */
  const adjustTextAreaHeight = (textarea: HTMLTextAreaElement) => {
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  
  /**
   * On textarea text change update its height and check if add
   * button should be enabled
   *
   * @param {React.ChangeEvent<HTMLTextAreaElement>} event
   */
  const onChange = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
    const value = event.target.value;
    setText(value);
    setDisabled(value.trim().length < minCommentLen);
    adjustTextAreaHeight(event.target);
  };
  
  /**
   * adds \t into a comment on Tab press
   * saves a comment on ctrl+enter press
   *
   * @param {React.KeyboardEvent<HTMLTextAreaElement>} event
   */
  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ): void => {
    if (event.key === 'Tab') {
      event.preventDefault();
      const textarea = textAreaRef.current;
      if (!textarea) {
        return;
      }
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newText = text.substring(0, start) + '\t' + text.substring(end);
      setText(newText);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 1;
      }, 0);
    } 
    else if (event.ctrlKey && event.key === 'Enter') {
      if (!disabled) {
        handleSaveClick();
      }
    }
    else if (event.key === 'Escape'){
      handleCancelClick();
    }
  };

  /**
   * needed to initialize comment with correct height
   *
   * @param {React.KeyboardEvent<HTMLTextAreaElement>} event
   */
  useEffect(() => {
    if (textAreaRef.current) {
      adjustTextAreaHeight(textAreaRef.current);
      textAreaRef.current.focus();
    }
  }, [isEditing]);

  return (
    <textarea
      className="jp-comments-comments-textarea"
      placeholder={placeholder}
      ref={textAreaRef}
      value={text}
      rows={2}
      onChange={onChange}
      onKeyDown={handleKeyDown}
    ></textarea>
  );
};
