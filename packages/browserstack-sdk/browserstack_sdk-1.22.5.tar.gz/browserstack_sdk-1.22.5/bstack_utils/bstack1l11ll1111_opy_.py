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
import re
from bstack_utils.bstack1l1l111111_opy_ import bstack1lll111ll11_opy_
def bstack1lll11l1111_opy_(fixture_name):
    if fixture_name.startswith(bstack111llll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖮ")):
        return bstack111llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᖯ")
    elif fixture_name.startswith(bstack111llll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖰ")):
        return bstack111llll_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᖱ")
    elif fixture_name.startswith(bstack111llll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖲ")):
        return bstack111llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᖳ")
    elif fixture_name.startswith(bstack111llll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖴ")):
        return bstack111llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᖵ")
def bstack1lll111l1l1_opy_(fixture_name):
    return bool(re.match(bstack111llll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᖶ"), fixture_name))
def bstack1lll11l1l1l_opy_(fixture_name):
    return bool(re.match(bstack111llll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᖷ"), fixture_name))
def bstack1lll11l111l_opy_(fixture_name):
    return bool(re.match(bstack111llll_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᖸ"), fixture_name))
def bstack1lll111lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack111llll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖹ")):
        return bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᖺ"), bstack111llll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᖻ")
    elif fixture_name.startswith(bstack111llll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᖼ")):
        return bstack111llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ᖽ"), bstack111llll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᖾ")
    elif fixture_name.startswith(bstack111llll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖿ")):
        return bstack111llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᗀ"), bstack111llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᗁ")
    elif fixture_name.startswith(bstack111llll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᗂ")):
        return bstack111llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᗃ"), bstack111llll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᗄ")
    return None, None
def bstack1lll11l1lll_opy_(hook_name):
    if hook_name in [bstack111llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᗅ"), bstack111llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᗆ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll111llll_opy_(hook_name):
    if hook_name in [bstack111llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᗇ"), bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᗈ")]:
        return bstack111llll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᗉ")
    elif hook_name in [bstack111llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᗊ"), bstack111llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᗋ")]:
        return bstack111llll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᗌ")
    elif hook_name in [bstack111llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᗍ"), bstack111llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᗎ")]:
        return bstack111llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᗏ")
    elif hook_name in [bstack111llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᗐ"), bstack111llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᗑ")]:
        return bstack111llll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᗒ")
    return hook_name
def bstack1lll11l1ll1_opy_(node, scenario):
    if hasattr(node, bstack111llll_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᗓ")):
        parts = node.nodeid.rsplit(bstack111llll_opy_ (u"ࠤ࡞ࠦᗔ"))
        params = parts[-1]
        return bstack111llll_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᗕ").format(scenario.name, params)
    return scenario.name
def bstack1lll11l11l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111llll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᗖ")):
            examples = list(node.callspec.params[bstack111llll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᗗ")].values())
        return examples
    except:
        return []
def bstack1lll11l1l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll111l1ll_opy_(report):
    try:
        status = bstack111llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗘ")
        if report.passed or (report.failed and hasattr(report, bstack111llll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᗙ"))):
            status = bstack111llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᗚ")
        elif report.skipped:
            status = bstack111llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᗛ")
        bstack1lll111ll11_opy_(status)
    except:
        pass
def bstack1llllllll1_opy_(status):
    try:
        bstack1lll111ll1l_opy_ = bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᗜ")
        if status == bstack111llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᗝ"):
            bstack1lll111ll1l_opy_ = bstack111llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᗞ")
        elif status == bstack111llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᗟ"):
            bstack1lll111ll1l_opy_ = bstack111llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᗠ")
        bstack1lll111ll11_opy_(bstack1lll111ll1l_opy_)
    except:
        pass
def bstack1lll11l11ll_opy_(item=None, report=None, summary=None, extra=None):
    return