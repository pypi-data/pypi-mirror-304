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
class bstack1lll1l1ll1_opy_:
    def __init__(self, handler):
        self._1ll1llll1ll_opy_ = None
        self.handler = handler
        self._1ll1llll1l1_opy_ = self.bstack1ll1lllll1l_opy_()
        self.patch()
    def patch(self):
        self._1ll1llll1ll_opy_ = self._1ll1llll1l1_opy_.execute
        self._1ll1llll1l1_opy_.execute = self.bstack1ll1lllll11_opy_()
    def bstack1ll1lllll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣᗡ"), driver_command, None, this, args)
            response = self._1ll1llll1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111llll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣᗢ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1llll1l1_opy_.execute = self._1ll1llll1ll_opy_
    @staticmethod
    def bstack1ll1lllll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver