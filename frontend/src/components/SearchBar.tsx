import React, { useState } from 'react';
import './SearchBar.css';


interface SearchBarProps {
  onSend: (inputValue: string) => void;
}


const SearchBar: React.FC<SearchBarProps> = ({ onSend }) => {
  const [searchActive, setSearchActive] = useState(false);
  const [inputValue, setInputValue] = useState("");

  const handleSearchClick = () => {
    console.log("oooof")
    console.log(inputValue)
    setSearchActive(true);
    onSend(inputValue);
  };

  return (
    <div className={`search-container ${searchActive ? 'active' : ''}`}>
      <h1 className={`title ${searchActive ? 'fade-out' : ''}`}>Phil AI</h1>
      <div className="search-bar">
        <input 
          type="text"
          placeholder="What brings you to donate today?"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
        />
        <button className="search-btn" onClick={handleSearchClick}>
          <i className="fas fa-arrow-right"></i>
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
