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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111ll111ll_opy_, bstack1l1llll111_opy_, bstack1lll1lll1_opy_, bstack1l111l1l11_opy_,
                                    bstack111l1lll11_opy_, bstack111ll11lll_opy_, bstack111ll11l11_opy_, bstack111l1lll1l_opy_)
from bstack_utils.messages import bstack1lll111ll1_opy_, bstack11l1111l1_opy_
from bstack_utils.proxy import bstack1lllll11ll_opy_, bstack1ll11lll11_opy_
bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
logger = logging.getLogger(__name__)
def bstack11l1111111_opy_(config):
    return config[bstack111llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧኲ")]
def bstack111llll1ll_opy_(config):
    return config[bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩኳ")]
def bstack1ll1l1llll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111111l1ll_opy_(obj):
    values = []
    bstack111l11111l_opy_ = re.compile(bstack111llll_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦኴ"), re.I)
    for key in obj.keys():
        if bstack111l11111l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11111l1lll_opy_(config):
    tags = []
    tags.extend(bstack111111l1ll_opy_(os.environ))
    tags.extend(bstack111111l1ll_opy_(config))
    return tags
def bstack1111l1l11l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111l111111_opy_(bstack111l11ll1l_opy_):
    if not bstack111l11ll1l_opy_:
        return bstack111llll_opy_ (u"ࠨࠩኵ")
    return bstack111llll_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥ኶").format(bstack111l11ll1l_opy_.name, bstack111l11ll1l_opy_.email)
def bstack111llll11l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111llllll_opy_ = repo.common_dir
        info = {
            bstack111llll_opy_ (u"ࠥࡷ࡭ࡧࠢ኷"): repo.head.commit.hexsha,
            bstack111llll_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢኸ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack111llll_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧኹ"): repo.active_branch.name,
            bstack111llll_opy_ (u"ࠨࡴࡢࡩࠥኺ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack111llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥኻ"): bstack111l111111_opy_(repo.head.commit.committer),
            bstack111llll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤኼ"): repo.head.commit.committed_datetime.isoformat(),
            bstack111llll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤኽ"): bstack111l111111_opy_(repo.head.commit.author),
            bstack111llll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣኾ"): repo.head.commit.authored_datetime.isoformat(),
            bstack111llll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ኿"): repo.head.commit.message,
            bstack111llll_opy_ (u"ࠧࡸ࡯ࡰࡶࠥዀ"): repo.git.rev_parse(bstack111llll_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣ዁")),
            bstack111llll_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣዂ"): bstack1111llllll_opy_,
            bstack111llll_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦዃ"): subprocess.check_output([bstack111llll_opy_ (u"ࠤࡪ࡭ࡹࠨዄ"), bstack111llll_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨዅ"), bstack111llll_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢ዆")]).strip().decode(
                bstack111llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ዇")),
            bstack111llll_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣወ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack111llll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤዉ"): repo.git.rev_list(
                bstack111llll_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣዊ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111ll1l11_opy_ = []
        for remote in remotes:
            bstack1111lll11l_opy_ = {
                bstack111llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢዋ"): remote.name,
                bstack111llll_opy_ (u"ࠥࡹࡷࡲࠢዌ"): remote.url,
            }
            bstack1111ll1l11_opy_.append(bstack1111lll11l_opy_)
        bstack111l11l1ll_opy_ = {
            bstack111llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤው"): bstack111llll_opy_ (u"ࠧ࡭ࡩࡵࠤዎ"),
            **info,
            bstack111llll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢዏ"): bstack1111ll1l11_opy_
        }
        bstack111l11l1ll_opy_ = bstack111l111l11_opy_(bstack111l11l1ll_opy_)
        return bstack111l11l1ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack111llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥዐ").format(err))
        return {}
def bstack111l111l11_opy_(bstack111l11l1ll_opy_):
    bstack1111llll1l_opy_ = bstack111l1l11l1_opy_(bstack111l11l1ll_opy_)
    if bstack1111llll1l_opy_ and bstack1111llll1l_opy_ > bstack111l1lll11_opy_:
        bstack1111111lll_opy_ = bstack1111llll1l_opy_ - bstack111l1lll11_opy_
        bstack1111l11ll1_opy_ = bstack1111ll11l1_opy_(bstack111l11l1ll_opy_[bstack111llll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤዑ")], bstack1111111lll_opy_)
        bstack111l11l1ll_opy_[bstack111llll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥዒ")] = bstack1111l11ll1_opy_
        logger.info(bstack111llll_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧዓ")
                    .format(bstack111l1l11l1_opy_(bstack111l11l1ll_opy_) / 1024))
    return bstack111l11l1ll_opy_
def bstack111l1l11l1_opy_(bstack1l1ll11lll_opy_):
    try:
        if bstack1l1ll11lll_opy_:
            bstack111l1ll11l_opy_ = json.dumps(bstack1l1ll11lll_opy_)
            bstack1111ll11ll_opy_ = sys.getsizeof(bstack111l1ll11l_opy_)
            return bstack1111ll11ll_opy_
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦዔ").format(e))
    return -1
def bstack1111ll11l1_opy_(field, bstack1111l1l1ll_opy_):
    try:
        bstack111111llll_opy_ = len(bytes(bstack111ll11lll_opy_, bstack111llll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫዕ")))
        bstack111l11llll_opy_ = bytes(field, bstack111llll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬዖ"))
        bstack11111l11ll_opy_ = len(bstack111l11llll_opy_)
        bstack11111l11l1_opy_ = ceil(bstack11111l11ll_opy_ - bstack1111l1l1ll_opy_ - bstack111111llll_opy_)
        if bstack11111l11l1_opy_ > 0:
            bstack111l1l1l11_opy_ = bstack111l11llll_opy_[:bstack11111l11l1_opy_].decode(bstack111llll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭዗"), errors=bstack111llll_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨዘ")) + bstack111ll11lll_opy_
            return bstack111l1l1l11_opy_
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢዙ").format(e))
    return field
def bstack11111ll11_opy_():
    env = os.environ
    if (bstack111llll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣዚ") in env and len(env[bstack111llll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤዛ")]) > 0) or (
            bstack111llll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦዜ") in env and len(env[bstack111llll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧዝ")]) > 0):
        return {
            bstack111llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዞ"): bstack111llll_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤዟ"),
            bstack111llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧዠ"): env.get(bstack111llll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨዡ")),
            bstack111llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨዢ"): env.get(bstack111llll_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢዣ")),
            bstack111llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧዤ"): env.get(bstack111llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨዥ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠣࡅࡌࠦዦ")) == bstack111llll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢዧ") and bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧየ"))):
        return {
            bstack111llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤዩ"): bstack111llll_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢዪ"),
            bstack111llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤያ"): env.get(bstack111llll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥዬ")),
            bstack111llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥይ"): env.get(bstack111llll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨዮ")),
            bstack111llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤዯ"): env.get(bstack111llll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢደ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠧࡉࡉࠣዱ")) == bstack111llll_opy_ (u"ࠨࡴࡳࡷࡨࠦዲ") and bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢዳ"))):
        return {
            bstack111llll_opy_ (u"ࠣࡰࡤࡱࡪࠨዴ"): bstack111llll_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧድ"),
            bstack111llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዶ"): env.get(bstack111llll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦዷ")),
            bstack111llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢዸ"): env.get(bstack111llll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣዹ")),
            bstack111llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨዺ"): env.get(bstack111llll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢዻ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠤࡆࡍࠧዼ")) == bstack111llll_opy_ (u"ࠥࡸࡷࡻࡥࠣዽ") and env.get(bstack111llll_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧዾ")) == bstack111llll_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢዿ"):
        return {
            bstack111llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጀ"): bstack111llll_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤጁ"),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጂ"): None,
            bstack111llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦጃ"): None,
            bstack111llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤጄ"): None
        }
    if env.get(bstack111llll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢጅ")) and env.get(bstack111llll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣጆ")):
        return {
            bstack111llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጇ"): bstack111llll_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥገ"),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጉ"): env.get(bstack111llll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢጊ")),
            bstack111llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጋ"): None,
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጌ"): env.get(bstack111llll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢግ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠨࡃࡊࠤጎ")) == bstack111llll_opy_ (u"ࠢࡵࡴࡸࡩࠧጏ") and bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢጐ"))):
        return {
            bstack111llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ጑"): bstack111llll_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤጒ"),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጓ"): env.get(bstack111llll_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣጔ")),
            bstack111llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጕ"): None,
            bstack111llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ጖"): env.get(bstack111llll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ጗"))
        }
    if env.get(bstack111llll_opy_ (u"ࠤࡆࡍࠧጘ")) == bstack111llll_opy_ (u"ࠥࡸࡷࡻࡥࠣጙ") and bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢጚ"))):
        return {
            bstack111llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥጛ"): bstack111llll_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤጜ"),
            bstack111llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥጝ"): env.get(bstack111llll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢጞ")),
            bstack111llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦጟ"): env.get(bstack111llll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣጠ")),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጡ"): env.get(bstack111llll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣጢ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠨࡃࡊࠤጣ")) == bstack111llll_opy_ (u"ࠢࡵࡴࡸࡩࠧጤ") and bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦጥ"))):
        return {
            bstack111llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጦ"): bstack111llll_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥጧ"),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጨ"): env.get(bstack111llll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤጩ")),
            bstack111llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጪ"): env.get(bstack111llll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧጫ")),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢጬ"): env.get(bstack111llll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧጭ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠥࡇࡎࠨጮ")) == bstack111llll_opy_ (u"ࠦࡹࡸࡵࡦࠤጯ") and bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣጰ"))):
        return {
            bstack111llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጱ"): bstack111llll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥጲ"),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጳ"): env.get(bstack111llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣጴ")),
            bstack111llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጵ"): env.get(bstack111llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨጶ")) or env.get(bstack111llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣጷ")),
            bstack111llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧጸ"): env.get(bstack111llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤጹ"))
        }
    if bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥጺ"))):
        return {
            bstack111llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጻ"): bstack111llll_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥጼ"),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጽ"): bstack111llll_opy_ (u"ࠧࢁࡽࡼࡿࠥጾ").format(env.get(bstack111llll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩጿ")), env.get(bstack111llll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧፀ"))),
            bstack111llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥፁ"): env.get(bstack111llll_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣፂ")),
            bstack111llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤፃ"): env.get(bstack111llll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦፄ"))
        }
    if bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢፅ"))):
        return {
            bstack111llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦፆ"): bstack111llll_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤፇ"),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦፈ"): bstack111llll_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣፉ").format(env.get(bstack111llll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩፊ")), env.get(bstack111llll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬፋ")), env.get(bstack111llll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ፌ")), env.get(bstack111llll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪፍ"))),
            bstack111llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤፎ"): env.get(bstack111llll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧፏ")),
            bstack111llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣፐ"): env.get(bstack111llll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦፑ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧፒ")) and env.get(bstack111llll_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢፓ")):
        return {
            bstack111llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦፔ"): bstack111llll_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤፕ"),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦፖ"): bstack111llll_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧፗ").format(env.get(bstack111llll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ፘ")), env.get(bstack111llll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩፙ")), env.get(bstack111llll_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬፚ"))),
            bstack111llll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ፛"): env.get(bstack111llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢ፜")),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ፝"): env.get(bstack111llll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ፞"))
        }
    if any([env.get(bstack111llll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ፟")), env.get(bstack111llll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ፠")), env.get(bstack111llll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤ፡"))]):
        return {
            bstack111llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ።"): bstack111llll_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢ፣"),
            bstack111llll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ፤"): env.get(bstack111llll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ፥")),
            bstack111llll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ፦"): env.get(bstack111llll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ፧")),
            bstack111llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ፨"): env.get(bstack111llll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ፩"))
        }
    if env.get(bstack111llll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ፪")):
        return {
            bstack111llll_opy_ (u"ࠣࡰࡤࡱࡪࠨ፫"): bstack111llll_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤ፬"),
            bstack111llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ፭"): env.get(bstack111llll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨ፮")),
            bstack111llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ፯"): env.get(bstack111llll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧ፰")),
            bstack111llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፱"): env.get(bstack111llll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨ፲"))
        }
    if env.get(bstack111llll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥ፳")) or env.get(bstack111llll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧ፴")):
        return {
            bstack111llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ፵"): bstack111llll_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨ፶"),
            bstack111llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ፷"): env.get(bstack111llll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ፸")),
            bstack111llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ፹"): bstack111llll_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤ፺") if env.get(bstack111llll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧ፻")) else None,
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፼"): env.get(bstack111llll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥ፽"))
        }
    if any([env.get(bstack111llll_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦ፾")), env.get(bstack111llll_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣ፿")), env.get(bstack111llll_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᎀ"))]):
        return {
            bstack111llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎁ"): bstack111llll_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᎂ"),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᎃ"): None,
            bstack111llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎄ"): env.get(bstack111llll_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᎅ")),
            bstack111llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᎆ"): env.get(bstack111llll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᎇ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧᎈ")):
        return {
            bstack111llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᎉ"): bstack111llll_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢᎊ"),
            bstack111llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎋ"): env.get(bstack111llll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᎌ")),
            bstack111llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎍ"): bstack111llll_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤᎎ").format(env.get(bstack111llll_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᎏ"))) if env.get(bstack111llll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨ᎐")) else None,
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᎑"): env.get(bstack111llll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᎒"))
        }
    if bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢ᎓"))):
        return {
            bstack111llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᎔"): bstack111llll_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤ᎕"),
            bstack111llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᎖"): env.get(bstack111llll_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢ᎗")),
            bstack111llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᎘"): env.get(bstack111llll_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣ᎙")),
            bstack111llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᎚"): env.get(bstack111llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᎛"))
        }
    if bstack1l11ll1lll_opy_(env.get(bstack111llll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤ᎜"))):
        return {
            bstack111llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᎝"): bstack111llll_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦ᎞"),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᎟"): bstack111llll_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨᎠ").format(env.get(bstack111llll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪᎡ")), env.get(bstack111llll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫᎢ")), env.get(bstack111llll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨᎣ"))),
            bstack111llll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎤ"): env.get(bstack111llll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧᎥ")),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎦ"): env.get(bstack111llll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᎧ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠨࡃࡊࠤᎨ")) == bstack111llll_opy_ (u"ࠢࡵࡴࡸࡩࠧᎩ") and env.get(bstack111llll_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣᎪ")) == bstack111llll_opy_ (u"ࠤ࠴ࠦᎫ"):
        return {
            bstack111llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᎬ"): bstack111llll_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦᎭ"),
            bstack111llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎮ"): bstack111llll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤᎯ").format(env.get(bstack111llll_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫᎰ"))),
            bstack111llll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᎱ"): None,
            bstack111llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᎲ"): None,
        }
    if env.get(bstack111llll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᎳ")):
        return {
            bstack111llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᎴ"): bstack111llll_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢᎵ"),
            bstack111llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᎶ"): None,
            bstack111llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎷ"): env.get(bstack111llll_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤᎸ")),
            bstack111llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᎹ"): env.get(bstack111llll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᎺ"))
        }
    if any([env.get(bstack111llll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢᎻ")), env.get(bstack111llll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᎼ")), env.get(bstack111llll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦᎽ")), env.get(bstack111llll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣᎾ"))]):
        return {
            bstack111llll_opy_ (u"ࠣࡰࡤࡱࡪࠨᎿ"): bstack111llll_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧᏀ"),
            bstack111llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏁ"): None,
            bstack111llll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏂ"): env.get(bstack111llll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᏃ")) or None,
            bstack111llll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏄ"): env.get(bstack111llll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᏅ"), 0)
        }
    if env.get(bstack111llll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᏆ")):
        return {
            bstack111llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᏇ"): bstack111llll_opy_ (u"ࠥࡋࡴࡉࡄࠣᏈ"),
            bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᏉ"): None,
            bstack111llll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏊ"): env.get(bstack111llll_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᏋ")),
            bstack111llll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᏌ"): env.get(bstack111llll_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᏍ"))
        }
    if env.get(bstack111llll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᏎ")):
        return {
            bstack111llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᏏ"): bstack111llll_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢᏐ"),
            bstack111llll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏑ"): env.get(bstack111llll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᏒ")),
            bstack111llll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᏓ"): env.get(bstack111llll_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᏔ")),
            bstack111llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏕ"): env.get(bstack111llll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᏖ"))
        }
    return {bstack111llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏗ"): None}
def get_host_info():
    return {
        bstack111llll_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢᏘ"): platform.node(),
        bstack111llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣᏙ"): platform.system(),
        bstack111llll_opy_ (u"ࠢࡵࡻࡳࡩࠧᏚ"): platform.machine(),
        bstack111llll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤᏛ"): platform.version(),
        bstack111llll_opy_ (u"ࠤࡤࡶࡨ࡮ࠢᏜ"): platform.architecture()[0]
    }
def bstack1ll1ll1l11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111111ll11_opy_():
    if bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫᏝ")):
        return bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᏞ")
    return bstack111llll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫᏟ")
def bstack111l1l1111_opy_(driver):
    info = {
        bstack111llll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᏠ"): driver.capabilities,
        bstack111llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫᏡ"): driver.session_id,
        bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᏢ"): driver.capabilities.get(bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᏣ"), None),
        bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᏤ"): driver.capabilities.get(bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᏥ"), None),
        bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧᏦ"): driver.capabilities.get(bstack111llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᏧ"), None),
    }
    if bstack111111ll11_opy_() == bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭Ꮸ"):
        info[bstack111llll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᏩ")] = bstack111llll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᏪ") if bstack1l11l1l111_opy_() else bstack111llll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᏫ")
    return info
