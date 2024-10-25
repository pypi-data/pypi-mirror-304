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
from browserstack_sdk.bstack1l11lll1ll_opy_ import bstack1l111ll11l_opy_
from browserstack_sdk.bstack11ll111lll_opy_ import RobotHandler
def bstack1l11l11l1l_opy_(framework):
    if framework.lower() == bstack111llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨኮ"):
        return bstack1l111ll11l_opy_.version()
    elif framework.lower() == bstack111llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨኯ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪኰ"):
        import behave
        return behave.__version__
    else:
        return bstack111llll_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࠬ኱")