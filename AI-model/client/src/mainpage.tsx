// src/mainpage.tsx
import { useEffect, useState, useRef } from 'react';
import Header from './header';
import QuestionModal from './question';
import { ask } from './api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './mainpage.css';
import arrowIcon from './assets/arrow 1 (1).png';

interface QA {
  question: string;
  answer: string;
}

export default function Mainpage() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversations, setConversations] = useState<QA[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Load stored conversations on mount
  useEffect(() => {
    const stored = localStorage.getItem('conversations');
    if (stored) setConversations(JSON.parse(stored));
  }, []);

  // Persist and scroll into view when list changes
  useEffect(() => {
    localStorage.setItem('conversations', JSON.stringify(conversations));
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversations]);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const answer = await ask(question);
      setConversations(prev => [...prev, { question: question.trim(), answer }]);
      setQuestion('');
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setConversations([]);
    localStorage.removeItem('conversations');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleAsk();
  };

  return (
    <div>
      <Header />
      <div className="answer-area">
        <ul className="answer-list">
          {conversations.map((item, idx) => (
            <li key={idx}>
              <QuestionModal question={item.question} />
              <div className="answer-markdown">
                <strong>Answer:</strong>
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {item.answer}
                </ReactMarkdown>
              </div>
              <hr />
            </li>
          ))}
        </ul>
        <div ref={bottomRef} />
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="input-area">
        <input
          className="input-bar"
          placeholder="Write your question here!"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={handleKeyPress}
          disabled={loading}
        />
        <button
          className="prompt-button"
          onClick={handleAsk}
          disabled={loading || !question.trim()}
        >
          {loading ? '…' : <img className="arrow" src={arrowIcon} alt="Submit" />}
        </button>
        <button className="reset-button" onClick={handleReset} disabled={loading && !conversations.length}>
          Reset
        </button>
      </div>
    </div>
  );
}
