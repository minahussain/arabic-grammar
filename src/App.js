import React, { useState, useEffect } from 'react';
import logo from './pom_logo.png';
import './styles/main.scss';
import SentenceList from './components/SentenceList';
import { trackPromise } from 'react-promise-tracker';

async function fetchPartsOfSpeech(config) {
  const response = await fetch('/api/pos', config);

  if (!response.ok) {
    const message = `An error has occured: ${response.status}`;    
    throw new Error(message);  
  }
  const pos = await response.json();
  return pos;
}

function App() {
  const [value, setValue] = useState("الكُوبُ عَلَى الطَّاوِلَةِ")
  const [partsOfSpeech, setPartsOfSpeech] = useState([])
  const [err, setErr] = useState('')

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
      fetchPartsOfSpeech(config).then(data => {
        console.log(data);
        setPartsOfSpeech(data);
      }).catch(error => {
        console.warn(error.message); // 'An error has occurred: 404'
        setErr(error.message);
      })
    );
    
  }, [value]);

  const handleChange = (e) => {
    setValue(e.target.value);
    setPartsOfSpeech([])
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo rotating" alt="logo" />
        <label>
          <p>Input sentence below:</p>
        </label>
        <textarea id="input-area" defaultValue={value} onChange={handleChange} 
          rows="4" cols="50" dir="auto" lang="ar" />
      </header>
      <div className="App">
        { !err && <SentenceList {...partsOfSpeech} /> }
      </div>
    </div>
  );
}

export default App;
