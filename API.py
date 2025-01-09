# this file main perpose is to provide the infromation needed to install Manga from the
# website called  "https://weebcentral.com/" this API will provide a simple way to grab
# the series on the website and scrap data like description names and pages domain note
# that this file does not install anything on the disk it simply grabs  the  data  from
# the site but it will give you access to the links that you need to  grap  the  series
# and its data. this files works as of 2025/9/1 where the site has just  been  released
# so changing to the site are going to be frequent and the code below will  change  the
# the structure of the code and the final ouput of the code should remain the same. 







from Structure import Chapter , Series
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import Constants
import requests
import Cypher
import time
import json
import os
import re



# this will grap the names and  the id that comes with the name of the manga
# it will also let you search through them using a function and show you the
# results
class NamesIDGraper:
    def __init__(self) -> None:
        self.SeriesData:list[Series] = [] # this will incude the name of the show to its ID
        self.SeriesDataDict:list[dict[str:str]] = []

    def GrapSeriesFromDisk(self) -> None:
        # this will get the Series data from disk and load
        # them up to the SeriesData var
        if os.path.exists(Constants.MANGANAMESTOIDFILE):
            with open(Constants.MANGANAMESTOIDFILE, "r") as json_file:
                self.SeriesDataDict = json.load(json_file)
            
            _arr = []
            for _series in self.SeriesDataDict:
                _object = Series()
                _object.DomainID = _series["DomainID"]
                _object.DomainName = _series["DomainName"]
                _object.Names = _series["Names"]
                _arr.append(_object)

            self.SeriesData = _arr
        else:
            print("Error: File not found ->  Function: GrapSeriesFromDisk -> Consider grabing them using 'GrapAllShowsOnline()' first")

    def SearchSeriesOnline(self, Text:str) -> list[dict[str:str]]: # this function will take your text and search the database
        # this will  simply  search  the data for you and 
        # provide you the list in real time
        # Define the base URL

        _url = Constants.WEBDOMAIN + Constants.SEARCHSIMPLE
        _params = {
            "location":"main"
        }
        _data = {
            "text" : Text
        }

        _SeriesData = []
        try:
            response = requests.post(_url, params=_params, data=_data)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                a_tags = soup.find_all('a')
                if not a_tags:
                    return _SeriesData
                for _tag in a_tags:
                    _series = self._extract_series_ID(_tag["href"])
                    if _series:
                        _SeriesData.append(_series)
                return _SeriesData
            else:
                print(f"Error: status code = {response.status_code} -> Function : SearchSeriesOnline -> Unknown Error Domain Changed or offline")
        except Exception as e:
            print(e)


    def GrapAllSeriesOnline(self) -> None:
        # this will graps all the Serie names to  id  and
        # will store them in a json file

        _url = Constants.WEBDOMAIN + Constants.SITEMAPS
        _pattern = Cypher.XML_URL_PATTERN
        _SeriesData = []
        try:
            response = requests.get(_url)
            if response.status_code == 200:
                _seriesUrls = re.findall(_pattern, response.text)
                for _seriesUrl in _seriesUrls:
                    _series = self._extract_series_ID(_seriesUrl)
                    if _series:
                        _SeriesData.append(_series)
                    self.SeriesData = _SeriesData
                self._SaveData()
            else:
                print(f"Error: status code = {response.status_code} -> Function : GrapAllSeriesOnline -> Unknown Error Domain Changed or offline")
        
        except Exception as e:
            print(e)


    def LegacyGrapAllShowsOnline(self) -> None: # this function should only be used as a backup
        # this will graps all the Serie names to  id  and
        # will store them in a json file

        _url =  Constants.WEBDOMAIN + Constants.SEARCHDATA
        _limit = Constants.SEARCHDATALIMIT
        _params = {
            "limit": _limit,
            "offset": 0,
            "order": "Ascending",
            "display_mode": "Minimal Display"
            }


        _SeriesData = []
        _MoreToGrap = True
        while _MoreToGrap:
            try:
                response = requests.get(_url, params=_params)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    a_tags = soup.find_all('a')
                    if not a_tags:
                        _MoreToGrap = False
                        self.SeriesData = _SeriesData
                        self._SaveData()
                        break
                    for _tag in a_tags:
                        _series = self._extract_series_ID(_tag["href"])
                        if _series:
                            _SeriesData.append(_series)
                    _params["offset"] +=  _limit
                else:
                    print(f"Error: status code = {response.status_code} -> Function : LegacyGrapAllShowsOnline -> retrying in 3 Seconds")
                    time.sleep(3)
                    
            except Exception as e:
                _MoreToGrap = False
                print(e)
                

    # this converst our Sereies object so we can store it
    # this function will not sote the Chapters Data
    def ConvertSeriesToDict(self) -> None:
        _arr = []
        for _series in self.SeriesData:
            _arr.append({
                "DomainID" : _series.DomainID,
                "DomainName" : _series.DomainName,
                "Names" : _series.Names,
                "DumbArray" : _series.DumbArray
                })
        self.SeriesDataDict = _arr




    def _extract_series_ID(self, url) -> Series:
        """
        Extract series ID and name from the given URL and store them in a dictionary.
        
        Args:
            url (str): The URL to extract data from.
            
        Returns:
            dict: A dictionary with the series name as the key and the series ID as the value.
        """
        _series = Series()
        path = urlparse(url).path
        parts = path.split('/')
        if len(parts) >= 3 and parts[1] == "series":
            _series.DomainID = parts[2]
            _series.DomainName = parts[3]
            return _series
        else:
            return None


    
    def _SaveData(self):
        self.ConvertSeriesToDict()
        with open("JsonFiles/SeriesNamesToID.json", "w") as json_file:
            json.dump(self.SeriesDataDict, json_file, indent=4)
        



