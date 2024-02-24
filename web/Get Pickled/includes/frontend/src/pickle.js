import React, { useState } from 'react';
import Header from "./Header";
import axios from 'axios';
import { backendURL } from './config/config';

const Pickle = () => {
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [results, setResults] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const nameRegex = /^[a-zA-Z]+$/;
    
    if (!nameRegex.test(name)) {
      setError('Name should not contain special characters');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('name', name);
      formData.append('key', '0');

      const response = await axios.post(
        `${backendURL}/form`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      
      setResults(response.data);
      setError('');
    } catch (error) {
      console.error('Error submitting form', error);
      alert('Failed to submit form. Please try again.');
    }
  };

  return (
    <div id='home-container'>
      <Header />
      <h1>Welcome to the Pickle Challenge</h1>
      <div>
        Find the pickled route (PS: I love hashed maps)
      </div>
      <div>
        This form displays various Countries and their Capitals or does it?
      </div>
      <form className="pickle-form" onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        {error && <div className="error-message">{error}</div>}
        <button type="submit" className="submit-button">Submit</button>
      </form>
      {results !== null && (
      <div className="results-container">
        <h2>Results:</h2>
        {results.length > 0 ? (
          <ul className="results-list">
            {results.map((result, index) => (
              <li key={index}>{result}</li>
            ))}
          </ul>
        ) : (
          <div className="results-list">[]</div>
        )}
      </div>
    )}
      <a href={process.env.PUBLIC_URL + '/server.txt'} download className='download-link'>
        Download source code
      </a>
    </div>
  );
};

export default Pickle;
