# coding: UTF-8
import sys
bstack111l1_opy_ = sys.version_info [0] == 2
bstack1ll11ll_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack111llll_opy_ (bstack11lll1l_opy_):
    global bstack111111_opy_
    bstack1ll1l_opy_ = ord (bstack11lll1l_opy_ [-1])
    bstack11_opy_ = bstack11lll1l_opy_ [:-1]
    bstack11l11l1_opy_ = bstack1ll1l_opy_ % len (bstack11_opy_)
    bstack1l1llll_opy_ = bstack11_opy_ [:bstack11l11l1_opy_] + bstack11_opy_ [bstack11l11l1_opy_:]
    if bstack111l1_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11ll_opy_ - (bstack11l1_opy_ + bstack1ll1l_opy_) % bstack1l11111_opy_) for bstack11l1_opy_, char in enumerate (bstack1l1llll_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack1ll11ll_opy_ - (bstack11l1_opy_ + bstack1ll1l_opy_) % bstack1l11111_opy_) for bstack11l1_opy_, char in enumerate (bstack1l1llll_opy_)])
    return eval (bstack1l1_opy_)
import threading
bstack1ll1llllll1_opy_ = 1000
bstack1lll11111ll_opy_ = 5
bstack1lll111l111_opy_ = 30
bstack1lll1111ll1_opy_ = 2
class bstack1lll11111l1_opy_:
    def __init__(self, handler, bstack1lll1111lll_opy_=bstack1ll1llllll1_opy_, bstack1lll1111l1l_opy_=bstack1lll11111ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll1111lll_opy_ = bstack1lll1111lll_opy_
        self.bstack1lll1111l1l_opy_ = bstack1lll1111l1l_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1ll1lllllll_opy_()
    def bstack1ll1lllllll_opy_(self):
        self.timer = threading.Timer(self.bstack1lll1111l1l_opy_, self.bstack1lll111l11l_opy_)
        self.timer.start()
    def bstack1lll1111l11_opy_(self):
        self.timer.cancel()
    def bstack1lll1111111_opy_(self):
        self.bstack1lll1111l11_opy_()
        self.bstack1ll1lllllll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll1111lll_opy_:
                t = threading.Thread(target=self.bstack1lll111l11l_opy_)
                t.start()
                self.bstack1lll1111111_opy_()
    def bstack1lll111l11l_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lll1111lll_opy_]
        del self.queue[:self.bstack1lll1111lll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lll1111l11_opy_()
        while len(self.queue) > 0:
            self.bstack1lll111l11l_opy_()