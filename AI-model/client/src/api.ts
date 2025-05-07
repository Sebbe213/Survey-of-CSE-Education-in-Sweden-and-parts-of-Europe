// src/api.ts
export async function ask(question: string): Promise<string> {
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    if (!res.ok) throw new Error(await res.text());
    const { answer } = await res.json();
    return answer;
  }
  