# you should  simply  provide the  Series ID that  you grapped
# with the NameIDGraper and this will fetch  the chapters data
# along with  the  seasons  data  and  the  pages  domain this
# function will take the Series struct as  pramater  and  fill
# it with data when you ru the function to grap the  data that
# is wanted
class SeriesDataGraper:
    def __init__(self, series:Series=None)-> None:
        self.Series = series


        self.filler_1 = "/chapter-select?current_chapter=none&current_page=None" # the domain needs to give the Series chapters data

    
    def GrapSeriesInfo(self):
        _url = Constants.WEBDOMAIN + Constants.SERIESPATH + self.Series.DomainID # this methode is more effiecent than the full list method
        try:
            response = requests.get(_url)
        except Exception as e:
            print(f"Error: {e} -> Function: GrapSeriesInfo -> try request again or Domain is down or Domain changed")
        if response.status_code == 200:
            self._extractReleventData(response.text)
        else:
            print(f"Error: status code = {response.status_code} -> Function : GrapChaptersInfo -> Domain Error webpage down or Domain changed")


    def GrapChaptersInfo(self) -> None:
        _url = Constants.WEBDOMAIN + Constants.SERIESPATH + self.Series.DomainID + self.filler_1 # this methode is more effiecent than the full list method
        try:
            response = requests.get(_url)
        except Exception as e:
            print(f"Error: {e} -> Function: GrapChaptersInfo -> try request again or consider changing the filler of the request")
        
        if response.status_code == 200:
            self._extractChaptersContent(response.text)
        else:
            print(f"Error: status code = {response.status_code} -> Function : GrapChaptersInfo -> Domain Error webpage down or Domain changed")


    def GrapSeriesCover(self) -> None: # this will grab the cover image of the show
        _url = Constants.COVERIMAGEDOMAIN + Constants.COVERPATH + Constants.COVERIMAGENORMALPATH + self.Series.DomainID + Constants.COVERIMAGEEXTENTION
        try:
            response = requests.get(_url)
        except Exception as e:
            print(f"Error: {e} -> Function: GrapSeriesCover -> try request again or Domain is down or Domain changed")
        
        if response.status_code == 200:
            self.Series.CoverImage = response.content
        else:
            print(f"Error: status code = {response.status_code} -> Function : GrapChaptersInfo -> Domain Error webpage down or Domain changed")



    def _extractReleventData(self, html_text:str): # this will extract the public name, and all the other 
                                                   # names it will extract the discription as well
        soup = BeautifulSoup(html_text, "html.parser")
        sort = soup.find_all('h1')
        
        _names = []

        _names.append(sort[1].text) # this will grap name

        sort = soup.find_all('p')
        _description = sort[0].text # this graps the discription

        sort = soup.find_all('li')
        
        filtered_li = [
            li for li in sort
            if li.find('strong') and li.find('strong').text.strip() == "Associated Name(s)"
        ]
        for li in filtered_li:
            nested_items = li.find('ul').find_all('li')  # Get nested <li> elements
            for item in nested_items:
                _names.append(item.text.strip())  # this contain the Alt names
        
        # store the data now
        self.Series.Names = _names
        self.Series.Description = _description




    def _extractChaptersContent(self, html_text:str):
        soup = BeautifulSoup(html_text, "html.parser")

        _seasonDict = {
            
        }

        _chapters = []

        a_tags = soup.find_all('a')
        for _tag in a_tags[::-1]:
            _header, _link = _tag.text, _tag["href"]
            _data = _header.split(" ")
            _chapter = _data[-1]
            _seasonTag = _data[0]
            try:
                _Season = _seasonDict[_seasonTag]
            except:
                _seasonDict[_seasonTag] = len(_seasonDict) + 1
                _Season = _seasonDict[_seasonTag]

            _chapterID = int((float(_chapter) * 10) + (100000 * float(_Season))) 


            # Populate the Chapter Structure
            ChapterObject = Chapter()
            ChapterObject.ChapterID = _chapterID
            ChapterObject.Link = _link
            ChapterObject.ChapterNumber = _chapter
            ChapterObject.Season = _Season
            ChapterObject.SeasonTag = _seasonTag
            _chapters.append(ChapterObject)
        
        self.Series.Chapters = _chapters
        self.Series.DumbArray.append(_seasonDict)


