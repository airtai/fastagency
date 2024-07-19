import React, { useState, useRef, useEffect, FormEvent } from 'react';
import { FaPencilAlt } from 'react-icons/fa';

interface EditableChatNameProps {
  chatId: number;
  chatName: string;
  onValueChange: (chatId: number, newValue: string) => void;
}

const EditableChatName: React.FC<EditableChatNameProps> = ({
  chatId,
  chatName,
  onValueChange,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [inputValue, setInputValue] = useState(chatName);

  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
    }
  }, [isEditing]);

  useEffect(() => {
    setInputValue(chatName);
  }, [chatName]);

  const handleIconClick = (event: React.MouseEvent) => {
    event.preventDefault();
    setIsEditing(true);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    onValueChange(chatId, inputValue);
    setIsEditing(false);
  };

  const handleBlur = () => {
    onValueChange(chatId, inputValue);
    setIsEditing(false);
  };

  return (
    <div className='editable-chat-name' style={{ width: '195px' }}>
      {!isEditing && (
        <span
          className='chat-name overflow-ellipsis overflow-hidden whitespace-nowrap'
          style={{ display: 'inherit' }}
        >
          {inputValue}
        </span>
      )}
      {isEditing && (
        <form onSubmit={handleSubmit} data-testid='edit-form'>
          <input
            ref={inputRef}
            type='text'
            onChange={handleInputChange}
            onBlur={handleBlur}
            value={inputValue}
            className='w-5/6 focus:outline-none focus:ring-0 focus:border-captn-light-blue bg-captn-light-cream text-captn-dark-blue'
            style={{
              height: '23px',
              paddingLeft: '5px',
              marginLeft: '-5px',
            }}
          />
        </form>
      )}
      {!isEditing && (
        <button
          className='edit-button absolute right-3 top-3 text-sm'
          onClick={handleIconClick}
          data-testid='edit-button'
        >
          <FaPencilAlt />
        </button>
      )}
    </div>
  );
};

export default EditableChatName;
