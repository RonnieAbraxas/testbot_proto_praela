
print("Starting TestBot")

# --- 1. Conversation state ----------------------------
history = []   # list of (user_message, bot_reply) tuples

# --- 2. Fake brain ------------------------------------
def generate_reply(user_message):
    # For now, the bot just mirrors what you said.
    # Later, this will call a real LLM.
    return f"I heard you say: {user_message}"

# --- 3. Chat loop --------------------------------------
while True:
    user = input("You: ").strip()

    if user.lower() in ("quit", "exit"):
        reply = "Goodbye!"
        print(reply)
        history.append(user, reply)
        output_file = "history.txt"
        with open(output_file, 'a') as convo:
            convo.write("\nOur Beautiful Convo (in tuplets): \n\n")
            for user_msg, bot_msg in history:
                convo.write(f"\nUser: {user_msg}\nBot: {bot_msg}\n\n")
        break

    reply = generate_reply(user)

    print("Bot:", reply)

    # Save the turn
    history.append((user, reply))

   
