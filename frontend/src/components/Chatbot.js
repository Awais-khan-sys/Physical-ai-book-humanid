import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hi! I\'m your Physical AI textbook assistant. Ask me anything about humanoid robotics, perception systems, control theory, or AI learning!'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Get selected text from the page (if any)
      const selectedText = window.getSelection().toString();

      // Call backend API
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userMessage,
          selected_text: selectedText || null,
          conversation_history: messages.slice(-6) // Last 6 messages for context
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get response from server');
      }

      const data = await response.json();

      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources
      }]);

    } catch (error) {
      console.error('Error querying chatbot:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Sorry, I encountered an error. Please make sure the backend server is running and try again.',
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Floating chat button */}
      <button
        className="chatbot-button"
        onClick={toggleChat}
        aria-label="Toggle chatbot"
        title="Ask me about Physical AI"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat modal */}
      <div className={`chatbot-modal ${isOpen ? 'open' : ''}`}>
        {/* Header */}
        <div className="chatbot-header">
          <div className="chatbot-header-content">
            <div className="chatbot-avatar">🤖</div>
            <div className="chatbot-header-text">
              <h3>AI Tutor</h3>
              <p>Physical AI Expert</p>
            </div>
          </div>
          <button
            className="chatbot-close"
            onClick={toggleChat}
            aria-label="Close chat"
          >
            ✕
          </button>
        </div>

        {/* Messages */}
        <div className="chatbot-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role} ${message.isError ? 'error' : ''}`}
            >
              <div className="message-avatar">
                {message.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <span className="sources-label">📚 Sources:</span>
                    {message.sources.slice(0, 2).map((source, idx) => (
                      <span key={idx} className="source-tag">
                        {source.chapter}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message assistant loading">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form className="chatbot-input-form" onSubmit={handleSubmit}>
          <input
            ref={inputRef}
            type="text"
            className="chatbot-input"
            placeholder="Ask about Physical AI..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            className="chatbot-send"
            disabled={!input.trim() || isLoading}
            aria-label="Send message"
          >
            ➤
          </button>
        </form>

        {/* Footer hint */}
        <div className="chatbot-footer">
          💡 Tip: Select text on the page and ask questions about it!
        </div>
      </div>
    </>
  );
};

export default Chatbot;
