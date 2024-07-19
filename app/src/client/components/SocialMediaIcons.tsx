import { DISCORD_URL, GITHUB_URL } from '../../shared/constants';

const SocialMediaIcons = () => {
  return (
    <div className='social-icons-wrapper flex'>
      <a
        href={`${DISCORD_URL}`}
        target='_blank'
        rel='noopener noreferrer'
        className='discord-link mx-2'
        aria-label='Discord Link'
      ></a>
      <a
        href={`${GITHUB_URL}`}
        target='_blank'
        rel='noopener noreferrer'
        className='github-link mx-1'
        aria-label='GitHub Link'
      ></a>
    </div>
  );
};

export default SocialMediaIcons;
