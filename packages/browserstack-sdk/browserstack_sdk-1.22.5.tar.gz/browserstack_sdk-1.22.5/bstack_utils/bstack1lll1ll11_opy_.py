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
import logging
import os
import threading
from bstack_utils.helper import bstack1l11ll1lll_opy_
from bstack_utils.constants import bstack111ll11l1l_opy_
logger = logging.getLogger(__name__)
class bstack1l1lll1111_opy_:
    bstack1lll111111l_opy_ = None
    @classmethod
    def bstack1l1ll11l1_opy_(cls):
        if cls.on():
            logger.info(
                bstack111llll_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ᝻").format(os.environ[bstack111llll_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧ᝼")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨ᝽"), None) is None or os.environ[bstack111llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩ᝾")] == bstack111llll_opy_ (u"ࠤࡱࡹࡱࡲࠢ᝿"):
            return False
        return True
    @classmethod
    def bstack1ll11lll1ll_opy_(cls, bs_config, framework=bstack111llll_opy_ (u"ࠥࠦក")):
        if framework == bstack111llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫខ"):
            return bstack1l11ll1lll_opy_(bs_config.get(bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩគ")))
        bstack1ll11ll1lll_opy_ = framework in bstack111ll11l1l_opy_
        return bstack1l11ll1lll_opy_(bs_config.get(bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪឃ"), bstack1ll11ll1lll_opy_))
    @classmethod
    def bstack1ll11ll1l1l_opy_(cls, framework):
        return framework in bstack111ll11l1l_opy_
    @classmethod
    def bstack1ll1l1ll11l_opy_(cls, bs_config, framework):
        return cls.bstack1ll11lll1ll_opy_(bs_config, framework) is True and cls.bstack1ll11ll1l1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫង"), None)
    @staticmethod
    def bstack11lll1l111_opy_():
        if getattr(threading.current_thread(), bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬច"), None):
            return {
                bstack111llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧឆ"): bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࠨជ"),
                bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫឈ"): getattr(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩញ"), None)
            }
        if getattr(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪដ"), None):
            return {
                bstack111llll_opy_ (u"ࠧࡵࡻࡳࡩࠬឋ"): bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ឌ"),
                bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩឍ"): getattr(threading.current_thread(), bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧណ"), None)
            }
        return None
    @staticmethod
    def bstack1ll11ll11ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lll1111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11ll111l1l_opy_(test, hook_name=None):
        bstack1ll11ll1l11_opy_ = test.parent
        if hook_name in [bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩត"), bstack111llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ថ"), bstack111llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬទ"), bstack111llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩធ")]:
            bstack1ll11ll1l11_opy_ = test
        scope = []
        while bstack1ll11ll1l11_opy_ is not None:
            scope.append(bstack1ll11ll1l11_opy_.name)
            bstack1ll11ll1l11_opy_ = bstack1ll11ll1l11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll11ll1ll1_opy_(hook_type):
        if hook_type == bstack111llll_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨន"):
            return bstack111llll_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨប")
        elif hook_type == bstack111llll_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢផ"):
            return bstack111llll_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦព")
    @staticmethod
    def bstack1ll11lll111_opy_(bstack1l1l11l1ll_opy_):
        try:
            if not bstack1l1lll1111_opy_.on():
                return bstack1l1l11l1ll_opy_
            if os.environ.get(bstack111llll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥភ"), None) == bstack111llll_opy_ (u"ࠨࡴࡳࡷࡨࠦម"):
                tests = os.environ.get(bstack111llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦយ"), None)
                if tests is None or tests == bstack111llll_opy_ (u"ࠣࡰࡸࡰࡱࠨរ"):
                    return bstack1l1l11l1ll_opy_
                bstack1l1l11l1ll_opy_ = tests.split(bstack111llll_opy_ (u"ࠩ࠯ࠫល"))
                return bstack1l1l11l1ll_opy_
        except Exception as exc:
            print(bstack111llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦវ"), str(exc))
        return bstack1l1l11l1ll_opy_