def bstack1l11l1l111_opy_():
    if bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᏬ")):
        return True
    if bstack1l11ll1lll_opy_(os.environ.get(bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭Ꮽ"), None)):
        return True
    return False
def bstack1l1ll1l1l1_opy_(bstack1111l1llll_opy_, url, data, config):
    headers = config.get(bstack111llll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᏮ"), None)
    proxies = bstack1lllll11ll_opy_(config, url)
    auth = config.get(bstack111llll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᏯ"), None)
    response = requests.request(
            bstack1111l1llll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1l11l111_opy_(bstack1lll1ll111_opy_, size):
    bstack1111lll11_opy_ = []
    while len(bstack1lll1ll111_opy_) > size:
        bstack1l1l111lll_opy_ = bstack1lll1ll111_opy_[:size]
        bstack1111lll11_opy_.append(bstack1l1l111lll_opy_)
        bstack1lll1ll111_opy_ = bstack1lll1ll111_opy_[size:]
    bstack1111lll11_opy_.append(bstack1lll1ll111_opy_)
    return bstack1111lll11_opy_
def bstack1111111l1l_opy_(message, bstack11111l1ll1_opy_=False):
    os.write(1, bytes(message, bstack111llll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᏰ")))
    os.write(1, bytes(bstack111llll_opy_ (u"ࠩ࡟ࡲࠬᏱ"), bstack111llll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᏲ")))
    if bstack11111l1ll1_opy_:
        with open(bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪᏳ") + os.environ[bstack111llll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᏴ")] + bstack111llll_opy_ (u"࠭࠮࡭ࡱࡪࠫᏵ"), bstack111llll_opy_ (u"ࠧࡢࠩ᏶")) as f:
            f.write(message + bstack111llll_opy_ (u"ࠨ࡞ࡱࠫ᏷"))
def bstack1111llll11_opy_():
    return os.environ[bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᏸ")].lower() == bstack111llll_opy_ (u"ࠪࡸࡷࡻࡥࠨᏹ")
def bstack11l1l1ll_opy_(bstack1111ll1l1l_opy_):
    return bstack111llll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᏺ").format(bstack111ll111ll_opy_, bstack1111ll1l1l_opy_)
def bstack1ll1llllll_opy_():
    return bstack11l1ll11l1_opy_().replace(tzinfo=None).isoformat() + bstack111llll_opy_ (u"ࠬࡠࠧᏻ")
def bstack111l11ll11_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack111llll_opy_ (u"࡚࠭ࠨᏼ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack111llll_opy_ (u"࡛ࠧࠩᏽ")))).total_seconds() * 1000
def bstack1111ll111l_opy_(timestamp):
    return bstack1111l11lll_opy_(timestamp).isoformat() + bstack111llll_opy_ (u"ࠨ࡜ࠪ᏾")
def bstack1111l1ll11_opy_(bstack11111l111l_opy_):
    date_format = bstack111llll_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧ᏿")
    bstack111l1l1l1l_opy_ = datetime.datetime.strptime(bstack11111l111l_opy_, date_format)
    return bstack111l1l1l1l_opy_.isoformat() + bstack111llll_opy_ (u"ࠪ࡞ࠬ᐀")
def bstack111111l11l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack111llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐁ")
    else:
        return bstack111llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᐂ")
def bstack1l11ll1lll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack111llll_opy_ (u"࠭ࡴࡳࡷࡨࠫᐃ")
def bstack11111ll111_opy_(val):
    return val.__str__().lower() == bstack111llll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᐄ")
def bstack11ll1ll111_opy_(bstack11111ll1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11111ll1l1_opy_ as e:
                print(bstack111llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᐅ").format(func.__name__, bstack11111ll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l111ll1_opy_(bstack11111l1l11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11111l1l11_opy_(cls, *args, **kwargs)
            except bstack11111ll1l1_opy_ as e:
                print(bstack111llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᐆ").format(bstack11111l1l11_opy_.__name__, bstack11111ll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l111ll1_opy_
    else:
        return decorator
def bstack1ll111ll1l_opy_(bstack11l11lll11_opy_):
    if bstack111llll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᐇ") in bstack11l11lll11_opy_ and bstack11111ll111_opy_(bstack11l11lll11_opy_[bstack111llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᐈ")]):
        return False
    if bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᐉ") in bstack11l11lll11_opy_ and bstack11111ll111_opy_(bstack11l11lll11_opy_[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᐊ")]):
        return False
    return True
def bstack1ll11lll1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1llll1ll1l_opy_(hub_url):
    if bstack1lll111l1_opy_() <= version.parse(bstack111llll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᐋ")):
        if hub_url != bstack111llll_opy_ (u"ࠨࠩᐌ"):
            return bstack111llll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᐍ") + hub_url + bstack111llll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᐎ")
        return bstack1lll1lll1_opy_
    if hub_url != bstack111llll_opy_ (u"ࠫࠬᐏ"):
        return bstack111llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᐐ") + hub_url + bstack111llll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᐑ")
    return bstack1l111l1l11_opy_
def bstack1111lll1l1_opy_():
    return isinstance(os.getenv(bstack111llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᐒ")), str)
def bstack11l11l11_opy_(url):
    return urlparse(url).hostname
def bstack11111111l_opy_(hostname):
    for bstack11l1l1l11_opy_ in bstack1l1llll111_opy_:
        regex = re.compile(bstack11l1l1l11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111111lll1_opy_(bstack1111l1111l_opy_, file_name, logger):
    bstack1ll1llll11_opy_ = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠨࢀࠪᐓ")), bstack1111l1111l_opy_)
    try:
        if not os.path.exists(bstack1ll1llll11_opy_):
            os.makedirs(bstack1ll1llll11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠩࢁࠫᐔ")), bstack1111l1111l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack111llll_opy_ (u"ࠪࡻࠬᐕ")):
                pass
            with open(file_path, bstack111llll_opy_ (u"ࠦࡼ࠱ࠢᐖ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll111ll1_opy_.format(str(e)))
def bstack11111lll11_opy_(file_name, key, value, logger):
    file_path = bstack111111lll1_opy_(bstack111llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᐗ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1l111l1_opy_ = json.load(open(file_path, bstack111llll_opy_ (u"࠭ࡲࡣࠩᐘ")))
        else:
            bstack1ll1l111l1_opy_ = {}
        bstack1ll1l111l1_opy_[key] = value
        with open(file_path, bstack111llll_opy_ (u"ࠢࡸ࠭ࠥᐙ")) as outfile:
            json.dump(bstack1ll1l111l1_opy_, outfile)
def bstack111l11l11_opy_(file_name, logger):
    file_path = bstack111111lll1_opy_(bstack111llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᐚ"), file_name, logger)
    bstack1ll1l111l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack111llll_opy_ (u"ࠩࡵࠫᐛ")) as bstack1l111ll1_opy_:
            bstack1ll1l111l1_opy_ = json.load(bstack1l111ll1_opy_)
    return bstack1ll1l111l1_opy_
def bstack1ll1l1l1l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᐜ") + file_path + bstack111llll_opy_ (u"ࠫࠥ࠭ᐝ") + str(e))
def bstack1lll111l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack111llll_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᐞ")
def bstack1ll1ll1lll_opy_(config):
    if bstack111llll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᐟ") in config:
        del (config[bstack111llll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᐠ")])
        return False
    if bstack1lll111l1_opy_() < version.parse(bstack111llll_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᐡ")):
        return False
    if bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᐢ")):
        return True
    if bstack111llll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᐣ") in config and config[bstack111llll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᐤ")] is False:
        return False
    else:
        return True
def bstack111l11ll1_opy_(args_list, bstack111l111lll_opy_):
    index = -1
    for value in bstack111l111lll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11llll1111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11llll1111_opy_ = bstack11llll1111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack111llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᐥ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack111llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐦ"), exception=exception)
    def bstack11l11ll1l1_opy_(self):
        if self.result != bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐧ"):
            return None
        if isinstance(self.exception_type, str) and bstack111llll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᐨ") in self.exception_type:
            return bstack111llll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᐩ")
        return bstack111llll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᐪ")
    def bstack1111l1l1l1_opy_(self):
        if self.result != bstack111llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐫ"):
            return None
        if self.bstack11llll1111_opy_:
            return self.bstack11llll1111_opy_
        return bstack1111lll111_opy_(self.exception)
def bstack1111lll111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111ll1ll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llll11l1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1llll1lll1_opy_(config, logger):
    try:
        import playwright
        bstack111l11l11l_opy_ = playwright.__file__
        bstack1111ll1lll_opy_ = os.path.split(bstack111l11l11l_opy_)
        bstack111l1l111l_opy_ = bstack1111ll1lll_opy_[0] + bstack111llll_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᐬ")
        os.environ[bstack111llll_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᐭ")] = bstack1ll11lll11_opy_(config)
        with open(bstack111l1l111l_opy_, bstack111llll_opy_ (u"ࠧࡳࠩᐮ")) as f:
            bstack11111ll1l_opy_ = f.read()
            bstack111l111l1l_opy_ = bstack111llll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᐯ")
            bstack11111lll1l_opy_ = bstack11111ll1l_opy_.find(bstack111l111l1l_opy_)
            if bstack11111lll1l_opy_ == -1:
              process = subprocess.Popen(bstack111llll_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᐰ"), shell=True, cwd=bstack1111ll1lll_opy_[0])
              process.wait()
              bstack111l1ll111_opy_ = bstack111llll_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᐱ")
              bstack111111l1l1_opy_ = bstack111llll_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᐲ")
              bstack111l1l1lll_opy_ = bstack11111ll1l_opy_.replace(bstack111l1ll111_opy_, bstack111111l1l1_opy_)
              with open(bstack111l1l111l_opy_, bstack111llll_opy_ (u"ࠬࡽࠧᐳ")) as f:
                f.write(bstack111l1l1lll_opy_)
    except Exception as e:
        logger.error(bstack11l1111l1_opy_.format(str(e)))
def bstack1l11111l1_opy_():
  try:
    bstack111l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᐴ"))
    bstack111l11l111_opy_ = []
    if os.path.exists(bstack111l11l1l1_opy_):
      with open(bstack111l11l1l1_opy_) as f:
        bstack111l11l111_opy_ = json.load(f)
      os.remove(bstack111l11l1l1_opy_)
    return bstack111l11l111_opy_
  except:
    pass
  return []
def bstack1l1l1l1ll_opy_(bstack1llll1llll_opy_):
  try:
    bstack111l11l111_opy_ = []
    bstack111l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111llll_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᐵ"))
    if os.path.exists(bstack111l11l1l1_opy_):
      with open(bstack111l11l1l1_opy_) as f:
        bstack111l11l111_opy_ = json.load(f)
    bstack111l11l111_opy_.append(bstack1llll1llll_opy_)
    with open(bstack111l11l1l1_opy_, bstack111llll_opy_ (u"ࠨࡹࠪᐶ")) as f:
        json.dump(bstack111l11l111_opy_, f)
  except:
    pass
def bstack1ll1lllll1_opy_(logger, bstack11111ll1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack111llll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᐷ"), bstack111llll_opy_ (u"ࠪࠫᐸ"))
    if test_name == bstack111llll_opy_ (u"ࠫࠬᐹ"):
        test_name = threading.current_thread().__dict__.get(bstack111llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᐺ"), bstack111llll_opy_ (u"࠭ࠧᐻ"))
    bstack1111l1lll1_opy_ = bstack111llll_opy_ (u"ࠧ࠭ࠢࠪᐼ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11111ll1ll_opy_:
        bstack1lll1l1ll_opy_ = os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᐽ"), bstack111llll_opy_ (u"ࠩ࠳ࠫᐾ"))
        bstack1ll1ll11l_opy_ = {bstack111llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᐿ"): test_name, bstack111llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᑀ"): bstack1111l1lll1_opy_, bstack111llll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᑁ"): bstack1lll1l1ll_opy_}
        bstack1111l11l11_opy_ = []
        bstack1111l1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᑂ"))
        if os.path.exists(bstack1111l1ll1l_opy_):
            with open(bstack1111l1ll1l_opy_) as f:
                bstack1111l11l11_opy_ = json.load(f)
        bstack1111l11l11_opy_.append(bstack1ll1ll11l_opy_)
        with open(bstack1111l1ll1l_opy_, bstack111llll_opy_ (u"ࠧࡸࠩᑃ")) as f:
            json.dump(bstack1111l11l11_opy_, f)
    else:
        bstack1ll1ll11l_opy_ = {bstack111llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑄ"): test_name, bstack111llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᑅ"): bstack1111l1lll1_opy_, bstack111llll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᑆ"): str(multiprocessing.current_process().name)}
        if bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᑇ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1ll11l_opy_)
  except Exception as e:
      logger.warn(bstack111llll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᑈ").format(e))
def bstack1l11ll1l1_opy_(error_message, test_name, index, logger):
  try:
    bstack11111ll11l_opy_ = []
    bstack1ll1ll11l_opy_ = {bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᑉ"): test_name, bstack111llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᑊ"): error_message, bstack111llll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᑋ"): index}
    bstack11111lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack111llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᑌ"))
    if os.path.exists(bstack11111lllll_opy_):
        with open(bstack11111lllll_opy_) as f:
            bstack11111ll11l_opy_ = json.load(f)
    bstack11111ll11l_opy_.append(bstack1ll1ll11l_opy_)
    with open(bstack11111lllll_opy_, bstack111llll_opy_ (u"ࠪࡻࠬᑍ")) as f:
        json.dump(bstack11111ll11l_opy_, f)
  except Exception as e:
    logger.warn(bstack111llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᑎ").format(e))
def bstack1l111llll_opy_(bstack1ll111l11_opy_, name, logger):
  try:
    bstack1ll1ll11l_opy_ = {bstack111llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᑏ"): name, bstack111llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᑐ"): bstack1ll111l11_opy_, bstack111llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᑑ"): str(threading.current_thread()._name)}
    return bstack1ll1ll11l_opy_
  except Exception as e:
    logger.warn(bstack111llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᑒ").format(e))
  return
def bstack1111l11l1l_opy_():
    return platform.system() == bstack111llll_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪᑓ")
def bstack11l1llll1_opy_(bstack111111l111_opy_, config, logger):
    bstack111l1l11ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111111l111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᑔ").format(e))
    return bstack111l1l11ll_opy_
def bstack1111ll1111_opy_(bstack1111l1l111_opy_, bstack111l1111ll_opy_):
    bstack111l1111l1_opy_ = version.parse(bstack1111l1l111_opy_)
    bstack111l1l1ll1_opy_ = version.parse(bstack111l1111ll_opy_)
    if bstack111l1111l1_opy_ > bstack111l1l1ll1_opy_:
        return 1
    elif bstack111l1111l1_opy_ < bstack111l1l1ll1_opy_:
        return -1
    else:
        return 0
def bstack11l1ll11l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l11lll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111111ll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll11l1_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack111llll_opy_ (u"ࠫ࡬࡫ࡴࠨᑕ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11111111_opy_ = caps.get(bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᑖ"))
    bstack1111lll1ll_opy_ = True
    if bstack11111ll111_opy_(caps.get(bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬᑗ"))) or bstack11111ll111_opy_(caps.get(bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧᑘ"))):
        bstack1111lll1ll_opy_ = False
    if bstack1ll1ll1lll_opy_({bstack111llll_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣᑙ"): bstack1111lll1ll_opy_}):
        bstack11111111_opy_ = bstack11111111_opy_ or {}
        bstack11111111_opy_[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᑚ")] = bstack1111111ll1_opy_(framework)
        bstack11111111_opy_[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᑛ")] = bstack1111llll11_opy_()
        if getattr(options, bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᑜ"), None):
            options.set_capability(bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᑝ"), bstack11111111_opy_)
        else:
            options[bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᑞ")] = bstack11111111_opy_
    else:
        if getattr(options, bstack111llll_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᑟ"), None):
            options.set_capability(bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᑠ"), bstack1111111ll1_opy_(framework))
            options.set_capability(bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᑡ"), bstack1111llll11_opy_())
        else:
            options[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᑢ")] = bstack1111111ll1_opy_(framework)
            options[bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᑣ")] = bstack1111llll11_opy_()
    return options
def bstack1111l111l1_opy_(bstack1111lllll1_opy_, framework):
    if bstack1111lllll1_opy_ and len(bstack1111lllll1_opy_.split(bstack111llll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᑤ"))) > 1:
        ws_url = bstack1111lllll1_opy_.split(bstack111llll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᑥ"))[0]
        if bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᑦ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111l1111_opy_ = json.loads(urllib.parse.unquote(bstack1111lllll1_opy_.split(bstack111llll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᑧ"))[1]))
            bstack11111l1111_opy_ = bstack11111l1111_opy_ or {}
            bstack11111l1111_opy_[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᑨ")] = str(framework) + str(__version__)
            bstack11111l1111_opy_[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᑩ")] = bstack1111llll11_opy_()
            bstack1111lllll1_opy_ = bstack1111lllll1_opy_.split(bstack111llll_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᑪ"))[0] + bstack111llll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᑫ") + urllib.parse.quote(json.dumps(bstack11111l1111_opy_))
    return bstack1111lllll1_opy_
def bstack1l111lll_opy_():
    global bstack11l1l111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l1l111_opy_ = BrowserType.connect
    return bstack11l1l111_opy_
def bstack1lllll11l_opy_(framework_name):
    global bstack11lll111l_opy_
    bstack11lll111l_opy_ = framework_name
    return framework_name
def bstack1ll1111l11_opy_(self, *args, **kwargs):
    global bstack11l1l111_opy_
    try:
        global bstack11lll111l_opy_
        if bstack111llll_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᑬ") in kwargs:
            kwargs[bstack111llll_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᑭ")] = bstack1111l111l1_opy_(
                kwargs.get(bstack111llll_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᑮ"), None),
                bstack11lll111l_opy_
            )
    except Exception as e:
        logger.error(bstack111llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤᑯ").format(str(e)))
    return bstack11l1l111_opy_(self, *args, **kwargs)
def bstack1111l11111_opy_(bstack111111ll1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lllll11ll_opy_(bstack111111ll1l_opy_, bstack111llll_opy_ (u"ࠥࠦᑰ"))
        if proxies and proxies.get(bstack111llll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᑱ")):
            parsed_url = urlparse(proxies.get(bstack111llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᑲ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack111llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᑳ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack111llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᑴ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack111llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫᑵ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack111llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬᑶ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11ll1l11l_opy_(bstack111111ll1l_opy_):
    bstack11111llll1_opy_ = {
        bstack111l1lll1l_opy_[bstack11111l1l1l_opy_]: bstack111111ll1l_opy_[bstack11111l1l1l_opy_]
        for bstack11111l1l1l_opy_ in bstack111111ll1l_opy_
        if bstack11111l1l1l_opy_ in bstack111l1lll1l_opy_
    }
    bstack11111llll1_opy_[bstack111llll_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᑷ")] = bstack1111l11111_opy_(bstack111111ll1l_opy_, bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᑸ")))
    bstack111l11lll1_opy_ = [element.lower() for element in bstack111ll11l11_opy_]
    bstack1111l111ll_opy_(bstack11111llll1_opy_, bstack111l11lll1_opy_)
    return bstack11111llll1_opy_
def bstack1111l111ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack111llll_opy_ (u"ࠧ࠰ࠪࠫࠬࠥᑹ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111l111ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111l111ll_opy_(item, keys)