# this class is  desinged  to  be  intialed once per thread you will 
# provide the chapter for this class and  run the function it has to
# grab the detial of the chapter note that this is not the installer
# installer this will be used for two things  to  get  the  chapters
# Pages domain and also to get the the number of pages
class ChaptersDataGraper:
    def __init__(self, chapter:Chapter = None):
        self.Chapter = chapter

    # this function will make the request and grap the data that is needed
    def GrapChapterInfromation(self) -> None:
        _url = self.Chapter.Link
        try:
            response = requests.get(_url)
        except Exception as e:
            print(f"Error: {e} -> Function: GrapChapterInfromation -> try request again or Domain is down or Domain changed")

        if response.status_code == 200:
            self._extractReleventData(response.text)
        else:
            print(f"Error: status code = {response.status_code} -> Function : GrapChaptersInfo -> Domain Error webpage down or Domain changed")
    
    # this function will check if the page exist for you or if you have grabed the data correctly then it will retun the page url that you asked for
    def PageUrlFromNum(self, PageNumber:int) -> str:
        if not self.Chapter.FirstPageLink:
            print("the Data has not been grabed yet consider using the 'GrapChapterInfromation()' function first")
            return
        if PageNumber > self.Chapter.PagesNumber:
            print(f"The page does not exist there is only '{self.Chapter.PagesNumber}' and you are request page '{PageNumber}' try a page from 1 to {self.Chapter.PagesNumber}")
            return

        return self._update_page_number(PageNumber)
        
    # this function will take the first page url and will change the page number on it
    def _update_page_number(self, PageNum) -> str:
        _splitedData = self.Chapter.FirstPageLink.split("/")
        _pageNameAndExtention = _splitedData[-1]
        _name, _extention = _pageNameAndExtention.split(".")
        _chapter, _pageNum = _name.split("-")
        _splitedData[-1] = f"{_chapter}-{PageNum:03}.{_extention}"
        _joinedData = "/".join(_splitedData)
        return _joinedData

    # this function is used to extract the data needed
    def _extractReleventData(self, html_text:str) -> None:
        soup = BeautifulSoup(html_text, "html.parser")
        _link = soup.find('link', {'as': 'image', 'rel': 'preload'})["href"] # find the Link of the first page

        _maxPage = re.search(Cypher.MAX_PAGE_PATTERN, html_text).group(1) # this graps the MaxPages

        # pass the varables to the chapters struct
        self.Chapter.FirstPageLink = _link
        self.Chapter.PagesNumber = int(_maxPage)



    def _getBaseUrl(self, url):
        index = url.find('/', url.find('//') + 2)
        if index != -1:
            return url[:index + 1]
        return url
