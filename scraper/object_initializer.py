class Tourney:
    def __init__(self):
        self.date = None
        self.time = None
        self.title = None
        self.entry = None
        self.region = None
        self.platforms = None
        self.game = None
        self.requirements = None
        self.skill = None
        self.url = None
    
    def set_date(self, date):
        self.date = date
    
    def set_time(self, time):
        self.time = time

    def set_title(self, title):
        self.title = title

    def set_entry(self, entry):
        self.entry = entry

    def set_region(self, region):
        self.region = region

    def set_platforms(self, platforms):
        self.platforms = platforms

    def set_game(self, game):
        self.game = game

    def set_requirements(self, requirements):
        self.requirements = requirements

    def set_skill(self, skill):
        self.skill = skill

    def set_url(self, url):
        self.url = url
