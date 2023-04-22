import discord
from discord.ext import commands
from discord import app_commands
from core.classes import Cog_Extension
import json
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import io

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Web_scraper(Cog_Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print("Web_scraper is ready")

    @app_commands.command(name="scrap_sheets", description="scrap sheets from everyonepiano.com")
    async def scrap_sheets(self, interaction: discord.Interaction, song_name: str):
        await interaction.response.defer(ephemeral=True)
        # 檢查回傳的是否是同一個人(已及是否在同一個頻道)

        def check(content):
            return content.author == interaction.user and content.channel == interaction.channel
        # await interaction.response.send_message(f"<@{interaction.user.id}>Please enter the song title u want to search.")
        # response = await self.client.wait_for('message', check=check)
        title = song_name.replace(' ', '+')

        url = "https://tw.everyonepiano.com/Music-search"

        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

        p = {
            "word": title
        }

        r = requests.get(url, headers=header, params=p)
        soup = BeautifulSoup(r.text, "html.parser")
        print(r.status_code)

        # list resort
        songs = soup.find_all('div', class_='MusicIndexBox')
        counts = 1
        info = ''
        for song in songs:
            title = song.find('div', class_='MITitle').a.text
            intro = song.find(
                'div', class_='col-xs-12 col-sm-10 col-md-8 MIMusicBar').text
            date = song.find('div', class_='col-xs-12 col-sm-10 col-md-8 MIMusicBar').find(
                'div', class_='MIMusicUpdate').text
            hid = song.find('div', class_='col-xs-12 col-sm-10 col-md-8 MIMusicBar').find(
                'div', class_='MusicBtn1 hidden-xs').text
            intro = intro.replace(date, '')
            intro = intro.replace(hid, '')
            intro = intro[38:]
            info = info+str(counts)+'.'+title+intro
            counts += 1
        # choose songs
        await interaction.followup.send(f"{info}<@{interaction.user.id}>Which song do u want to download?(please enter the number and split by \",\".")
        num = await self.client.wait_for('message', check=check)
        try:
            input_num = [int(i) for i in num.content.split(',')]
        except:
            await interaction.followup.send(f"<@{interaction.user.id}>You didn't input with correct format.")
            return 1

        # open img
        for i in input_num:
            url = "https://tw.everyonepiano.com" + \
                songs[i-1].find('div', class_='MITitle').a['href']
            r = requests.get(url, headers=header)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = songs[i-1].find('div', class_='MITitle').a.text
            print(title)
            sheets = soup.find('div', id='EOPReadScrollerW').find_all(
                'div', class_='EOPSingleWuxianpu')
            # set up
            counts2 = 0
            pdf = FPDF('P', 'mm', 'A4')
            for sheet in sheets:
                if counts2 != 0:
                    url = "https://tw.everyonepiano.com"+sheet.a['href']
                    r = requests.get(url, headers=header)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    result = soup.find('div', 'EOPStavePIC').img['src']
                    result_url = "https://tw.everyonepiano.com"+result
                    pdf.add_page()
                    pdf.image(result_url, x=0, y=0, w=210)
                    counts2 += 1
                else:  # Online Music Stand
                    counts2 += 1
                    continue
            print("finished")
            bstring = pdf.output(dest='S').encode('latin-1')
            # non-english filename can't be displayed
            await interaction.followup.send(f"<@{interaction.user.id}>This is your sheet.", file=discord.File(io.BytesIO(bstring), filename=f'{i}.pdf'), ephemeral=True)


async def setup(client):
    await client.add_cog(Web_scraper(client), guilds=[discord.Object(id=int(jdata["PY_guild_id"]))])
