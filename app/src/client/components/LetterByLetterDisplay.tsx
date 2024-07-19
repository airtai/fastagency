import React, { useState, useEffect } from 'react';
import Markdown from 'markdown-to-jsx';

// Define a type for the component props
interface LetterByLetterDisplayProps {
  sentence: string;
  speed?: number; // Mark speed as optional with a default value
  onStreamAnimationComplete?: () => void;
}

const LetterByLetterDisplay: React.FC<LetterByLetterDisplayProps> = ({
  sentence,
  speed = 100,
  onStreamAnimationComplete,
}) => {
  const [displayText, setDisplayText] = useState<string>('');

  useEffect(() => {
    if (displayText.length < sentence.length) {
      const timer = setTimeout(() => {
        setDisplayText((prev) => sentence.substring(0, prev.length + 1));
      }, speed);

      // Clean up the timeout to prevent memory leaks
      return () => clearTimeout(timer);
    } else if (onStreamAnimationComplete) {
      // Call the onStreamAnimationComplete function if it exists and the animation is complete
      onStreamAnimationComplete();
    }
    // Ensure to list all dependencies required for the effect
  }, [displayText, sentence, speed]);

  return <Markdown>{displayText}</Markdown>;
};

export default LetterByLetterDisplay;
