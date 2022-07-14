import asyncio

class TaskManager():
    def __init__(self, searchRequests, pages, sorting, saveTime) -> None:
        self.searchRequests = searchRequests
        self.pages = pages
        self.sorting = sorting
        self.saveTime = saveTime

    def start(self):
        pass