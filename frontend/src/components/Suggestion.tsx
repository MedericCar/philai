import React from 'react';
import './Suggestion.css';

export interface SuggestionProps {
  title: string;
  country: string;
  themeName: string;
  summary: string;
  imageLink: string;
}

const Suggestion: React.FC<SuggestionProps> = ({ title, country, themeName, summary, imageLink }) => {
  const style = {
    backgroundImage: `url(${imageLink})`
  };

  return (
    <div className="suggestion" style={style}>
      <div className="suggestion-text">
        <p className="suggestion-location">{country}</p>
        <h3 className="suggestion-title">{title}</h3>
      </div>
    </div>
  );
};

export default Suggestion;
