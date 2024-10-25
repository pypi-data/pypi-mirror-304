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
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l1111111_opy_, bstack111llll1ll_opy_, bstack1l1ll1l1l1_opy_, bstack11ll1ll111_opy_, bstack111111ll11_opy_, bstack111l1l1111_opy_, bstack1111111l1l_opy_, bstack1ll1llllll_opy_
from bstack_utils.bstack1lll111111l_opy_ import bstack1lll11111l1_opy_
import bstack_utils.bstack11l111l11_opy_ as bstack11l1ll1l1_opy_
from bstack_utils.bstack1lll1ll11_opy_ import bstack1l1lll1111_opy_
import bstack_utils.bstack1lll111l11_opy_ as bstack1l1111ll_opy_
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1l111l_opy_
from bstack_utils.bstack11lll1lll1_opy_ import bstack11ll11111l_opy_
bstack1ll1l111lll_opy_ = bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᙖ")
logger = logging.getLogger(__name__)
class bstack1l11l1lll_opy_:
    bstack1lll111111l_opy_ = None
    bs_config = None
    bstack1111ll1l_opy_ = None
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def launch(cls, bs_config, bstack1111ll1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1111ll1l_opy_ = bstack1111ll1l_opy_
        try:
            cls.bstack1ll1l1llll1_opy_()
            bstack111llll1l1_opy_ = bstack11l1111111_opy_(bs_config)
            bstack11l111l111_opy_ = bstack111llll1ll_opy_(bs_config)
            data = bstack11l1ll1l1_opy_.bstack1ll1l1l1ll1_opy_(bs_config, bstack1111ll1l_opy_)
            config = {
                bstack111llll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᙗ"): (bstack111llll1l1_opy_, bstack11l111l111_opy_),
                bstack111llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᙘ"): cls.default_headers()
            }
            response = bstack1l1ll1l1l1_opy_(bstack111llll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᙙ"), cls.request_url(bstack111llll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪᙚ")), data, config)
            if response.status_code != 200:
                bstack1ll1l11l11l_opy_ = response.json()
                if bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᙛ")] == False:
                    cls.bstack1ll1l1l1111_opy_(bstack1ll1l11l11l_opy_)
                    return
                cls.bstack1ll1l11l111_opy_(bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᙜ")])
                cls.bstack1ll1l11l1ll_opy_(bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᙝ")])
                return None
            bstack1ll1l1ll1ll_opy_ = cls.bstack1ll1l1l111l_opy_(response)
            return bstack1ll1l1ll1ll_opy_
        except Exception as error:
            logger.error(bstack111llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧᙞ").format(str(error)))
            return None
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def stop(cls, bstack1ll1l1l1l11_opy_=None):
        if not bstack1l1lll1111_opy_.on() and not bstack1l1111ll_opy_.on():
            return
        if os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᙟ")) == bstack111llll_opy_ (u"ࠤࡱࡹࡱࡲࠢᙠ") or os.environ.get(bstack111llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᙡ")) == bstack111llll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᙢ"):
            logger.error(bstack111llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᙣ"))
            return {
                bstack111llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙤ"): bstack111llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᙥ"),
                bstack111llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙦ"): bstack111llll_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᙧ")
            }
        try:
            cls.bstack1lll111111l_opy_.shutdown()
            data = {
                bstack111llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙨ"): bstack1ll1llllll_opy_()
            }
            if not bstack1ll1l1l1l11_opy_ is None:
                data[bstack111llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨᙩ")] = [{
                    bstack111llll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᙪ"): bstack111llll_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫᙫ"),
                    bstack111llll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧᙬ"): bstack1ll1l1l1l11_opy_
                }]
            config = {
                bstack111llll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ᙭"): cls.default_headers()
            }
            bstack1111ll1l1l_opy_ = bstack111llll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ᙮").format(os.environ[bstack111llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣᙯ")])
            bstack1ll1ll111l1_opy_ = cls.request_url(bstack1111ll1l1l_opy_)
            response = bstack1l1ll1l1l1_opy_(bstack111llll_opy_ (u"ࠫࡕ࡛ࡔࠨᙰ"), bstack1ll1ll111l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111llll_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦᙱ"))
        except Exception as error:
            logger.error(bstack111llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥᙲ") + str(error))
            return {
                bstack111llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᙳ"): bstack111llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᙴ"),
                bstack111llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙵ"): str(error)
            }
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def bstack1ll1l1l111l_opy_(cls, response):
        bstack1ll1l11l11l_opy_ = response.json()
        bstack1ll1l1ll1ll_opy_ = {}
        if bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠪ࡮ࡼࡺࠧᙶ")) is None:
            os.environ[bstack111llll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᙷ")] = bstack111llll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᙸ")
        else:
            os.environ[bstack111llll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᙹ")] = bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠧ࡫ࡹࡷࠫᙺ"), bstack111llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᙻ"))
        os.environ[bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᙼ")] = bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᙽ"), bstack111llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᙾ"))
        if bstack1l1lll1111_opy_.bstack1ll1l1ll11l_opy_(cls.bs_config, cls.bstack1111ll1l_opy_.get(bstack111llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ᙿ"), bstack111llll_opy_ (u"࠭ࠧ "))) is True:
            bstack1ll1l1lll1l_opy_, bstack1ll1l1111ll_opy_, bstack1ll1l1l1l1l_opy_ = cls.bstack1ll1l111l1l_opy_(bstack1ll1l11l11l_opy_)
            if bstack1ll1l1lll1l_opy_ != None and bstack1ll1l1111ll_opy_ != None:
                bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚁ")] = {
                    bstack111llll_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫᚂ"): bstack1ll1l1lll1l_opy_,
                    bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚃ"): bstack1ll1l1111ll_opy_,
                    bstack111llll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᚄ"): bstack1ll1l1l1l1l_opy_
                }
            else:
                bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚅ")] = {}
        else:
            bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚆ")] = {}
        if bstack1l1111ll_opy_.bstack111lllll1l_opy_(cls.bs_config) is True:
            bstack1ll1l11l1l1_opy_, bstack1ll1l1111ll_opy_ = cls.bstack1ll1l111l11_opy_(bstack1ll1l11l11l_opy_)
            if bstack1ll1l11l1l1_opy_ != None and bstack1ll1l1111ll_opy_ != None:
                bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚇ")] = {
                    bstack111llll_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫᚈ"): bstack1ll1l11l1l1_opy_,
                    bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᚉ"): bstack1ll1l1111ll_opy_,
                }
            else:
                bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚊ")] = {}
        else:
            bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚋ")] = {}
        if bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚌ")].get(bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᚍ")) != None or bstack1ll1l1ll1ll_opy_[bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚎ")].get(bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᚏ")) != None:
            cls.bstack1ll1l11ll1l_opy_(bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠨ࡬ࡺࡸࠬᚐ")), bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚑ")))
        return bstack1ll1l1ll1ll_opy_
    @classmethod
    def bstack1ll1l111l1l_opy_(cls, bstack1ll1l11l11l_opy_):
        if bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᚒ")) == None:
            cls.bstack1ll1l11l111_opy_()
            return [None, None, None]
        if bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚓ")][bstack111llll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᚔ")] != True:
            cls.bstack1ll1l11l111_opy_(bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᚕ")])
            return [None, None, None]
        logger.debug(bstack111llll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᚖ"))
        os.environ[bstack111llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᚗ")] = bstack111llll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᚘ")
        if bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠪ࡮ࡼࡺࠧᚙ")):
            os.environ[bstack111llll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᚚ")] = bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠬࡰࡷࡵࠩ᚛")]
            os.environ[bstack111llll_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ᚜")] = json.dumps({
                bstack111llll_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ᚝"): bstack11l1111111_opy_(cls.bs_config),
                bstack111llll_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ᚞"): bstack111llll1ll_opy_(cls.bs_config)
            })
        if bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ᚟")):
            os.environ[bstack111llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᚠ")] = bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚡ")]
        if bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚢ")].get(bstack111llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚣ"), {}).get(bstack111llll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᚤ")):
            os.environ[bstack111llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᚥ")] = str(bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᚦ")][bstack111llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᚧ")][bstack111llll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᚨ")])
        return [bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠬࡰࡷࡵࠩᚩ")], bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚪ")], os.environ[bstack111llll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᚫ")]]
    @classmethod
    def bstack1ll1l111l11_opy_(cls, bstack1ll1l11l11l_opy_):
        if bstack1ll1l11l11l_opy_.get(bstack111llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚬ")) == None:
            cls.bstack1ll1l11l1ll_opy_()
            return [None, None]
        if bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚭ")][bstack111llll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᚮ")] != True:
            cls.bstack1ll1l11l1ll_opy_(bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚯ")])
            return [None, None]
        if bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚰ")].get(bstack111llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚱ")):
            logger.debug(bstack111llll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᚲ"))
            parsed = json.loads(os.getenv(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᚳ"), bstack111llll_opy_ (u"ࠩࡾࢁࠬᚴ")))
            capabilities = bstack11l1ll1l1_opy_.bstack1ll1l1ll111_opy_(bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚵ")][bstack111llll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᚶ")][bstack111llll_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚷ")], bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚸ"), bstack111llll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᚹ"))
            bstack1ll1l11l1l1_opy_ = capabilities[bstack111llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᚺ")]
            os.environ[bstack111llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᚻ")] = bstack1ll1l11l1l1_opy_
            parsed[bstack111llll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚼ")] = capabilities[bstack111llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚽ")]
            os.environ[bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᚾ")] = json.dumps(parsed)
            scripts = bstack11l1ll1l1_opy_.bstack1ll1l1ll111_opy_(bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚿ")][bstack111llll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᛀ")][bstack111llll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᛁ")], bstack111llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᛂ"), bstack111llll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫᛃ"))
            bstack1l1l111l_opy_.bstack11l111lll1_opy_(scripts)
            commands = bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛄ")][bstack111llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛅ")][bstack111llll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧᛆ")].get(bstack111llll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᛇ"))
            bstack1l1l111l_opy_.bstack11l1111ll1_opy_(commands)
            bstack1l1l111l_opy_.store()
        return [bstack1ll1l11l1l1_opy_, bstack1ll1l11l11l_opy_[bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᛈ")]]
    @classmethod
    def bstack1ll1l11l111_opy_(cls, response=None):
        os.environ[bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛉ")] = bstack111llll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛊ")
        os.environ[bstack111llll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᛋ")] = bstack111llll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᛌ")
        os.environ[bstack111llll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᛍ")] = bstack111llll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛎ")
        os.environ[bstack111llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᛏ")] = bstack111llll_opy_ (u"ࠩࡱࡹࡱࡲࠧᛐ")
        os.environ[bstack111llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᛑ")] = bstack111llll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᛒ")
        os.environ[bstack111llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᛓ")] = bstack111llll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛔ")
        cls.bstack1ll1l1l1111_opy_(response, bstack111llll_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᛕ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l11l1ll_opy_(cls, response=None):
        os.environ[bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᛖ")] = bstack111llll_opy_ (u"ࠩࡱࡹࡱࡲࠧᛗ")
        os.environ[bstack111llll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᛘ")] = bstack111llll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᛙ")
        os.environ[bstack111llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᛚ")] = bstack111llll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛛ")
        cls.bstack1ll1l1l1111_opy_(response, bstack111llll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᛜ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l11ll1l_opy_(cls, bstack1ll1l1ll1l1_opy_, bstack1ll1l1111ll_opy_):
        os.environ[bstack111llll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛝ")] = bstack1ll1l1ll1l1_opy_
        os.environ[bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛞ")] = bstack1ll1l1111ll_opy_
    @classmethod
    def bstack1ll1l1l1111_opy_(cls, response=None, product=bstack111llll_opy_ (u"ࠥࠦᛟ")):
        if response == None:
            logger.error(product + bstack111llll_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨᛠ"))
        for error in response[bstack111llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᛡ")]:
            bstack11111ll1l1_opy_ = error[bstack111llll_opy_ (u"࠭࡫ࡦࡻࠪᛢ")]
            error_message = error[bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛣ")]
            if error_message:
                if bstack11111ll1l1_opy_ == bstack111llll_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢᛤ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111llll_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥᛥ") + product + bstack111llll_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᛦ"))
    @classmethod
    def bstack1ll1l1llll1_opy_(cls):
        if cls.bstack1lll111111l_opy_ is not None:
            return
        cls.bstack1lll111111l_opy_ = bstack1lll11111l1_opy_(cls.bstack1ll1l1l1lll_opy_)
        cls.bstack1lll111111l_opy_.start()
    @classmethod
    def bstack11ll1l11ll_opy_(cls):
        if cls.bstack1lll111111l_opy_ is None:
            return
        cls.bstack1lll111111l_opy_.shutdown()
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def bstack1ll1l1l1lll_opy_(cls, bstack11ll1l1lll_opy_, bstack1ll1l1l11l1_opy_=bstack111llll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᛧ")):
        config = {
            bstack111llll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᛨ"): cls.default_headers()
        }
        response = bstack1l1ll1l1l1_opy_(bstack111llll_opy_ (u"࠭ࡐࡐࡕࡗࠫᛩ"), cls.request_url(bstack1ll1l1l11l1_opy_), bstack11ll1l1lll_opy_, config)
        bstack11l11l111l_opy_ = response.json()
    @classmethod
    def bstack11ll1l1111_opy_(cls, bstack11ll1l1lll_opy_, bstack1ll1l1l11l1_opy_=bstack111llll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᛪ")):
        if not bstack11l1ll1l1_opy_.bstack1ll1l11ll11_opy_(bstack11ll1l1lll_opy_[bstack111llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᛫")]):
            return
        bstack1llll11l_opy_ = bstack11l1ll1l1_opy_.bstack1ll1l11lll1_opy_(bstack11ll1l1lll_opy_[bstack111llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᛬")], bstack11ll1l1lll_opy_.get(bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ᛭")))
        if bstack1llll11l_opy_ != None:
            if bstack11ll1l1lll_opy_.get(bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᛮ")) != None:
                bstack11ll1l1lll_opy_[bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᛯ")][bstack111llll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᛰ")] = bstack1llll11l_opy_
            else:
                bstack11ll1l1lll_opy_[bstack111llll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᛱ")] = bstack1llll11l_opy_
        if bstack1ll1l1l11l1_opy_ == bstack111llll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᛲ"):
            cls.bstack1ll1l1llll1_opy_()
            cls.bstack1lll111111l_opy_.add(bstack11ll1l1lll_opy_)
        elif bstack1ll1l1l11l1_opy_ == bstack111llll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᛳ"):
            cls.bstack1ll1l1l1lll_opy_([bstack11ll1l1lll_opy_], bstack1ll1l1l11l1_opy_)
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def bstack11l1l111l_opy_(cls, bstack11l1ll1111_opy_):
        bstack1ll1ll1111l_opy_ = []
        for log in bstack11l1ll1111_opy_:
            bstack1ll1l1lll11_opy_ = {
                bstack111llll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᛴ"): bstack111llll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭ᛵ"),
                bstack111llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᛶ"): log[bstack111llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᛷ")],
                bstack111llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᛸ"): log[bstack111llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᛹")],
                bstack111llll_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩ᛺"): {},
                bstack111llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᛻"): log[bstack111llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᛼")],
            }
            if bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᛽") in log:
                bstack1ll1l1lll11_opy_[bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᛾")] = log[bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᛿")]
            elif bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜀ") in log:
                bstack1ll1l1lll11_opy_[bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜁ")] = log[bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜂ")]
            bstack1ll1ll1111l_opy_.append(bstack1ll1l1lll11_opy_)
        cls.bstack11ll1l1111_opy_({
            bstack111llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜃ"): bstack111llll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᜄ"),
            bstack111llll_opy_ (u"࠭࡬ࡰࡩࡶࠫᜅ"): bstack1ll1ll1111l_opy_
        })
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def bstack1ll1ll11111_opy_(cls, steps):
        bstack1ll1l11llll_opy_ = []
        for step in steps:
            bstack1ll1l111ll1_opy_ = {
                bstack111llll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᜆ"): bstack111llll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫᜇ"),
                bstack111llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᜈ"): step[bstack111llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᜉ")],
                bstack111llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᜊ"): step[bstack111llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᜋ")],
                bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜌ"): step[bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᜍ")],
                bstack111llll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᜎ"): step[bstack111llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᜏ")]
            }
            if bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜐ") in step:
                bstack1ll1l111ll1_opy_[bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᜑ")] = step[bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᜒ")]
            elif bstack111llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜓ") in step:
                bstack1ll1l111ll1_opy_[bstack111llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ᜔ࠧ")] = step[bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᜕")]
            bstack1ll1l11llll_opy_.append(bstack1ll1l111ll1_opy_)
        cls.bstack11ll1l1111_opy_({
            bstack111llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜖"): bstack111llll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ᜗"),
            bstack111llll_opy_ (u"ࠫࡱࡵࡧࡴࠩ᜘"): bstack1ll1l11llll_opy_
        })
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def bstack11llllll1_opy_(cls, screenshot):
        cls.bstack11ll1l1111_opy_({
            bstack111llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ᜙"): bstack111llll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ᜚"),
            bstack111llll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ᜛"): [{
                bstack111llll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭᜜"): bstack111llll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫ᜝"),
                bstack111llll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭᜞"): datetime.datetime.utcnow().isoformat() + bstack111llll_opy_ (u"ࠫ࡟࠭ᜟ"),
                bstack111llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᜠ"): screenshot[bstack111llll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᜡ")],
                bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜢ"): screenshot[bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜣ")]
            }]
        }, bstack1ll1l1l11l1_opy_=bstack111llll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᜤ"))
    @classmethod
    @bstack11ll1ll111_opy_(class_method=True)
    def bstack1ll1lll111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll1l1111_opy_({
            bstack111llll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᜥ"): bstack111llll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᜦ"),
            bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᜧ"): {
                bstack111llll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᜨ"): cls.current_test_uuid(),
                bstack111llll_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨᜩ"): cls.bstack11lll11111_opy_(driver)
            }
        })
    @classmethod
    def bstack11llll11ll_opy_(cls, event: str, bstack11ll1l1lll_opy_: bstack11ll11111l_opy_):
        bstack11ll11lll1_opy_ = {
            bstack111llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜪ"): event,
            bstack11ll1l1lll_opy_.bstack11ll111l11_opy_(): bstack11ll1l1lll_opy_.bstack11l1lllll1_opy_(event)
        }
        cls.bstack11ll1l1111_opy_(bstack11ll11lll1_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111llll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᜫ"), None) is None or os.environ[bstack111llll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᜬ")] == bstack111llll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᜭ")) and (os.environ.get(bstack111llll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᜮ"), None) is None or os.environ[bstack111llll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᜯ")] == bstack111llll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᜰ")):
            return False
        return True
    @staticmethod
    def bstack1ll1l1lllll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l1lll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111llll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᜱ"): bstack111llll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᜲ"),
            bstack111llll_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭ᜳ"): bstack111llll_opy_ (u"ࠫࡹࡸࡵࡦ᜴ࠩ")
        }
        if os.environ.get(bstack111llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᜵"), None):
            headers[bstack111llll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᜶")] = bstack111llll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ᜷").format(os.environ[bstack111llll_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ᜸")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111llll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ᜹").format(bstack1ll1l111lll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ᜺"), None)
    @staticmethod
    def bstack11lll11111_opy_(driver):
        return {
            bstack111111ll11_opy_(): bstack111l1l1111_opy_(driver)
        }
    @staticmethod
    def bstack1ll1l1l11ll_opy_(exception_info, report):
        return [{bstack111llll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᜻"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11l11ll1l1_opy_(typename):
        if bstack111llll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ᜼") in typename:
            return bstack111llll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᜽")
        return bstack111llll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ᜾")