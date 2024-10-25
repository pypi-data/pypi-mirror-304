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
from collections import deque
from bstack_utils.constants import *
class bstack1l1ll1l111_opy_:
    def __init__(self):
        self._1lll1l11l1l_opy_ = deque()
        self._1lll11lllll_opy_ = {}
        self._1lll1l11ll1_opy_ = False
    def bstack1lll1l1l111_opy_(self, test_name, bstack1lll1l111l1_opy_):
        bstack1lll1l1l1ll_opy_ = self._1lll11lllll_opy_.get(test_name, {})
        return bstack1lll1l1l1ll_opy_.get(bstack1lll1l111l1_opy_, 0)
    def bstack1lll1l1ll11_opy_(self, test_name, bstack1lll1l111l1_opy_):
        bstack1lll1l1ll1l_opy_ = self.bstack1lll1l1l111_opy_(test_name, bstack1lll1l111l1_opy_)
        self.bstack1lll1l11lll_opy_(test_name, bstack1lll1l111l1_opy_)
        return bstack1lll1l1ll1l_opy_
    def bstack1lll1l11lll_opy_(self, test_name, bstack1lll1l111l1_opy_):
        if test_name not in self._1lll11lllll_opy_:
            self._1lll11lllll_opy_[test_name] = {}
        bstack1lll1l1l1ll_opy_ = self._1lll11lllll_opy_[test_name]
        bstack1lll1l1ll1l_opy_ = bstack1lll1l1l1ll_opy_.get(bstack1lll1l111l1_opy_, 0)
        bstack1lll1l1l1ll_opy_[bstack1lll1l111l1_opy_] = bstack1lll1l1ll1l_opy_ + 1
    def bstack1l11ll11_opy_(self, bstack1lll1l1111l_opy_, bstack1lll1l11111_opy_):
        bstack1lll1l111ll_opy_ = self.bstack1lll1l1ll11_opy_(bstack1lll1l1111l_opy_, bstack1lll1l11111_opy_)
        bstack1lll1l11l11_opy_ = bstack111ll1l11l_opy_[bstack1lll1l11111_opy_]
        bstack1lll1l1l11l_opy_ = bstack111llll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᖇ").format(bstack1lll1l1111l_opy_, bstack1lll1l11l11_opy_, bstack1lll1l111ll_opy_)
        self._1lll1l11l1l_opy_.append(bstack1lll1l1l11l_opy_)
    def bstack11l11111_opy_(self):
        return len(self._1lll1l11l1l_opy_) == 0
    def bstack1lll111111_opy_(self):
        bstack1lll1l1l1l1_opy_ = self._1lll1l11l1l_opy_.popleft()
        return bstack1lll1l1l1l1_opy_
    def capturing(self):
        return self._1lll1l11ll1_opy_
    def bstack1l1ll1ll1l_opy_(self):
        self._1lll1l11ll1_opy_ = True
    def bstack1l11ll1l_opy_(self):
        self._1lll1l11ll1_opy_ = False