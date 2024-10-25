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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll11l1l_opy_
bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
def bstack1lll11ll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll11lll11_opy_(bstack1lll11ll1l1_opy_, bstack1lll11lll1l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll11ll1l1_opy_):
        with open(bstack1lll11ll1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll11ll111_opy_(bstack1lll11ll1l1_opy_):
        pac = get_pac(url=bstack1lll11ll1l1_opy_)
    else:
        raise Exception(bstack111llll_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᖈ").format(bstack1lll11ll1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111llll_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᖉ"), 80))
        bstack1lll11llll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll11llll1_opy_ = bstack111llll_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᖊ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll11lll1l_opy_, bstack1lll11llll1_opy_)
    return proxy_url
def bstack1ll111l1l1_opy_(config):
    return bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᖋ") in config or bstack111llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᖌ") in config
def bstack1ll11lll11_opy_(config):
    if not bstack1ll111l1l1_opy_(config):
        return
    if config.get(bstack111llll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᖍ")):
        return config.get(bstack111llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᖎ"))
    if config.get(bstack111llll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᖏ")):
        return config.get(bstack111llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᖐ"))
def bstack1lllll11ll_opy_(config, bstack1lll11lll1l_opy_):
    proxy = bstack1ll11lll11_opy_(config)
    proxies = {}
    if config.get(bstack111llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᖑ")) or config.get(bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᖒ")):
        if proxy.endswith(bstack111llll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᖓ")):
            proxies = bstack1l1l11ll1l_opy_(proxy, bstack1lll11lll1l_opy_)
        else:
            proxies = {
                bstack111llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖔ"): proxy
            }
    bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᖕ"), proxies)
    return proxies
def bstack1l1l11ll1l_opy_(bstack1lll11ll1l1_opy_, bstack1lll11lll1l_opy_):
    proxies = {}
    global bstack1lll11ll1ll_opy_
    if bstack111llll_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ᖖ") in globals():
        return bstack1lll11ll1ll_opy_
    try:
        proxy = bstack1lll11lll11_opy_(bstack1lll11ll1l1_opy_, bstack1lll11lll1l_opy_)
        if bstack111llll_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦᖗ") in proxy:
            proxies = {}
        elif bstack111llll_opy_ (u"ࠧࡎࡔࡕࡒࠥᖘ") in proxy or bstack111llll_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧᖙ") in proxy or bstack111llll_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨᖚ") in proxy:
            bstack1lll11ll11l_opy_ = proxy.split(bstack111llll_opy_ (u"ࠣࠢࠥᖛ"))
            if bstack111llll_opy_ (u"ࠤ࠽࠳࠴ࠨᖜ") in bstack111llll_opy_ (u"ࠥࠦᖝ").join(bstack1lll11ll11l_opy_[1:]):
                proxies = {
                    bstack111llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖞ"): bstack111llll_opy_ (u"ࠧࠨᖟ").join(bstack1lll11ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖠ"): str(bstack1lll11ll11l_opy_[0]).lower() + bstack111llll_opy_ (u"ࠢ࠻࠱࠲ࠦᖡ") + bstack111llll_opy_ (u"ࠣࠤᖢ").join(bstack1lll11ll11l_opy_[1:])
                }
        elif bstack111llll_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣᖣ") in proxy:
            bstack1lll11ll11l_opy_ = proxy.split(bstack111llll_opy_ (u"ࠥࠤࠧᖤ"))
            if bstack111llll_opy_ (u"ࠦ࠿࠵࠯ࠣᖥ") in bstack111llll_opy_ (u"ࠧࠨᖦ").join(bstack1lll11ll11l_opy_[1:]):
                proxies = {
                    bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖧ"): bstack111llll_opy_ (u"ࠢࠣᖨ").join(bstack1lll11ll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack111llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖩ"): bstack111llll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᖪ") + bstack111llll_opy_ (u"ࠥࠦᖫ").join(bstack1lll11ll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack111llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖬ"): proxy
            }
    except Exception as e:
        print(bstack111llll_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᖭ"), bstack1lllll11l1l_opy_.format(bstack1lll11ll1l1_opy_, str(e)))
    bstack1lll11ll1ll_opy_ = proxies
    return proxies