import discord
import json
from discord.ext import commands

# Create an instance of the Intents class and enable all intents
intents = discord.Intents.default()
intents.messages = True  

# Pass the intents to the Bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready to help with Life Science!")

bot.run("MTMwNjUxODk5NDk5OTcwNTY1MQ.GzKZLs.ALZB_O2JdCq8VEXVKCxUnz5xjC_j5tJvUXoauc")

@bot.command(name="start_quiz")
async def start_quiz(ctx, topic):
    with open("questions.json") as f:
        questions = json.load(f)
    
    if topic not in questions:
        await ctx.send("Topic not found. Available topics: Genetics, Ecology, etc.")
        return

    question_data = questions[topic][0]  # Get the first question for simplicity
    options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(question_data["options"])])
    await ctx.send(f"{question_data['question']}\n{options}")

# @bot.command(name="answer")
# async def answer(ctx, choice: int):
#     user_answer = choice - 1  # Adjust for 0-based indexing
#     question_data = questions[topic][0]  # Using the first question for demonstration

#     if question_data["options"][user_answer] == question_data["answer"]:
#         await ctx.send("Correct! 🎉")
#     else:
#         await ctx.send(f"Incorrect. {question_data['explanation']}")

