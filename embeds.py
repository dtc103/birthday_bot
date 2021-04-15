import discord
from datetime import date

def day_embed():
    '''returns the embed for the birthday day query'''
    embed = discord.Embed(color=discord.Color.blurple())
    embed.add_field(name="Choose day", value="Type in a number between 1 and 31")

    return embed

def month_embed():
    '''returns the embed for the birthday month query'''
    embed = discord.Embed(color=discord.Color.blurple())
    embed.add_field(name="Choose month", value="Type in a number between 1 and 12")

    return embed

def year_embed():
    '''returns the embed for the birthday year query'''
    embed = discord.Embed(color=discord.Color.blurple())
    embed.add_field(name="Choose year", value=f"Type in a number between 1900 and {date.today().year - 12}")

    return embed

#FUTURE FEATURE
def get_timezone_embed():
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
    pass


