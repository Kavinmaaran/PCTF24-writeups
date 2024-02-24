import React, { useEffect } from 'react';
import axios from 'axios';
import { backendURL } from './config/config';
const Home = () => {
  useEffect(() => {
    const fetchData = async () => {
      try {
        // const backendUrl = process.env.REACT_APP_BACKEND_URL;
        await axios.post(`${backendURL}/you_know_who`, { gift: 'gift?' }, {
          headers: { 'Content-Type': 'application/json' },
        });
        
      } catch (error) {
        console.error('Error fetching gift', error);
      }
    };
    fetchData();


    const createSnowflake = () => {
      const snowflake = document.createElement('div');
      snowflake.classList.add('snowflake');
      const topPosition = -5; 
      const leftPosition = Math.random() * window.innerWidth;
      snowflake.style.top = `${topPosition}px`;
      snowflake.style.left = `${leftPosition}px`;
      const animationDuration = Math.random() * 10 + 5; 
      snowflake.style.animationDuration = `${animationDuration}s`;
      document.getElementById('home-container').appendChild(snowflake);
    };

  
    for (let i = 0; i < 20; i++) {
      createSnowflake();
    }

    const snowfallInterval = setInterval(() => {
      createSnowflake();
    }, 2000);

    return () => clearInterval(snowfallInterval);
  }, []); 
  
  return (
    <div id='home-container'>
      <h1>Good way around, now find your gift</h1>
      <div>Merry XMas again</div>
      <p>Tim, who is also searching for his gift for his Secret Santa, finds a note lying on the floor, its content read,
      <br></br>
      <br></br>
      "XML, or eXtensible Markup Language, is a versatile and widely used markup language designed to store and transport data in a structured format. Its primary function is to facilitate the interchange of information between systems, making it a fundamental tool in web development, data representation, and configuration settings. It is widely used to transfer data across the web, but has its own flaws too, there are a lot of vulnerabilities in XML which hackers exploit to get access to the website."
      <br></br>
      <br></br>
      I think Tim is too dumb to understand this, but I guess you aren't.</p>
    </div>
  );
};

export default Home;
