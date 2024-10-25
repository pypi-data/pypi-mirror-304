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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l11l1ll1_opy_ as bstack11l1111l11_opy_
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1l111l_opy_
from bstack_utils.helper import bstack1ll1llllll_opy_, bstack11l1ll11l1_opy_, bstack1ll111ll1l_opy_, bstack11l1111111_opy_, bstack111llll1ll_opy_, bstack11111ll11_opy_, get_host_info, bstack111llll11l_opy_, bstack1l1ll1l1l1_opy_, bstack11ll1ll111_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11ll1ll111_opy_(class_method=False)
def _11l111l11l_opy_(driver, bstack11l11lll1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111llll_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩ༄"): caps.get(bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ༅"), None),
        bstack111llll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ༆"): bstack11l11lll1l_opy_.get(bstack111llll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ༇"), None),
        bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫ༈"): caps.get(bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ༉"), None),
        bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ༊"): caps.get(bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ་"), None)
    }
  except Exception as error:
    logger.debug(bstack111llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭༌") + str(error))
  return response
def on():
    if os.environ.get(bstack111llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ།"), None) is None or os.environ[bstack111llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ༎")] == bstack111llll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ༏"):
        return False
    return True
def bstack111lllll1l_opy_(config):
  return config.get(bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭༐"), False) or any([p.get(bstack111llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༑"), False) == True for p in config.get(bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ༒"), [])])
def bstack1l111l11_opy_(config, bstack1lll1l1ll_opy_):
  try:
    if not bstack1ll111ll1l_opy_(config):
      return False
    bstack111llllll1_opy_ = config.get(bstack111llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ༓"), False)
    if int(bstack1lll1l1ll_opy_) < len(config.get(bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭༔"), [])) and config[bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༕")][bstack1lll1l1ll_opy_]:
      bstack11l11l1111_opy_ = config[bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ༖")][bstack1lll1l1ll_opy_].get(bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭༗"), None)
    else:
      bstack11l11l1111_opy_ = config.get(bstack111llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ༘ࠧ"), None)
    if bstack11l11l1111_opy_ != None:
      bstack111llllll1_opy_ = bstack11l11l1111_opy_
    bstack11l11l1lll_opy_ = os.getenv(bstack111llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙༙࠭")) is not None and len(os.getenv(bstack111llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ༚"))) > 0 and os.getenv(bstack111llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ༛")) != bstack111llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ༜")
    return bstack111llllll1_opy_ and bstack11l11l1lll_opy_
  except Exception as error:
    logger.debug(bstack111llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ༝") + str(error))
  return False
def bstack11111ll1_opy_(test_tags):
  bstack11l11l11ll_opy_ = os.getenv(bstack111llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ༞"))
  if bstack11l11l11ll_opy_ is None:
    return True
  bstack11l11l11ll_opy_ = json.loads(bstack11l11l11ll_opy_)
  try:
    include_tags = bstack11l11l11ll_opy_[bstack111llll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ༟")] if bstack111llll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭༠") in bstack11l11l11ll_opy_ and isinstance(bstack11l11l11ll_opy_[bstack111llll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ༡")], list) else []
    exclude_tags = bstack11l11l11ll_opy_[bstack111llll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ༢")] if bstack111llll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ༣") in bstack11l11l11ll_opy_ and isinstance(bstack11l11l11ll_opy_[bstack111llll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ༤")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨ༥") + str(error))
  return False
def bstack11l11l11l1_opy_(config, bstack11l111ll1l_opy_, bstack11l1111lll_opy_, bstack11l111llll_opy_):
  bstack111llll1l1_opy_ = bstack11l1111111_opy_(config)
  bstack11l111l111_opy_ = bstack111llll1ll_opy_(config)
  if bstack111llll1l1_opy_ is None or bstack11l111l111_opy_ is None:
    logger.error(bstack111llll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ༦"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ༧"), bstack111llll_opy_ (u"ࠩࡾࢁࠬ༨")))
    data = {
        bstack111llll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ༩"): config[bstack111llll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ༪")],
        bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ༫"): config.get(bstack111llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ༬"), os.path.basename(os.getcwd())),
        bstack111llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪ༭"): bstack1ll1llllll_opy_(),
        bstack111llll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭༮"): config.get(bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ༯"), bstack111llll_opy_ (u"ࠪࠫ༰")),
        bstack111llll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ༱"): {
            bstack111llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ༲"): bstack11l111ll1l_opy_,
            bstack111llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ༳"): bstack11l1111lll_opy_,
            bstack111llll_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ༴"): __version__,
            bstack111llll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ༵ࠪ"): bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ༶"),
            bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭༷ࠪ"): bstack111llll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭༸"),
            bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲ༹ࠬ"): bstack11l111llll_opy_
        },
        bstack111llll_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ༺"): settings,
        bstack111llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨ༻"): bstack111llll11l_opy_(),
        bstack111llll_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨ༼"): bstack11111ll11_opy_(),
        bstack111llll_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫ༽"): get_host_info(),
        bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ༾"): bstack1ll111ll1l_opy_(config)
    }
    headers = {
        bstack111llll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ༿"): bstack111llll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨཀ"),
    }
    config = {
        bstack111llll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫཁ"): (bstack111llll1l1_opy_, bstack11l111l111_opy_),
        bstack111llll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨག"): headers
    }
    response = bstack1l1ll1l1l1_opy_(bstack111llll_opy_ (u"ࠨࡒࡒࡗ࡙࠭གྷ"), bstack11l1111l11_opy_ + bstack111llll_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩང"), data, config)
    bstack11l11l111l_opy_ = response.json()
    if bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫཅ")]:
      parsed = json.loads(os.getenv(bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬཆ"), bstack111llll_opy_ (u"ࠬࢁࡽࠨཇ")))
      parsed[bstack111llll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ཈")] = bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠧࡥࡣࡷࡥࠬཉ")][bstack111llll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩཊ")]
      os.environ[bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪཋ")] = json.dumps(parsed)
      bstack1l1l111l_opy_.bstack11l111lll1_opy_(bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠪࡨࡦࡺࡡࠨཌ")][bstack111llll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬཌྷ")])
      bstack1l1l111l_opy_.bstack11l1111ll1_opy_(bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠬࡪࡡࡵࡣࠪཎ")][bstack111llll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨཏ")])
      bstack1l1l111l_opy_.store()
      return bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠧࡥࡣࡷࡥࠬཐ")][bstack111llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ད")], bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠩࡧࡥࡹࡧࠧདྷ")][bstack111llll_opy_ (u"ࠪ࡭ࡩ࠭ན")]
    else:
      logger.error(bstack111llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬཔ") + bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཕ")])
      if bstack11l11l111l_opy_[bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧབ")] == bstack111llll_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩབྷ"):
        for bstack11l11111ll_opy_ in bstack11l11l111l_opy_[bstack111llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨམ")]:
          logger.error(bstack11l11111ll_opy_[bstack111llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཙ")])
      return None, None
  except Exception as error:
    logger.error(bstack111llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦཚ") +  str(error))
    return None, None
def bstack11l11l1l11_opy_():
  if os.getenv(bstack111llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཛ")) is None:
    return {
        bstack111llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬཛྷ"): bstack111llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬཝ"),
        bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཞ"): bstack111llll_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧཟ")
    }
  data = {bstack111llll_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪའ"): bstack1ll1llllll_opy_()}
  headers = {
      bstack111llll_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪཡ"): bstack111llll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬར") + os.getenv(bstack111llll_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥལ")),
      bstack111llll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬཤ"): bstack111llll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪཥ")
  }
  response = bstack1l1ll1l1l1_opy_(bstack111llll_opy_ (u"ࠨࡒࡘࡘࠬས"), bstack11l1111l11_opy_ + bstack111llll_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫཧ"), data, { bstack111llll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫཨ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111llll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧཀྵ") + bstack11l1ll11l1_opy_().isoformat() + bstack111llll_opy_ (u"ࠬࡠࠧཪ"))
      return {bstack111llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ཫ"): bstack111llll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨཬ"), bstack111llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ཭"): bstack111llll_opy_ (u"ࠩࠪ཮")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨ཯") + str(error))
    return {
        bstack111llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ཰"): bstack111llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵཱࠫ"),
        bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ིࠧ"): str(error)
    }
