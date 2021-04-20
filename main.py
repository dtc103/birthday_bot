import discord
from discord.ext import commands, tasks

import os
from dotenv import load_dotenv

from birthday import BirthdayCog

import sqlite3
import database_test

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

#to get access to the "getch memeber method"
bot = commands.Bot(command_prefix="bday$", intents=intents)
bot.add_cog(BirthdayCog(bot))

bot.run(TOKEN)

#conn = sqlite3.connect("birthdays.db")
#database_test.fill_random_values(conn, 15)
#database_test.delete_table(conn)