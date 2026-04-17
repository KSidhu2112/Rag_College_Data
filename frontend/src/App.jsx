import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { 
  Send, Bot, User, Loader2, Sparkles, Database, 
  Sidebar as SidebarIcon, Plus, MessageSquare, 
  Settings, GraduationCap, ChevronDown,
  LayoutGrid, BookOpen, Clock, Calendar
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';

const API_BASE_URL = 'http://localhost:8001';

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '### Welcome to LearnHub AI\nYour personal assistant for college information. Ask me anything about:\n\n* **Student Data** (Attendance, Records)\n* **Courses** (Syllabus, 3rd Year CSE subjects)\n* **Faculty** (HODs, Office Hours)\n* **Events** (Notices, Festivals)\n\nWhat can I help you find today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState('default_user');
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchSessions = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/sessions`);
      setSessions(response.data.sessions || []);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  useEffect(() => {
    const fetchHistory = async (session_id) => {
      try {
        const response = await axios.get(`${API_BASE_URL}/history?session_id=${session_id}`);
        if (response.data.history && response.data.history.length > 0) {
          setMessages(response.data.history);
        } else {
          setMessages([{ role: 'assistant', content: '### Welcome to LearnHub AI\nYour personal assistant for college information. Ask me anything about:\n\n* **Student Data** (Attendance, Records)\n* **Courses** (Syllabus, 3rd Year CSE subjects)\n* **Faculty** (HODs, Office Hours)\n* **Events** (Notices, Festivals)\n\nWhat can I help you find today?' }]);
        }
      } catch (error) {
        console.error('Error fetching history:', error);
      }
    };
    
    fetchHistory(currentSessionId);
    fetchSessions();
  }, [currentSessionId]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        question: input,
        session_id: currentSessionId
      });

      const assistantMessage = { 
        role: 'assistant', 
        content: response.data.answer,
        sources: response.data.sources 
      };
      setMessages((prev) => [...prev, assistantMessage]);
      fetchSessions(); // Refresh sidebar labels
    } catch (error) {
      console.error('Error fetching response:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'I apologize, but I am having trouble connecting to the knowledge base right now. Please ensure the backend server is running and data ingestion is complete.' 
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const newChat = () => {
    const newId = `session_${Date.now()}`;
    setCurrentSessionId(newId);
    setMessages([]);
  };

  const switchSession = (id) => {
    setCurrentSessionId(id);
  };

  return (
    <div className="dashboard-container">
      
      {/* Sidebar */}
      <aside className={`sidebar ${isSidebarOpen ? '' : 'sidebar-closed'} ${isSidebarOpen && window.innerWidth < 768 ? 'mobile-open' : ''}`}>
        <div className="sidebar-header">
          <div className="logo-container">
            <GraduationCap size={24} color="white" />
          </div>
          <span className="sidebar-logo-text">LearnHub</span>
        </div>
        
        <button onClick={newChat} className="new-chat-btn">
          <Plus size={18} />
          <span>New Session</span>
        </button>

        <nav className="nav-section custom-scrollbar">
          <div className="nav-group">
            <div className="nav-label">Navigation</div>
            <SidebarNavItem icon={<LayoutGrid size={18} />} label="Overview" active />
            <SidebarNavItem icon={<BookOpen size={18} />} label="Curriculum" />
            <SidebarNavItem icon={<Calendar size={18} />} label="Events" />
            <SidebarNavItem icon={<Clock size={18} />} label="Attendance" />
          </div>
          
          <div className="nav-group">
            <div className="nav-label">History</div>
            <div className="history-list custom-scrollbar">
              {sessions.length > 0 ? (
                sessions.map((session) => (
                  <div 
                    key={session.id} 
                    className={`nav-item history-item ${currentSessionId === session.id ? 'active' : ''}`}
                    onClick={() => switchSession(session.id)}
                  >
                    <MessageSquare size={16} />
                    <span className="truncate">{session.label}</span>
                  </div>
                ))
              ) : (
                <div style={{ padding: '0 12px', fontSize: '0.8rem', color: 'var(--text-dark)' }}>
                  Recent logs will appear here.
                </div>
              )}
            </div>
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="nav-item">
            <Settings size={18} />
            <span>Preferences</span>
          </div>
          <div className="nav-item" style={{ marginTop: '8px', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.2)' }}>
            <Sparkles size={14} color="#6366f1" />
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary)' }}>Gemini 1.5 Pro</span>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        
        {/* Top Floating Navbar */}
        <header className="top-nav">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
            >
              <SidebarIcon size={22} />
            </button>
            <div style={{ height: '20px', width: '1px', background: 'var(--border-subtle)' }}></div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 500 }}>
              Deep Retrieval Engine
              <ChevronDown size={14} />
            </div>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div className="avatar user" style={{ width: '32px', height: '32px', fontSize: '0.7rem', fontWeight: 700 }}>JD</div>
          </div>
        </header>

        {/* Chat Content */}
        <div className="chat-window custom-scrollbar">
          <div className="chat-container">
            
            {messages.length === 0 && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="welcome-screen"
              >
                <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
                  <div className="logo-container" style={{ width: '60px', height: '60px' }}>
                    <Database size={32} color="white" />
                  </div>
                </div>
                <h1>How can I help you today?</h1>
                <p>Access college data, curriculum, and faculty information instantly with our AI-powered retrieval system.</p>
                
                <div className="quick-actions">
                  <QuickAction label="Last Year Placements?" sub="Placement Statistics" />
                  <QuickAction label="IT Dept Faculty List" sub="Faculty Directory" />
                  <QuickAction label="Library Rules Overview" sub="Campus Policy" />
                  <QuickAction label="Hostel Fee Structure" sub="Admin & Finance" />
                </div>
              </motion.div>
            )}

            <AnimatePresence>
              {messages.map((msg, index) => (
                <ChatMessage key={index} msg={msg} />
              ))}
            </AnimatePresence>
            
            {isLoading && (
              <div className="message-row bot-msg">
                <div className="avatar bot">
                  <Loader2 size={20} className="animate-spin" />
                </div>
                <div className="message-content">
                  <div className="message-bubble" style={{ width: '100px', height: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                     <div className="loading-dots">...</div>
                  </div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="input-area">
          <div className="input-container">
            <form onSubmit={handleSendMessage} className="input-wrapper">
              <textarea
                rows="1"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage(e);
                  }
                }}
                placeholder="Ask LearnHub anything..."
                className="chat-input"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="send-button"
              >
                <Send size={20} />
              </button>
            </form>
            <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.7rem', color: 'var(--text-dark)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 600 }}>
              AI can make mistakes. Check important info.
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}

function SidebarNavItem({ icon, label, active = false }) {
  return (
    <div className={`nav-item ${active ? 'active' : ''}`}>
      {icon}
      <span>{label}</span>
    </div>
  );
}

function QuickAction({ label, sub }) {
  return (
    <div className="action-card">
      <span>{label}</span>
      <small>{sub}</small>
    </div>
  );
}

function ChatMessage({ msg }) {
  const isUser = msg.role === 'user';
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`message-row ${isUser ? 'user-msg' : 'bot-msg'}`}
    >
      <div className={`avatar ${isUser ? 'user' : 'bot'}`}>
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      
      <div className="message-content">
        <div className="message-bubble">
          <div className="whitespace-pre-wrap">{msg.content}</div>
        </div>

        {!isUser && msg.sources && msg.sources.length > 0 && (
          <div className="source-badges">
            {msg.sources.map((source, sIdx) => (
              <div key={sIdx} className="source-badge">
                <Database size={10} />
                <span>{source.source.toUpperCase()}</span>
                {source.page !== 'N/A' && <span>P. {source.page}</span>}
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default App;
