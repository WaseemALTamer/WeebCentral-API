



class Series:
    def __init__(self):
        self.DomainID:str = None
        self.DomainName:str = None
        self.Names:list[str] = [] 
        self.Chapters:list[Chapter] = []
        self.DumbArray:list[dict|str] = []
        self.CoverImage:bytes = None
        self.Description:str = None



class Chapter:
    def __init__(self):
        self.ChapterID:int = None
        self.ChapterNumber:float|int = None
        self.SeasonTag:str = None
        self.Season:int = None
        self.Link:str = None
        self.PagesNumber:int = None
        self.FirstPageLink:str = None
        self.FirstPageQickLink:str = None
        self.Date:str = None
