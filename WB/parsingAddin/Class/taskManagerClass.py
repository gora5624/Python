import multiprocessing
if __name__ == '__main__':
    from parserClass import Parser
else:
    from Class.parserClass import Parser


class TaskManager():
    def __init__(self, searchRequests, pages, sorting, saveTime) -> None:
        self.searchRequests = searchRequests
        self.pages = pages
        self.sorting = sorting
        self.saveTime = saveTime

    def start(self):
        # pool = multiprocessing.Pool()
        # for searchRequest in self.searchRequests:
        #     pool.apply_async(self.parsingSearchRequest, args=(searchRequest,))
        # pool.close()
        # pool.join()
        for searchRequest in self.searchRequests:
            self.parsingSearchRequest(searchRequest)

    
    def parsingSearchRequest(self, searchRequest):
        parser = Parser(searchRequest, self.sorting, self.pages)
        parser.parserMain()