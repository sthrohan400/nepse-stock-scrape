'''
    Python module to Scrape data from http://www.nepalstock.com/main/todays_price/index/ table
    Python Process Runs Every 5 Minutes and Scrape the data format it and stores in Primary and Seconday
    Storage.
    Scrape function usage aiohttp and asyncio module to gather data
'''
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from config import config
from rediscache import RedisCacheLibrary


def formatListTuple(html):

    tempcontents = []
    soup = BeautifulSoup(html, 'html.parser')
    cont = soup.find('div', {"id" : "home-contents"})
    cont = cont.findAllNext('tr')
    try:
        del cont[0]
        del cont[1]
    except IndexError as e:
        return []
    for val in cont:

        # check all these data exists
        try:
            val = val.findAllNext('td')
            if "Traded Companies" in val[1].text or "Price" in val[3].text or "Price" in val[4].text:
                continue
            temp = (val[1].text, val[2].text, val[3].text, val[4].text, val[5].text, val[6].text, val[7].text, val[8].text)
            tempcontents.append(temp)
        except IndexError as e:
            continue
    return tempcontents


def formatIndex(html):
    contents_url = []
    soup = BeautifulSoup(html, 'html.parser')
    cont = soup.find('div', {"id": "home-contents"})
    pager = cont.find('div', {"class": "pager"})
    pager_href = pager.findAllNext('a', href=True)
    for item in pager_href:
        try:
            item['href'] = item['href']
        except KeyError:
            continue
        if len(item['href']) < 50:
            continue
        if '/todays_price/' in item['href']:
            contents_url.append(item['href'])
        else:
            continue

    return contents_url


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main(urls):
    contents_url = []
    data_contents = [] #"" for csv
    async with aiohttp.ClientSession() as session:
        # /** Loop Multiple Urls for Data scrape **/
        html = await asyncio.gather(*[fetch(session, val) for val in urls])
        # html = await fetch(session, urls)
        for con in html:
            tempurl = formatIndex(con)
            contents_url = contents_url + tempurl
        # run gathering data
        contents_url = contents_url + urls
        print(contents_url)
        html = await asyncio.gather(*[fetch(session, val) for val in contents_url])
        for c in html:
            tempcontents = formatListTuple(c)
            data_contents = data_contents + tempcontents

        # Set data to redis
        if(len(data_contents) > 0):
           # RedisCacheLibrary.getInstance(config).push("nepse",data_contents)
            print(data_contents)




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config.get('url')))
