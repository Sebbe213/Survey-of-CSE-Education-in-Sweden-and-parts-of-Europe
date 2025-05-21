// src/about.tsx
import Header from './header';
import './about.css';


export default function About() {

  return (
    <>
      <Header />
      <main className="about-page">
        <h1>About Us</h1>
        <p>
          We are a team from Chalmers University of Technology and the University of Gothenburg who developed an AI-powered tool as part of our bachelor thesis. Our goal was to find the metrics and develop a system on how to evaluate the quality of higher education in a way that is transparent.
          This tool uses retrieval augmented generation (RAG) and large language models (LLMs) to provide accurate, interactive answers based on real university data and student priorities. Rather than relying solely on traditional ranking metrics, our system is built around factors that matter most to students such as teaching quality, employability, student experience etc.
          By embedding institutional data, survey insights and our written report, the AI enables users to explore, compare, and question educational quality in a way that's transparent, student centred, and grounded in real data, not just reputation.
          This is not just a chatbot it’s a prototype for how AI can support smarter decision-making in higher education.
        </p>
      </main>
    </>
  );
}