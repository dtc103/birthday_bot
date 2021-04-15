import discord
from discord.ext import commands, tasks
import json
from datetime import date
import asyncio
import utilities
import sqlite3
import os
import birthday_database_ops
import embeds

class BirthdayCog(commands.Cog):
    admin_roles = ["Admin", "Mod(keeping the streets clean)"]
    bd_channel_id=808719852025151559 #Sket: 787140921623969833
    bd_role_id=808719851500732484 #Sket: 790591300579360769

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
            birthday TEXT(10), //in format: dd-mm-yyyy
            timezone TEXT(10),
            PRIMARY KEY(userid)
        );"""

        create_admin_table = """CREATE TABLE admin_roles(
            roleid TEXT(200) NOT NULL,
            PRIMARY KEY(roleid)
        );"""

        create_message_table = """CREATE TABLE message_info(
            messageid TEXT(200) NOT NULL,
            channelid TEXT(200) NOT NULL,
            PRIMARY KEY(messageid)
        );"""

        cursor.execute(create_bd_table)
        #cursor.execute(create_admin_table)
        #cursor.execute(create_message_table)

        self.birthday_database_connection.commit()


##################### USER COMMANDS ############################################################
    @commands.command(name="add")
    async def add_birthday(self, ctx: commands.Context, day: int=None, month: int=None, year: int=None):
        if self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are already on the birthday list")
            return

        if ctx.guild == None:
            return
        
        if day is None or month is None or year is None:
            (day, month, year, timezone) = await self.query_birthday_data(ctx)

        if day < 1 or day > 31:
            await ctx.send(f"invalid day input - day has to be between 1 and 31")
            return
        
        if month < 1 or month > 12:
            await ctx.send(f"invalid month input - month has to be between 1 and 12")
            return 
        
        if year < 1900 or year > int(date.today().year) - 12:
            await ctx.send(f"invalid year input - year has to be between 1900 and {date.today().year - 12}")
            return

        birthday_database_ops.save_birthday(self.birthday_database_connection, ctx.author.id, ctx.author.name, day, month, year, timezone)

    @commands.command(name="remove")
    async def remove_birthday(self, ctx: commands.Context):
        if not self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are not even on the birthday list yet")
            return

        if ctx.guild == None:
            return

        if await utilities.wait_for_query(self.bot, ctx, "Do you really want to delete your birthday from the birthday list?"):
            await self.remove_bd_role(ctx.author)
            birthday_database_ops.remove_birthday(self.birthday_database_connection, ctx.author.id)

    @commands.command(name="edit")
    async def edit_birthday(self, ctx: commands.Context, day=None, month=None, year=None):
        if not self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are not on the birthday list yet")
            return

        if ctx.guild == None:
            return

        if day is None or month is None or year is None:
            (day, month, year, timezon) = await self.query_birthday_data(ctx)

        if day < 1 or day > 31:
            await ctx.send(f"invalid day input - day has to be between 1 and 31")
            return
        
        if month < 1 or month > 12:
            await ctx.send(f"invalid month input - month has to be between 1 and 12")
            return 
        
        if year < 1900 or year > int(date.today().year) - 12:
            await ctx.send(f"invalid year input - year has to be between 1900 and {date.today().year - 12}")
            return

        timezone = None
        
        birthday_database_ops.edit_birthday(self.birthday_database_connection, ctx.author.id, day, month, year, timezone)


##################### ADMIN COMMANDS ###########################################################
    @commands.group(name="admin", pass_context=True)
    @commands.has_role(admin_roles)
    async def admin(self, ctx: commands.Context):
        pass

    @admin.command(name="delete")
    async def admin_delete(self, ctx, user):
        pass 

    @admin.command(name="permissions")
    async def permissions(self, ctx):
        pass

    @admin.command(name="channel")
    async def choose_channel(self, ctx):
        channel = await utilities.choose_channel(self.bot, ctx, timeout=20)
        self.bd_channel_id = channel.id

    @admin.command(name="role")
    async def choose_role(self, ctx):
        role = await utilities.choose_role(self.bot, ctx, timeout=30)
        self.bd_role_id = role.id


##################### LOOPS ####################################################################
    @tasks.loop(minutes=15)
    async def check_role(self):
        #TODO also check if every user in the database is still in the server and delete his account if he left the server, but is still on the list
        

        #if current date fits to the dates in 
        curr_date = date.today().strftime("%d/%m/%Y")
        pass

    @check_role.before_loop
    async def before_check_role(self):
        #load whole database into current memory
        pass

##################### HELPERS ##################################################################
    def already_on_list(self, member: discord.Member):
        '''checks if member is already on the list and in the database'''

        for userid in birthday_database_ops.get_birthday_users(self.birthday_database_connection):
            if str(member.id) == userid:
                return True

        return False 

    async def query_birthday_data(self, ctx):
        #answering day
        day_embed = embeds.day_embed()
        await ctx.send(embed=day_embed)
        try:
            day = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
        except:
            await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 31")
            return

        #answering month
        month_embed = embeds.month_embed()
        await ctx.send(embed=month_embed)
        try:
            month = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
        except:
            await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 12")
            return

        #answering year
        year_embed = embeds.year_embed()
        await ctx.send(embed=year_embed)
        try:
            year = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
        except:
            await ctx.send(f"invalid input format - input has to be a NUMBER between 1900 and {date.today().year - 12}")
            return

        timezone = None
        #TODO FUTURE FEATURE 
        # if await utilities.wait_for_query(self.bot, ctx, message="Do you want to add your timezone for more accuracy?"):
        #     timezone_embed = embeds.timezone_embed()
        #     await ctx.send(embed=timezone_embed)
        #     try:
        #         timezone = await utilities.wait_for_message(self.bot, ctx, "type in the number of your timezone")
        #     except:
        #         await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 24")

        #     if timezone < 1 or timezone > 24:
        #         await ctx.send(f"invalid timezone input - timezone has to be one of these shown above")
        #         return

        return (day, month, year, timezone)

    async def remove_bd_role(self, member: discord.Member):
        await member.remove_roles(list(discord.utils.find(lambda role: role.id == self.bd_role_id, self.bot.guilds[0].roles)))     

    async def add_bd_role(self, member):
        await member.add_roles(list(discord.utils.find(lambda role: role.id == self.bd_role_id, self.bot.guilds[0].roles)))

    def show_table(self):
        #TODO
        pass

    async def birthday_notification(self, channelid, userid):
        '''mentions the user who has birthday'''
        pass