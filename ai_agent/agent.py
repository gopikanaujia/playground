# Improved AI Agent with Basic Memory

class SimpleAIAgent:
    def __init__(self):
        self.conversation_history = []
        self.responses = {
            'greetings': ["Hello! How can I help you?", "Hi there! What would you like to know?"],
            'python': ["Python is great for data analysis and automation.", "Python is a versatile programming language."],
            'sql': ["SQL helps manage and query databases.", "SQL is essential for working with data."],
            'data': ["Data analysis involves finding insights from information.", "Data processing is key for making decisions."],
            'farewells': ["Goodbye! Have a great day!", "See you later!"],
            'unknown': ["I'm not sure about that. Try asking about Python or SQL.", "I don't understand. Ask me about programming!"]
        }

    def get_response(self, question):
        """Generate response based on keywords and context."""
        question = question.lower()
        intent = self.classify_intent(question)

        # Get response from list
        response_list = self.responses.get(intent, self.responses['unknown'])
        response = response_list[0]  # Pick first response

        # Add context if continuing conversation
        if self.conversation_history and len(self.conversation_history) > 0:
            last_intent = self.conversation_history[-1]['intent']
            if last_intent == intent and intent != 'greetings' and intent != 'farewells':
                response += " We were just talking about this!"

        # Save to history
        self.conversation_history.append({
            'question': question,
            'intent': intent,
            'response': response
        })

        # Keep only last 3 conversations
        if len(self.conversation_history) > 3:
            self.conversation_history.pop(0)

        return response

    def classify_intent(self, question):
        """Classify the intent based on keywords."""
        if any(word in question for word in ['hello', 'hi', 'hey']):
            return 'greetings'
        elif 'python' in question:
            return 'python'
        elif any(word in question for word in ['sql', 'database']):
            return 'sql'
        elif any(word in question for word in ['data', 'analysis']):
            return 'data'
        elif any(word in question for word in ['bye', 'goodbye']):
            return 'farewells'
        else:
            return 'unknown'

if __name__ == "__main__":
    agent = SimpleAIAgent()
    print("AI Agent: Hello! Ask me questions about programming. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("AI Agent: Goodbye!")
            break

        response = agent.get_response(user_input)
        print(f"AI Agent: {response}")