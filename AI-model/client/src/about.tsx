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
          We are a team of Computer Science and Engineering students at Chalmers University
          of Technology and University of Gothenburg. 
        </p>
        <p>
          Feel free to reach out if you have questions about our work or the tool itself!
        </p>
      </main>
    </>
  );
}
