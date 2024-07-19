import React from 'react';

interface TextInputProps {
  id: string;
  type: string;
  value: string;
  placeholder: string;
  onChange: (value: string) => void;
}

export const TextInput: React.FC<TextInputProps> = ({ id, type, value, placeholder, onChange }) => (
  <input
    type={type}
    value={value}
    placeholder={placeholder}
    onChange={(e) => onChange(e.target.value)}
    className='my-2 p-2 border rounded w-full'
    id={id}
  />
);
