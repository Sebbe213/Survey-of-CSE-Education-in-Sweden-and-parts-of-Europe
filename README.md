# Survey-of-CSE-Education-in-Sweden-and-Europe

## About
This project is a bachelor thesis with the aim of finding the best parameters to assess university quality. The main focus will be to use data from multiple universities to determine how Chalmers University and the University of Gothenburg can become top educators. 

In this github repository you will find data scraped from the www that concerns:
- Teacher acknowledgements
- Student teacher ratio
- Employability (percent of students that get a job after graduation)
- Student barometers
-  More to come.....

  Inside of the folders you will find scraped data, prompts, sources and figures made with Python.   
  
## Method
The data scraping will be conducted using the latest AI technologies, specifically deep research. By leveraging some of the most powerful LLMs and APIs and combining them with effective prompt engineering, we hope to efficiently and accurately gather data.

## LLMS 
The LLMS planed to be used are: 
- ChatGPT
- DeepSeek R1
- Grok
- Perplexity
- Gemini 

The process will first consist of triangulation. This means that we will utilize multiple LLMs, providing the same prompt to all of them. This ensures that the prompt given is well structured and consistent, as well as verifying the accuracy of the scraped data. By comparing the outputs of the LLMs, we can quickly spot any ambiguities in our prompts.

## Prompt Engineering
Our strategy for prompt engineering is simple. It consists of a few steps.

- Be specific – Try to be as specific in your prompt as possible. A good strategy is to think that you are explaining to a child. This helps narrow down the fields of possible responses, creating a more accurate output.
- Always include a goal – Define a clear mission that the LLM needs to solve. Example: Your objective is to help a research team find data about life span in Sweden.
- Give it a role – Make the model act as something specific. Example: You are a school teacher...
- Include constraints and disclaimers – Specify things that the LLM should look out for or avoid. Example: Do not include sources from non-government organizations.
- Include examples for clarity – Provide examples of how the data should be presented or what kind of data should be scraped.
