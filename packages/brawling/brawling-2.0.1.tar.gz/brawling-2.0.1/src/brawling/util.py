from enum import Enum

__all__ = [
    "catching",
    "RequestPaginator",
    "AsyncRequestPaginator",
    "BrawlerID"
]

class catching:
    def __init__(self, on_error: str = None) -> None:
        self.success = None
        self.on_error = on_error

    def __enter__(self):
        self.success = True

    def __exit__(self, type_, value, traceback_):
        self.success = False
        if self.on_error:
            print(self.on_error)
            print(value)
        return True

class RequestPaginator:
    def __init__(self, client, url: str, per_page: int, limit: int, cls_factory):
        self.client = client
        self.url = url
        self.per_page = per_page
        self.cls = cls_factory
        self.done = 0
        self.limit = limit

    def __iter__(self):
        marker = None
        while True:
            if self.limit != 0 and self.done >= self.limit:
                break

            params = {
                "limit": self.per_page
            }

            if marker:
                params["after"] = marker

            page = self.client.get(self.url, params)

            # im lazy
            if type(page).__name__.endswith('ErrorResponse'):
                return page

            items = self.client._unwrap_list(page["items"], self.cls)
            if len(items) == 0:
                break

            self.done += len(items)
            if self.limit != 0 and self.done > self.limit:
                diff = self.done - self.limit
                items = items[:-diff]

            marker = page["paging"]["cursors"].get("after", None)

            yield items

            if marker is None:
                break

class AsyncRequestPaginator(RequestPaginator):
    def __init__(self, client, url: str, per_page: int, limit: int, cls_factory):
        super().__init__(client, url, per_page, limit, cls_factory)

    def __aiter__(self):
        self.marker = None
        self.reqstop = False
        return self

    async def __anext__(self):
        if self.reqstop or (self.limit != 0 and self.done >= self.limit):
            raise StopAsyncIteration

        params = {
            "limit": self.per_page
        }

        if self.marker:
            params["after"] = self.marker

        page = await self.client.get(self.url, params)

        # im lazy
        if type(page).__name__.endswith('ErrorResponse'):
            self.reqstop = True
            return page

        items = self.client._unwrap_list(page["items"], self.cls)
        if len(items) == 0:
            raise StopAsyncIteration

        self.done += len(items)
        if self.limit != 0 and self.done > self.limit:
            diff = self.done - self.limit
            items = items[:-diff]

        self.marker = page["paging"]["cursors"].get("after", None)
        if self.marker is None:
            self.reqstop = True

        return items


# Might not be always up to date
class BrawlerID(Enum):
    SHELLY = 16000000
    COLT = 16000001
    BULL = 16000002
    BROCK = 16000003
    RICO = 16000004
    SPIKE = 16000005
    BARLEY = 16000006
    JESSIE = 16000007
    NITA = 16000008
    DYNAMIKE = 16000009
    EL_PRIMO = 16000010
    MORTIS = 16000011
    CROW = 16000012
    POCO = 16000013
    BO = 16000014
    PIPER = 16000015
    PAM = 16000016
    TARA = 16000017
    DARRYL = 16000018
    PENNY = 16000019
    FRANK = 16000020
    GENE = 16000021
    TICK = 16000022
    LEON = 16000023
    ROSA = 16000024
    CARL = 16000025
    BIBI = 16000026
    # This is 8bit but you can't make a variable starting with a number lol
    _8BIT = 16000027
    SANDY = 16000028
    BEA = 16000029
    EMZ = 16000030
    MR_P = 16000031
    MAX = 16000032
    JACKY = 16000034
    GALE = 16000035
    NANI = 16000036
    SPROUT = 16000037
    SURGE = 16000038
    COLETTE = 16000039
    AMBER = 16000040
    LOU = 16000041
    BYRON = 16000042
    EDGAR = 16000043
    RUFFS = 16000044
    STU = 16000045
    BELLE = 16000046
    SQUEAK = 16000047
    GROM = 16000048
    BUZZ = 16000049
    GRIFF = 16000050
    ASH = 16000051
    MEG = 16000052
    LOLA = 16000053
    FANG = 16000054
    EVE = 16000056
    JANET = 16000057
    BONNIE = 16000058
    OTIS = 16000059
    SAM = 16000060
    GUS = 16000061
    BUSTER = 16000062
    CHESTER = 16000063
    GRAY = 16000064
    MANDY = 16000065
    R_T = 16000066
    WILLOW = 16000067
