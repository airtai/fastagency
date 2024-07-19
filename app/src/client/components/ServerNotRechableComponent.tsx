import AnimatedCharacterLoader from './AnimatedCharacterLoader';

export default function ServerNotRechableComponent() {
  return (
    <div
      className='server-error-component sticky top-0 z-999 flex w-full justify-center bg-airt-secondary'
      style={{ zIndex: 99999 }}
      data-testid='server-error-component'
    >
      <AnimatedCharacterLoader
        loadingMessage={
          "Oops! Something went wrong. Our server is currently unavailable. Please do not refresh your browser. We're trying to reconnect..."
        }
        showLogo={false}
        bgColor='airt-secondary'
      />
    </div>
  );
}
