import discord
from discord.ext import commands, tasks

import json

from datetime import date

import asyncio

import utilities

import sqlite3

import os

class BirthdayCog(commands.Cog):
    edit_permission_roles = ["Admin", "Mod(keeping the streets clean)"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if os.path.exists("birthdays.db"):
            self.birthday_database_connection = sqlite3.connect("birthdays.db")
            return
        
        self.birthday_database_connection = sqlite3.connect("birthdays.db")
        cursor = self.birthday_database_connection.cursor()

        create_bd_table = """CREATE TABLE birthdays(
            userid TEXT(200) NOT NULL,
            username TEXT(200),
            birthday TEXT(10),
            timezone TEXT(10),
            PRIMARY KEY(userid)
        );
        """
        cursor.execute(create_bd_table)
        self.birthday_database_connection.commit()


    @commands.command(name="add")
    async def add_birthday(self, ctx: commands.Context, day: int=None, month: int=None, year: int=None):
        if self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are already on the birthday list")
            return

        if ctx.guild == None:
            return
        
        if day is None or month is None or year is None:
            #answering day
            day_embed = self.get_day_embed()
            await ctx.send(embed=day_embed)
            try:
                day = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
            except:
                await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 31")
                return
            
            if day < 1 or day > 31:
                await ctx.send(f"invalid number input - day has to be between 1 and 31")
                return 

            #answering month
            month_embed = self.get_month_embed()
            await ctx.send(embed=month_embed)
            try:
                month = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
            except:
                await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 12")
                return

            if month < 1 or month > 12:
                await ctx.send(f"invalid number input - month has to be between 1 and 12")
                return 

            #answering year
            year_embed = self.get_year_embed()
            await ctx.send(embed=year_embed)
            try:
                year = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
            except:
                await ctx.send(f"invalid input format - input has to be a NUMBER between 1900 and {date.today().year - 12}")
                return
            
            if year < 1900 or year > int(date.today().year) - 12:
                await ctx.send(f"invalid number input - year has to be between 1900 and {date.today().year - 12}")
                return
        
        
        if day < 1 or day > 31:
            await ctx.send(f"invalid number input - day has to be between 1 and 31")
            return
        
        if month < 1 or month > 12:
            await ctx.send(f"invalid number input - month has to be between 1 and 12")
            return 
        
        if year < 1900 or year > int(date.today().year) - 12:
            await ctx.send(f"invalid number input - year has to be between 1900 and {date.today().year - 12}")
            return

        #TODO timezone 
        if await utilities.wait_for_query(self.bot, ctx, message="Do you want to add your timezone for more accuracy?"):
            timezone_embed = self.get_timezone_embed()
            await ctx.send(embed=timezone_embed)

            try:
                timezone = int(await utilities.wait_for_message(self.bot, ctx, "type in the number of your timezone"))
            except:
                await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 24")

            if timezone < 1 or timezone > 24:
                await ctx.send(f"invalid number input - month has to be between 1 and 12")
                return

            self.save_birthday(ctx.author, day, month, year, timezone)
        
        self.save_birthday(ctx.author, day, month, year)

        pass

    @commands.command("remove")
    async def remove_birthday(self, ctx: commands.Context):
        if not self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are not even on the birthday list yet")
            return

        if ctx.guild == None:
            return

        pass

    @commands.command("edit")
    async def update_birthday(self, ctx: commands.Context):
        if not self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are not on the birthday list yet")
            return

        if ctx.guild == None:
            return
        
        pass
    
    def save_birthday(self, member: discord.Member, day, month, year, timezone=None):
        db_cursor = self.birthday_database_connection.cursor()

        date = f"{day}-{month}-{year}"

        if timezone is not None:
            stmt = "INSERT INTO birthdays (userid, username, birthday, timezone) VALUES(?, ?, ?, NULL);"
            try:
                db_cursor.execute(stmt, (member.id, member.name, date))
            except:
                #id was already added
                pass
        else:
            stmt = "INSERT INTO birthdays (userid, username, birthday, timezone) VALUES(?, ?, ?, ?);"
            db_cursor.execute(stmt, (member.id, member.name, date, timezone))

        self.birthday_database_connection.commit()
        

    def already_on_list(self, member: discord.Member):
        cursor = self.birthday_database_connection.cursor()

        stmt = "SELECT userid FROM birthdays;"
        cursor.execute(stmt)

        for userid in cursor.fetchall():
            if str(member.id) == userid[0]:
                return True

        return False

    def get_day_embed(self):
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Choose day", value="Type in a number between 1 and 31")

        return embed

    def get_month_embed(self):
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Choose day", value="Type in a number between 1 and 12")

        return embed

    def get_year_embed(self):
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Choose day", value=f"Type in a number between 1990 and {date.today().year - 12}")

        return embed

    def get_timezone_embed(self):
        pass

    @commands.group(name="admin", pass_context=True)
    @commands.has_role(edit_permission_roles)
    async def admin(self, ctx: commands.Context):
        pass

    @admin.command(name="delete")
    async def admin_delete(self, ctx, user):
        pass

    @tasks.loop(hours=1)
    async def check_role(self):
        #if current date fits to the dates in 
        curr_date = date.today().strftime("%d/%m/%Y")
        pass

    @check_role.before_loop
    async def before_check_role(self):
        #load whole database into current memory
        pass