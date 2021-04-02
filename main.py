import discord
from discord.ext import commands, tasks

import os
from dotenv import load_dotenv

from birthday import BirthdayCog

import sqlite3

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="B!")
bot.add_cog(BirthdayCog(bot))

bot.run(TOKEN)

#conn = sqlite3.connect("birthdays.db")
#cursor = conn.cursor()

#cursor.execute("INSERT INTO birthdays (userid, username, birthday, timezone) VALUES('12231', 'otherName', '3-2-1998', NULL);")
#conn.commit()