import aiohttp, asyncio
from bs4 import BeautifulSoup

class Comment:
    def __init__(self, data) -> dict:

        self.data = data
        
        for k, v in self.data.items():
            self.__setattr__(k, v)
            
class FindResult:
    def __init__(self, json_data: dict):
        self.json = json_data
        self.names = list(map(lambda x: x["name"], self.json))
        
    def find_by_author(self, author: str) -> dict:
        for i in self.json:
            if i["author"] == author:
                return i
        return None

async def FindLevelByName(name: str) -> FindResult:
    """
    returns levels by its name
    """
    with aiohttp.ClientSession() as ClientSession:
        async with ClientSession.get('https://gdbrowser.com/api/search/' + name + '?') as response:
            findpage = await response.json()
        return FindResult(findpage)

class Level:
    """
    Find you level by ID
    """

    def __init__(self, LevelID: int) -> dict:
        async def get():
            async with aiohttp.ClientSession() as ClientSession:
                async with ClientSession.get('https://gdbrowser.com/api/level/' + str(LevelID)) as response:
                    return await response.json()
        self.__parse_result = asyncio.run(get())
        for name, value in self.response.items():
            self.__setattr__(name, value)
    
    @property
    def response(self) -> dict:
        return self.__parse_result

    def __str__(self) -> str:
        return str(self.response)

    async def Comments(self):
        """Retrieves level comments"""
        async with aiohttp.ClientSession() as ClientSession:
            async with ClientSession.get(f'https://gdbrowser.com/api/comments/{self.id}?count=10000000') as response:
                comments = await response.json()

        return list(map(lambda x: Comment(x), comments))

class Account:
    """Search for an account by its name / account ID"""

    async def __init__(self, User: str) -> dict:
        async with aiohttp.ClientSession() as ClientSession:
            async with ClientSession.get("https://gdbrowser.com/u/" + str(User)) as response:
                AccPage = await response.text()
        soup = BeautifulSoup(AccPage, 'lxml')
        self.Page = AccPage
        self.Name = soup.find_all('span')[0].text
        self.stars = soup.find_all('span')[1].text
        self.diamonds = soup.find_all('span')[2].text
        self.coins = soup.find_all('span')[3].text
        self.usercoins = soup.find_all('span')[4].text
        self.demons = soup.find_all('span')[5].text
        self.cp = soup.find_all('span')[7].text
        self.top = int(soup.find_all('p')[4].text)
        AIDandUID = soup.find_all(class_="profilePostHide")[4].text
        AIDandUID = "".join("".join(AIDandUID.split('Player ID:')).split('\nAccount ID: ')[1]).split('\n')[0]
        AIDandUID = AIDandUID.split(' ')
        self.accountID = AIDandUID[0]
        self.playerID = AIDandUID[1]

    async def Comments(self) -> dict:
        """Returns comments from the page"""
        async with aiohttp.ClientSession() as ClientSession:
            async with ClientSession.get(f"https://gdbrowser.com/api/comments/{self.accountID}?type=profile&count=10000000") as response:
                CommentsPage = await response.json()
            return CommentsPage