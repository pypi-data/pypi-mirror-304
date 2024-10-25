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
import builtins
import logging
class bstack11lll1l1ll_opy_:
    def __init__(self, handler):
        self._111lll1111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111ll1llll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111llll_opy_ (u"ࠧࡪࡰࡩࡳࠬ࿎"), bstack111llll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧ࿏"), bstack111llll_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪ࿐"), bstack111llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ࿑")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111ll1ll11_opy_
        self._111ll1ll1l_opy_()
    def _111ll1ll11_opy_(self, *args, **kwargs):
        self._111lll1111_opy_(*args, **kwargs)
        message = bstack111llll_opy_ (u"ࠫࠥ࠭࿒").join(map(str, args)) + bstack111llll_opy_ (u"ࠬࡢ࡮ࠨ࿓")
        self._log_message(bstack111llll_opy_ (u"࠭ࡉࡏࡈࡒࠫ࿔"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭࿕"): level, bstack111llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿖"): msg})
    def _111ll1ll1l_opy_(self):
        for level, bstack111lll111l_opy_ in self._111ll1llll_opy_.items():
            setattr(logging, level, self._111ll1lll1_opy_(level, bstack111lll111l_opy_))
    def _111ll1lll1_opy_(self, level, bstack111lll111l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111lll111l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111lll1111_opy_
        for level, bstack111lll111l_opy_ in self._111ll1llll_opy_.items():
            setattr(logging, level, bstack111lll111l_opy_)