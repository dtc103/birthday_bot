import discord
from discord.ext import commands, tasks

import json

from datetime import date

import asyncio

import utilities

import sqlite3

import os

class BirthdayCog(commands.Cog):
    admin_roles = ["Admin", "Mod(keeping the streets clean)"]
    bd_channel_id=787140921623969833
    bd_role_id=790591300579360769

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

        self.save_birthday_db(ctx.author, day, month, year, timezone)

    @commands.command(name="remove")
    async def remove_birthday(self, ctx: commands.Context):
        if not self.already_on_list(ctx.author):
            await ctx.send(f"{ctx.author.mention} you are not even on the birthday list yet")
            return

        if ctx.guild == None:
            return

        if await utilities.wait_for_query("Do you really want to delete your birthday from the birthday list?"):
            self.remove_birthday_db(ctx.author)

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
        
        self.edit_birthday_db(ctx.author, day, month, year, timezone)
        
        pass

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
        '''checks if member is already on the list'''
        cursor = self.birthday_database_connection.cursor()

        stmt = "SELECT userid FROM birthdays;"
        cursor.execute(stmt)

        for userid in cursor.fetchall():
            if str(member.id) == userid[0]:
                return True

        return False

    def get_day_embed(self):
        '''returns the embed for the birthday day query'''
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Choose day", value="Type in a number between 1 and 31")

        return embed

    def get_month_embed(self):
        '''returns the embed for the birthday month query'''
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Choose month", value="Type in a number between 1 and 12")

        return embed

    def get_year_embed(self):
        '''returns the embed for the birthday year query'''
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="Choose year", value=f"Type in a number between 1900 and {date.today().year - 12}")

        return embed

    def get_timezone_embed(self):
        '''returns the embed for the timeone query
            UTC-12:00 International Date Line West
            UTC-11:00 Coordinated universal Time-11
            UTC-10:00 Aleutian Islands, Hawaii
            UTC-9:30 Marquesas Islands
            UTC-9:00 Alaska, Coordinated Universal Time-09
            UTC-8:00 Baja California, Pacific Standard Time(Mexico, Canada, USA)
            UTC-7:00 Arizona, Chihuahua, La paz, Mazatlan, Mountain Standard Time(Mexico, Canada, USA)
            UTC-6:00 Central America, Central Standard Time(Mexico, Canadam, USA), Easter Island, Guadalajara, Mexico City, Monterrey, Saskatchewan
            UTC-5:00 Bogota, Lima, Quito, Rio Branco, Chetumal, Eastern Standard Time(Mexico, Canada, USA), Hiti, Havana, Indiana, Turks, Caicos
            UTC-4:00 Asuncion, Atlantic Standard Time(Canada), Caracas, Cuiaba, Georgetown La Paz, Manaus, San Juan, Santiago
            UTC-3:30 Newfoundland Standard Time
            UTC-3:00 Araguaina, Brasilia, Cayenne, Fortaleza, Buesnos Aires, Greenland, Montevideo, Punta Arenas, Saint Pierre and Miquelon, Salvador
            UTC-2:00 Coordinated Universal Time-02
            UTC-1:00 Azores, Cabo Verde
            UTC+00:00 Dublin, Edinburgh, Lisbon, London, Monrovia Reykjavik, Sao Tome, Greenwich Standard Time
            UTC+01:00 Casablanca, Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna, Belgrade, Bratislava, Budapest, Ljubljana, Prague, Brussels, Copenhagen, Madrid, paris, Sarajevo, Skopje, Warsaw, Zagreb, West Central Africa
            UTC+02:00 Amman, Athens Bucharest, Beirut, Cairo, Chisinau, Damascus, Gaza, Hebron, Harare, Pretoria, Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius, Jersusalem, Kaliningrad, Khartoum, Tripoli, Windhoek
            UTC+03:00 Baghdad, Istanbul, Kuwait, Riyadh, Mins, Moscow, St. Petersburg, Nairobi
            UTC+03:30 Tehran
            UTC+04:00 Abu Dhabi, Muscat, Astrakhan, Ulyanovsk, Baku, Azerbaijan, Izhevsk, Samara, Port Louis, Saratov, Tbilisi, Volgograd, Yerevan
            UTC+04:30 Kabul, Afghanistan
            UTC+05:00 Ashgabat, Tashkent, West Asia Standard Time, Ekaterinburg, Islamabad, Karachi, Pakistan, Qyzylorda
            UTC+05:30 Chennai, Kolkata, Mumbai, New Dheli, India Standard Time, Sri Jayawardenepura, Sri Lanka, Standard Time
            UTC+05:45 Kathmandu, Nepal Standard Time
            UTC+06:00 Astana, Dhaka, Omsk, Bangladesh Standard Time, Central Asia Standard Time
            UTC+06:30 Yangon(Rangoon), Myanmar Standard Time
            UTC+07:00 Bangkik, Hanoi, Jakarta, Barnaul, Gorno-Altaysk, Hovd, Krasnoyarsk, North Asia Standard Time
            UTC+08:00 Beijing, Chongqing, Hong Kong, Urumqi, China Standard Time, Irkutsk, Kuala Lumpur, Singapore, Perth, Taipei, Ulaanbaatar
            UTC+8:45 Eucla, Australian Central Western Standard Time
            UTC+09:00 Chita, Osaka, Sapporo, Tokyo, Pyongyang, Seoul, Yakutsk, Korea Standard Time
            UTC+09:30 Adelaide, Darwin Central Australian Standard Time
            UTC+10:00 Brisbane, Canberra, Melbourne, Sydney, Guam, Port Moresby, Hobart, Vladivostok, Eastern Australia Standard Time, West Pacific Standarf Time
            UTC+10:30 Lord Howe Island
            UTC+11:00 Bougainville island, Chokurdah, Magadan, Norflok Island, Sakhalin, Solomon Islands, New Caledonia
            UTC+12:00 Anadyr, Petropavlovsk-Kachatsky, Auckland, Wellington, New Zealand Standard Time, Fiji
            UTC+12:45 Chatham islands
            UTC+13:00 Nuku'alofa, Samoa
            UTC+14:00 Kiritimati island, Line Islands Standard time
        '''
        #TODO
        pass

    async def query_birthday_data(self, ctx):
        #answering day
        day_embed = self.get_day_embed()
        await ctx.send(embed=day_embed)
        try:
            day = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
        except:
            await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 31")
            return

        #answering month
        month_embed = self.get_month_embed()
        await ctx.send(embed=month_embed)
        try:
            month = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
        except:
            await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 12")
            return

        #answering year
        year_embed = self.get_year_embed()
        await ctx.send(embed=year_embed)
        try:
            year = int((await utilities.wait_for_message(self.bot, ctx, timeout=20)).content)
        except:
            await ctx.send(f"invalid input format - input has to be a NUMBER between 1900 and {date.today().year - 12}")
            return

        #TODO timezone 
        timezone = None
        if await utilities.wait_for_query(self.bot, ctx, message="Do you want to add your timezone for more accuracy?"):
            timezone_embed = self.get_timezone_embed()
            await ctx.send(embed=timezone_embed)
            try:
                timezone = await utilities.wait_for_message(self.bot, ctx, "type in the number of your timezone")
            except:
                await ctx.send(f"invalid input format - input has to be a NUMBER between 1 and 24")

            if timezone < 1 or timezone > 24:
                await ctx.send(f"invalid timezone input - timezone has to be one of these shown above")
                return

        return (day, month, year, timezone)

    def save_birthday_db(self, member: discord.Member, day, month, year, timezone=None):
        db_cursor = self.birthday_database_connection.cursor()

        date = f"{day}-{month}-{year}"

        if timezone is not None:
            stmt = "INSERT INTO birthdays (userid, username, birthday, timezone) VALUES(?, ?, ?, NULL);"
            db_cursor.execute(stmt, (str(member.id), member.name, date))
        else:
            stmt = "INSERT INTO birthdays (userid, username, birthday, timezone) VALUES(?, ?, ?, ?);"
            db_cursor.execute(stmt, (str(member.id), member.name, date, timezone))

        self.birthday_database_connection.commit()

    def edit_birthday_db(self, member: discord.Member, day, month, year, timezone=None):
        db_cursor = self.birthday_database_connection.cursor()
        
        if timezone is not None:
            stmt = """UPDATE birthdays SET day=?, month=?, year=?, timezone=? WHERE userid=?;"""
            db_cursor.execute(stmt, (day, month, year, timezone, str(member.id)))
        else:
            stmt = """UPDATE birthdays SET day=?, month=?, year=?, timezone=NULL WHERE userid=?;"""
            db_cursor.execute(stmt, (day, month, year, str(member.id)))
        
        self.birthday_database_connection.commit()

    async def remove_birthday_db(self, member: discord.Member):
        await remove_bd_role(self, member)

        db_cursor = self.birthday_database_connection.cursor()
        stmt = """DELETE FROM birthdays WHERE userid=?;"""
        db_cursor.execute(stmt, (str(member.id)))

        self.birthday_database_connection.commit()

    async def remove_bd_role(self, member: discord.Member):
        await member.remove_roles(list(discord.utils.find(lambda role: role.id == self.bd_role_id, self.bot.guilds[0].roles)))     

    async def add_bd_role(self, member):
        await member.add_roles(list(discord.utils.find(lambda role: role.id == self.bd_role_id, self.bot.guilds[0].roles)))

    def show_table(self):
        #TODO
        pass

    async def birthday_notification(self, channelid):
        pass