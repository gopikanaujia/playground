# Improved AI Agent

This is an enhanced conversational AI agent that uses keyword matching with basic conversation memory and context awareness.

## Features
- **Intent Classification**: Identifies user intents (greetings, python, sql, data, farewells, unknown)
- **Conversation Memory**: Remembers the last 3 interactions
- **Context Awareness**: References previous topics if continuing the same conversation
- **Multiple Responses**: Has variety in responses for each intent

## How it works
1. User input is converted to lowercase
2. Keywords are checked to classify intent
3. Response is selected based on intent
4. If the conversation is continuing on the same topic, it adds context
5. Interaction is saved to memory

## Usage
Run the script: `python agent.py`

Example interaction:
```
AI Agent: Hello! Ask me questions about programming. Type 'quit' to exit.
You: What is Python?
AI Agent: Python is great for data analysis and automation.
You: Tell me more about Python
AI Agent: Python is a versatile programming language. We were just talking about this!
You: What about SQL?
AI Agent: SQL helps manage and query databases.
You: quit
AI Agent: Goodbye!
```

## Walkthrough
1. The agent uses a class to maintain state
2. `classify_intent()` checks for keywords in the input
3. `get_response()` selects appropriate response and adds context if needed
4. Conversation history helps provide more relevant responses

This demonstrates basic AI concepts like intent recognition, state management, and context awareness.