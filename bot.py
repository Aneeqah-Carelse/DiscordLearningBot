import discord
import json
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load questions once when the bot starts
with open("questions.json") as f:
    questions = json.load(f)

# Track each user’s current question state
user_state = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready to help with Life Science!")

@bot.command(name="start_quiz")
async def start_quiz(ctx, year):
    await ctx.send("Please answer the question by using `!answer <letter>`.")
    if year not in questions:
        await ctx.send("Year not found. Available topics: 2023, 2022, 2021, etc.")
        return

    # Initialize user state for the quiz
    user_state[ctx.author.id] = {
        "Year": year,
        "question_index": 0
    }

    await send_question(ctx)

async def send_question(ctx):
    """Send the current question to the user."""
    state = user_state.get(ctx.author.id)
    if not state:
        await ctx.send("Please start a quiz first by using `!start_quiz <topic>`.")
        return

    topic = state["Year"]
    question_index = state["question_index"]
    question_data = questions[topic][question_index]

    # Use letters (A, B, C, D) for options
    options = "\n".join([f"{chr(65 + i)}. {opt}" for i, opt in enumerate(question_data["options"])])
    await ctx.send(f"{question_data['question']}\n{options}")

@bot.command(name="answer")
async def answer(ctx, choice: str):
    state = user_state.get(ctx.author.id)
    if not state:
        await ctx.send("Please start a quiz first by using `!start_quiz <year>`.")
        return

    # Convert choice to uppercase to standardize input (e.g., 'a' or 'A')
    choice = choice.upper()

    # Ensure the choice is a valid letter (A, B, C, D)
    valid_choices = ['A', 'B', 'C', 'D']
    if choice not in valid_choices:
        await ctx.send("Please enter a valid option (A, B, C, or D).")
        return

    topic = state["Year"]
    question_index = state["question_index"]
    question_data = questions[topic][question_index]

    # Map the letter choice (A, B, C, D) to the corresponding option index (0, 1, 2, 3)
    letter_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    user_answer_index = letter_to_index[choice]

    # Get the correct answer letter (A, B, C, D) and the user's selected answer
    correct_answer = question_data["answer"]
    user_answer = question_data["options"][user_answer_index]

    # Check if the selected answer matches the correct answer
    if correct_answer == choice:
        await ctx.send("Correct! 🎉")
    else:
        # Provide feedback with the incorrect answer choice and explanation
        await ctx.send(f"Incorrect. You selected {choice}. The correct answer is {correct_answer}. {question_data['explanation']}")

    # Move to the next question if available
    state["question_index"] += 1
    if state["question_index"] < len(questions[topic]):
        await send_question(ctx)
    else:
        await ctx.send("Quiz complete! Well done!")
        del user_state[ctx.author.id]

bot.run(os.getenv("DISCORD_TOKEN"))