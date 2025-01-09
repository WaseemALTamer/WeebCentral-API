```python
from API import NamesIDGraper, SeriesDataGraper, ChaptersDataGraper
```


```python

# this will search the data base this relies on the weebcentral Search Function
# this will return the series in stucture you can  view  the  "Series" stucture
# in the Stucture.py file.
Searcher = NamesIDGraper() # this will only get the domain id and the domain name
_series = Searcher.SearchSeriesOnline("dr.stone")

for _s in _series:
    print(_s.__dict__)
```

    {'DomainID': '01J76XYC1GAF2FWQ59Q0Y17TPA', 'DomainName': 'Dr-Stone', 'Names': [], 'Chapters': [], 'DumbArray': [], 'CoverImage': None, 'Description': None}
    {'DomainID': '01J76XY8NKJ7V60598350EEYW8', 'DomainName': 'Stone-Ocean', 'Names': [], 'Chapters': [], 'DumbArray': [], 'CoverImage': None, 'Description': None}
    {'DomainID': '01J76XYBQB0VY5GTAQFMN3CJ9H', 'DomainName': 'Livingstone', 'Names': [], 'Chapters': [], 'DumbArray': [], 'CoverImage': None, 'Description': None}
    {'DomainID': '01J76XYD7HNZG7GSXBRWYG4CNQ', 'DomainName': 'Dr-Stone-Reboot-Byakuya', 'Names': [], 'Chapters': [], 'DumbArray': [], 'CoverImage': None, 'Description': None}
    


```python
# if you want the data of specific seires name after searching for it you can simpy 
# just access it spereitly

print(_series[0].DomainName)
print(_series[0].DomainID)
```

    Dr-Stone
    01J76XYC1GAF2FWQ59Q0Y17TPA
    


```python
# if you want to grab all the Series from the data base  names  and ids
# you there is a function for that as well dont use the legacy function
# because that is ineffecient only use it if this function breaks

Searcher.GrapAllSeriesOnline() # this will store the results on SeriesData var
len(Searcher.SeriesData) # this will show the number of series found
```




    8600




```python
# assume you found the series that you want the data from  _my_series
# will assume that it is that series that you want we will go forward
# and populate the series based on what you need

# this cell will assume that you want general data

_my_series = _series[0]

DataGraber = SeriesDataGraper() # this class will grab the relevent information for you
                                # note that this will not get the tags authers but they
                                # might be implemented for the futuer

DataGraber.Series = _my_series # give the class access to the Series struct that contain
                               # the Series DomainID and it only needs  the  DomainID to
                               # grab the information

DataGraber.GrapSeriesInfo() # this will grab the names and discription
DataGraber.GrapChaptersInfo() # this will grab the Chapter info
DataGraber.GrapSeriesCover() # this will grab the cover image of the series

print(f"Names found:{_my_series.Names}")
print(f"Chapters found: {len(_my_series.Chapters)}")
print(f"Description:{_my_series.Description}")
print(f"CoverImageSize: {len(_my_series.CoverImage)}")
print(f"Other Info: {_my_series.DumbArray}") # this mainly contain the seasons tag and which season it is

```

    Names found:['Dr. STONE']
    Chapters found: 235
    Description:One day Ooki Taiju builds his courage to confesses to Yuzuriha, the girl he loves, when the sky is filled with a strange light. Everyone touched by that light is turned to stone. After a thousands years trapped in stone, he breaks out of his shell and starts to explore the world until he finds his old friend Senku, who was freed from his stone state half a year ago.
    
    Taiju and Senku decide to team up and bring back the now lost human civilization, starting by investigating the true nature of the light that turned them all to stone thousands of years ago and how to fix the situation.
    CoverImageSize: 61694
    Other Info: [{'Z=': 1, 'Ex': 2}, {'Z=': 1, 'Ex': 2}]
    


```python
# now that you got you series chapters you want to grab the information for that chapter
# now you can use the ChaptersDataGraper class to do that for you same way you  got  the
# information for the series we can now get the infromation for  the  chapter  we assume
# that  _my_Cahtper is your chapter that you want to get the information for


_my_Cahtper = _my_series.Chapters[0]

DataGraber = ChaptersDataGraper() # this  will  grab  the  data  for you of the  chapter
                                  # the chapter will comes   with   its   own  DomainId,  
                                  # ChapterNumber,  SeasonTag, Link, and  Season  Number
                                  # this information is filled when you run the function 
                                  # SeriesDataGraper.GrapChaptersInfo()

DataGraber.Chapter = _my_Cahtper # pass the chapter to the class

DataGraber.GrapChapterInfromation() # get the rest of the information this will mostly
                                    # get you the number  of  pages  the  chapter  has
                                    # and the link for the first image

_my_Cahtper.__dict__
```




    {'ChapterID': 100010,
     'ChapterNumber': '1',
     'SeasonTag': 'Z=',
     'Season': 1,
     'Link': 'https://weebcentral.com/chapters/01J76XYYHDJ12SRYE8YP1JQF10',
     'PagesNumber': 53,
     'FirstPageLink': 'https://official.lowee.us/manga/Dr-Stone/0001-001.png'}


