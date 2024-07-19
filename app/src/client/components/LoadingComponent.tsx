const wrapperStyles = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '4rem',
};

const commonMessageStyles = {
  display: 'flex',
  alignItems: 'center',
  gap: '.5rem',
  borderRadius: '.5rem',
  padding: '1rem',
};

const MessageIcon = () => (
  <svg
    className='animate-spin -ml-1 mr-3 h-5 w-5 text-airt-font-base'
    xmlns='http://www.w3.org/2000/svg'
    fill='none'
    viewBox='0 0 24 24'
  >
    <circle className='opacity-25' cx='12' cy='12' r='10' stroke='currentColor' strokeWidth='4'></circle>
    <path
      className='opacity-75'
      fill='currentColor'
      d='M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z'
    ></path>
  </svg>
);

export default function LoadingComponent() {
  return (
    <div style={wrapperStyles}>
      <div className='text-airt-font-base' style={commonMessageStyles}>
        <div className='relative rounded-xl overflow-auto p-8'>
          <div className='flex items-center justify-center'>
            <button
              type='button'
              className='inline-flex items-center px-4 py-2 leading-6 text-sm shadow rounded-md transition ease-in-out duration-150 cursor-not-allowed border border-airt-font-base'
              disabled
            >
              <MessageIcon /> Loading...
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
