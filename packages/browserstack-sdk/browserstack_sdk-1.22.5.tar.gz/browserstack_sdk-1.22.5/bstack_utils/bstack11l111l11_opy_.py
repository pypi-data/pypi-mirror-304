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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111llll11l_opy_, bstack11111ll11_opy_, get_host_info, bstack11111l1lll_opy_, \
 bstack1ll111ll1l_opy_, bstack1llll11l1l_opy_, bstack11ll1ll111_opy_, bstack1111111l1l_opy_, bstack1ll1llllll_opy_
import bstack_utils.bstack1lll111l11_opy_ as bstack1l1111ll_opy_
from bstack_utils.bstack1lll1ll11_opy_ import bstack1l1lll1111_opy_
from bstack_utils.percy import bstack111llllll_opy_
from bstack_utils.config import Config
bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack111llllll_opy_()
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll1l1l1ll1_opy_(bs_config, bstack1111ll1l_opy_):
  try:
    data = {
        bstack111llll_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ᜿"): bstack111llll_opy_ (u"ࠩ࡭ࡷࡴࡴࠧᝀ"),
        bstack111llll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩᝁ"): bs_config.get(bstack111llll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᝂ"), bstack111llll_opy_ (u"ࠬ࠭ᝃ")),
        bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝄ"): bs_config.get(bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᝅ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᝆ"): bs_config.get(bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᝇ")),
        bstack111llll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᝈ"): bs_config.get(bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᝉ"), bstack111llll_opy_ (u"ࠬ࠭ᝊ")),
        bstack111llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᝋ"): bstack1ll1llllll_opy_(),
        bstack111llll_opy_ (u"ࠧࡵࡣࡪࡷࠬᝌ"): bstack11111l1lll_opy_(bs_config),
        bstack111llll_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫᝍ"): get_host_info(),
        bstack111llll_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪᝎ"): bstack11111ll11_opy_(),
        bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᝏ"): os.environ.get(bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᝐ")),
        bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪᝑ"): os.environ.get(bstack111llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫᝒ"), False),
        bstack111llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩᝓ"): bstack111llll11l_opy_(),
        bstack111llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᝔"): bstack1ll11llll11_opy_(),
        bstack111llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭᝕"): bstack1ll1l11111l_opy_(bstack1111ll1l_opy_),
        bstack111llll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ᝖"): bstack1l1l1l1l_opy_(bs_config, bstack1111ll1l_opy_.get(bstack111llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ᝗"), bstack111llll_opy_ (u"ࠬ࠭᝘"))),
        bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᝙"): bstack1ll111ll1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack111llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ᝚").format(str(error)))
    return None
def bstack1ll1l11111l_opy_(framework):
  return {
    bstack111llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ᝛"): framework.get(bstack111llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ᝜"), bstack111llll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ᝝")),
    bstack111llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᝞"): framework.get(bstack111llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᝟")),
    bstack111llll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᝠ"): framework.get(bstack111llll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᝡ")),
    bstack111llll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᝢ"): bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᝣ"),
    bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᝤ"): framework.get(bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᝥ"))
  }
def bstack1l1l1l1l_opy_(bs_config, framework):
  bstack1l1l11lll1_opy_ = False
  bstack1lll1l1l1_opy_ = False
  if bstack111llll_opy_ (u"ࠬࡧࡰࡱࠩᝦ") in bs_config:
    bstack1l1l11lll1_opy_ = True
  else:
    bstack1lll1l1l1_opy_ = True
  bstack1llll11l_opy_ = {
    bstack111llll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᝧ"): bstack1l1lll1111_opy_.bstack1ll11lll1ll_opy_(bs_config, framework),
    bstack111llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝨ"): bstack1l1111ll_opy_.bstack111lllll1l_opy_(bs_config),
    bstack111llll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᝩ"): bs_config.get(bstack111llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᝪ"), False),
    bstack111llll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᝫ"): bstack1lll1l1l1_opy_,
    bstack111llll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᝬ"): bstack1l1l11lll1_opy_
  }
  return bstack1llll11l_opy_
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll11llll11_opy_():
  try:
    bstack1ll11lllll1_opy_ = json.loads(os.getenv(bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᝭"), bstack111llll_opy_ (u"࠭ࡻࡾࠩᝮ")))
    return {
        bstack111llll_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᝯ"): bstack1ll11lllll1_opy_
    }
  except Exception as error:
    logger.error(bstack111llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢᝰ").format(str(error)))
    return {}
def bstack1ll1l1ll111_opy_(array, bstack1ll11llllll_opy_, bstack1ll11lll1l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll11llllll_opy_]
    result[key] = o[bstack1ll11lll1l1_opy_]
  return result
def bstack1ll1l11ll11_opy_(bstack11ll1lll1_opy_=bstack111llll_opy_ (u"ࠩࠪ᝱")):
  bstack1ll1l111111_opy_ = bstack1l1111ll_opy_.on()
  bstack1ll11llll1l_opy_ = bstack1l1lll1111_opy_.on()
  bstack1ll11lll11l_opy_ = percy.bstack1llll111l_opy_()
  if bstack1ll11lll11l_opy_ and not bstack1ll11llll1l_opy_ and not bstack1ll1l111111_opy_:
    return bstack11ll1lll1_opy_ not in [bstack111llll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᝲ"), bstack111llll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᝳ")]
  elif bstack1ll1l111111_opy_ and not bstack1ll11llll1l_opy_:
    return bstack11ll1lll1_opy_ not in [bstack111llll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᝴"), bstack111llll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᝵"), bstack111llll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ᝶")]
  return bstack1ll1l111111_opy_ or bstack1ll11llll1l_opy_ or bstack1ll11lll11l_opy_
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll1l11lll1_opy_(bstack11ll1lll1_opy_, test=None):
  bstack1ll1l1111l1_opy_ = bstack1l1111ll_opy_.on()
  if not bstack1ll1l1111l1_opy_ or bstack11ll1lll1_opy_ not in [bstack111llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ᝷")] or test == None:
    return None
  return {
    bstack111llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᝸"): bstack1ll1l1111l1_opy_ and bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᝹"), None) == True and bstack1l1111ll_opy_.bstack11111ll1_opy_(test[bstack111llll_opy_ (u"ࠫࡹࡧࡧࡴࠩ᝺")])
  }