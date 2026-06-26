import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Database, BarChart3, Package, Store } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hello! I am your FMCG Data Assistant. Ask me anything about sales, promotions, inventory, or products.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      // Pointing to local FastAPI server
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage
      });
      
      setMessages(prev => [...prev, { role: 'ai', content: response.data.reply }]);
    } catch (error) {
      console.error("Error communicating with AI:", error);
      let errorMsg = "Sorry, I encountered an error. Is the backend server running?";
      if (error.response && error.response.data && error.response.data.detail) {
        errorMsg = error.response.data.detail;
      }
      setMessages(prev => [...prev, { role: 'ai', content: errorMsg }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar Context */}
      <div className="sidebar">
        <div>
          <h1>FMCG Insights</h1>
          <p>Powered by LangChain & LLM</p>
        </div>
        
        <div className="schema-section">
          <h3><Database size={16} style={{display: 'inline', verticalAlign: 'middle', marginRight: '6px'}}/> Data Sources</h3>
          
          <div>
            <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px'}}>
              <BarChart3 size={16} color="#60a5fa" />
              <span style={{fontWeight: 500}}>Sales & Promotions</span>
            </div>
            <div className="schema-badge">revenue</div>
            <div className="schema-badge">units_sold</div>
            <div className="schema-badge">promotion_type</div>
          </div>
          
          <div style={{marginTop: '16px'}}>
            <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px'}}>
              <Package size={16} color="#a78bfa" />
              <span style={{fontWeight: 500}}>Inventory</span>
            </div>
            <div className="schema-badge">opening_stock</div>
            <div className="schema-badge">stockout_flag</div>
          </div>
          
          <div style={{marginTop: '16px'}}>
            <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px'}}>
              <Store size={16} color="#34d399" />
              <span style={{fontWeight: 500}}>Masters</span>
            </div>
            <div className="schema-badge">product_master</div>
            <div className="schema-badge">store_master</div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="chat-area">
        <div className="chat-history">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="sender">{msg.role === 'ai' ? 'AI Assistant' : 'You'}</div>
              <div className="content">{msg.content}</div>
            </div>
          ))}
          {isLoading && (
            <div className="message ai">
              <div className="sender">AI Assistant</div>
              <div className="loading">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="input-area">
          <input 
            type="text" 
            placeholder="Ask about revenue, stockouts, or promotions..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <button onClick={handleSend} disabled={isLoading || !input.trim()}>
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
