import React, { useEffect } from 'react';
import Header from "./Header";
const Secure = () => {
    useEffect(() => {
        const createSnowflake = () => {
          const snowflake = document.createElement('div');
          snowflake.classList.add('snowflake');
          const topPosition = -5; 
          const leftPosition = Math.random() * window.innerWidth;
          snowflake.style.top = `${topPosition}px`;
          snowflake.style.left = `${leftPosition}px`;
          const animationDuration = Math.random() * 10 + 5; 
          snowflake.style.animationDuration = `${animationDuration}s`;
          document.getElementById('secure-container').appendChild(snowflake);
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
      <div id="secure-container">
        <div className="component">
            <Header />
            <h1 id="secure-title">Merry XMas</h1>
            <h3 id="secure-subtitle">The route to your secret santa lies with the bots</h3>
        </div>
        
      </div>
    );
  };
 
export default Secure;