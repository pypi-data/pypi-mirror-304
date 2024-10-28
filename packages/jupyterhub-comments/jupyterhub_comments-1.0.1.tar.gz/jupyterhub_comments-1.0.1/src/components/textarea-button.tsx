import React from 'react';


/**
 * Button element that is used in add/edit comment form
 *
 * @param {{
 *   text: string;
 *   disabled?: boolean;
 *   onClick: () => void;
 * }} param0
 * @param {string} param0.text button text
 * @param {boolean} param0.disabled is button disabled
 * @param {() => void} param0.onClick function that should be called on button click
 * @returns {React.JSX.Element}
 */
export const TextAreaButton = ({
  text,
  disabled,
  onClick
}: {
  text: string;
  disabled?: boolean;
  onClick: () => void;
}): React.JSX.Element => {
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onClick();
  };

  return (
    <button
      className="jp-mod-styled jp-mod-reject jp-ArrayOperationsButton"
      onClick={handleClick}
      disabled={disabled}
      style={{
        cursor: 'pointer'
      }}
    >
      {text}
    </button>
  );
};
