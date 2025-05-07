// src/mainpage.tsx
import { useEffect, useState } from 'react';
import Header from './header';
import QuestionModal from './question';
import { ask } from './api';
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

  // Load from localStorage once
  useEffect(() => {
    const stored = localStorage.getItem('conversations');
    if (stored) {
      setConversations(JSON.parse(stored));
    }
  }, []);

  // Persist list whenever it changes
  useEffect(() => {
    localStorage.setItem('conversations', JSON.stringify(conversations));
  }, [conversations]);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);

    try {
      const answer = await ask(question);
      setConversations((prev) => [
        ...prev,
        {question: question.trim(), answer}
      ]);
      setQuestion('');
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setConversations([]);
    console.log("I am pressed!");
    localStorage.removeItem('conversations');
  };

  function HandleKeyPress(event: React.KeyboardEvent) {
    if (event.key === 'Enter') {
      handleAsk();
    }
  }

  return (
      <div>
        <Header/>
        <div className="answer-area">
          <ul className="answer-list">
            {conversations.map((item, idx) => (
                <li key={idx}>
                  <QuestionModal question={item.question}/>
                  <p>Answer: {item.answer}</p>
                  <hr/>
                </li>
            ))}
          </ul>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="input-area">
          <input
              className="input-bar"
              placeholder="Write your question here!"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={HandleKeyPress}
              disabled={loading}
          />
          <button
              className="prompt-button"
              onClick={handleAsk}
              disabled={loading || !question.trim()}
          >
            <img className="arrow" src={arrowIcon} alt="Submit"/>
          </button>
          <button
              className="reset-button"
              onClick={handleReset}
              disabled={loading && conversations.length === 0}
          >
            Reset
          </button>
        </div>
      </div>
  );
}