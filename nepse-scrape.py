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
contents = []


def format(html):
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    cont = soup.find('div', {"id" : "home-contents"})
    cont = cont.findAllNext('tr')
    # print(cont)
    # print(html)
    # Remove 0 and 1 index from list
    try:
        del cont[0]
        del cont[1]
    except IndexError as e:
        return []
    #converting data to list objects
    #print(cont)
    for val in cont:
        # check all these data exists
        try:
            val = val.findAllNext('td')
            temp = {}
            temp['stock'] = val[1].text
            temp['no_transaction'] = val[2].text
            temp['max_price'] = val[3].text
            temp['min_price'] = val[4].text
            temp['close_price'] = val[5].text
            temp['no_of_share_transaction'] = val[6].text
            temp['amount'] = val[7].text
            temp['previous_close_price'] = val[8].text
            contents.append(temp)
        except IndexError as e:
            continue
    #print(contents)
    return contents

def formatIndex(html):
    contents_url = []
    soup = BeautifulSoup(html, 'html.parser')
    cont = soup.find('div', {"id": "home-contents"})
    pager = cont.find('div', {"class": "pager"})
    pager_href = pager.findAllNext('a', href=True)
    for item in pager_href:
        if len(item['href']) < 50:
            continue
        contents_url.append(item['href'])
    return contents_url

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main(urls):
    contents = []
    contents_url = []
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
            tempcontents = format(c)
            contents = contents + tempcontents
        print(contents)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(config.get('url')))
