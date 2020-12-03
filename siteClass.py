class Website:
    def __init__(self, title, description, url, content="", oLinks = ""):
        self.title = title
        self.description = description
        self.url = url
        self._content = content
        self._oLinks = oLinks

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def oLinks(self):
        return self._oLinks

    @oLinks.setter
    def oLinks(self, value):
        self._oLinks = value

    def function(self):
        print("Title: "+ self.title)
        print("\nDescription: " + self.description)
        print("\nURL = " + self.url)
        print("\ncontent = " + self.content)
        print("\nlinks = {}".format(self.oLinks))


# site1 = Website("Angels", "urlurl")
