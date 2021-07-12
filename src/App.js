import React, { useState, useEffect } from 'react';
import logo from './pom_logo.png';
import './App.css';
import SentenceList from './SentenceList/SentenceList';
import { trackPromise } from 'react-promise-tracker';

function App() {
  const [value, setValue] = useState("الكُوبُ عَلَى الطَّاوِلَةِ");
  const [partsOfSpeech, setPartsOfSpeech] = useState([]);
  const url = '/api/pos';

  useEffect(() => {
    // clean value input i.e. remove special chars, emojis, hashtags, digits
    const config = {
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json;'
      }, 
      beforeSend: function(jqXHR) {
        jqXHR.overrideMimeType('text/html;charset=iso-8859-1');
      },
      method: 'POST',
      body: JSON.stringify(value)
    }

    trackPromise(
      fetch('/api/pos', config).then(res => res.json()).then(data => {
        console.log(data);
        setPartsOfSpeech(data);
      }).catch(console.error)
    );
    
  }, [value]);

  const handleChange = (e) => {
    setValue(e.target.value);
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo rotating" alt="logo" />
        <label>
          <p>Please enter your sentence:</p>
        </label>
        <textarea id="input-area" defaultValue={value} onChange={handleChange} 
          rows="4" cols="50" dir="auto" lang="ar" />
      </header>
      <div className="App">
        <SentenceList {...partsOfSpeech} />
      </div>
    </div>
  );
}

export default App;
