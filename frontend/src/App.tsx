import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css';

import Answer from './components/Answer';
import SearchBar from './components/SearchBar';
import { SuggestionProps } from './components/Suggestion';


function generateUniqueId() {
  return `id-${new Date().getTime()}-${Math.random().toString(36).substr(2, 9)}`;
}


const App: React.FC = () => {

  const [showContent, setShowContent] = useState(false);  
  const [answerContent, setAnswerContent] = useState("");
  const [answerSuggestions, setAnswerSuggestions] = useState<SuggestionProps[]>([]);
  
  const [uuid, setUuid] = useState('');
  useEffect(() => {
    // Generate a new UUID and set it in state
    const newUuid = generateUniqueId();
    setUuid(newUuid);
  }, []);


  const handleSearchActivate = async (inputValue: string) => {
    
    // Clear previous response
    setShowContent(false);
    setAnswerContent("");
    setAnswerSuggestions([]);

    console.log("Calling backend with:", inputValue);
    console.log(uuid)
    const response = await axios.post('http://localhost:8000/chat', { text: inputValue, chat_uuid: uuid });
    console.log(response)

    setAnswerContent(response.data.answer)
    setAnswerSuggestions(response.data.projects)
    setShowContent(true);
  }

  return (
    <div className="app-container">
      <SearchBar onSend={handleSearchActivate}/>
      {showContent && <Answer content={answerContent} suggestions={answerSuggestions}/>}
    </div>
  );
}

export default App;
