// src/about.tsx
import Header from './header';
import ibrahim from './assets/ibrahim.jpg';
import diana    from './assets/diana.jpg';
import leo      from './assets/leo.jpg';
import felix    from './assets/felix.jpg';
import radwan   from './assets/radwan.jpg';
import sebbe    from './assets/sebbe.jpg';
import './about.css';


interface Student {
  name: string;
  image: string;
  desc: string;
}

export default function About() {
  const students: Student[] = [
    { name: 'Ibrahim Muhammad',            image: ibrahim, desc: 'Computer Science Engineering, Year 3' },
    { name: 'Diana Lam ',                  image: diana,   desc: 'Computer Science Engineering, Year 3' },
    { name: 'Leonard Österholm',           image: leo,     desc: 'Computer Science Engineering, Year 3' },
    { name: 'Felix Nyiri Magnusson',       image: felix,   desc: 'Computer Science Engineering, Year 3' },
    { name: 'Radwan Rashdan',              image: radwan,  desc: 'Computer Science Engineering, Year 3' },
    { name: 'Sebastian Raoof',             image: sebbe,   desc: 'Computer Science Engineering, Year 3' },
  ];

  return (
    <>
      <Header />
      <main className="about-page">
        <h1>About Us</h1>
        <p>
          We are a team of Computer Science and Engineering students at Chalmers University
          of Technology and University of Gothenburg. 
        </p>
        <div className="student-grid">
          {students.map((s) => (
            <div key={s.name} className="student-card">
              <img src={s.image} alt={s.name} className="student-img" />
              <div className="student-name">{s.name}</div>
              <div className="student-desc">{s.desc}</div>
            </div>
          ))}
        </div>
      </main>
    </>
  );
}