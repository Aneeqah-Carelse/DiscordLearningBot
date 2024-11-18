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
async def start_quiz(ctx, topic):
    if topic not in questions:
        await ctx.send("Topic not found. Available topics: Genetics, Ecology, etc.")
        return

    # Initialize user state for the quiz
    user_state[ctx.author.id] = {
        "topic": topic,
        "question_index": 0
    }

    await send_question(ctx)

async def send_question(ctx):
    """Send the current question to the user."""
    state = user_state.get(ctx.author.id)
    if not state:
        await ctx.send("Please start a quiz first by using `!start_quiz <topic>`.")
        return

    topic = state["topic"]
    question_index = state["question_index"]
    question_data = questions[topic][question_index]
    options = "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(question_data["options"])])
    await ctx.send(f"{question_data['question']}\n{options}")

@bot.command(name="answer")
async def answer(ctx, choice: int):
    state = user_state.get(ctx.author.id)
    if not state:
        await ctx.send("Please start a quiz first by using `!start_quiz <topic>`.")
        return

    topic = state["topic"]
    question_index = state["question_index"]
    question_data = questions[topic][question_index]

    user_answer = choice - 1
    if question_data["options"][user_answer] == question_data["answer"]:
        await ctx.send("Correct! 🎉")
    else:
        await ctx.send(f"Incorrect. {question_data['explanation']}")

    # Move to the next question if available
    state["question_index"] += 1
    if state["question_index"] < len(questions[topic]):
        await send_question(ctx)
    else:
        await ctx.send("Quiz complete! Well done!")
        del user_state[ctx.author.id]

bot.run(os.getenv("DISCORD_TOKEN"))