import { MouseEventHandler, ReactNode } from 'react';

interface ButtonProps {
  onClick: MouseEventHandler<HTMLButtonElement>;
  label?: string;
  theme?: 'light' | 'dark';
}

export default function Button({ onClick, label, theme = 'dark' }: ButtonProps) {
  const buttonBG = theme === 'dark' ? 'bg-airt-primary' : 'bg-airt-secondary';
  const buttonTextColor = theme === 'dark' ? 'text-airt-font-base' : 'bg-airt-primary';
  return (
    <button
      className={`rounded-md px-3.5 py-2.5 text-sm  ${buttonBG} ${buttonTextColor}   hover:bg-opacity-85 shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}
