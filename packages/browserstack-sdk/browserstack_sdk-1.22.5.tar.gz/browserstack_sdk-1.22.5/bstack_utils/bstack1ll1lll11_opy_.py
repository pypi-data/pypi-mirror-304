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
import logging
import bstack_utils.bstack1lll111l11_opy_ as bstack1l1111ll_opy_
from bstack_utils.helper import bstack1llll11l1l_opy_
logger = logging.getLogger(__name__)
def bstack1l111111l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1ll1lll1l_opy_(context, *args):
    tags = getattr(args[0], bstack111llll_opy_ (u"ࠬࡺࡡࡨࡵࠪ࿅"), [])
    bstack1l111ll1l_opy_ = bstack1l1111ll_opy_.bstack11111ll1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l111ll1l_opy_
    try:
      bstack1ll1ll111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111111l_opy_(bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶ࿆ࠬ")) else context.browser
      if bstack1ll1ll111l_opy_ and bstack1ll1ll111l_opy_.session_id and bstack1l111ll1l_opy_ and bstack1llll11l1l_opy_(
              threading.current_thread(), bstack111llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿇"), None):
          threading.current_thread().isA11yTest = bstack1l1111ll_opy_.bstack11llllll11_opy_(bstack1ll1ll111l_opy_, bstack1l111ll1l_opy_)
    except Exception as e:
       logger.debug(bstack111llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ࿈").format(str(e)))
def bstack11111l1l1_opy_(bstack1ll1ll111l_opy_):
    if bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭࿉"), None) and bstack1llll11l1l_opy_(
      threading.current_thread(), bstack111llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ࿊"), None) and not bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧ࿋"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1111ll_opy_.bstack11l1ll1l_opy_(bstack1ll1ll111l_opy_, name=bstack111llll_opy_ (u"ࠧࠨ࿌"), path=bstack111llll_opy_ (u"ࠨࠢ࿍"))