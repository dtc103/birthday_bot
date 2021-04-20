import discord
from discord.ext import commands, tasks
import json
from datetime import date, datetime
import asyncio
import utilities
import sqlite3
import os
import birthday_database_ops
import embeds
import re
import birthday_utils

class BirthdayCog(commands.Cog):
    admin_roles = ["Admin", "Mod(keeping the streets clean)"]
    bd_channel_id=808719852025151559 #Sket: 787140921623969833
    bd_role_id=808719851500732484 #Sket: 790591300579360769
    sket_or_test_server = 1 #1=test server, 0=sket

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if os.path.exists("birthdays.db"):
            self.birthday_database_connection = sqlite3.connect("birthdays.db")
            self.check_role.start()
            return
        
        self.birthday_database_connection = sqlite3.connect("birthdays.db")
        cursor = self.birthday_database_connection.cursor()

        create_bd_table = """CREATE TABLE birthdays(
            userid TEXT(200) NOT NULL,
            username TEXT(200),
            birthday TEXT(10),
            is_congratulated BOOLEAN NOT NULL,
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
        cursor.execute(create_admin_table)
        cursor.execute(create_message_table)

        self.birthday_database_connection.commit()

        self.check_role.start()


##################### USER COMMANDS ############################################################
    @commands.command(name="add")
    async def add_birthday(self, ctx: commands.Context, day: int=None, month: int=None):
        if self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are already on the birthday list")
            return

        if ctx.guild == None:
            return

        timezone = None
        
        if day is None or month is None:
            (day, month, timezone) = await self.query_birthday_data(ctx)

        if day < 1 or day > 31:
            await ctx.send(f"invalid day input - day has to be between 1 and 31")
            return
        
        if month < 1 or month > 12:
            await ctx.send(f"invalid month input - month has to be between 1 and 12")
            return 

        birthday_database_ops.save_birthday(self.birthday_database_connection, ctx.author.id, ctx.author.name, day, month, timezone)
        await self.update_table()

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
            await self.update_table()

    @commands.command(name="edit")
    async def edit_birthday(self, ctx: commands.Context, day: int=None, month: int=None):
        if not self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are not on the birthday list yet")
            return

        if ctx.guild == None:
            return

        timezone = None

        if day is None or month is None:
            (day, month, year, timezon) = await self.query_birthday_data(ctx)

        if day < 1 or day > 31:
            await ctx.send(f"invalid day input - day has to be between 1 and 31")
            return
        
        if month < 1 or month > 12:
            await ctx.send(f"invalid month input - month has to be between 1 and 12")
            return 
        
        birthday_database_ops.edit_birthday(self.birthday_database_connection, ctx.author.id, day, month, timezone)
        await self.update_table()


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
    @tasks.loop(seconds=10)#minutes=15)
    async def check_role(self):
        update_table = False

        if self.bot.is_ready():
            #update_table = await self.remove_left_users_from_database()

            curr_date = datetime.utcnow().strftime("%d-%m")

            for userid, username, birthday, is_congratulated, _ in birthday_database_ops.get_birthday_users(self.birthday_database_connection):
                if birthday == curr_date and is_congratulated == 0:
                    await self.congratulate(int(userid))
                if birthday != curr_date and is_congratulated == 1:
                    user = self.bot.guilds[self.sket_or_test_server].get_member(int(userid))
                    await self.remove_bd_role(user)
            
            print(curr_date)

##################### HELPERS ##################################################################
    def already_on_list(self, member: discord.Member):
        '''checks if member is already on the list and in the database'''

        for userid, _, _, _, _ in birthday_database_ops.get_birthday_users(self.birthday_database_connection):
            if member.id == int(userid):
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

        return (day, month, timezone)

    async def remove_bd_role(self, member: discord.Member):
        if a:=discord.utils.find(lambda role: role.id == self.bd_role_id, self.bot.guilds[self.sket_or_test_server].roles):
            await member.remove_roles(a)
            birthday_database_ops.set_congratulated(self.birthday_database_connection, member.id, False)   

    async def add_bd_role(self, member):
        if a:=discord.utils.find(lambda role: role.id == self.bd_role_id, self.bot.guilds[self.sket_or_test_server].roles):
            await member.add_roles(a)
            birthday_database_ops.set_congratulated(self.birthday_database_connection, member.id, True)

    async def remove_left_users_from_database(self):
        '''checks, if there are users in the database, which are not in the server anymore and removes them
        returns true, if users got deleted, false if no one left
        '''
        removed_user = False

        intents = discord.Intents.default()
        intents.members = True

        for memberid, _, _, _, _ in birthday_database_ops.get_birthday_users(self.birthday_database_connection):
            await self.bot.guilds[self.sket_or_test_server].fetch_members(limit=None).flatten()
            if self.bot.guilds[self.sket_or_test_server].get_member(int(memberid)) is None:
                birthday_database_ops.remove_birthday(self.birthday_database_connection, memberid)
                removed_user = True

        return removed_user

    async def update_table(self):
        bd_table = ""

        birthday_list = []

        for userid, username, birthday, _, _ in birthday_database_ops.get_birthday_users(self.birthday_database_connection):
            m = re.search(r"(\d\d)-(\d\d)", birthday)
            day = int(m.group(1))
            month = int(m.group(2))

            birthday_list.append((userid, username, day, month))
        
        #sorted list
        birthday_list = sorted(birthday_list, key=lambda e: (self.takeFourth(e), self.takeThird(e)))

    

        #channel = self.bot.guilds[self.sket_or_test_server].get_channel(self.bd_channel_id)

        # if len(birthday_database_ops.get_bd_channel(self.birthday_database_connection)) > 0:
        #     for messageid, channelid in birthday_database_ops.get_bd_channel(self.birthday_database_connection):
        #         channel = self.bot.guilds[self.sket_or_test_server].get_channel(int(channelid))
        #         former_message = await channel.fetch_message(int(messageid))
        #         await channel.delete_messages([former_message])

        #         message = await channel.send(embed=embed)
        #         birthday_database_ops.set_bd_channel(self.birthday_database_connection, message.id, former_message, channelid)
        # else:
        #     channel = self.bot.guilds[self.sket_or_test_server].get_channel(self.bd_channel_id)
        #     message = await channel.send(embed=embed)
        #     birthday_database_ops.set_bd_channel(self.birthday_database_connection, message.id, None, self.bd_channel_id)
    
    def takeThird(self, elem):
        return elem[2]
    def takeFourth(self, elem):
        return elem[3]

    async def congratulate(self, userid):
        '''mentions the user who has birthday and assigns the birthday role'''
        user = self.bot.guilds[self.sket_or_test_server].get_member(userid)
        channel = self.bot.guilds[self.sket_or_test_server].get_channel(self.bd_channel_id)

        await self.add_bd_role(user)

        await channel.send(f"BDAY {user.mention}")

    