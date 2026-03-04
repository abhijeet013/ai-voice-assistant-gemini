Audio-Based Customer Support Agent

Project Overview - 

This project is an AI-powered Audio-Based Customer Support Agent developed for an online technology company.
It enables users to communicate through both voice and text. The system can listen to spoken queries, process them using a generative AI model, and respond with both text and synthesized speech.

The project combines speech recognition, Google Gemini (Generative AI), and text-to-speech (gTTS) technologies through a Streamlit interface.
It is designed to simulate a real-world technical support chatbot capable of handling customer-related issues, maintaining context during conversations, and interacting naturally.

Features -
1.Voice input using SpeechRecognition
2.Text input for manual queries
3.Generative AI responses using the Gemini API
4.Voice output through gTTS and Pygame
5.Mid-session context memory for follow-up queries
6.Customer information sidebar (Name and ID fields)
7.System health monitor showing component status
8.Option to clear conversation history
9.Streamlit-based interface for easy interaction 

Dependencies used in this project:
1.streamlit
2.google-generativeai
3.gtts
4.SpeechRecognition
5.pygame
6.python-dotenv

How It Works -
1.The user either speaks or types a query.
2.The system converts speech to text using SpeechRecognition.
3.The query, along with chat history, is processed by the Gemini API.
4.The AI generates a professional support response.
5.The response is both displayed as text and read aloud using gTTS and Pygame.
6.Conversation history is maintained until reset.

Example Queries -

1.I can’t log into my account.
2.How do I update my payment method?
3.The app keeps crashing, what can I do?
4.Can I cancel my subscription?
5.How do I reset my password?

note - If you ask something unrelated, such as “What is the capital of France?”, the assistant will respond:
“I’m sorry, I can only help with technology or customer support queries.”

By -
Abhijeet Singh
B.Tech CS/IT Student
symbiosis university of applied sciences, indore
email- Singhgourabhijeet013@gmail.com