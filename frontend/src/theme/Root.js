import React from 'react';
import Chatbot from '../components/Chatbot';

// This component wraps the entire application
// Perfect place to add global components like the chatbot
export default function Root({ children }) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}
