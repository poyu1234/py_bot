import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import requests
from bs4 import BeautifulSoup
import wget
import os
from fpdf import FPDF
import io

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Web_scraper(Cog_Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print("Web_scraper is ready")

    @commands.command()
    async def eop(self, ctx):
        # 檢查回傳的是否是同一個人(已及是否在同一個頻道)
        def check(title):
            return title.author == ctx.author and title.channel == ctx.message.channel

        await ctx.send("Please enter the song title u want to search.")
        response = await self.client.wait_for('message', check=check)
        title = response.content.replace(' ', '+')

        url = "https://tw.everyonepiano.com/Music-search"

        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

        p = {
            "word": title
        }

        r = requests.get(url, headers=header, params=p)
        soup = BeautifulSoup(r.text, "html.parser")
        # print(r.status_code)

        # list resort
        songs = soup.find_all('div', class_='MusicIndexBox')
        counts = 1
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
            info = str(counts)+'.'+title+intro
            await ctx.send(info)
            counts += 1
        # choose songs
        await ctx.send("which song do u want to download?(please enter the number and split by \",\"")
        response = await self.client.wait_for('message', check=check)
        try:
            input_num = [int(i) for i in response.content.split(',')]
        except:
            await ctx.send("You didn't input with correct format.")
            return 1

        # open img
        for i in input_num:
            url = "https://tw.everyonepiano.com" + \
                songs[i-1].find('div', class_='MITitle').a['href']
            r = requests.get(url, headers=header)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = songs[i-1].find('div', class_='MITitle').a.text
            sheets = soup.find('div', id='EOPReadScrollerW').find_all(
                'div', class_='EOPSingleWuxianpu')
            # set up
            name = './tem_file/'+title
            counts2 = 0
            pdf = FPDF('P', 'mm', 'A4')
            for sheet in sheets:
                if counts2 != 0:
                    url = "https://tw.everyonepiano.com"+sheet.a['href']
                    r = requests.get(url, headers=header)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    result = soup.find('div', 'EOPStavePIC').img['src']
                    result_url = "https://tw.everyonepiano.com"+result
                    # download img
                    filename = wget.download(
                        result_url, out=name+'('+str(counts2)+').png')
                    pdf.add_page()
                    pdf.image(name+'('+str(counts2)+').png', x=0, y=0, w=210)
                    # delete
                    os.remove(filename)
                    counts2 += 1
                else:  # Online Music Stand
                    counts2 += 1
                    continue

            bstring = pdf.output(dest='S').encode('latin-1')
            await ctx.send(file=discord.File(io.BytesIO(bstring), filename=f'{title}.pdf'))


async def setup(client):
    await client.add_cog(Web_scraper(client))
