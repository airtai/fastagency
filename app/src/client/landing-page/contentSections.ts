import { GITHUB_URL, DISCORD_URL } from '../../shared/constants';
import daBoiAvatar from '../static/da-boi.png';
import avatarPlaceholder from '../static/avatar-placeholder.png';

export const navigation = [
  { name: 'Home', href: '/' },
  { name: 'Build', href: '/build' },
  { name: 'Playground', href: '/playground' },
  { name: 'Tutorial', href: '/tutorial' },
  { name: 'Pricing', href: '/pricing' },
  { name: 'Examples', href: '/examples' },
];
export const features = [
  {
    name: 'Build with Your Own APIs: Integrate Seamlessly with Custom Agent Design',
    description:
      'Integrate your existing systems seamlessly by defining agents with your own REST APIs. FastAgency allows you to craft bespoke agents tailored to your specific business processes, enabling a personalized approach to AI-driven solutions. This flexibility ensures that you can create highly specialized services that address unique challenges effectively.',
    icon: '⚙️', //'🤝',
    href: '',
  },
  {
    name: 'Set It and Forget It: Achieve Autonomous Operations with Minimal Oversight',
    description:
      'Our platform empowers your agents to operate autonomously, handling complex tasks and decision-making without constant human oversight. This feature not only enhances operational efficiency but also allows your team to focus on strategic activities, boosting productivity and innovation across the board.',
    icon: '🤖', //'🔐',
    href: '',
  },
  {
    name: 'Launch Faster Than Ever: Accelerate Time-to-Market with Rapid Deployment',
    description:
      "Accelerate your time-to-market with FastAgency's streamlined deployment process. Our framework is designed for speed, allowing you to move from concept to launch in record time. This rapid deployment capability ensures that you can quickly adapt to market changes and gain a competitive edge.",
    icon: '⚡',
    href: '',
  },
  {
    name: 'Start Collecting Revenue in Just a Week with Rapid Monetization',
    description:
      'Dive into the market swiftly with FastAgency. Our platform enables you to go from setup to sales within a week, allowing you to start generating revenue almost immediately. This rapid monetization feature is designed to give businesses a significant head start, accelerating the return on investment and enabling you to capitalize on AI-driven opportunities faster than ever.',
    icon: '💸',
    href: '',
  },
];
export const testimonials = [
  {
    name: 'Da Boi',
    role: 'Wasp Mascot',
    avatarSrc: daBoiAvatar,
    socialUrl: 'https://twitter.com/wasplang',
    quote: "I don't even know how to code. I'm just a plushie.",
  },
  {
    name: 'Mr. Foobar',
    role: 'Founder @ Cool Startup',
    avatarSrc: avatarPlaceholder,
    socialUrl: '',
    quote: 'This product makes me cooler than I already am.',
  },
  {
    name: 'Jamie',
    role: 'Happy Customer',
    avatarSrc: avatarPlaceholder,
    socialUrl: '#',
    quote: 'My cats love it!',
  },
];

export const faqs = [
  {
    id: 1,
    question: 'Whats the meaning of life?',
    answer: '42.',
    href: 'https://en.wikipedia.org/wiki/42_(number)',
  },
];
export const footerNavigation = {
  app: [
    { name: 'Discord', href: DISCORD_URL },
    { name: 'GitHub', href: GITHUB_URL },
    // { name: 'Blog', href: BLOG_URL },
  ],
  company: [
    { name: 'Privacy', href: '/privacy' },
    { name: 'Terms & Conditions', href: '/toc' },
  ],
};
