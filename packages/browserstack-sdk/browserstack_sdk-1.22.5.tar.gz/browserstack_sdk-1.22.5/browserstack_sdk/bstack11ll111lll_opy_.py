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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11l11lll11_opy_, bstack11l1l11111_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l11lll11_opy_ = bstack11l11lll11_opy_
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11ll111l1l_opy_(bstack11l11ll1ll_opy_):
        bstack11l11ll11l_opy_ = []
        if bstack11l11ll1ll_opy_:
            tokens = str(os.path.basename(bstack11l11ll1ll_opy_)).split(bstack111llll_opy_ (u"ࠥࡣࠧ໿"))
            camelcase_name = bstack111llll_opy_ (u"ࠦࠥࠨༀ").join(t.title() for t in tokens)
            suite_name, bstack11l11ll111_opy_ = os.path.splitext(camelcase_name)
            bstack11l11ll11l_opy_.append(suite_name)
        return bstack11l11ll11l_opy_
    @staticmethod
    def bstack11l11ll1l1_opy_(typename):
        if bstack111llll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ༁") in typename:
            return bstack111llll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ༂")
        return bstack111llll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ༃")