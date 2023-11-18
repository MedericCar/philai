import React, { useState } from 'react';
import Suggestion, { SuggestionProps } from './Suggestion';
import './Answer.css'

interface AnswerProps {
  content: string;
  suggestions: SuggestionProps[];
}

const Answer: React.FC<AnswerProps> = ({ content, suggestions }) => {
  return (
    <div className="answer">
      <div className="answer-container">
        <h1>Answer</h1>
        <p>{content}</p>
      </div>
      <div className="suggestions-container">
        {suggestions.map((suggestion, index) => (
          <Suggestion key={index} {...suggestion} />
        ))}
      </div>
    </div>
  );
};

export default Answer;