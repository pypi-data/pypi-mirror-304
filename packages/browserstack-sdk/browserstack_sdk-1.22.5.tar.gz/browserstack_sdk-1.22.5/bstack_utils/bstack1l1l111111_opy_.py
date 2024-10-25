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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111111lll1_opy_, bstack11l11l11_opy_, bstack1llll11l1l_opy_, bstack11111111l_opy_, \
    bstack11111lll11_opy_
def bstack1l11ll11l_opy_(bstack1ll1llll111_opy_):
    for driver in bstack1ll1llll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l1lll_opy_(driver, status, reason=bstack111llll_opy_ (u"ࠪࠫᗣ")):
    bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
    if bstack1l111l11ll_opy_.bstack11l1l1l1l1_opy_():
        return
    bstack111ll1ll_opy_ = bstack111l1ll1l_opy_(bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗤ"), bstack111llll_opy_ (u"ࠬ࠭ᗥ"), status, reason, bstack111llll_opy_ (u"࠭ࠧᗦ"), bstack111llll_opy_ (u"ࠧࠨᗧ"))
    driver.execute_script(bstack111ll1ll_opy_)
def bstack1l1l11ll_opy_(page, status, reason=bstack111llll_opy_ (u"ࠨࠩᗨ")):
    try:
        if page is None:
            return
        bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
        if bstack1l111l11ll_opy_.bstack11l1l1l1l1_opy_():
            return
        bstack111ll1ll_opy_ = bstack111l1ll1l_opy_(bstack111llll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᗩ"), bstack111llll_opy_ (u"ࠪࠫᗪ"), status, reason, bstack111llll_opy_ (u"ࠫࠬᗫ"), bstack111llll_opy_ (u"ࠬ࠭ᗬ"))
        page.evaluate(bstack111llll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᗭ"), bstack111ll1ll_opy_)
    except Exception as e:
        print(bstack111llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧᗮ"), e)
def bstack111l1ll1l_opy_(type, name, status, reason, bstack11l11l1l1_opy_, bstack1lll1l11ll_opy_):
    bstack11l11ll1l_opy_ = {
        bstack111llll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨᗯ"): type,
        bstack111llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗰ"): {}
    }
    if type == bstack111llll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᗱ"):
        bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗲ")][bstack111llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᗳ")] = bstack11l11l1l1_opy_
        bstack11l11ll1l_opy_[bstack111llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗴ")][bstack111llll_opy_ (u"ࠧࡥࡣࡷࡥࠬᗵ")] = json.dumps(str(bstack1lll1l11ll_opy_))
    if type == bstack111llll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᗶ"):
        bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗷ")][bstack111llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᗸ")] = name
    if type == bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗹ"):
        bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᗺ")][bstack111llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᗻ")] = status
        if status == bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᗼ") and str(reason) != bstack111llll_opy_ (u"ࠣࠤᗽ"):
            bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗾ")][bstack111llll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᗿ")] = json.dumps(str(reason))
    bstack1ll11llll1_opy_ = bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᘀ").format(json.dumps(bstack11l11ll1l_opy_))
    return bstack1ll11llll1_opy_
def bstack1l1lllllll_opy_(url, config, logger, bstack1l1ll11l1l_opy_=False):
    hostname = bstack11l11l11_opy_(url)
    is_private = bstack11111111l_opy_(hostname)
    try:
        if is_private or bstack1l1ll11l1l_opy_:
            file_path = bstack111111lll1_opy_(bstack111llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᘁ"), bstack111llll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᘂ"), logger)
            if os.environ.get(bstack111llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᘃ")) and eval(
                    os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᘄ"))):
                return
            if (bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᘅ") in config and not config[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᘆ")]):
                os.environ[bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᘇ")] = str(True)
                bstack1ll1llll11l_opy_ = {bstack111llll_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᘈ"): hostname}
                bstack11111lll11_opy_(bstack111llll_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᘉ"), bstack111llll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬᘊ"), bstack1ll1llll11l_opy_, logger)
    except Exception as e:
        pass
def bstack11llllllll_opy_(caps, bstack1ll1lll1ll1_opy_):
    if bstack111llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘋ") in caps:
        caps[bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᘌ")][bstack111llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᘍ")] = True
        if bstack1ll1lll1ll1_opy_:
            caps[bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘎ")][bstack111llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᘏ")] = bstack1ll1lll1ll1_opy_
    else:
        caps[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᘐ")] = True
        if bstack1ll1lll1ll1_opy_:
            caps[bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᘑ")] = bstack1ll1lll1ll1_opy_
def bstack1lll111ll11_opy_(bstack11l1llll1l_opy_):
    bstack1ll1lll1lll_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᘒ"), bstack111llll_opy_ (u"ࠩࠪᘓ"))
    if bstack1ll1lll1lll_opy_ == bstack111llll_opy_ (u"ࠪࠫᘔ") or bstack1ll1lll1lll_opy_ == bstack111llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᘕ"):
        threading.current_thread().testStatus = bstack11l1llll1l_opy_
    else:
        if bstack11l1llll1l_opy_ == bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᘖ"):
            threading.current_thread().testStatus = bstack11l1llll1l_opy_