def bstack11l111ll_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11l111l1l1_opy_ = caps.get(bstack111llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨཱི"), {}).get(bstack111llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩུࠬ"), caps.get(bstack111llll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦཱུࠩ"), bstack111llll_opy_ (u"ࠪࠫྲྀ")))
    if bstack11l111l1l1_opy_:
      logger.warn(bstack111llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣཷ"))
      return False
    if options:
      bstack11l1111l1l_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack11l1111l1l_opy_ = desired_capabilities
    else:
      bstack11l1111l1l_opy_ = {}
    browser = caps.get(bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪླྀ"), bstack111llll_opy_ (u"࠭ࠧཹ")).lower() or bstack11l1111l1l_opy_.get(bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩེࠬ"), bstack111llll_opy_ (u"ࠨཻࠩ")).lower()
    if browser != bstack111llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦོࠩ"):
      logger.warn(bstack111llll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨཽ"))
      return False
    browser_version = caps.get(bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬཾ")) or caps.get(bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧཿ")) or bstack11l1111l1l_opy_.get(bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴྀࠧ")) or bstack11l1111l1l_opy_.get(bstack111llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨཱྀ"), {}).get(bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩྂ")) or bstack11l1111l1l_opy_.get(bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪྃ"), {}).get(bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲ྄ࠬ"))
    if browser_version and browser_version != bstack111llll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫ྅") and int(browser_version.split(bstack111llll_opy_ (u"ࠬ࠴ࠧ྆"))[0]) <= 98:
      logger.warn(bstack111llll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠺࠱ࠦ྇"))
      return False
    if not options:
      bstack11l111l1ll_opy_ = caps.get(bstack111llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬྈ")) or bstack11l1111l1l_opy_.get(bstack111llll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ྉ"), {})
      if bstack111llll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ྊ") in bstack11l111l1ll_opy_.get(bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨྋ"), []):
        logger.warn(bstack111llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨྌ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack111llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢྍ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack111lllllll_opy_ = config.get(bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ྎ"), {})
    bstack111lllllll_opy_[bstack111llll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪྏ")] = os.getenv(bstack111llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ྐ"))
    bstack11l11111l1_opy_ = json.loads(os.getenv(bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪྑ"), bstack111llll_opy_ (u"ࠪࡿࢂ࠭ྒ"))).get(bstack111llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬྒྷ"))
    caps[bstack111llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬྔ")] = True
    if bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧྕ") in caps:
      caps[bstack111llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨྖ")][bstack111llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨྗ")] = bstack111lllllll_opy_
      caps[bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ྘")][bstack111llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪྙ")][bstack111llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬྚ")] = bstack11l11111l1_opy_
    else:
      caps[bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫྛ")] = bstack111lllllll_opy_
      caps[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬྜ")][bstack111llll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྜྷ")] = bstack11l11111l1_opy_
  except Exception as error:
    logger.debug(bstack111llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤྞ") +  str(error))
def bstack11llllll11_opy_(driver, bstack11l11l1l1l_opy_):
  try:
    setattr(driver, bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩྟ"), True)
    session = driver.session_id
    if session:
      bstack11l111111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l111111l_opy_ = False
      bstack11l111111l_opy_ = url.scheme in [bstack111llll_opy_ (u"ࠥ࡬ࡹࡺࡰࠣྠ"), bstack111llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥྡ")]
      if bstack11l111111l_opy_:
        if bstack11l11l1l1l_opy_:
          logger.info(bstack111llll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧྡྷ"))
      return bstack11l11l1l1l_opy_
  except Exception as e:
    logger.error(bstack111llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤྣ") + str(e))
    return False
def bstack11l1ll1l_opy_(driver, name, path):
  try:
    bstack111lllll11_opy_ = {
        bstack111llll_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧྤ"): threading.current_thread().current_test_uuid,
        bstack111llll_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ྥ"): os.environ.get(bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧྦ"), bstack111llll_opy_ (u"ࠪࠫྦྷ")),
        bstack111llll_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨྨ"): os.environ.get(bstack111llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ྩ"), bstack111llll_opy_ (u"࠭ࠧྪ"))
    }
    logger.debug(bstack111llll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪྫ"))
    logger.debug(driver.execute_async_script(bstack1l1l111l_opy_.perform_scan, {bstack111llll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣྫྷ"): name}))
    logger.debug(driver.execute_async_script(bstack1l1l111l_opy_.bstack111llll111_opy_, bstack111lllll11_opy_))
    logger.info(bstack111llll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧྭ"))
  except Exception as bstack11l111ll11_opy_:
    logger.error(bstack111llll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧྮ") + str(path) + bstack111llll_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨྯ") + str(bstack11l111ll11_opy_))