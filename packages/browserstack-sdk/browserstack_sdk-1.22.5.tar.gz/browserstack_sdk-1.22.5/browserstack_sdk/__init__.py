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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack111l1l1l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1llll11l1_opy_ import bstack1l1ll1l111_opy_
import time
import requests
def bstack1l111l11l1_opy_():
  global CONFIG
  headers = {
        bstack111llll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111llll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lllll11ll_opy_(CONFIG, bstack1111llll_opy_)
  try:
    response = requests.get(bstack1111llll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1l111l1l_opy_ = response.json()[bstack111llll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1ll11l111_opy_.format(response.json()))
      return bstack1l1l111l1l_opy_
    else:
      logger.debug(bstack1llll1lll_opy_.format(bstack111llll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1llll1lll_opy_.format(e))
def bstack11l1l1ll1_opy_(hub_url):
  global CONFIG
  url = bstack111llll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111llll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lllll11ll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1111111l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1111l1l1_opy_.format(hub_url, e))
def bstack1l11l1ll1l_opy_():
  try:
    global bstack11l111lll_opy_
    bstack1l1l111l1l_opy_ = bstack1l111l11l1_opy_()
    bstack1llll11ll_opy_ = []
    results = []
    for bstack1ll1111111_opy_ in bstack1l1l111l1l_opy_:
      bstack1llll11ll_opy_.append(bstack1llll1l1ll_opy_(target=bstack11l1l1ll1_opy_,args=(bstack1ll1111111_opy_,)))
    for t in bstack1llll11ll_opy_:
      t.start()
    for t in bstack1llll11ll_opy_:
      results.append(t.join())
    bstack1l11lll11l_opy_ = {}
    for item in results:
      hub_url = item[bstack111llll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111llll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l11lll11l_opy_[hub_url] = latency
    bstack11l1111ll_opy_ = min(bstack1l11lll11l_opy_, key= lambda x: bstack1l11lll11l_opy_[x])
    bstack11l111lll_opy_ = bstack11l1111ll_opy_
    logger.debug(bstack1l111ll11_opy_.format(bstack11l1111ll_opy_))
  except Exception as e:
    logger.debug(bstack1lll11111_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1ll1l1ll11_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1llll1_opy_, bstack1l1ll1l1l1_opy_, bstack11l1l1ll_opy_, bstack1llll11l1l_opy_, bstack1ll111ll1l_opy_, \
  Notset, bstack1ll1ll1lll_opy_, \
  bstack111l11l11_opy_, bstack1ll1l1l1l_opy_, bstack111l11ll1_opy_, bstack11111ll11_opy_, bstack1ll11lll1l_opy_, bstack1ll1ll1l11_opy_, \
  bstack1ll1l1llll_opy_, \
  bstack1llll1lll1_opy_, bstack1l11111l1_opy_, bstack1l1l1l1ll_opy_, bstack1l111llll_opy_, \
  bstack1ll1lllll1_opy_, bstack1l11ll1l1_opy_, bstack1l11ll1lll_opy_, bstack11ll1l11l_opy_
from bstack_utils.bstack1l11l1l1l1_opy_ import bstack1l11l11l1l_opy_
from bstack_utils.bstack1l11111l1l_opy_ import bstack1lll1l1ll1_opy_
from bstack_utils.bstack1l1l111111_opy_ import bstack1l1l1lll_opy_, bstack1l1l11ll_opy_
from bstack_utils.bstack111lll1ll_opy_ import bstack1l11l1lll_opy_
from bstack_utils.bstack1lll1ll11_opy_ import bstack1l1lll1111_opy_
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1l111l_opy_
from bstack_utils.proxy import bstack1l1l11ll1l_opy_, bstack1lllll11ll_opy_, bstack1ll11lll11_opy_, bstack1ll111l1l1_opy_
import bstack_utils.bstack1lll111l11_opy_ as bstack1l1111ll_opy_
from browserstack_sdk.bstack1l11lll1ll_opy_ import *
from browserstack_sdk.bstack1l1ll111l_opy_ import *
from bstack_utils.bstack1l11ll1111_opy_ import bstack1llllllll1_opy_
from browserstack_sdk.bstack1ll1l1l11l_opy_ import *
import bstack_utils.bstack11l111l11_opy_ as bstack11l1ll1l1_opy_
import bstack_utils.bstack1ll1lll11_opy_ as bstack11l11l111_opy_
bstack1l1ll11ll1_opy_ = bstack111llll_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1l1lll1ll1_opy_ = bstack111llll_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack11l1lllll_opy_ = None
CONFIG = {}
bstack1l1l1lll11_opy_ = {}
bstack1l111l1l1l_opy_ = {}
bstack1llll11111_opy_ = None
bstack1ll111lll_opy_ = None
bstack11lll1ll1_opy_ = None
bstack1lll1l1l_opy_ = -1
bstack11l111111_opy_ = 0
bstack1llll111_opy_ = bstack1l1lll111l_opy_
bstack11ll1ll1l_opy_ = 1
bstack1lll1l1l11_opy_ = False
bstack1ll11l1ll_opy_ = False
bstack11lll111l_opy_ = bstack111llll_opy_ (u"ࠨࠩࢂ")
bstack1l1lll1l_opy_ = bstack111llll_opy_ (u"ࠩࠪࢃ")
bstack11l1l1l1l_opy_ = False
bstack111l111l1_opy_ = True
bstack1l11ll11l1_opy_ = bstack111llll_opy_ (u"ࠪࠫࢄ")
bstack1l1111111l_opy_ = []
bstack11l111lll_opy_ = bstack111llll_opy_ (u"ࠫࠬࢅ")
bstack1111l111_opy_ = False
bstack1111ll11_opy_ = None
bstack111lll11l_opy_ = None
bstack1ll1llll1l_opy_ = None
bstack1lll11l11l_opy_ = -1
bstack1l1111l1l1_opy_ = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠬࢄࠧࢆ")), bstack111llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack111llll_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack11l1ll1ll_opy_ = 0
bstack1ll11llll_opy_ = 0
bstack1ll1111ll1_opy_ = []
bstack1llll1111l_opy_ = []
bstack1l1111111_opy_ = []
bstack1l11l11l_opy_ = []
bstack1l11l1l1l_opy_ = bstack111llll_opy_ (u"ࠨࠩࢉ")
bstack11111lll1_opy_ = bstack111llll_opy_ (u"ࠩࠪࢊ")
bstack111l1lll1_opy_ = False
bstack1ll11ll11l_opy_ = False
bstack1llll1l11_opy_ = {}
bstack1l1l1l11_opy_ = None
bstack11lll11ll_opy_ = None
bstack1lll11ll1_opy_ = None
bstack11lll1l11_opy_ = None
bstack1l11l11ll1_opy_ = None
bstack1l1l1ll1ll_opy_ = None
bstack1lll11ll1l_opy_ = None
bstack1l11l111l_opy_ = None
bstack1l11llll11_opy_ = None
bstack11l11111l_opy_ = None
bstack1l1l11l11l_opy_ = None
bstack1l1lll11l1_opy_ = None
bstack1l1ll1l1_opy_ = None
bstack1l1lll1l1_opy_ = None
bstack1l11lll1l1_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack1ll1ll11l1_opy_ = None
bstack1l1lllll11_opy_ = None
bstack1l11l1l11_opy_ = None
bstack1ll1l1111l_opy_ = None
bstack111ll11l1_opy_ = None
bstack11l1l111_opy_ = None
bstack11ll11lll_opy_ = False
bstack1l111l1ll1_opy_ = bstack111llll_opy_ (u"ࠥࠦࢋ")
logger = bstack1ll1l1ll11_opy_.get_logger(__name__, bstack1llll111_opy_)
bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
percy = bstack111llllll_opy_()
bstack111l1ll1_opy_ = bstack1l1ll1l111_opy_()
bstack1l1ll1ll11_opy_ = bstack1ll1l1l11l_opy_()
def bstack1lll1111l1_opy_():
  global CONFIG
  global bstack111l1lll1_opy_
  global bstack1l111l11ll_opy_
  bstack1lll11l11_opy_ = bstack1lll1l11l1_opy_(CONFIG)
  if bstack1ll111ll1l_opy_(CONFIG):
    if (bstack111llll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1lll11l11_opy_ and str(bstack1lll11l11_opy_[bstack111llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack111llll_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
      bstack111l1lll1_opy_ = True
    bstack1l111l11ll_opy_.bstack1lll1l1lll_opy_(bstack1lll11l11_opy_.get(bstack111llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
  else:
    bstack111l1lll1_opy_ = True
    bstack1l111l11ll_opy_.bstack1lll1l1lll_opy_(True)
def bstack1l1ll1ll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll111l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l111ll1l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111llll_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack111llll_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l11ll11l1_opy_
      bstack1l11ll11l1_opy_ += bstack111llll_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1llll1ll_opy_ = re.compile(bstack111llll_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1ll1l1l1ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1llll1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111llll_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack111llll_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1l11l1111l_opy_():
  bstack11111l1ll_opy_ = bstack1l111ll1l1_opy_()
  if bstack11111l1ll_opy_ and os.path.exists(os.path.abspath(bstack11111l1ll_opy_)):
    fileName = bstack11111l1ll_opy_
  if bstack111llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack111llll_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack111llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack111llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack1lll1ll_opy_ = os.path.abspath(fileName)
  else:
    bstack1lll1ll_opy_ = bstack111llll_opy_ (u"࢛ࠬ࠭")
  bstack1ll111l1ll_opy_ = os.getcwd()
  bstack1l1l11l1l_opy_ = bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l1ll1111_opy_ = bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack1lll1ll_opy_)) and bstack1ll111l1ll_opy_ != bstack111llll_opy_ (u"ࠣࠤ࢞"):
    bstack1lll1ll_opy_ = os.path.join(bstack1ll111l1ll_opy_, bstack1l1l11l1l_opy_)
    if not os.path.exists(bstack1lll1ll_opy_):
      bstack1lll1ll_opy_ = os.path.join(bstack1ll111l1ll_opy_, bstack1l1ll1111_opy_)
    if bstack1ll111l1ll_opy_ != os.path.dirname(bstack1ll111l1ll_opy_):
      bstack1ll111l1ll_opy_ = os.path.dirname(bstack1ll111l1ll_opy_)
    else:
      bstack1ll111l1ll_opy_ = bstack111llll_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack1lll1ll_opy_):
    bstack1l1l1l111l_opy_(
      bstack1l11llll1l_opy_.format(os.getcwd()))
  try:
    with open(bstack1lll1ll_opy_, bstack111llll_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack111llll_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1llll1ll_opy_)
      yaml.add_constructor(bstack111llll_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1ll1l1l1ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1lll1ll_opy_, bstack111llll_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l1l1l111l_opy_(bstack1l1111l11l_opy_.format(str(exc)))
def bstack1l1l11ll11_opy_(config):
  bstack1lll11111l_opy_ = bstack1l1l1ll1_opy_(config)
  for option in list(bstack1lll11111l_opy_):
    if option.lower() in bstack1l1lll1ll_opy_ and option != bstack1l1lll1ll_opy_[option.lower()]:
      bstack1lll11111l_opy_[bstack1l1lll1ll_opy_[option.lower()]] = bstack1lll11111l_opy_[option]
      del bstack1lll11111l_opy_[option]
  return config
def bstack11l1111l_opy_():
  global bstack1l111l1l1l_opy_
  for key, bstack1llll111ll_opy_ in bstack1l1l111l11_opy_.items():
    if isinstance(bstack1llll111ll_opy_, list):
      for var in bstack1llll111ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l111l1l1l_opy_[key] = os.environ[var]
          break
    elif bstack1llll111ll_opy_ in os.environ and os.environ[bstack1llll111ll_opy_] and str(os.environ[bstack1llll111ll_opy_]).strip():
      bstack1l111l1l1l_opy_[key] = os.environ[bstack1llll111ll_opy_]
  if bstack111llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1l111l1l1l_opy_[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1l111l1l1l_opy_[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack111llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1l1l1llll_opy_():
  global bstack1l1l1lll11_opy_
  global bstack1l11ll11l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111llll_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1l1l1lll11_opy_[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1l1l1lll11_opy_[bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack111llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack111111ll_opy_ in bstack1l1ll1llll_opy_.items():
    if isinstance(bstack111111ll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack111111ll_opy_:
          if idx < len(sys.argv) and bstack111llll_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1l1l1lll11_opy_:
            bstack1l1l1lll11_opy_[key] = sys.argv[idx + 1]
            bstack1l11ll11l1_opy_ += bstack111llll_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack111llll_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111llll_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack111111ll_opy_.lower() == val.lower() and not key in bstack1l1l1lll11_opy_:
          bstack1l1l1lll11_opy_[key] = sys.argv[idx + 1]
          bstack1l11ll11l1_opy_ += bstack111llll_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack111111ll_opy_ + bstack111llll_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack111l1l1ll_opy_(config):
  bstack1lllll1l1_opy_ = config.keys()
  for bstack111ll1111_opy_, bstack111lll1l1_opy_ in bstack1ll1111l1_opy_.items():
    if bstack111lll1l1_opy_ in bstack1lllll1l1_opy_:
      config[bstack111ll1111_opy_] = config[bstack111lll1l1_opy_]
      del config[bstack111lll1l1_opy_]
  for bstack111ll1111_opy_, bstack111lll1l1_opy_ in bstack1l1l1l111_opy_.items():
    if isinstance(bstack111lll1l1_opy_, list):
      for bstack1l1ll11l_opy_ in bstack111lll1l1_opy_:
        if bstack1l1ll11l_opy_ in bstack1lllll1l1_opy_:
          config[bstack111ll1111_opy_] = config[bstack1l1ll11l_opy_]
          del config[bstack1l1ll11l_opy_]
          break
    elif bstack111lll1l1_opy_ in bstack1lllll1l1_opy_:
      config[bstack111ll1111_opy_] = config[bstack111lll1l1_opy_]
      del config[bstack111lll1l1_opy_]
  for bstack1l1ll11l_opy_ in list(config):
    for bstack1l1l1l1l1_opy_ in bstack111111lll_opy_:
      if bstack1l1ll11l_opy_.lower() == bstack1l1l1l1l1_opy_.lower() and bstack1l1ll11l_opy_ != bstack1l1l1l1l1_opy_:
        config[bstack1l1l1l1l1_opy_] = config[bstack1l1ll11l_opy_]
        del config[bstack1l1ll11l_opy_]
  bstack111ll1l1l_opy_ = [{}]
  if not config.get(bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ")):
    config[bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")] = [{}]
  bstack111ll1l1l_opy_ = config[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ")]
  for platform in bstack111ll1l1l_opy_:
    for bstack1l1ll11l_opy_ in list(platform):
      for bstack1l1l1l1l1_opy_ in bstack111111lll_opy_:
        if bstack1l1ll11l_opy_.lower() == bstack1l1l1l1l1_opy_.lower() and bstack1l1ll11l_opy_ != bstack1l1l1l1l1_opy_:
          platform[bstack1l1l1l1l1_opy_] = platform[bstack1l1ll11l_opy_]
          del platform[bstack1l1ll11l_opy_]
  for bstack111ll1111_opy_, bstack111lll1l1_opy_ in bstack1l1l1l111_opy_.items():
    for platform in bstack111ll1l1l_opy_:
      if isinstance(bstack111lll1l1_opy_, list):
        for bstack1l1ll11l_opy_ in bstack111lll1l1_opy_:
          if bstack1l1ll11l_opy_ in platform:
            platform[bstack111ll1111_opy_] = platform[bstack1l1ll11l_opy_]
            del platform[bstack1l1ll11l_opy_]
            break
      elif bstack111lll1l1_opy_ in platform:
        platform[bstack111ll1111_opy_] = platform[bstack111lll1l1_opy_]
        del platform[bstack111lll1l1_opy_]
  for bstack111l11lll_opy_ in bstack111ll1l11_opy_:
    if bstack111l11lll_opy_ in config:
      if not bstack111ll1l11_opy_[bstack111l11lll_opy_] in config:
        config[bstack111ll1l11_opy_[bstack111l11lll_opy_]] = {}
      config[bstack111ll1l11_opy_[bstack111l11lll_opy_]].update(config[bstack111l11lll_opy_])
      del config[bstack111l11lll_opy_]
  for platform in bstack111ll1l1l_opy_:
    for bstack111l11lll_opy_ in bstack111ll1l11_opy_:
      if bstack111l11lll_opy_ in list(platform):
        if not bstack111ll1l11_opy_[bstack111l11lll_opy_] in platform:
          platform[bstack111ll1l11_opy_[bstack111l11lll_opy_]] = {}
        platform[bstack111ll1l11_opy_[bstack111l11lll_opy_]].update(platform[bstack111l11lll_opy_])
        del platform[bstack111l11lll_opy_]
  config = bstack1l1l11ll11_opy_(config)
  return config
def bstack1lll1l11l_opy_(config):
  global bstack1l1lll1l_opy_
  if bstack1ll111ll1l_opy_(config) and bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ") in config and str(config[bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ")]).lower() != bstack111llll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢸ"):
    if not bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ") in config:
      config[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ")] = {}
    if not config[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")].get(bstack111llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧࢼ")) and not bstack111llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack1ll1llllll_opy_ = datetime.datetime.now()
      bstack1l1lll11ll_opy_ = bstack1ll1llllll_opy_.strftime(bstack111llll_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack1lll1lllll_opy_ = bstack111llll_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111llll_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1l1lll11ll_opy_, hostname, bstack1lll1lllll_opy_)
      config[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack111llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack1l1lll1l_opy_ = config[bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")].get(bstack111llll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ"))
  return config
def bstack11lllll11_opy_():
  bstack11llllll1l_opy_ =  bstack11111ll11_opy_()[bstack111llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack11llllll1l_opy_ if bstack11llllll1l_opy_ else -1
def bstack1l1ll1l1ll_opy_(bstack11llllll1l_opy_):
  global CONFIG
  if not bstack111llll_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack111llll_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack11llllll1l_opy_)
  )
def bstack1l1l11lll_opy_():
  global CONFIG
  if not bstack111llll_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack111llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack1ll1llllll_opy_ = datetime.datetime.now()
  bstack1l1lll11ll_opy_ = bstack1ll1llllll_opy_.strftime(bstack111llll_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack111llll_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1l1lll11ll_opy_
  )
def bstack111ll1l1_opy_():
  global CONFIG
  if bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack111llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack111llll_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack111llll_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack1l1l11lll_opy_()
    os.environ[bstack111llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack111llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack111llll_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack11llllll1l_opy_ = bstack111llll_opy_ (u"ࠩࠪࣞ")
  bstack1ll111llll_opy_ = bstack11lllll11_opy_()
  if bstack1ll111llll_opy_ != -1:
    bstack11llllll1l_opy_ = bstack111llll_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1ll111llll_opy_)
  if bstack11llllll1l_opy_ == bstack111llll_opy_ (u"ࠫࠬ࣠"):
    bstack11l1l11l_opy_ = bstack1l11lll11_opy_(CONFIG[bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack11l1l11l_opy_ != -1:
      bstack11llllll1l_opy_ = str(bstack11l1l11l_opy_)
  if bstack11llllll1l_opy_:
    bstack1l1ll1l1ll_opy_(bstack11llllll1l_opy_)
    os.environ[bstack111llll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack1l1lllll1l_opy_(bstack111l1lll_opy_, bstack1l1l11l1l1_opy_, path):
  bstack1l1ll11lll_opy_ = {
    bstack111llll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack1l1l11l1l1_opy_
  }
  if os.path.exists(path):
    bstack1ll1l111l1_opy_ = json.load(open(path, bstack111llll_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack1ll1l111l1_opy_ = {}
  bstack1ll1l111l1_opy_[bstack111l1lll_opy_] = bstack1l1ll11lll_opy_
  with open(path, bstack111llll_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack1ll1l111l1_opy_, outfile)
def bstack1l11lll11_opy_(bstack111l1lll_opy_):
  bstack111l1lll_opy_ = str(bstack111l1lll_opy_)
  bstack1ll1llll11_opy_ = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠫࢃ࠭ࣧ")), bstack111llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack1ll1llll11_opy_):
      os.makedirs(bstack1ll1llll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"࠭ࡾࠨࣩ")), bstack111llll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack111llll_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111llll_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack111llll_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111llll_opy_ (u"ࠫࡷ࣮࠭")) as bstack1l111ll1_opy_:
      bstack11l1ll11l_opy_ = json.load(bstack1l111ll1_opy_)
    if bstack111l1lll_opy_ in bstack11l1ll11l_opy_:
      bstack1lllllll1_opy_ = bstack11l1ll11l_opy_[bstack111l1lll_opy_][bstack111llll_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack1ll11ll1l1_opy_ = int(bstack1lllllll1_opy_) + 1
      bstack1l1lllll1l_opy_(bstack111l1lll_opy_, bstack1ll11ll1l1_opy_, file_path)
      return bstack1ll11ll1l1_opy_
    else:
      bstack1l1lllll1l_opy_(bstack111l1lll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll111ll1_opy_.format(str(e)))
    return -1
def bstack1l111lll1l_opy_(config):
  if not config[bstack111llll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack111llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack1llll1111_opy_(config, index=0):
  global bstack11l1l1l1l_opy_
  bstack11111111_opy_ = {}
  caps = bstack1l11l1l1_opy_ + bstack1ll11l1111_opy_
  if bstack11l1l1l1l_opy_:
    caps += bstack11llllll_opy_
  for key in config:
    if key in caps + [bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack11111111_opy_[key] = config[key]
  if bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack11ll1111_opy_ in config[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack11ll1111_opy_ in caps:
        continue
      bstack11111111_opy_[bstack11ll1111_opy_] = config[bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index][bstack11ll1111_opy_]
  bstack11111111_opy_[bstack111llll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࣶࠧ")] = socket.gethostname()
  if bstack111llll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ") in bstack11111111_opy_:
    del (bstack11111111_opy_[bstack111llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ")])
  return bstack11111111_opy_
def bstack1ll11ll1l_opy_(config):
  global bstack11l1l1l1l_opy_
  bstack1ll1l1l1l1_opy_ = {}
  caps = bstack1ll11l1111_opy_
  if bstack11l1l1l1l_opy_:
    caps += bstack11llllll_opy_
  for key in caps:
    if key in config:
      bstack1ll1l1l1l1_opy_[key] = config[key]
  return bstack1ll1l1l1l1_opy_
def bstack1l1l111ll1_opy_(bstack11111111_opy_, bstack1ll1l1l1l1_opy_):
  bstack1ll1l1lll_opy_ = {}
  for key in bstack11111111_opy_.keys():
    if key in bstack1ll1111l1_opy_:
      bstack1ll1l1lll_opy_[bstack1ll1111l1_opy_[key]] = bstack11111111_opy_[key]
    else:
      bstack1ll1l1lll_opy_[key] = bstack11111111_opy_[key]
  for key in bstack1ll1l1l1l1_opy_:
    if key in bstack1ll1111l1_opy_:
      bstack1ll1l1lll_opy_[bstack1ll1111l1_opy_[key]] = bstack1ll1l1l1l1_opy_[key]
    else:
      bstack1ll1l1lll_opy_[key] = bstack1ll1l1l1l1_opy_[key]
  return bstack1ll1l1lll_opy_
def bstack111llll1_opy_(config, index=0):
  global bstack11l1l1l1l_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l1l1ll1l_opy_ = bstack11l1llll1_opy_(bstack1l11l1l1ll_opy_, config, logger)
  bstack1ll1l1l1l1_opy_ = bstack1ll11ll1l_opy_(config)
  bstack11l1l1lll_opy_ = bstack1ll11l1111_opy_
  bstack11l1l1lll_opy_ += bstack1l1l1l11l1_opy_
  bstack1ll1l1l1l1_opy_ = update(bstack1ll1l1l1l1_opy_, bstack1l1l1ll1l_opy_)
  if bstack11l1l1l1l_opy_:
    bstack11l1l1lll_opy_ += bstack11llllll_opy_
  if bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ") in config:
    if bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࣺࠧ") in config[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")][index]:
      caps[bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ")] = config[bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index][bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")]
    if bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣿ") in config[bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index]:
      caps[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ")] = str(config[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index][bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")])
    bstack111lllll1_opy_ = bstack11l1llll1_opy_(bstack1l11l1l1ll_opy_, config[bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index], logger)
    bstack11l1l1lll_opy_ += list(bstack111lllll1_opy_.keys())
    for bstack1l11l1l11l_opy_ in bstack11l1l1lll_opy_:
      if bstack1l11l1l11l_opy_ in config[bstack111llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1l11l1l11l_opy_ == bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack111lllll1_opy_[bstack1l11l1l11l_opy_] = str(config[bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1l11l1l11l_opy_] * 1.0)
          except:
            bstack111lllll1_opy_[bstack1l11l1l11l_opy_] = str(config[bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1l11l1l11l_opy_])
        else:
          bstack111lllll1_opy_[bstack1l11l1l11l_opy_] = config[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l11l1l11l_opy_]
        del (config[bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l11l1l11l_opy_])
    bstack1ll1l1l1l1_opy_ = update(bstack1ll1l1l1l1_opy_, bstack111lllll1_opy_)
  bstack11111111_opy_ = bstack1llll1111_opy_(config, index)
  for bstack1l1ll11l_opy_ in bstack1ll11l1111_opy_ + list(bstack1l1l1ll1l_opy_.keys()):
    if bstack1l1ll11l_opy_ in bstack11111111_opy_:
      bstack1ll1l1l1l1_opy_[bstack1l1ll11l_opy_] = bstack11111111_opy_[bstack1l1ll11l_opy_]
      del (bstack11111111_opy_[bstack1l1ll11l_opy_])
  if bstack1ll1ll1lll_opy_(config):
    bstack11111111_opy_[bstack111llll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1ll1l1l1l1_opy_)
    caps[bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack11111111_opy_
  else:
    bstack11111111_opy_[bstack111llll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack1l1l111ll1_opy_(bstack11111111_opy_, bstack1ll1l1l1l1_opy_))
    if bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1llll1ll1l_opy_():
  global bstack11l111lll_opy_
  if bstack1lll111l1_opy_() <= version.parse(bstack111llll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack11l111lll_opy_ != bstack111llll_opy_ (u"ࠪࠫग"):
      return bstack111llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack11l111lll_opy_ + bstack111llll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1lll1lll1_opy_
  if bstack11l111lll_opy_ != bstack111llll_opy_ (u"࠭ࠧच"):
    return bstack111llll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack11l111lll_opy_ + bstack111llll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1l111l1l11_opy_
def bstack1111l1lll_opy_(options):
  return hasattr(options, bstack111llll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l11lll111_opy_(options, bstack1l1l1ll111_opy_):
  for bstack1l11l111ll_opy_ in bstack1l1l1ll111_opy_:
    if bstack1l11l111ll_opy_ in [bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack111llll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack1l11l111ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l111ll_opy_] = update(options._experimental_options[bstack1l11l111ll_opy_],
                                                         bstack1l1l1ll111_opy_[bstack1l11l111ll_opy_])
    else:
      options.add_experimental_option(bstack1l11l111ll_opy_, bstack1l1l1ll111_opy_[bstack1l11l111ll_opy_])
  if bstack111llll_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack1l1l1ll111_opy_:
    for arg in bstack1l1l1ll111_opy_[bstack111llll_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack1l1l1ll111_opy_[bstack111llll_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack111llll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack1l1l1ll111_opy_:
    for ext in bstack1l1l1ll111_opy_[bstack111llll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack1l1l1ll111_opy_[bstack111llll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack111l11l1l_opy_(options, bstack1l111l111l_opy_):
  if bstack111llll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1l111l111l_opy_:
    for bstack1ll1lllll_opy_ in bstack1l111l111l_opy_[bstack111llll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1ll1lllll_opy_ in options._preferences:
        options._preferences[bstack1ll1lllll_opy_] = update(options._preferences[bstack1ll1lllll_opy_], bstack1l111l111l_opy_[bstack111llll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1ll1lllll_opy_])
      else:
        options.set_preference(bstack1ll1lllll_opy_, bstack1l111l111l_opy_[bstack111llll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1ll1lllll_opy_])
  if bstack111llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1l111l111l_opy_:
    for arg in bstack1l111l111l_opy_[bstack111llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1lll11lll_opy_(options, bstack1ll11l1ll1_opy_):
  if bstack111llll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack1ll11l1ll1_opy_:
    options.use_webview(bool(bstack1ll11l1ll1_opy_[bstack111llll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1l11lll111_opy_(options, bstack1ll11l1ll1_opy_)
def bstack1ll1lll1ll_opy_(options, bstack1ll111111l_opy_):
  for bstack111lll111_opy_ in bstack1ll111111l_opy_:
    if bstack111lll111_opy_ in [bstack111llll_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack111llll_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack111lll111_opy_, bstack1ll111111l_opy_[bstack111lll111_opy_])
  if bstack111llll_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1ll111111l_opy_:
    for arg in bstack1ll111111l_opy_[bstack111llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack111llll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1ll111111l_opy_:
    options.bstack11lllll1l1_opy_(bool(bstack1ll111111l_opy_[bstack111llll_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack1l1l11l11_opy_(options, bstack1l1lll1l11_opy_):
  for bstack11llll11_opy_ in bstack1l1lll1l11_opy_:
    if bstack11llll11_opy_ in [bstack111llll_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack111llll_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack11llll11_opy_] = bstack1l1lll1l11_opy_[bstack11llll11_opy_]
  if bstack111llll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1l1lll1l11_opy_:
    for bstack11111llll_opy_ in bstack1l1lll1l11_opy_[bstack111llll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1l11l11l11_opy_(
        bstack11111llll_opy_, bstack1l1lll1l11_opy_[bstack111llll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack11111llll_opy_])
  if bstack111llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1l1lll1l11_opy_:
    for arg in bstack1l1lll1l11_opy_[bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1l1l1l1l11_opy_(options, caps):
  if not hasattr(options, bstack111llll_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack111llll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1l11lll111_opy_(options, caps[bstack111llll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack111llll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack111l11l1l_opy_(options, caps[bstack111llll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack111llll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack1ll1lll1ll_opy_(options, caps[bstack111llll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack111llll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1lll11lll_opy_(options, caps[bstack111llll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack111llll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack1l1l11l11_opy_(options, caps[bstack111llll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1ll1llll1_opy_(caps):
  global bstack11l1l1l1l_opy_
  if isinstance(os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack11l1l1l1l_opy_ = eval(os.getenv(bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack11l1l1l1l_opy_:
    if bstack1l1ll1ll1_opy_() < version.parse(bstack111llll_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack111llll_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack111llll_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack111llll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack111llll_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack111llll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack111llll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack111llll_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack111llll_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack111llll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack111llll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack111llll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack111llll_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1111l1lll_opy_(options):
        return None
      for bstack1l1ll11l_opy_ in caps.keys():
        options.set_capability(bstack1l1ll11l_opy_, caps[bstack1l1ll11l_opy_])
      bstack1l1l1l1l11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l11llll_opy_(options, bstack1ll1ll1l_opy_):
  if not bstack1111l1lll_opy_(options):
    return
  for bstack1l1ll11l_opy_ in bstack1ll1ll1l_opy_.keys():
    if bstack1l1ll11l_opy_ in bstack1l1l1l11l1_opy_:
      continue
    if bstack1l1ll11l_opy_ in options._caps and type(options._caps[bstack1l1ll11l_opy_]) in [dict, list]:
      options._caps[bstack1l1ll11l_opy_] = update(options._caps[bstack1l1ll11l_opy_], bstack1ll1ll1l_opy_[bstack1l1ll11l_opy_])
    else:
      options.set_capability(bstack1l1ll11l_opy_, bstack1ll1ll1l_opy_[bstack1l1ll11l_opy_])
  bstack1l1l1l1l11_opy_(options, bstack1ll1ll1l_opy_)
  if bstack111llll_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack111llll_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack111llll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1l11ll1ll_opy_(proxy_config):
  if bstack111llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack111llll_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack111llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack111llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack111llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack111llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack111llll_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack111llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack111llll_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack111llll_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack111llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack111llll_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack11lll1lll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack111llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1l11ll1ll_opy_(config[bstack111llll_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack111llll_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack1ll11l1l_opy_(self):
  global CONFIG
  global bstack1l1lll11l1_opy_
  try:
    proxy = bstack1ll11lll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111llll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack1l1l11ll1l_opy_(proxy, bstack1llll1ll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l1l_opy_ = proxies.popitem()
          if bstack111llll_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1l111l1l_opy_:
            return bstack1l111l1l_opy_
          else:
            return bstack111llll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1l111l1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1l1lll11l1_opy_(self)
def bstack1l11ll1l11_opy_():
  global CONFIG
  return bstack1ll111l1l1_opy_(CONFIG) and bstack1ll1ll1l11_opy_() and bstack1lll111l1_opy_() >= version.parse(bstack1l1l1l11l_opy_)
def bstack1ll11lll1_opy_():
  global CONFIG
  return (bstack111llll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack111llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack1ll1l1llll_opy_()
def bstack1l1l1ll1_opy_(config):
  bstack1lll11111l_opy_ = {}
  if bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack1lll11111l_opy_ = config[bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack111llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack1lll11111l_opy_ = config[bstack111llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack1ll11lll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack111llll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack1lll11111l_opy_[bstack111llll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111llll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack1lllll11ll_opy_(config, bstack1llll1ll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111l1l_opy_ = proxies.popitem()
          if bstack111llll_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack1l111l1l_opy_:
            parsed_url = urlparse(bstack1l111l1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111llll_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack1l111l1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll11111l_opy_[bstack111llll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll11111l_opy_[bstack111llll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll11111l_opy_[bstack111llll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll11111l_opy_[bstack111llll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack1lll11111l_opy_
def bstack1lll1l11l1_opy_(config):
  if bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack11llllllll_opy_(caps):
  global bstack1l1lll1l_opy_
  if bstack111llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack111llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack111llll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack1l1lll1l_opy_:
      caps[bstack111llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack111llll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack1l1lll1l_opy_
  else:
    caps[bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack1l1lll1l_opy_:
      caps[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack1l1lll1l_opy_
def bstack1111l1l1l_opy_():
  global CONFIG
  if not bstack1ll111ll1l_opy_(CONFIG):
    return
  if bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack1l11ll1lll_opy_(CONFIG[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    if (
      bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍") in CONFIG
      and bstack1l11ll1lll_opy_(CONFIG[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")].get(bstack111llll_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨএ")))
    ):
      logger.debug(bstack111llll_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨঐ"))
      return
    bstack1lll11111l_opy_ = bstack1l1l1ll1_opy_(CONFIG)
    bstack1ll11111ll_opy_(CONFIG[bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1lll11111l_opy_)
def bstack1ll11111ll_opy_(key, bstack1lll11111l_opy_):
  global bstack11l1lllll_opy_
  logger.info(bstack1l111ll111_opy_)
  try:
    bstack11l1lllll_opy_ = Local()
    bstack1ll111ll1_opy_ = {bstack111llll_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1ll111ll1_opy_.update(bstack1lll11111l_opy_)
    logger.debug(bstack11l1lll11_opy_.format(str(bstack1ll111ll1_opy_)))
    bstack11l1lllll_opy_.start(**bstack1ll111ll1_opy_)
    if bstack11l1lllll_opy_.isRunning():
      logger.info(bstack1l1ll11l11_opy_)
  except Exception as e:
    bstack1l1l1l111l_opy_(bstack1l11111l11_opy_.format(str(e)))
def bstack1l1l11111_opy_():
  global bstack11l1lllll_opy_
  if bstack11l1lllll_opy_.isRunning():
    logger.info(bstack11lll11l_opy_)
    bstack11l1lllll_opy_.stop()
  bstack11l1lllll_opy_ = None
def bstack11ll111l1_opy_(bstack111l111ll_opy_=[]):
  global CONFIG
  bstack1ll11l1l1l_opy_ = []
  bstack1ll1llll_opy_ = [bstack111llll_opy_ (u"ࠨࡱࡶࠫও"), bstack111llll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack111llll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack111l111ll_opy_:
      bstack1ll11ll1_opy_ = {}
      for k in bstack1ll1llll_opy_:
        val = CONFIG[bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack111llll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1ll11ll1_opy_[k] = val
      if(err[bstack111llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack111llll_opy_ (u"ࠪࠫজ")):
        bstack1ll11ll1_opy_[bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack111llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack111llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1ll11l1l1l_opy_.append(bstack1ll11ll1_opy_)
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1ll11l1l1l_opy_
def bstack111l1l11_opy_(file_name):
  bstack1l1l1ll1l1_opy_ = []
  try:
    bstack1l111llll1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l111llll1_opy_):
      with open(bstack1l111llll1_opy_) as f:
        bstack1ll1111lll_opy_ = json.load(f)
        bstack1l1l1ll1l1_opy_ = bstack1ll1111lll_opy_
      os.remove(bstack1l111llll1_opy_)
    return bstack1l1l1ll1l1_opy_
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
    return bstack1l1l1ll1l1_opy_
def bstack1l11ll11l_opy_():
  global bstack1l111l1ll1_opy_
  global bstack1l1111111l_opy_
  global bstack1ll1111ll1_opy_
  global bstack1llll1111l_opy_
  global bstack1l1111111_opy_
  global bstack11111lll1_opy_
  global CONFIG
  bstack1l1l11111l_opy_ = os.environ.get(bstack111llll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1l1l11111l_opy_ in [bstack111llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack111llll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1l1111l11_opy_()
  percy.shutdown()
  if bstack1l111l1ll1_opy_:
    logger.warning(bstack1l1ll1lll_opy_.format(str(bstack1l111l1ll1_opy_)))
  else:
    try:
      bstack1ll1l111l1_opy_ = bstack111l11l11_opy_(bstack111llll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1ll1l111l1_opy_.get(bstack111llll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1ll1l111l1_opy_.get(bstack111llll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack111llll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1l1ll1lll_opy_.format(str(bstack1ll1l111l1_opy_[bstack111llll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack111llll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll1l1111_opy_)
  global bstack11l1lllll_opy_
  if bstack11l1lllll_opy_:
    bstack1l1l11111_opy_()
  try:
    for driver in bstack1l1111111l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11lll1l1l_opy_)
  if bstack11111lll1_opy_ == bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1l1111111_opy_ = bstack111l1l11_opy_(bstack111llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack11111lll1_opy_ == bstack111llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1llll1111l_opy_) == 0:
    bstack1llll1111l_opy_ = bstack111l1l11_opy_(bstack111llll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1llll1111l_opy_) == 0:
      bstack1llll1111l_opy_ = bstack111l1l11_opy_(bstack111llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1llll1l111_opy_ = bstack111llll_opy_ (u"ࠩࠪর")
  if len(bstack1ll1111ll1_opy_) > 0:
    bstack1llll1l111_opy_ = bstack11ll111l1_opy_(bstack1ll1111ll1_opy_)
  elif len(bstack1llll1111l_opy_) > 0:
    bstack1llll1l111_opy_ = bstack11ll111l1_opy_(bstack1llll1111l_opy_)
  elif len(bstack1l1111111_opy_) > 0:
    bstack1llll1l111_opy_ = bstack11ll111l1_opy_(bstack1l1111111_opy_)
  elif len(bstack1l11l11l_opy_) > 0:
    bstack1llll1l111_opy_ = bstack11ll111l1_opy_(bstack1l11l11l_opy_)
  if bool(bstack1llll1l111_opy_):
    bstack11111l111_opy_(bstack1llll1l111_opy_)
  else:
    bstack11111l111_opy_()
  bstack1ll1l1l1l_opy_(bstack1ll1l111ll_opy_, logger)
  bstack1ll1l1ll11_opy_.bstack11l1l111l_opy_(CONFIG)
  if len(bstack1l1111111_opy_) > 0:
    sys.exit(len(bstack1l1111111_opy_))
def bstack1llll1l1l1_opy_(bstack1ll11l11l_opy_, frame):
  global bstack1l111l11ll_opy_
  logger.error(bstack1l11ll111_opy_)
  bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭঱"), bstack1ll11l11l_opy_)
  if hasattr(signal, bstack111llll_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬল")):
    bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ঳"), signal.Signals(bstack1ll11l11l_opy_).name)
  else:
    bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭঴"), bstack111llll_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫ঵"))
  bstack1l1l11111l_opy_ = os.environ.get(bstack111llll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩশ"))
  if bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩষ"):
    bstack1l11l1lll_opy_.stop(bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪস")))
  bstack1l11ll11l_opy_()
  sys.exit(1)
def bstack1l1l1l111l_opy_(err):
  logger.critical(bstack1l111l1111_opy_.format(str(err)))
  bstack11111l111_opy_(bstack1l111l1111_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11ll11l_opy_)
  bstack1l1111l11_opy_()
  sys.exit(1)
def bstack11l1l1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11111l111_opy_(message, True)
  atexit.unregister(bstack1l11ll11l_opy_)
  bstack1l1111l11_opy_()
  sys.exit(1)
def bstack1ll1l1ll1l_opy_():
  global CONFIG
  global bstack1l1l1lll11_opy_
  global bstack1l111l1l1l_opy_
  global bstack111l111l1_opy_
  CONFIG = bstack1l11l1111l_opy_()
  load_dotenv(CONFIG.get(bstack111llll_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬহ")))
  bstack11l1111l_opy_()
  bstack1l1l1llll_opy_()
  CONFIG = bstack111l1l1ll_opy_(CONFIG)
  update(CONFIG, bstack1l111l1l1l_opy_)
  update(CONFIG, bstack1l1l1lll11_opy_)
  CONFIG = bstack1lll1l11l_opy_(CONFIG)
  bstack111l111l1_opy_ = bstack1ll111ll1l_opy_(CONFIG)
  os.environ[bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ঺")] = bstack111l111l1_opy_.__str__()
  bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ঻"), bstack111l111l1_opy_)
  if (bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") in CONFIG and bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫঽ") in bstack1l1l1lll11_opy_) or (
          bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬা") in CONFIG and bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ি") not in bstack1l111l1l1l_opy_):
    if os.getenv(bstack111llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨী")):
      CONFIG[bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧু")] = os.getenv(bstack111llll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪূ"))
    else:
      bstack111ll1l1_opy_()
  elif (bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪৃ") not in CONFIG and bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৄ") in CONFIG) or (
          bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৅") in bstack1l111l1l1l_opy_ and bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭৆") not in bstack1l1l1lll11_opy_):
    del (CONFIG[bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ে")])
  if bstack1l111lll1l_opy_(CONFIG):
    bstack1l1l1l111l_opy_(bstack1ll111l1_opy_)
  bstack1l1llll1l_opy_()
  bstack1l11111lll_opy_()
  if bstack11l1l1l1l_opy_:
    CONFIG[bstack111llll_opy_ (u"ࠬࡧࡰࡱࠩৈ")] = bstack1l11111111_opy_(CONFIG)
    logger.info(bstack1l111lll1_opy_.format(CONFIG[bstack111llll_opy_ (u"࠭ࡡࡱࡲࠪ৉")]))
  if not bstack111l111l1_opy_:
    CONFIG[bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৊")] = [{}]
def bstack1l11l11111_opy_(config, bstack1l11l1l111_opy_):
  global CONFIG
  global bstack11l1l1l1l_opy_
  CONFIG = config
  bstack11l1l1l1l_opy_ = bstack1l11l1l111_opy_
def bstack1l11111lll_opy_():
  global CONFIG
  global bstack11l1l1l1l_opy_
  if bstack111llll_opy_ (u"ࠨࡣࡳࡴࠬো") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1lll11ll_opy_)
    bstack11l1l1l1l_opy_ = True
    bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨৌ"), True)
def bstack1l11111111_opy_(config):
  bstack111l1l1l_opy_ = bstack111llll_opy_ (u"্ࠪࠫ")
  app = config[bstack111llll_opy_ (u"ࠫࡦࡶࡰࠨৎ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll1ll1111_opy_:
      if os.path.exists(app):
        bstack111l1l1l_opy_ = bstack11111l11l_opy_(config, app)
      elif bstack1ll1l11l11_opy_(app):
        bstack111l1l1l_opy_ = app
      else:
        bstack1l1l1l111l_opy_(bstack1l1llll11l_opy_.format(app))
    else:
      if bstack1ll1l11l11_opy_(app):
        bstack111l1l1l_opy_ = app
      elif os.path.exists(app):
        bstack111l1l1l_opy_ = bstack11111l11l_opy_(app)
      else:
        bstack1l1l1l111l_opy_(bstack1lll1111l_opy_)
  else:
    if len(app) > 2:
      bstack1l1l1l111l_opy_(bstack11ll1l111_opy_)
    elif len(app) == 2:
      if bstack111llll_opy_ (u"ࠬࡶࡡࡵࡪࠪ৏") in app and bstack111llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐") in app:
        if os.path.exists(app[bstack111llll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৑")]):
          bstack111l1l1l_opy_ = bstack11111l11l_opy_(config, app[bstack111llll_opy_ (u"ࠨࡲࡤࡸ࡭࠭৒")], app[bstack111llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৓")])
        else:
          bstack1l1l1l111l_opy_(bstack1l1llll11l_opy_.format(app))
      else:
        bstack1l1l1l111l_opy_(bstack11ll1l111_opy_)
    else:
      for key in app:
        if key in bstack1ll1l11lll_opy_:
          if key == bstack111llll_opy_ (u"ࠪࡴࡦࡺࡨࠨ৔"):
            if os.path.exists(app[key]):
              bstack111l1l1l_opy_ = bstack11111l11l_opy_(config, app[key])
            else:
              bstack1l1l1l111l_opy_(bstack1l1llll11l_opy_.format(app))
          else:
            bstack111l1l1l_opy_ = app[key]
        else:
          bstack1l1l1l111l_opy_(bstack1lll111lll_opy_)
  return bstack111l1l1l_opy_
def bstack1ll1l11l11_opy_(bstack111l1l1l_opy_):
  import re
  bstack1l1111l1l_opy_ = re.compile(bstack111llll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৕"))
  bstack1l1l1111ll_opy_ = re.compile(bstack111llll_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ৖"))
  if bstack111llll_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬৗ") in bstack111l1l1l_opy_ or re.fullmatch(bstack1l1111l1l_opy_, bstack111l1l1l_opy_) or re.fullmatch(bstack1l1l1111ll_opy_, bstack111l1l1l_opy_):
    return True
  else:
    return False
def bstack11111l11l_opy_(config, path, bstack11llll111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111llll_opy_ (u"ࠧࡳࡤࠪ৘")).read()).hexdigest()
  bstack1l1l1111_opy_ = bstack1l1lllll1_opy_(md5_hash)
  bstack111l1l1l_opy_ = None
  if bstack1l1l1111_opy_:
    logger.info(bstack11l11l1l_opy_.format(bstack1l1l1111_opy_, md5_hash))
    return bstack1l1l1111_opy_
  bstack1l1ll1lll1_opy_ = MultipartEncoder(
    fields={
      bstack111llll_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭৙"): (os.path.basename(path), open(os.path.abspath(path), bstack111llll_opy_ (u"ࠩࡵࡦࠬ৚")), bstack111llll_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧ৛")),
      bstack111llll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧড়"): bstack11llll111_opy_
    }
  )
  response = requests.post(bstack1l1lll11l_opy_, data=bstack1l1ll1lll1_opy_,
                           headers={bstack111llll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫঢ়"): bstack1l1ll1lll1_opy_.content_type},
                           auth=(config[bstack111llll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ৞")], config[bstack111llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪয়")]))
  try:
    res = json.loads(response.text)
    bstack111l1l1l_opy_ = res[bstack111llll_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩৠ")]
    logger.info(bstack1l1l1111l_opy_.format(bstack111l1l1l_opy_))
    bstack1ll1l1l111_opy_(md5_hash, bstack111l1l1l_opy_)
  except ValueError as err:
    bstack1l1l1l111l_opy_(bstack1ll11l1lll_opy_.format(str(err)))
  return bstack111l1l1l_opy_
def bstack1l1llll1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11ll1ll1l_opy_
  bstack1l1l1llll1_opy_ = 1
  bstack111ll11ll_opy_ = 1
  if bstack111llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩৡ") in CONFIG:
    bstack111ll11ll_opy_ = CONFIG[bstack111llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪৢ")]
  else:
    bstack111ll11ll_opy_ = bstack11llll1l1_opy_(framework_name, args) or 1
  if bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ") in CONFIG:
    bstack1l1l1llll1_opy_ = len(CONFIG[bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৤")])
  bstack11ll1ll1l_opy_ = int(bstack111ll11ll_opy_) * int(bstack1l1l1llll1_opy_)
def bstack11llll1l1_opy_(framework_name, args):
  if framework_name == bstack1l1l1ll11_opy_ and args and bstack111llll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ৥") in args:
      bstack11lll111_opy_ = args.index(bstack111llll_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ০"))
      return int(args[bstack11lll111_opy_ + 1]) or 1
  return 1
def bstack1l1lllll1_opy_(md5_hash):
  bstack1llll11l11_opy_ = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠨࢀࠪ১")), bstack111llll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ২"), bstack111llll_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৩"))
  if os.path.exists(bstack1llll11l11_opy_):
    bstack1lll1lll1l_opy_ = json.load(open(bstack1llll11l11_opy_, bstack111llll_opy_ (u"ࠫࡷࡨࠧ৪")))
    if md5_hash in bstack1lll1lll1l_opy_:
      bstack1l11ll1ll1_opy_ = bstack1lll1lll1l_opy_[md5_hash]
      bstack1l11111ll1_opy_ = datetime.datetime.now()
      bstack1l1lll11_opy_ = datetime.datetime.strptime(bstack1l11ll1ll1_opy_[bstack111llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৫")], bstack111llll_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৬"))
      if (bstack1l11111ll1_opy_ - bstack1l1lll11_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11ll1ll1_opy_[bstack111llll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৭")]):
        return None
      return bstack1l11ll1ll1_opy_[bstack111llll_opy_ (u"ࠨ࡫ࡧࠫ৮")]
  else:
    return None
def bstack1ll1l1l111_opy_(md5_hash, bstack111l1l1l_opy_):
  bstack1ll1llll11_opy_ = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠩࢁࠫ৯")), bstack111llll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৰ"))
  if not os.path.exists(bstack1ll1llll11_opy_):
    os.makedirs(bstack1ll1llll11_opy_)
  bstack1llll11l11_opy_ = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠫࢃ࠭ৱ")), bstack111llll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৲"), bstack111llll_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৳"))
  bstack1lll1ll11l_opy_ = {
    bstack111llll_opy_ (u"ࠧࡪࡦࠪ৴"): bstack111l1l1l_opy_,
    bstack111llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ৵"): datetime.datetime.strftime(datetime.datetime.now(), bstack111llll_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭৶")),
    bstack111llll_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৷"): str(__version__)
  }
  if os.path.exists(bstack1llll11l11_opy_):
    bstack1lll1lll1l_opy_ = json.load(open(bstack1llll11l11_opy_, bstack111llll_opy_ (u"ࠫࡷࡨࠧ৸")))
  else:
    bstack1lll1lll1l_opy_ = {}
  bstack1lll1lll1l_opy_[md5_hash] = bstack1lll1ll11l_opy_
  with open(bstack1llll11l11_opy_, bstack111llll_opy_ (u"ࠧࡽࠫࠣ৹")) as outfile:
    json.dump(bstack1lll1lll1l_opy_, outfile)
def bstack11ll1l1ll_opy_(self):
  return
def bstack1ll11lllll_opy_(self):
  return
def bstack11ll11111_opy_(self):
  global bstack1l1ll1l1_opy_
  bstack1l1ll1l1_opy_(self)
def bstack1l1ll11111_opy_():
  global bstack1ll1llll1l_opy_
  bstack1ll1llll1l_opy_ = True
def bstack1ll11l11_opy_(self):
  global bstack11lll111l_opy_
  global bstack1llll11111_opy_
  global bstack11lll11ll_opy_
  try:
    if bstack111llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৺") in bstack11lll111l_opy_ and self.session_id != None and bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৻"), bstack111llll_opy_ (u"ࠨࠩৼ")) != bstack111llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৽"):
      bstack1l11l1lll1_opy_ = bstack111llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ৾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৿")
      if bstack1l11l1lll1_opy_ == bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ਀"):
        bstack1ll1lllll1_opy_(logger)
      if self != None:
        bstack1l1l1lll_opy_(self, bstack1l11l1lll1_opy_, bstack111llll_opy_ (u"࠭ࠬࠡࠩਁ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111llll_opy_ (u"ࠧࠨਂ")
    if bstack111llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ") in bstack11lll111l_opy_ and getattr(threading.current_thread(), bstack111llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ਄"), None):
      bstack1l111ll11l_opy_.bstack1ll111ll11_opy_(self, bstack1llll1l11_opy_, logger, wait=True)
    if bstack111llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪਅ") in bstack11lll111l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l1l1lll_opy_(self, bstack111llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦਆ"))
      bstack11l11l111_opy_.bstack11111l1l1_opy_(self)
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨਇ") + str(e))
  bstack11lll11ll_opy_(self)
  self.session_id = None
def bstack111ll11l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1lll11l1_opy_
    global bstack11lll111l_opy_
    command_executor = kwargs.get(bstack111llll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩਈ"), bstack111llll_opy_ (u"ࠧࠨਉ"))
    bstack1lllll1111_opy_ = False
    if type(command_executor) == str and bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਊ") in command_executor:
      bstack1lllll1111_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ਋") in str(getattr(command_executor, bstack111llll_opy_ (u"ࠪࡣࡺࡸ࡬ࠨ਌"), bstack111llll_opy_ (u"ࠫࠬ਍"))):
      bstack1lllll1111_opy_ = True
    else:
      return bstack1l1l1l11_opy_(self, *args, **kwargs)
    if bstack1lllll1111_opy_:
      if kwargs.get(bstack111llll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭਎")):
        kwargs[bstack111llll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧਏ")] = bstack1lll11l1_opy_(kwargs[bstack111llll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨਐ")], bstack11lll111l_opy_)
      elif kwargs.get(bstack111llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ਑")):
        kwargs[bstack111llll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ਒")] = bstack1lll11l1_opy_(kwargs[bstack111llll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪਓ")], bstack11lll111l_opy_)
  except Exception as e:
    logger.error(bstack111llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦਔ").format(str(e)))
  return bstack1l1l1l11_opy_(self, *args, **kwargs)
def bstack11ll1l1l_opy_(self, command_executor=bstack111llll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨਕ"), *args, **kwargs):
  bstack11ll1ll1_opy_ = bstack111ll11l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l1lll1111_opy_.on():
    return bstack11ll1ll1_opy_
  try:
    logger.debug(bstack111llll_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪਖ").format(str(command_executor)))
    logger.debug(bstack111llll_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩਗ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਘ") in command_executor._url:
      bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਙ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ਚ") in command_executor):
    bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬਛ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l11l1lll_opy_.bstack1ll1lll111_opy_(self)
  return bstack11ll1ll1_opy_
def bstack11l1ll11_opy_(args):
  return bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ਜ") in str(args)
def bstack1ll111l1l_opy_(self, driver_command, *args, **kwargs):
  global bstack1ll1l1111l_opy_
  global bstack11ll11lll_opy_
  bstack11111lll_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪਝ"), None) and bstack1llll11l1l_opy_(
          threading.current_thread(), bstack111llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ਞ"), None)
  bstack1l111111ll_opy_ = getattr(self, bstack111llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਟ"), None) != None and getattr(self, bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩਠ"), None) == True
  if not bstack11ll11lll_opy_ and bstack111l111l1_opy_ and bstack111llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਡ") in CONFIG and CONFIG[bstack111llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫਢ")] == True and bstack1l1l111l_opy_.bstack111l111l_opy_(driver_command) and (bstack1l111111ll_opy_ or bstack11111lll_opy_) and not bstack11l1ll11_opy_(args):
    try:
      bstack11ll11lll_opy_ = True
      logger.debug(bstack111llll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧਣ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111llll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫਤ").format(str(err)))
    bstack11ll11lll_opy_ = False
  response = bstack1ll1l1111l_opy_(self, driver_command, *args, **kwargs)
  if (bstack111llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in str(bstack11lll111l_opy_).lower() or bstack111llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਦ") in str(bstack11lll111l_opy_).lower()) and bstack1l1lll1111_opy_.on():
    try:
      if driver_command == bstack111llll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ਧ"):
        bstack1l11l1lll_opy_.bstack11llllll1_opy_({
            bstack111llll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩਨ"): response[bstack111llll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ਩")],
            bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬਪ"): bstack1l11l1lll_opy_.current_test_uuid() if bstack1l11l1lll_opy_.current_test_uuid() else bstack1l1lll1111_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1ll1l1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1llll11111_opy_
  global bstack1lll1l1l_opy_
  global bstack11lll1ll1_opy_
  global bstack1lll1l1l11_opy_
  global bstack1ll11l1ll_opy_
  global bstack11lll111l_opy_
  global bstack1l1l1l11_opy_
  global bstack1l1111111l_opy_
  global bstack1lll11l11l_opy_
  global bstack1llll1l11_opy_
  CONFIG[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack11lll111l_opy_) + str(__version__)
  command_executor = bstack1llll1ll1l_opy_()
  logger.debug(bstack1l1l1ll11l_opy_.format(command_executor))
  proxy = bstack11lll1lll_opy_(CONFIG, proxy)
  bstack1lll1l1ll_opy_ = 0 if bstack1lll1l1l_opy_ < 0 else bstack1lll1l1l_opy_
  try:
    if bstack1lll1l1l11_opy_ is True:
      bstack1lll1l1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll11l1ll_opy_ is True:
      bstack1lll1l1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1lll1l1ll_opy_ = 0
  bstack1ll1ll1l_opy_ = bstack111llll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
  logger.debug(bstack1lll1111ll_opy_.format(str(bstack1ll1ll1l_opy_)))
  if bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ") in CONFIG and bstack1l11ll1lll_opy_(CONFIG[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")]):
    bstack11llllllll_opy_(bstack1ll1ll1l_opy_)
  if bstack1l1111ll_opy_.bstack1l111l11_opy_(CONFIG, bstack1lll1l1ll_opy_) and bstack1l1111ll_opy_.bstack11l111ll_opy_(bstack1ll1ll1l_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1l1111ll_opy_.set_capabilities(bstack1ll1ll1l_opy_, CONFIG)
  if desired_capabilities:
    bstack11l11llll_opy_ = bstack111l1l1ll_opy_(desired_capabilities)
    bstack11l11llll_opy_[bstack111llll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩਮ")] = bstack1ll1ll1lll_opy_(CONFIG)
    bstack11l111ll1_opy_ = bstack111llll1_opy_(bstack11l11llll_opy_)
    if bstack11l111ll1_opy_:
      bstack1ll1ll1l_opy_ = update(bstack11l111ll1_opy_, bstack1ll1ll1l_opy_)
    desired_capabilities = None
  if options:
    bstack1l11llll_opy_(options, bstack1ll1ll1l_opy_)
  if not options:
    options = bstack1ll1llll1_opy_(bstack1ll1ll1l_opy_)
  bstack1llll1l11_opy_ = CONFIG.get(bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ"))[bstack1lll1l1ll_opy_]
  if proxy and bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਰ")):
    options.proxy(proxy)
  if options and bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ਱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll111l1_opy_() < version.parse(bstack111llll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਲ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll1ll1l_opy_)
  logger.info(bstack111llll11_opy_)
  if bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਲ਼")):
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ਴")):
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩਵ")):
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1llll1llll_opy_ = bstack111llll_opy_ (u"ࠪࠫਸ਼")
    if bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ਷")):
      bstack1llll1llll_opy_ = self.caps.get(bstack111llll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਸ"))
    else:
      bstack1llll1llll_opy_ = self.capabilities.get(bstack111llll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਹ"))
    if bstack1llll1llll_opy_:
      bstack1l1l1l1ll_opy_(bstack1llll1llll_opy_)
      if bstack1lll111l1_opy_() <= version.parse(bstack111llll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ਺")):
        self.command_executor._url = bstack111llll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ਻") + bstack11l111lll_opy_ + bstack111llll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ਼")
      else:
        self.command_executor._url = bstack111llll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ਽") + bstack1llll1llll_opy_ + bstack111llll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਾ")
      logger.debug(bstack1l1l1111l1_opy_.format(bstack1llll1llll_opy_))
    else:
      logger.debug(bstack1l1l111ll_opy_.format(bstack111llll_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਿ")))
  except Exception as e:
    logger.debug(bstack1l1l111ll_opy_.format(e))
  if bstack111llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬੀ") in bstack11lll111l_opy_:
    bstack11l11lll_opy_(bstack1lll1l1l_opy_, bstack1lll11l11l_opy_)
  bstack1llll11111_opy_ = self.session_id
  if bstack111llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧੁ") in bstack11lll111l_opy_ or bstack111llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨੂ") in bstack11lll111l_opy_ or bstack111llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃") in bstack11lll111l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l11l1lll_opy_.bstack1ll1lll111_opy_(self)
  bstack1l1111111l_opy_.append(self)
  if bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄") in CONFIG and bstack111llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੅") in CONFIG[bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆")][bstack1lll1l1ll_opy_]:
    bstack11lll1ll1_opy_ = CONFIG[bstack111llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ")][bstack1lll1l1ll_opy_][bstack111llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ")]
  logger.debug(bstack1llllll1l_opy_.format(bstack1llll11111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll111ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1111l111_opy_
      if(bstack111llll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ੉") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠩࢁࠫ੊")), bstack111llll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪੋ"), bstack111llll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ੌ")), bstack111llll_opy_ (u"ࠬࡽ੍ࠧ")) as fp:
          fp.write(bstack111llll_opy_ (u"ࠨࠢ੎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111llll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ੏")))):
          with open(args[1], bstack111llll_opy_ (u"ࠨࡴࠪ੐")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111llll_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨੑ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1ll11ll1_opy_)
            lines.insert(1, bstack1l1lll1ll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111llll_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੒")), bstack111llll_opy_ (u"ࠫࡼ࠭੓")) as bstack1ll11ll111_opy_:
              bstack1ll11ll111_opy_.writelines(lines)
        CONFIG[bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੔")] = str(bstack11lll111l_opy_) + str(__version__)
        bstack1lll1l1ll_opy_ = 0 if bstack1lll1l1l_opy_ < 0 else bstack1lll1l1l_opy_
        try:
          if bstack1lll1l1l11_opy_ is True:
            bstack1lll1l1ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1ll11l1ll_opy_ is True:
            bstack1lll1l1ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1lll1l1ll_opy_ = 0
        CONFIG[bstack111llll_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ੕")] = False
        CONFIG[bstack111llll_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ੖")] = True
        bstack1ll1ll1l_opy_ = bstack111llll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
        logger.debug(bstack1lll1111ll_opy_.format(str(bstack1ll1ll1l_opy_)))
        if CONFIG.get(bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ੗")):
          bstack11llllllll_opy_(bstack1ll1ll1l_opy_)
        if bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੘") in CONFIG and bstack111llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਖ਼") in CONFIG[bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")][bstack1lll1l1ll_opy_]:
          bstack11lll1ll1_opy_ = CONFIG[bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")][bstack1lll1l1ll_opy_][bstack111llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੜ")]
        args.append(os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠧࡿࠩ੝")), bstack111llll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack111llll_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੟")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll1ll1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111llll_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੠"))
      bstack1111l111_opy_ = True
      return bstack1l11lll1l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l11l1ll11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1lll1l1l_opy_
    global bstack11lll1ll1_opy_
    global bstack1lll1l1l11_opy_
    global bstack1ll11l1ll_opy_
    global bstack11lll111l_opy_
    CONFIG[bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭੡")] = str(bstack11lll111l_opy_) + str(__version__)
    bstack1lll1l1ll_opy_ = 0 if bstack1lll1l1l_opy_ < 0 else bstack1lll1l1l_opy_
    try:
      if bstack1lll1l1l11_opy_ is True:
        bstack1lll1l1ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1ll11l1ll_opy_ is True:
        bstack1lll1l1ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1lll1l1ll_opy_ = 0
    CONFIG[bstack111llll_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ੢")] = True
    bstack1ll1ll1l_opy_ = bstack111llll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
    logger.debug(bstack1lll1111ll_opy_.format(str(bstack1ll1ll1l_opy_)))
    if CONFIG.get(bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੣")):
      bstack11llllllll_opy_(bstack1ll1ll1l_opy_)
    if bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG and bstack111llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੥") in CONFIG[bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੦")][bstack1lll1l1ll_opy_]:
      bstack11lll1ll1_opy_ = CONFIG[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧")][bstack1lll1l1ll_opy_][bstack111llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੨")]
    import urllib
    import json
    bstack1l1lll111_opy_ = bstack111llll_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ੩") + urllib.parse.quote(json.dumps(bstack1ll1ll1l_opy_))
    browser = self.connect(bstack1l1lll111_opy_)
    return browser
except Exception as e:
    pass
def bstack11l11l1ll_opy_():
    global bstack1111l111_opy_
    global bstack11lll111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1111l11_opy_
        if not bstack111l111l1_opy_:
          global bstack11l1l111_opy_
          if not bstack11l1l111_opy_:
            from bstack_utils.helper import bstack1l111lll_opy_, bstack1lllll11l_opy_
            bstack11l1l111_opy_ = bstack1l111lll_opy_()
            bstack1lllll11l_opy_(bstack11lll111l_opy_)
          BrowserType.connect = bstack1ll1111l11_opy_
          return
        BrowserType.launch = bstack1l11l1ll11_opy_
        bstack1111l111_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll111ll_opy_
      bstack1111l111_opy_ = True
    except Exception as e:
      pass
def bstack111ll111l_opy_(context, bstack1l11111ll_opy_):
  try:
    context.page.evaluate(bstack111llll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ੪"), bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ੫")+ json.dumps(bstack1l11111ll_opy_) + bstack111llll_opy_ (u"ࠣࡿࢀࠦ੬"))
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ੭"), e)
def bstack1ll1l11111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111llll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੮"), bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ੯") + json.dumps(message) + bstack111llll_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨੰ") + json.dumps(level) + bstack111llll_opy_ (u"࠭ࡽࡾࠩੱ"))
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥੲ"), e)
def bstack1l11lllll1_opy_(self, url):
  global bstack1l1lll1l1_opy_
  try:
    bstack1l1lllllll_opy_(url)
  except Exception as err:
    logger.debug(bstack1111ll1ll_opy_.format(str(err)))
  try:
    bstack1l1lll1l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1l11l_opy_ = str(e)
      if any(err_msg in bstack1ll1l11l_opy_ for err_msg in bstack1llll1l1_opy_):
        bstack1l1lllllll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1111ll1ll_opy_.format(str(err)))
    raise e
def bstack1lll1ll1_opy_(self):
  global bstack111lll11l_opy_
  bstack111lll11l_opy_ = self
  return
def bstack1lll111l1l_opy_(self):
  global bstack1111ll11_opy_
  bstack1111ll11_opy_ = self
  return
def bstack1l1llll1_opy_(test_name, bstack1ll1ll1l1l_opy_):
  global CONFIG
  if percy.bstack1llll111l_opy_() == bstack111llll_opy_ (u"ࠣࡶࡵࡹࡪࠨੳ"):
    bstack1l1l1lll1l_opy_ = os.path.relpath(bstack1ll1ll1l1l_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1l1lll1l_opy_)
    bstack1ll11l111l_opy_ = suite_name + bstack111llll_opy_ (u"ࠤ࠰ࠦੴ") + test_name
    threading.current_thread().percySessionName = bstack1ll11l111l_opy_
def bstack1llll1ll11_opy_(self, test, *args, **kwargs):
  global bstack1lll11ll1_opy_
  test_name = None
  bstack1ll1ll1l1l_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll1ll1l1l_opy_ = str(test.source)
  bstack1l1llll1_opy_(test_name, bstack1ll1ll1l1l_opy_)
  bstack1lll11ll1_opy_(self, test, *args, **kwargs)
def bstack11l1lll1_opy_(driver, bstack1ll11l111l_opy_):
  if not bstack111l1lll1_opy_ and bstack1ll11l111l_opy_:
      bstack11l11ll1l_opy_ = {
          bstack111llll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪੵ"): bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੶"),
          bstack111llll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੷"): {
              bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸"): bstack1ll11l111l_opy_
          }
      }
      bstack1ll11llll1_opy_ = bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੹").format(json.dumps(bstack11l11ll1l_opy_))
      driver.execute_script(bstack1ll11llll1_opy_)
  if bstack1ll111lll_opy_:
      bstack11ll1l11_opy_ = {
          bstack111llll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੺"): bstack111llll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ੻"),
          bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੼"): {
              bstack111llll_opy_ (u"ࠫࡩࡧࡴࡢࠩ੽"): bstack1ll11l111l_opy_ + bstack111llll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ੾"),
              bstack111llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੿"): bstack111llll_opy_ (u"ࠧࡪࡰࡩࡳࠬ઀")
          }
      }
      if bstack1ll111lll_opy_.status == bstack111llll_opy_ (u"ࠨࡒࡄࡗࡘ࠭ઁ"):
          bstack1lll11ll11_opy_ = bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧં").format(json.dumps(bstack11ll1l11_opy_))
          driver.execute_script(bstack1lll11ll11_opy_)
          bstack1l1l1lll_opy_(driver, bstack111llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪઃ"))
      elif bstack1ll111lll_opy_.status == bstack111llll_opy_ (u"ࠫࡋࡇࡉࡍࠩ઄"):
          reason = bstack111llll_opy_ (u"ࠧࠨઅ")
          bstack11ll11l11_opy_ = bstack1ll11l111l_opy_ + bstack111llll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧઆ")
          if bstack1ll111lll_opy_.message:
              reason = str(bstack1ll111lll_opy_.message)
              bstack11ll11l11_opy_ = bstack11ll11l11_opy_ + bstack111llll_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧઇ") + reason
          bstack11ll1l11_opy_[bstack111llll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫઈ")] = {
              bstack111llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨઉ"): bstack111llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩઊ"),
              bstack111llll_opy_ (u"ࠫࡩࡧࡴࡢࠩઋ"): bstack11ll11l11_opy_
          }
          bstack1lll11ll11_opy_ = bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪઌ").format(json.dumps(bstack11ll1l11_opy_))
          driver.execute_script(bstack1lll11ll11_opy_)
          bstack1l1l1lll_opy_(driver, bstack111llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ઍ"), reason)
          bstack1l11ll1l1_opy_(reason, str(bstack1ll111lll_opy_), str(bstack1lll1l1l_opy_), logger)
def bstack1lll1l11_opy_(driver, test):
  if percy.bstack1llll111l_opy_() == bstack111llll_opy_ (u"ࠢࡵࡴࡸࡩࠧ઎") and percy.bstack1111111l1_opy_() == bstack111llll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥએ"):
      bstack1lll1l1l1l_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઐ"), None)
      bstack11lllllll1_opy_(driver, bstack1lll1l1l1l_opy_, test)
  if bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧઑ"), None) and bstack1llll11l1l_opy_(
          threading.current_thread(), bstack111llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ઒"), None):
      logger.info(bstack111llll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧઓ"))
      bstack1l1111ll_opy_.bstack11l1ll1l_opy_(driver, name=test.name, path=test.source)
def bstack1llll111l1_opy_(test, bstack1ll11l111l_opy_):
    try:
      data = {}
      if test:
        data[bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫઔ")] = bstack1ll11l111l_opy_
      if bstack1ll111lll_opy_:
        if bstack1ll111lll_opy_.status == bstack111llll_opy_ (u"ࠧࡑࡃࡖࡗࠬક"):
          data[bstack111llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ")] = bstack111llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩગ")
        elif bstack1ll111lll_opy_.status == bstack111llll_opy_ (u"ࠪࡊࡆࡏࡌࠨઘ"):
          data[bstack111llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઙ")] = bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬચ")
          if bstack1ll111lll_opy_.message:
            data[bstack111llll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭છ")] = str(bstack1ll111lll_opy_.message)
      user = CONFIG[bstack111llll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩજ")]
      key = CONFIG[bstack111llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઝ")]
      url = bstack111llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧઞ").format(user, key, bstack1llll11111_opy_)
      headers = {
        bstack111llll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩટ"): bstack111llll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧઠ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1111l1ll1_opy_.format(str(e)))
def bstack1ll111l111_opy_(test, bstack1ll11l111l_opy_):
  global CONFIG
  global bstack1111ll11_opy_
  global bstack111lll11l_opy_
  global bstack1llll11111_opy_
  global bstack1ll111lll_opy_
  global bstack11lll1ll1_opy_
  global bstack11lll1l11_opy_
  global bstack1l11l11ll1_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack111ll11l1_opy_
  global bstack1l1111111l_opy_
  global bstack1llll1l11_opy_
  try:
    if not bstack1llll11111_opy_:
      with open(os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠬࢄࠧડ")), bstack111llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઢ"), bstack111llll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩણ"))) as f:
        bstack1l1ll1l1l_opy_ = json.loads(bstack111llll_opy_ (u"ࠣࡽࠥત") + f.read().strip() + bstack111llll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫથ") + bstack111llll_opy_ (u"ࠥࢁࠧદ"))
        bstack1llll11111_opy_ = bstack1l1ll1l1l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1111111l_opy_:
    for driver in bstack1l1111111l_opy_:
      if bstack1llll11111_opy_ == driver.session_id:
        if test:
          bstack1lll1l11_opy_(driver, test)
        bstack11l1lll1_opy_(driver, bstack1ll11l111l_opy_)
  elif bstack1llll11111_opy_:
    bstack1llll111l1_opy_(test, bstack1ll11l111l_opy_)
  if bstack1111ll11_opy_:
    bstack1l11l11ll1_opy_(bstack1111ll11_opy_)
  if bstack111lll11l_opy_:
    bstack1l1l1ll1ll_opy_(bstack111lll11l_opy_)
  if bstack1ll1llll1l_opy_:
    bstack111ll11l1_opy_()
def bstack11l11lll1_opy_(self, test, *args, **kwargs):
  bstack1ll11l111l_opy_ = None
  if test:
    bstack1ll11l111l_opy_ = str(test.name)
  bstack1ll111l111_opy_(test, bstack1ll11l111l_opy_)
  bstack11lll1l11_opy_(self, test, *args, **kwargs)
def bstack11lll1ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll11ll1l_opy_
  global CONFIG
  global bstack1l1111111l_opy_
  global bstack1llll11111_opy_
  bstack1ll1ll111l_opy_ = None
  try:
    if bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪધ"), None):
      try:
        if not bstack1llll11111_opy_:
          with open(os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠬࢄࠧન")), bstack111llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭઩"), bstack111llll_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩપ"))) as f:
            bstack1l1ll1l1l_opy_ = json.loads(bstack111llll_opy_ (u"ࠣࡽࠥફ") + f.read().strip() + bstack111llll_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫબ") + bstack111llll_opy_ (u"ࠥࢁࠧભ"))
            bstack1llll11111_opy_ = bstack1l1ll1l1l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l1111111l_opy_:
        for driver in bstack1l1111111l_opy_:
          if bstack1llll11111_opy_ == driver.session_id:
            bstack1ll1ll111l_opy_ = driver
    bstack1l111ll1l_opy_ = bstack1l1111ll_opy_.bstack11111ll1_opy_(test.tags)
    if bstack1ll1ll111l_opy_:
      threading.current_thread().isA11yTest = bstack1l1111ll_opy_.bstack11llllll11_opy_(bstack1ll1ll111l_opy_, bstack1l111ll1l_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l111ll1l_opy_
  except:
    pass
  bstack1lll11ll1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll111lll_opy_
  bstack1ll111lll_opy_ = self._test
def bstack1l1111ll1l_opy_():
  global bstack1l1111l1l1_opy_
  try:
    if os.path.exists(bstack1l1111l1l1_opy_):
      os.remove(bstack1l1111l1l1_opy_)
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧમ") + str(e))
def bstack1111lllll_opy_():
  global bstack1l1111l1l1_opy_
  bstack1ll1l111l1_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1111l1l1_opy_):
      with open(bstack1l1111l1l1_opy_, bstack111llll_opy_ (u"ࠬࡽࠧય")):
        pass
      with open(bstack1l1111l1l1_opy_, bstack111llll_opy_ (u"ࠨࡷࠬࠤર")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1111l1l1_opy_):
      bstack1ll1l111l1_opy_ = json.load(open(bstack1l1111l1l1_opy_, bstack111llll_opy_ (u"ࠧࡳࡤࠪ઱")))
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪલ") + str(e))
  finally:
    return bstack1ll1l111l1_opy_
def bstack11l11lll_opy_(platform_index, item_index):
  global bstack1l1111l1l1_opy_
  try:
    bstack1ll1l111l1_opy_ = bstack1111lllll_opy_()
    bstack1ll1l111l1_opy_[item_index] = platform_index
    with open(bstack1l1111l1l1_opy_, bstack111llll_opy_ (u"ࠤࡺ࠯ࠧળ")) as outfile:
      json.dump(bstack1ll1l111l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ઴") + str(e))
def bstack1lllll1l11_opy_(bstack1lllll1ll1_opy_):
  global CONFIG
  bstack1l11lll1_opy_ = bstack111llll_opy_ (u"ࠫࠬવ")
  if not bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ") in CONFIG:
    logger.info(bstack111llll_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪષ"))
  try:
    platform = CONFIG[bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")][bstack1lllll1ll1_opy_]
    if bstack111llll_opy_ (u"ࠨࡱࡶࠫહ") in platform:
      bstack1l11lll1_opy_ += str(platform[bstack111llll_opy_ (u"ࠩࡲࡷࠬ઺")]) + bstack111llll_opy_ (u"ࠪ࠰ࠥ࠭઻")
    if bstack111llll_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴ઼ࠧ") in platform:
      bstack1l11lll1_opy_ += str(platform[bstack111llll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઽ")]) + bstack111llll_opy_ (u"࠭ࠬࠡࠩા")
    if bstack111llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫિ") in platform:
      bstack1l11lll1_opy_ += str(platform[bstack111llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬી")]) + bstack111llll_opy_ (u"ࠩ࠯ࠤࠬુ")
    if bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬૂ") in platform:
      bstack1l11lll1_opy_ += str(platform[bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ૃ")]) + bstack111llll_opy_ (u"ࠬ࠲ࠠࠨૄ")
    if bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫૅ") in platform:
      bstack1l11lll1_opy_ += str(platform[bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૆")]) + bstack111llll_opy_ (u"ࠨ࠮ࠣࠫે")
    if bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪૈ") in platform:
      bstack1l11lll1_opy_ += str(platform[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫૉ")]) + bstack111llll_opy_ (u"ࠫ࠱ࠦࠧ૊")
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬો") + str(e))
  finally:
    if bstack1l11lll1_opy_[len(bstack1l11lll1_opy_) - 2:] == bstack111llll_opy_ (u"࠭ࠬࠡࠩૌ"):
      bstack1l11lll1_opy_ = bstack1l11lll1_opy_[:-2]
    return bstack1l11lll1_opy_
def bstack1lll1llll_opy_(path, bstack1l11lll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1111ll11l_opy_ = ET.parse(path)
    bstack1111l111l_opy_ = bstack1111ll11l_opy_.getroot()
    bstack1lll1l1111_opy_ = None
    for suite in bstack1111l111l_opy_.iter(bstack111llll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ્࠭")):
      if bstack111llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ૎") in suite.attrib:
        suite.attrib[bstack111llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ૏")] += bstack111llll_opy_ (u"ࠪࠤࠬૐ") + bstack1l11lll1_opy_
        bstack1lll1l1111_opy_ = suite
    bstack1111111ll_opy_ = None
    for robot in bstack1111l111l_opy_.iter(bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑")):
      bstack1111111ll_opy_ = robot
    bstack1ll1111l1l_opy_ = len(bstack1111111ll_opy_.findall(bstack111llll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૒")))
    if bstack1ll1111l1l_opy_ == 1:
      bstack1111111ll_opy_.remove(bstack1111111ll_opy_.findall(bstack111llll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ૓"))[0])
      bstack111111l11_opy_ = ET.Element(bstack111llll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭૔"), attrib={bstack111llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭૕"): bstack111llll_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ૖"), bstack111llll_opy_ (u"ࠪ࡭ࡩ࠭૗"): bstack111llll_opy_ (u"ࠫࡸ࠶ࠧ૘")})
      bstack1111111ll_opy_.insert(1, bstack111111l11_opy_)
      bstack1l1lll1lll_opy_ = None
      for suite in bstack1111111ll_opy_.iter(bstack111llll_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૙")):
        bstack1l1lll1lll_opy_ = suite
      bstack1l1lll1lll_opy_.append(bstack1lll1l1111_opy_)
      bstack11l11ll1_opy_ = None
      for status in bstack1lll1l1111_opy_.iter(bstack111llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭૚")):
        bstack11l11ll1_opy_ = status
      bstack1l1lll1lll_opy_.append(bstack11l11ll1_opy_)
    bstack1111ll11l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬ૛") + str(e))
def bstack11ll11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1lllll11_opy_
  global CONFIG
  if bstack111llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ૜") in options:
    del options[bstack111llll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ૝")]
  bstack1l1ll11lll_opy_ = bstack1111lllll_opy_()
  for bstack11l1lll1l_opy_ in bstack1l1ll11lll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪ૞"), str(bstack11l1lll1l_opy_), bstack111llll_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨ૟"))
    bstack1lll1llll_opy_(path, bstack1lllll1l11_opy_(bstack1l1ll11lll_opy_[bstack11l1lll1l_opy_]))
  bstack1l1111ll1l_opy_()
  return bstack1l1lllll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll111lll1_opy_(self, ff_profile_dir):
  global bstack1l11l111l_opy_
  if not ff_profile_dir:
    return None
  return bstack1l11l111l_opy_(self, ff_profile_dir)
def bstack11ll11ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1lll1l_opy_
  bstack1111lll1_opy_ = []
  if bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ") in CONFIG:
    bstack1111lll1_opy_ = CONFIG[bstack111llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111llll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣૢ")],
      pabot_args[bstack111llll_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤૣ")],
      argfile,
      pabot_args.get(bstack111llll_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢ૤")),
      pabot_args[bstack111llll_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨ૥")],
      platform[0],
      bstack1l1lll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111llll_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૦")] or [(bstack111llll_opy_ (u"ࠧࠨ૧"), None)]
    for platform in enumerate(bstack1111lll1_opy_)
  ]
def bstack1lllllll1l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack111l1l11l_opy_=bstack111llll_opy_ (u"࠭ࠧ૨")):
  global bstack11l11111l_opy_
  self.platform_index = platform_index
  self.bstack11l1l11ll_opy_ = bstack111l1l11l_opy_
  bstack11l11111l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll11l111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l11l11l_opy_
  global bstack1l11ll11l1_opy_
  bstack1l1ll111_opy_ = copy.deepcopy(item)
  if not bstack111llll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૩") in item.options:
    bstack1l1ll111_opy_.options[bstack111llll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૪")] = []
  bstack11ll1111l_opy_ = bstack1l1ll111_opy_.options[bstack111llll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૫")].copy()
  for v in bstack1l1ll111_opy_.options[bstack111llll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૬")]:
    if bstack111llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ૭") in v:
      bstack11ll1111l_opy_.remove(v)
    if bstack111llll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૮") in v:
      bstack11ll1111l_opy_.remove(v)
    if bstack111llll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ૯") in v:
      bstack11ll1111l_opy_.remove(v)
  bstack11ll1111l_opy_.insert(0, bstack111llll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩ૰").format(bstack1l1ll111_opy_.platform_index))
  bstack11ll1111l_opy_.insert(0, bstack111llll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨ૱").format(bstack1l1ll111_opy_.bstack11l1l11ll_opy_))
  bstack1l1ll111_opy_.options[bstack111llll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૲")] = bstack11ll1111l_opy_
  if bstack1l11ll11l1_opy_:
    bstack1l1ll111_opy_.options[bstack111llll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૳")].insert(0, bstack111llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧ૴").format(bstack1l11ll11l1_opy_))
  return bstack1l1l11l11l_opy_(caller_id, datasources, is_last, bstack1l1ll111_opy_, outs_dir)
def bstack111lll1l_opy_(command, item_index):
  if bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૵")):
    os.environ[bstack111llll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ૶")] = json.dumps(CONFIG[bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૷")][item_index % bstack11l111111_opy_])
  global bstack1l11ll11l1_opy_
  if bstack1l11ll11l1_opy_:
    command[0] = command[0].replace(bstack111llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૸"), bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ૹ") + str(
      item_index) + bstack111llll_opy_ (u"ࠪࠤࠬૺ") + bstack1l11ll11l1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪૻ"),
                                    bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩૼ") + str(item_index), 1)
def bstack1ll1ll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l11llll11_opy_
  bstack111lll1l_opy_(command, item_index)
  return bstack1l11llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll11111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l11llll11_opy_
  bstack111lll1l_opy_(command, item_index)
  return bstack1l11llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llllll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l11llll11_opy_
  bstack111lll1l_opy_(command, item_index)
  return bstack1l11llll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack111ll1ll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1lll1_opy_
  bstack1lll1ll1ll_opy_ = bstack1ll1lll1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111llll_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭૽")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111llll_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ૾")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1ll1ll_opy_
def bstack1ll111111_opy_(runner, hook_name, context, element, bstack111l1llll_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l1ll1ll11_opy_.bstack1l11111l_opy_(hook_name, element)
    bstack111l1llll_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l1ll1ll11_opy_.bstack1l1l11llll_opy_(element)
      if hook_name not in [bstack111llll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ૿"), bstack111llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ଀")] and args and hasattr(args[0], bstack111llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪଁ")):
        args[0].error_message = bstack111llll_opy_ (u"ࠫࠬଂ")
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧଃ").format(str(e)))
def bstack1111l11l1_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    if runner.hooks.get(bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ଄")).__name__ != bstack111llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣࡩ࡫ࡦࡢࡷ࡯ࡸࡤ࡮࡯ࡰ࡭ࠥଅ"):
      bstack1ll111111_opy_(runner, name, context, runner, bstack111l1llll_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l111111l_opy_(bstack111llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧଆ")) else context.browser
      runner.driver_initialised = bstack111llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨଇ")
    except Exception as e:
      logger.debug(bstack111llll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧ࠽ࠤࢀࢃࠧଈ").format(str(e)))
def bstack1llllll111_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    bstack1ll111111_opy_(runner, name, context, context.feature, bstack111l1llll_opy_, *args)
    try:
      if not bstack111l1lll1_opy_:
        bstack1ll1ll111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111111l_opy_(bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଉ")) else context.browser
        if is_driver_active(bstack1ll1ll111l_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111llll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨଊ")
          bstack1l11111ll_opy_ = str(runner.feature.name)
          bstack111ll111l_opy_(context, bstack1l11111ll_opy_)
          bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଋ") + json.dumps(bstack1l11111ll_opy_) + bstack111llll_opy_ (u"ࠧࡾࡿࠪଌ"))
    except Exception as e:
      logger.debug(bstack111llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ଍").format(str(e)))
def bstack1ll1111l_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    if hasattr(context, bstack111llll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ଎")):
        bstack1l1ll1ll11_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack111llll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬଏ")) else context.feature
    bstack1ll111111_opy_(runner, name, context, target, bstack111l1llll_opy_, *args)
def bstack1l1l1lllll_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l1ll1ll11_opy_.start_test(context)
    bstack1ll111111_opy_(runner, name, context, context.scenario, bstack111l1llll_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack11l11l111_opy_.bstack1ll1lll1l_opy_(context, *args)
    try:
      bstack1ll1ll111l_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଐ"), context.browser)
      if is_driver_active(bstack1ll1ll111l_opy_):
        bstack1l11l1lll_opy_.bstack1ll1lll111_opy_(bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ଑"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ଒")
        if (not bstack111l1lll1_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l11111ll_opy_ = str(runner.feature.name)
          bstack1l11111ll_opy_ = feature_name + bstack111llll_opy_ (u"ࠧࠡ࠯ࠣࠫଓ") + scenario_name
          if runner.driver_initialised == bstack111llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥଔ"):
            bstack111ll111l_opy_(context, bstack1l11111ll_opy_)
            bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧକ") + json.dumps(bstack1l11111ll_opy_) + bstack111llll_opy_ (u"ࠪࢁࢂ࠭ଖ"))
    except Exception as e:
      logger.debug(bstack111llll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬଗ").format(str(e)))
def bstack1l1l11ll1_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    bstack1ll111111_opy_(runner, name, context, args[0], bstack111l1llll_opy_, *args)
    try:
      bstack1ll1ll111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111111l_opy_(bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଘ")) else context.browser
      if is_driver_active(bstack1ll1ll111l_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦଙ")
        bstack1l1ll1ll11_opy_.bstack1lll1llll1_opy_(args[0])
        if runner.driver_initialised == bstack111llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧଚ"):
          feature_name = bstack1l11111ll_opy_ = str(runner.feature.name)
          bstack1l11111ll_opy_ = feature_name + bstack111llll_opy_ (u"ࠨࠢ࠰ࠤࠬଛ") + context.scenario.name
          bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧଜ") + json.dumps(bstack1l11111ll_opy_) + bstack111llll_opy_ (u"ࠪࢁࢂ࠭ଝ"))
    except Exception as e:
      logger.debug(bstack111llll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨଞ").format(str(e)))
def bstack1l1lllll_opy_(runner, name, context, bstack111l1llll_opy_, *args):
  bstack1l1ll1ll11_opy_.bstack1l11l1111_opy_(args[0])
  try:
    bstack1l1l1l1111_opy_ = args[0].status.name
    bstack1ll1ll111l_opy_ = threading.current_thread().bstackSessionDriver if bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଟ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1ll1ll111l_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111llll_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ଠ")
        feature_name = bstack1l11111ll_opy_ = str(runner.feature.name)
        bstack1l11111ll_opy_ = feature_name + bstack111llll_opy_ (u"ࠧࠡ࠯ࠣࠫଡ") + context.scenario.name
        bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ଢ") + json.dumps(bstack1l11111ll_opy_) + bstack111llll_opy_ (u"ࠩࢀࢁࠬଣ"))
    if str(bstack1l1l1l1111_opy_).lower() == bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪତ"):
      bstack11lll11l1_opy_ = bstack111llll_opy_ (u"ࠫࠬଥ")
      bstack111l1111l_opy_ = bstack111llll_opy_ (u"ࠬ࠭ଦ")
      bstack1l1111llll_opy_ = bstack111llll_opy_ (u"࠭ࠧଧ")
      try:
        import traceback
        bstack11lll11l1_opy_ = runner.exception.__class__.__name__
        bstack11ll111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111l1111l_opy_ = bstack111llll_opy_ (u"ࠧࠡࠩନ").join(bstack11ll111l_opy_)
        bstack1l1111llll_opy_ = bstack11ll111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l111111_opy_.format(str(e)))
      bstack11lll11l1_opy_ += bstack1l1111llll_opy_
      bstack1ll1l11111_opy_(context, json.dumps(str(args[0].name) + bstack111llll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ଩") + str(bstack111l1111l_opy_)),
                          bstack111llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣପ"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣଫ"):
        bstack1l1l11ll_opy_(getattr(context, bstack111llll_opy_ (u"ࠫࡵࡧࡧࡦࠩବ"), None), bstack111llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧଭ"), bstack11lll11l1_opy_)
        bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫମ") + json.dumps(str(args[0].name) + bstack111llll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨଯ") + str(bstack111l1111l_opy_)) + bstack111llll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨର"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢ଱"):
        bstack1l1l1lll_opy_(bstack1ll1ll111l_opy_, bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪଲ"), bstack111llll_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣଳ") + str(bstack11lll11l1_opy_))
    else:
      bstack1ll1l11111_opy_(context, bstack111llll_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ଴"), bstack111llll_opy_ (u"ࠨࡩ࡯ࡨࡲࠦଵ"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧଶ"):
        bstack1l1l11ll_opy_(getattr(context, bstack111llll_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ଷ"), None), bstack111llll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤସ"))
      bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨହ") + json.dumps(str(args[0].name) + bstack111llll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣ଺")) + bstack111llll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ଻"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ଼ࠦ"):
        bstack1l1l1lll_opy_(bstack1ll1ll111l_opy_, bstack111llll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଽ"))
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥࡹࡴࡦࡲ࠽ࠤࢀࢃࠧା").format(str(e)))
  bstack1ll111111_opy_(runner, name, context, args[0], bstack111l1llll_opy_, *args)
def bstack1l1ll1l11l_opy_(runner, name, context, bstack111l1llll_opy_, *args):
  bstack1l1ll1ll11_opy_.end_test(args[0])
  try:
    bstack11l11ll11_opy_ = args[0].status.name
    bstack1ll1ll111l_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨି"), context.browser)
    bstack11l11l111_opy_.bstack11111l1l1_opy_(bstack1ll1ll111l_opy_)
    if str(bstack11l11ll11_opy_).lower() == bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪୀ"):
      bstack11lll11l1_opy_ = bstack111llll_opy_ (u"ࠫࠬୁ")
      bstack111l1111l_opy_ = bstack111llll_opy_ (u"ࠬ࠭ୂ")
      bstack1l1111llll_opy_ = bstack111llll_opy_ (u"࠭ࠧୃ")
      try:
        import traceback
        bstack11lll11l1_opy_ = runner.exception.__class__.__name__
        bstack11ll111l_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111l1111l_opy_ = bstack111llll_opy_ (u"ࠧࠡࠩୄ").join(bstack11ll111l_opy_)
        bstack1l1111llll_opy_ = bstack11ll111l_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l111111_opy_.format(str(e)))
      bstack11lll11l1_opy_ += bstack1l1111llll_opy_
      bstack1ll1l11111_opy_(context, json.dumps(str(args[0].name) + bstack111llll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ୅") + str(bstack111l1111l_opy_)),
                          bstack111llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ୆"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧେ") or runner.driver_initialised == bstack111llll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫୈ"):
        bstack1l1l11ll_opy_(getattr(context, bstack111llll_opy_ (u"ࠬࡶࡡࡨࡧࠪ୉"), None), bstack111llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ୊"), bstack11lll11l1_opy_)
        bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬୋ") + json.dumps(str(args[0].name) + bstack111llll_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢୌ") + str(bstack111l1111l_opy_)) + bstack111llll_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾ୍ࠩ"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ୎") or runner.driver_initialised == bstack111llll_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ୏"):
        bstack1l1l1lll_opy_(bstack1ll1ll111l_opy_, bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ୐"), bstack111llll_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ୑") + str(bstack11lll11l1_opy_))
    else:
      bstack1ll1l11111_opy_(context, bstack111llll_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣ୒"), bstack111llll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ୓"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ୔") or runner.driver_initialised == bstack111llll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪ୕"):
        bstack1l1l11ll_opy_(getattr(context, bstack111llll_opy_ (u"ࠫࡵࡧࡧࡦࠩୖ"), None), bstack111llll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧୗ"))
      bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ୘") + json.dumps(str(args[0].name) + bstack111llll_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦ୙")) + bstack111llll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ୚"))
      if runner.driver_initialised == bstack111llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ୛") or runner.driver_initialised == bstack111llll_opy_ (u"ࠪ࡭ࡳࡹࡴࡦࡲࠪଡ଼"):
        bstack1l1l1lll_opy_(bstack1ll1ll111l_opy_, bstack111llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦଢ଼"))
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ୞").format(str(e)))
  bstack1ll111111_opy_(runner, name, context, context.scenario, bstack111l1llll_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1lll11lll1_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    target = context.scenario if hasattr(context, bstack111llll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨୟ")) else context.feature
    bstack1ll111111_opy_(runner, name, context, target, bstack111l1llll_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1lllll111_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    try:
      bstack1ll1ll111l_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ୠ"), context.browser)
      if context.failed is True:
        bstack1l1ll1ll_opy_ = []
        bstack1111l1l11_opy_ = []
        bstack11ll1lll_opy_ = []
        bstack1ll111l11_opy_ = bstack111llll_opy_ (u"ࠨࠩୡ")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1ll1ll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11ll111l_opy_ = traceback.format_tb(exc_tb)
            bstack1ll1l11l1l_opy_ = bstack111llll_opy_ (u"ࠩࠣࠫୢ").join(bstack11ll111l_opy_)
            bstack1111l1l11_opy_.append(bstack1ll1l11l1l_opy_)
            bstack11ll1lll_opy_.append(bstack11ll111l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l111111_opy_.format(str(e)))
        bstack11lll11l1_opy_ = bstack111llll_opy_ (u"ࠪࠫୣ")
        for i in range(len(bstack1l1ll1ll_opy_)):
          bstack11lll11l1_opy_ += bstack1l1ll1ll_opy_[i] + bstack11ll1lll_opy_[i] + bstack111llll_opy_ (u"ࠫࡡࡴࠧ୤")
        bstack1ll111l11_opy_ = bstack111llll_opy_ (u"ࠬࠦࠧ୥").join(bstack1111l1l11_opy_)
        if runner.driver_initialised in [bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ୦"), bstack111llll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ୧")]:
          bstack1ll1l11111_opy_(context, bstack1ll111l11_opy_, bstack111llll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ୨"))
          bstack1l1l11ll_opy_(getattr(context, bstack111llll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ୩"), None), bstack111llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ୪"), bstack11lll11l1_opy_)
          bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ୫") + json.dumps(bstack1ll111l11_opy_) + bstack111llll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ୬"))
          bstack1l1l1lll_opy_(bstack1ll1ll111l_opy_, bstack111llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ୭"), bstack111llll_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧ୮") + str(bstack11lll11l1_opy_))
          bstack1ll1ll11l_opy_ = bstack1l111llll_opy_(bstack1ll111l11_opy_, runner.feature.name, logger)
          if (bstack1ll1ll11l_opy_ != None):
            bstack1l11l11l_opy_.append(bstack1ll1ll11l_opy_)
      else:
        if runner.driver_initialised in [bstack111llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ୯"), bstack111llll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ୰")]:
          bstack1ll1l11111_opy_(context, bstack111llll_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨୱ") + str(runner.feature.name) + bstack111llll_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ୲"), bstack111llll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ୳"))
          bstack1l1l11ll_opy_(getattr(context, bstack111llll_opy_ (u"࠭ࡰࡢࡩࡨࠫ୴"), None), bstack111llll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ୵"))
          bstack1ll1ll111l_opy_.execute_script(bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭୶") + json.dumps(bstack111llll_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ୷") + str(runner.feature.name) + bstack111llll_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧ୸")) + bstack111llll_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪ୹"))
          bstack1l1l1lll_opy_(bstack1ll1ll111l_opy_, bstack111llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ୺"))
          bstack1ll1ll11l_opy_ = bstack1l111llll_opy_(bstack1ll111l11_opy_, runner.feature.name, logger)
          if (bstack1ll1ll11l_opy_ != None):
            bstack1l11l11l_opy_.append(bstack1ll1ll11l_opy_)
    except Exception as e:
      logger.debug(bstack111llll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ୻").format(str(e)))
    bstack1ll111111_opy_(runner, name, context, context.feature, bstack111l1llll_opy_, *args)
def bstack1l1111l111_opy_(runner, name, context, bstack111l1llll_opy_, *args):
    bstack1ll111111_opy_(runner, name, context, runner, bstack111l1llll_opy_, *args)
def bstack1ll1ll1ll_opy_(self, name, context, *args):
  if bstack111l111l1_opy_:
    platform_index = int(threading.current_thread()._name) % bstack11l111111_opy_
    bstack1lll11llll_opy_ = CONFIG[bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ୼")][platform_index]
    os.environ[bstack111llll_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ୽")] = json.dumps(bstack1lll11llll_opy_)
  global bstack111l1llll_opy_
  if not hasattr(self, bstack111llll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࡪࠧ୾")):
    self.driver_initialised = None
  bstack1l1111l1_opy_ = {
      bstack111llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧ୿"): bstack1111l11l1_opy_,
      bstack111llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ஀"): bstack1llllll111_opy_,
      bstack111llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡺࡡࡨࠩ஁"): bstack1ll1111l_opy_,
      bstack111llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨஂ"): bstack1l1l1lllll_opy_,
      bstack111llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠬஃ"): bstack1l1l11ll1_opy_,
      bstack111llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡶࡨࡴࠬ஄"): bstack1l1lllll_opy_,
      bstack111llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪஅ"): bstack1l1ll1l11l_opy_,
      bstack111llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡷࡥ࡬࠭ஆ"): bstack1lll11lll1_opy_,
      bstack111llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫஇ"): bstack1lllll111_opy_,
      bstack111llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨஈ"): bstack1l1111l111_opy_
  }
  handler = bstack1l1111l1_opy_.get(name, bstack111l1llll_opy_)
  handler(self, name, context, bstack111l1llll_opy_, *args)
  if name in [bstack111llll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭உ"), bstack111llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨஊ"), bstack111llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫ஋")]:
    try:
      bstack1ll1ll111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111111l_opy_(bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ஌")) else context.browser
      bstack11llll11l_opy_ = (
        (name == bstack111llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭஍") and self.driver_initialised == bstack111llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣஎ")) or
        (name == bstack111llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬஏ") and self.driver_initialised == bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢஐ")) or
        (name == bstack111llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ஑") and self.driver_initialised in [bstack111llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥஒ"), bstack111llll_opy_ (u"ࠤ࡬ࡲࡸࡺࡥࡱࠤஓ")]) or
        (name == bstack111llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧஔ") and self.driver_initialised == bstack111llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤக"))
      )
      if bstack11llll11l_opy_:
        self.driver_initialised = None
        bstack1ll1ll111l_opy_.quit()
    except Exception:
      pass
def bstack1111l11ll_opy_(config, startdir):
  return bstack111llll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥ஖").format(bstack111llll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ஗"))
notset = Notset()
def bstack1llll1ll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l11l1ll1_opy_
  if str(name).lower() == bstack111llll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ஘"):
    return bstack111llll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢங")
  else:
    return bstack1l11l1ll1_opy_(self, name, default, skip)
def bstack1l111l11l_opy_(item, when):
  global bstack1ll1ll11l1_opy_
  try:
    bstack1ll1ll11l1_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll11111l1_opy_():
  return
def bstack111l1ll1l_opy_(type, name, status, reason, bstack11l11l1l1_opy_, bstack1lll1l11ll_opy_):
  bstack11l11ll1l_opy_ = {
    bstack111llll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩச"): type,
    bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஛"): {}
  }
  if type == bstack111llll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ஜ"):
    bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ஝")][bstack111llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬஞ")] = bstack11l11l1l1_opy_
    bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪட")][bstack111llll_opy_ (u"ࠨࡦࡤࡸࡦ࠭஠")] = json.dumps(str(bstack1lll1l11ll_opy_))
  if type == bstack111llll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ஡"):
    bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஢")][bstack111llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩண")] = name
  if type == bstack111llll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨத"):
    bstack11l11ll1l_opy_[bstack111llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ஥")][bstack111llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ஦")] = status
    if status == bstack111llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ஧"):
      bstack11l11ll1l_opy_[bstack111llll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬந")][bstack111llll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪன")] = json.dumps(str(reason))
  bstack1ll11llll1_opy_ = bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩப").format(json.dumps(bstack11l11ll1l_opy_))
  return bstack1ll11llll1_opy_
def bstack1l11lll1l_opy_(driver_command, response):
    if driver_command == bstack111llll_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ஫"):
        bstack1l11l1lll_opy_.bstack11llllll1_opy_({
            bstack111llll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ஬"): response[bstack111llll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭஭")],
            bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨம"): bstack1l11l1lll_opy_.current_test_uuid()
        })
def bstack1lll1lll_opy_(item, call, rep):
  global bstack1l11l1l11_opy_
  global bstack1l1111111l_opy_
  global bstack111l1lll1_opy_
  name = bstack111llll_opy_ (u"ࠩࠪய")
  try:
    if rep.when == bstack111llll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨர"):
      bstack1llll11111_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack111l1lll1_opy_:
          name = str(rep.nodeid)
          bstack111ll1ll_opy_ = bstack111l1ll1l_opy_(bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬற"), name, bstack111llll_opy_ (u"ࠬ࠭ல"), bstack111llll_opy_ (u"࠭ࠧள"), bstack111llll_opy_ (u"ࠧࠨழ"), bstack111llll_opy_ (u"ࠨࠩவ"))
          threading.current_thread().bstack1ll1l1l1_opy_ = name
          for driver in bstack1l1111111l_opy_:
            if bstack1llll11111_opy_ == driver.session_id:
              driver.execute_script(bstack111ll1ll_opy_)
      except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩஶ").format(str(e)))
      try:
        bstack1llllllll1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫஷ"):
          status = bstack111llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫஸ") if rep.outcome.lower() == bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬஹ") else bstack111llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭஺")
          reason = bstack111llll_opy_ (u"ࠧࠨ஻")
          if status == bstack111llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ஼"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111llll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ஽") if status == bstack111llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪா") else bstack111llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪி")
          data = name + bstack111llll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧீ") if status == bstack111llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ு") else name + bstack111llll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪூ") + reason
          bstack1l1l1l1l1l_opy_ = bstack111l1ll1l_opy_(bstack111llll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ௃"), bstack111llll_opy_ (u"ࠩࠪ௄"), bstack111llll_opy_ (u"ࠪࠫ௅"), bstack111llll_opy_ (u"ࠫࠬெ"), level, data)
          for driver in bstack1l1111111l_opy_:
            if bstack1llll11111_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l1l1l1l_opy_)
      except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩே").format(str(e)))
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪை").format(str(e)))
  bstack1l11l1l11_opy_(item, call, rep)
def bstack11lllllll1_opy_(driver, bstack1l1ll111ll_opy_, test=None):
  global bstack1lll1l1l_opy_
  if test != None:
    bstack1l1l11l1_opy_ = getattr(test, bstack111llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ௉"), None)
    bstack111lll11_opy_ = getattr(test, bstack111llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ொ"), None)
    PercySDK.screenshot(driver, bstack1l1ll111ll_opy_, bstack1l1l11l1_opy_=bstack1l1l11l1_opy_, bstack111lll11_opy_=bstack111lll11_opy_, bstack1ll1ll11_opy_=bstack1lll1l1l_opy_)
  else:
    PercySDK.screenshot(driver, bstack1l1ll111ll_opy_)
def bstack11l111l1_opy_(driver):
  if bstack111l1ll1_opy_.bstack11l11111_opy_() is True or bstack111l1ll1_opy_.capturing() is True:
    return
  bstack111l1ll1_opy_.bstack1l1ll1ll1l_opy_()
  while not bstack111l1ll1_opy_.bstack11l11111_opy_():
    bstack1lllll111l_opy_ = bstack111l1ll1_opy_.bstack1lll111111_opy_()
    bstack11lllllll1_opy_(driver, bstack1lllll111l_opy_)
  bstack111l1ll1_opy_.bstack1l11ll1l_opy_()
def bstack111l11111_opy_(sequence, driver_command, response = None, bstack1l111l1lll_opy_ = None, args = None):
    try:
      if sequence != bstack111llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩோ"):
        return
      if percy.bstack1llll111l_opy_() == bstack111llll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤௌ"):
        return
      bstack1lllll111l_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫்ࠧ"), None)
      for command in bstack1lll1ll1l1_opy_:
        if command == driver_command:
          for driver in bstack1l1111111l_opy_:
            bstack11l111l1_opy_(driver)
      bstack11lllll1_opy_ = percy.bstack1111111l1_opy_()
      if driver_command in bstack111111l1_opy_[bstack11lllll1_opy_]:
        bstack111l1ll1_opy_.bstack1l11ll11_opy_(bstack1lllll111l_opy_, driver_command)
    except Exception as e:
      pass
def bstack1111ll111_opy_(framework_name):
  if bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ௎")):
      return
  bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ௏"), True)
  global bstack11lll111l_opy_
  global bstack1111l111_opy_
  global bstack1ll11ll11l_opy_
  bstack11lll111l_opy_ = framework_name
  logger.info(bstack1l11ll11ll_opy_.format(bstack11lll111l_opy_.split(bstack111llll_opy_ (u"ࠧ࠮ࠩௐ"))[0]))
  bstack1lll1111l1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack111l111l1_opy_:
      Service.start = bstack11ll1l1ll_opy_
      Service.stop = bstack1ll11lllll_opy_
      webdriver.Remote.get = bstack1l11lllll1_opy_
      WebDriver.close = bstack11ll11111_opy_
      WebDriver.quit = bstack1ll11l11_opy_
      webdriver.Remote.__init__ = bstack1ll1l1ll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack111l111l1_opy_:
        webdriver.Remote.__init__ = bstack11ll1l1l_opy_
    WebDriver.execute = bstack1ll111l1l_opy_
    bstack1111l111_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack111l111l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1ll11111_opy_
  except Exception as e:
    pass
  bstack11l11l1ll_opy_()
  if not bstack1111l111_opy_:
    bstack11l1l1l1_opy_(bstack111llll_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ௑"), bstack1lll11l1l_opy_)
  if bstack1l11ll1l11_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1ll11l1l_opy_
    except Exception as e:
      logger.error(bstack11l1111l1_opy_.format(str(e)))
  if bstack1ll11lll1_opy_():
    bstack1llll1lll1_opy_(CONFIG, logger)
  if (bstack111llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௒") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1llll111l_opy_() == bstack111llll_opy_ (u"ࠥࡸࡷࡻࡥࠣ௓"):
          bstack1lll1l1ll1_opy_(bstack111l11111_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll111lll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lll111l1l_opy_
      except Exception as e:
        logger.warn(bstack1llllll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lll1ll1_opy_
      except Exception as e:
        logger.debug(bstack1l1111lll_opy_ + str(e))
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1llllll1ll_opy_)
    Output.start_test = bstack1llll1ll11_opy_
    Output.end_test = bstack11l11lll1_opy_
    TestStatus.__init__ = bstack11lll1ll_opy_
    QueueItem.__init__ = bstack1lllllll1l_opy_
    pabot._create_items = bstack11ll11ll_opy_
    try:
      from pabot import __version__ as bstack11111l11_opy_
      if version.parse(bstack11111l11_opy_) >= version.parse(bstack111llll_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫ௔")):
        pabot._run = bstack1llllll1l1_opy_
      elif version.parse(bstack11111l11_opy_) >= version.parse(bstack111llll_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ௕")):
        pabot._run = bstack1ll11111l_opy_
      else:
        pabot._run = bstack1ll1ll1ll1_opy_
    except Exception as e:
      pabot._run = bstack1ll1ll1ll1_opy_
    pabot._create_command_for_execution = bstack1lll11l111_opy_
    pabot._report_results = bstack11ll11l1_opy_
  if bstack111llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௖") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1l111l111_opy_)
    Runner.run_hook = bstack1ll1ll1ll_opy_
    Step.run = bstack111ll1ll1_opy_
  if bstack111llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧௗ") in str(framework_name).lower():
    if not bstack111l111l1_opy_:
      return
    try:
      if percy.bstack1llll111l_opy_() == bstack111llll_opy_ (u"ࠣࡶࡵࡹࡪࠨ௘"):
          bstack1lll1l1ll1_opy_(bstack111l11111_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1111l11ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll11111l1_opy_
      Config.getoption = bstack1llll1ll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1lll1lll_opy_
    except Exception as e:
      pass
def bstack1lllll1lll_opy_():
  global CONFIG
  if bstack111llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ௙") in CONFIG and int(CONFIG[bstack111llll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ௚")]) > 1:
    logger.warn(bstack111111111_opy_)
def bstack1l111l1l1_opy_(arg, bstack1111llll1_opy_, bstack1l1l1ll1l1_opy_=None):
  global CONFIG
  global bstack11l111lll_opy_
  global bstack11l1l1l1l_opy_
  global bstack111l111l1_opy_
  global bstack1l111l11ll_opy_
  bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௛")
  if bstack1111llll1_opy_ and isinstance(bstack1111llll1_opy_, str):
    bstack1111llll1_opy_ = eval(bstack1111llll1_opy_)
  CONFIG = bstack1111llll1_opy_[bstack111llll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ௜")]
  bstack11l111lll_opy_ = bstack1111llll1_opy_[bstack111llll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ௝")]
  bstack11l1l1l1l_opy_ = bstack1111llll1_opy_[bstack111llll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௞")]
  bstack111l111l1_opy_ = bstack1111llll1_opy_[bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ௟")]
  bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ௠"), bstack111l111l1_opy_)
  os.environ[bstack111llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ௡")] = bstack1l1l11111l_opy_
  os.environ[bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ௢")] = json.dumps(CONFIG)
  os.environ[bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ௣")] = bstack11l111lll_opy_
  os.environ[bstack111llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ௤")] = str(bstack11l1l1l1l_opy_)
  os.environ[bstack111llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭௥")] = str(True)
  if bstack111l11ll1_opy_(arg, [bstack111llll_opy_ (u"ࠨ࠯ࡱࠫ௦"), bstack111llll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ௧")]) != -1:
    os.environ[bstack111llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ௨")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1llllll_opy_)
    return
  bstack1lll1ll1l_opy_()
  global bstack11ll1ll1l_opy_
  global bstack1lll1l1l_opy_
  global bstack1l1lll1l_opy_
  global bstack1l11ll11l1_opy_
  global bstack1llll1111l_opy_
  global bstack1ll11ll11l_opy_
  global bstack1lll1l1l11_opy_
  arg.append(bstack111llll_opy_ (u"ࠦ࠲࡝ࠢ௩"))
  arg.append(bstack111llll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣ௪"))
  arg.append(bstack111llll_opy_ (u"ࠨ࠭ࡘࠤ௫"))
  arg.append(bstack111llll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ௬"))
  global bstack1l1l1l11_opy_
  global bstack11lll11ll_opy_
  global bstack1ll1l1111l_opy_
  global bstack1lll11ll1l_opy_
  global bstack1l11l111l_opy_
  global bstack11l11111l_opy_
  global bstack1l1l11l11l_opy_
  global bstack1l1ll1l1_opy_
  global bstack1l1lll1l1_opy_
  global bstack1l1lll11l1_opy_
  global bstack1l11l1ll1_opy_
  global bstack1ll1ll11l1_opy_
  global bstack1l11l1l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l1l11_opy_ = webdriver.Remote.__init__
    bstack11lll11ll_opy_ = WebDriver.quit
    bstack1l1ll1l1_opy_ = WebDriver.close
    bstack1l1lll1l1_opy_ = WebDriver.get
    bstack1ll1l1111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll111l1l1_opy_(CONFIG) and bstack1ll1ll1l11_opy_():
    if bstack1lll111l1_opy_() < version.parse(bstack1l1l1l11l_opy_):
      logger.error(bstack1lll11l1ll_opy_.format(bstack1lll111l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1lll11l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l1111l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l11l1ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack1ll1ll11l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l11llllll_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l11l1l11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111llll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ௭"))
  bstack1l1lll1l_opy_ = CONFIG.get(bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭௮"), {}).get(bstack111llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ௯"))
  bstack1lll1l1l11_opy_ = True
  bstack1111ll111_opy_(bstack111l11l1_opy_)
  os.environ[bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ௰")] = CONFIG[bstack111llll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ௱")]
  os.environ[bstack111llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ௲")] = CONFIG[bstack111llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ௳")]
  os.environ[bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ௴")] = bstack111l111l1_opy_.__str__()
  from _pytest.config import main as bstack1lllll11_opy_
  bstack1111l11l_opy_ = []
  try:
    bstack1ll1l1ll1_opy_ = bstack1lllll11_opy_(arg)
    if bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠭௵") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111lll11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1111l11l_opy_.append(bstack1l111lll11_opy_)
    try:
      bstack1l11l11l1_opy_ = (bstack1111l11l_opy_, int(bstack1ll1l1ll1_opy_))
      bstack1l1l1ll1l1_opy_.append(bstack1l11l11l1_opy_)
    except:
      bstack1l1l1ll1l1_opy_.append((bstack1111l11l_opy_, bstack1ll1l1ll1_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1111l11l_opy_.append({bstack111llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ௶"): bstack111llll_opy_ (u"ࠫࡕࡸ࡯ࡤࡧࡶࡷࠥ࠭௷") + os.environ.get(bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ௸")), bstack111llll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ௹"): traceback.format_exc(), bstack111llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭௺"): int(os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ௻")))})
    bstack1l1l1ll1l1_opy_.append((bstack1111l11l_opy_, 1))
def bstack11ll11ll1_opy_(arg):
  global bstack1ll11llll_opy_
  bstack1111ll111_opy_(bstack111111ll1_opy_)
  os.environ[bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ௼")] = str(bstack11l1l1l1l_opy_)
  from behave.__main__ import main as bstack11lllllll_opy_
  status_code = bstack11lllllll_opy_(arg)
  if status_code != 0:
    bstack1ll11llll_opy_ = status_code
def bstack1lll1l111_opy_():
  logger.info(bstack1ll11ll1ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ௽"), help=bstack111llll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬ௾"))
  parser.add_argument(bstack111llll_opy_ (u"ࠬ࠳ࡵࠨ௿"), bstack111llll_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪఀ"), help=bstack111llll_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ఁ"))
  parser.add_argument(bstack111llll_opy_ (u"ࠨ࠯࡮ࠫం"), bstack111llll_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨః"), help=bstack111llll_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫఄ"))
  parser.add_argument(bstack111llll_opy_ (u"ࠫ࠲࡬ࠧఅ"), bstack111llll_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఆ"), help=bstack111llll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬఇ"))
  bstack111l1ll11_opy_ = parser.parse_args()
  try:
    bstack1l111lllll_opy_ = bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫఈ")
    if bstack111l1ll11_opy_.framework and bstack111l1ll11_opy_.framework not in (bstack111llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨఉ"), bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪఊ")):
      bstack1l111lllll_opy_ = bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩఋ")
    bstack1ll111l11l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l111lllll_opy_)
    bstack1111lll1l_opy_ = open(bstack1ll111l11l_opy_, bstack111llll_opy_ (u"ࠫࡷ࠭ఌ"))
    bstack111l11ll_opy_ = bstack1111lll1l_opy_.read()
    bstack1111lll1l_opy_.close()
    if bstack111l1ll11_opy_.username:
      bstack111l11ll_opy_ = bstack111l11ll_opy_.replace(bstack111llll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ఍"), bstack111l1ll11_opy_.username)
    if bstack111l1ll11_opy_.key:
      bstack111l11ll_opy_ = bstack111l11ll_opy_.replace(bstack111llll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨఎ"), bstack111l1ll11_opy_.key)
    if bstack111l1ll11_opy_.framework:
      bstack111l11ll_opy_ = bstack111l11ll_opy_.replace(bstack111llll_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨఏ"), bstack111l1ll11_opy_.framework)
    file_name = bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫఐ")
    file_path = os.path.abspath(file_name)
    bstack1l11l11ll_opy_ = open(file_path, bstack111llll_opy_ (u"ࠩࡺࠫ఑"))
    bstack1l11l11ll_opy_.write(bstack111l11ll_opy_)
    bstack1l11l11ll_opy_.close()
    logger.info(bstack1ll1lll1l1_opy_)
    try:
      os.environ[bstack111llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬఒ")] = bstack111l1ll11_opy_.framework if bstack111l1ll11_opy_.framework != None else bstack111llll_opy_ (u"ࠦࠧఓ")
      config = yaml.safe_load(bstack111l11ll_opy_)
      config[bstack111llll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬఔ")] = bstack111llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬక")
      bstack11lllll1l_opy_(bstack1ll1l1l11_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1llll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l1111ll1_opy_.format(str(e)))
def bstack11lllll1l_opy_(bstack11ll1lll1_opy_, config, bstack111l1l111_opy_={}):
  global bstack111l111l1_opy_
  global bstack11111lll1_opy_
  global bstack1l111l11ll_opy_
  if not config:
    return
  bstack1l11llll1_opy_ = bstack1l111111l1_opy_ if not bstack111l111l1_opy_ else (
    bstack1ll11l11ll_opy_ if bstack111llll_opy_ (u"ࠧࡢࡲࡳࠫఖ") in config else bstack1lllllllll_opy_)
  bstack1l1l11lll1_opy_ = False
  bstack1lll1l1l1_opy_ = False
  if bstack111l111l1_opy_ is True:
      if bstack111llll_opy_ (u"ࠨࡣࡳࡴࠬగ") in config:
          bstack1l1l11lll1_opy_ = True
      else:
          bstack1lll1l1l1_opy_ = True
  bstack1llll11l_opy_ = bstack11l1ll1l1_opy_.bstack1l1l1l1l_opy_(config, bstack11111lll1_opy_)
  data = {
    bstack111llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫఘ"): config[bstack111llll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬఙ")],
    bstack111llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧచ"): config[bstack111llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨఛ")],
    bstack111llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪజ"): bstack11ll1lll1_opy_,
    bstack111llll_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫఝ"): os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪఞ"), bstack11111lll1_opy_),
    bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫట"): bstack1l11l1l1l_opy_,
    bstack111llll_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬఠ"): bstack1l11111l1_opy_(),
    bstack111llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧడ"): {
      bstack111llll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఢ"): str(config[bstack111llll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ణ")]) if bstack111llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧత") in config else bstack111llll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤథ"),
      bstack111llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫద"): sys.version,
      bstack111llll_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬధ"): bstack1ll11l11l1_opy_(os.getenv(bstack111llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨన"), bstack111llll_opy_ (u"ࠧࠨ఩"))),
      bstack111llll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨప"): bstack111llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧఫ"),
      bstack111llll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩబ"): bstack1l11llll1_opy_,
      bstack111llll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧభ"): bstack1llll11l_opy_,
      bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩమ"): os.environ[bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩయ")],
      bstack111llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨర"): bstack1l11l11l1l_opy_(os.environ.get(bstack111llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨఱ"), bstack11111lll1_opy_)),
      bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪల"): config[bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫళ")] if config[bstack111llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬఴ")] else bstack111llll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦవ"),
      bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭శ"): str(config[bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧష")]) if bstack111llll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨస") in config else bstack111llll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣహ"),
      bstack111llll_opy_ (u"ࠨࡱࡶࠫ఺"): sys.platform,
      bstack111llll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ఻"): socket.gethostname(),
      bstack111llll_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨ఼ࠬ"): bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ఽ"))
    }
  }
  if not bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬా")) is None:
    data[bstack111llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩి")][bstack111llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡏࡨࡸࡦࡪࡡࡵࡣࠪీ")] = {
      bstack111llll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨు"): bstack111llll_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧూ"),
      bstack111llll_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪృ"): bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫౄ")),
      bstack111llll_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࡓࡻ࡭ࡣࡧࡵࠫ౅"): bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩె"))
    }
  if bstack11ll1lll1_opy_ == bstack1ll1l11ll_opy_:
    data[bstack111llll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪే")][bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬࠭ై")] = bstack11ll1l11l_opy_(config)
    data[bstack111llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ౉")][bstack111llll_opy_ (u"ࠪ࡭ࡸࡖࡥࡳࡥࡼࡅࡺࡺ࡯ࡆࡰࡤࡦࡱ࡫ࡤࠨొ")] = percy.bstack11llll1l_opy_
    data[bstack111llll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧో")][bstack111llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡆࡺ࡯࡬ࡥࡋࡧࠫౌ")] = percy.bstack1l111ll1ll_opy_
  update(data[bstack111llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴ్ࠩ")], bstack111l1l111_opy_)
  try:
    response = bstack1l1ll1l1l1_opy_(bstack111llll_opy_ (u"ࠧࡑࡑࡖࡘࠬ౎"), bstack11l1l1ll_opy_(bstack1lll1l111l_opy_), data, {
      bstack111llll_opy_ (u"ࠨࡣࡸࡸ࡭࠭౏"): (config[bstack111llll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ౐")], config[bstack111llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭౑")])
    })
    if response:
      logger.debug(bstack111ll111_opy_.format(bstack11ll1lll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11ll11l1l_opy_.format(str(e)))
def bstack1ll11l11l1_opy_(framework):
  return bstack111llll_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ౒").format(str(framework), __version__) if framework else bstack111llll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨ౓").format(
    __version__)
def bstack1lll1ll1l_opy_():
  global CONFIG
  global bstack1llll111_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll1l1ll1l_opy_()
    logger.debug(bstack1ll11111_opy_.format(str(CONFIG)))
    bstack1llll111_opy_ = bstack1ll1l1ll11_opy_.bstack11llll1ll_opy_(CONFIG, bstack1llll111_opy_)
    bstack1lll1111l1_opy_()
  except Exception as e:
    logger.error(bstack111llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ౔") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lll1111_opy_
  atexit.register(bstack1l11ll11l_opy_)
  signal.signal(signal.SIGINT, bstack1llll1l1l1_opy_)
  signal.signal(signal.SIGTERM, bstack1llll1l1l1_opy_)
def bstack1lll1111_opy_(exctype, value, traceback):
  global bstack1l1111111l_opy_
  try:
    for driver in bstack1l1111111l_opy_:
      bstack1l1l1lll_opy_(driver, bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪౕࠧ"), bstack111llll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱౖࠦ") + str(value))
  except Exception:
    pass
  bstack11111l111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11111l111_opy_(message=bstack111llll_opy_ (u"ࠩࠪ౗"), bstack1ll11lll_opy_ = False):
  global CONFIG
  bstack11lll1l1_opy_ = bstack111llll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬౘ") if bstack1ll11lll_opy_ else bstack111llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪౙ")
  try:
    if message:
      bstack111l1l111_opy_ = {
        bstack11lll1l1_opy_ : str(message)
      }
      bstack11lllll1l_opy_(bstack1ll1l11ll_opy_, CONFIG, bstack111l1l111_opy_)
    else:
      bstack11lllll1l_opy_(bstack1ll1l11ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1llll11ll1_opy_.format(str(e)))
def bstack1l1l11l111_opy_(bstack1lll1ll111_opy_, size):
  bstack1111lll11_opy_ = []
  while len(bstack1lll1ll111_opy_) > size:
    bstack1l1l111lll_opy_ = bstack1lll1ll111_opy_[:size]
    bstack1111lll11_opy_.append(bstack1l1l111lll_opy_)
    bstack1lll1ll111_opy_ = bstack1lll1ll111_opy_[size:]
  bstack1111lll11_opy_.append(bstack1lll1ll111_opy_)
  return bstack1111lll11_opy_
def bstack1ll1l111_opy_(args):
  if bstack111llll_opy_ (u"ࠬ࠳࡭ࠨౚ") in args and bstack111llll_opy_ (u"࠭ࡰࡥࡤࠪ౛") in args:
    return True
  return False
def run_on_browserstack(bstack1ll1l11ll1_opy_=None, bstack1l1l1ll1l1_opy_=None, bstack11lllll1ll_opy_=False):
  global CONFIG
  global bstack11l111lll_opy_
  global bstack11l1l1l1l_opy_
  global bstack11111lll1_opy_
  global bstack1l111l11ll_opy_
  bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠧࠨ౜")
  bstack1ll1l1l1l_opy_(bstack1ll1l111ll_opy_, logger)
  if bstack1ll1l11ll1_opy_ and isinstance(bstack1ll1l11ll1_opy_, str):
    bstack1ll1l11ll1_opy_ = eval(bstack1ll1l11ll1_opy_)
  if bstack1ll1l11ll1_opy_:
    CONFIG = bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨౝ")]
    bstack11l111lll_opy_ = bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ౞")]
    bstack11l1l1l1l_opy_ = bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ౟")]
    bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ౠ"), bstack11l1l1l1l_opy_)
    bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬౡ")
  bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨౢ"), uuid4().__str__())
  logger.debug(bstack111llll_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥ࠿ࠪౣ") + bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ౤")))
  if not bstack11lllll1ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1llllll_opy_)
      return
    if sys.argv[1] == bstack111llll_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ౥") or sys.argv[1] == bstack111llll_opy_ (u"ࠪ࠱ࡻ࠭౦"):
      logger.info(bstack111llll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫ౧").format(__version__))
      return
    if sys.argv[1] == bstack111llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ౨"):
      bstack1lll1l111_opy_()
      return
  args = sys.argv
  bstack1lll1ll1l_opy_()
  global bstack11ll1ll1l_opy_
  global bstack11l111111_opy_
  global bstack1lll1l1l11_opy_
  global bstack1ll11l1ll_opy_
  global bstack1lll1l1l_opy_
  global bstack1l1lll1l_opy_
  global bstack1l11ll11l1_opy_
  global bstack1ll1111ll1_opy_
  global bstack1llll1111l_opy_
  global bstack1ll11ll11l_opy_
  global bstack11l1ll1ll_opy_
  bstack11l111111_opy_ = len(CONFIG.get(bstack111llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౩"), []))
  if not bstack1l1l11111l_opy_:
    if args[1] == bstack111llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౪") or args[1] == bstack111llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ౫"):
      bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ౬")
      args = args[2:]
    elif args[1] == bstack111llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ౭"):
      bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౮")
      args = args[2:]
    elif args[1] == bstack111llll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ౯"):
      bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ౰")
      args = args[2:]
    elif args[1] == bstack111llll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ౱"):
      bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ౲")
      args = args[2:]
    elif args[1] == bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౳"):
      bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ౴")
      args = args[2:]
    elif args[1] == bstack111llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ౵"):
      bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ౶")
      args = args[2:]
    else:
      if not bstack111llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ౷") in CONFIG or str(CONFIG[bstack111llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ౸")]).lower() in [bstack111llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ౹"), bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ౺")]:
        bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ౻")
        args = args[1:]
      elif str(CONFIG[bstack111llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ౼")]).lower() == bstack111llll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ౽"):
        bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ౾")
        args = args[1:]
      elif str(CONFIG[bstack111llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ౿")]).lower() == bstack111llll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧಀ"):
        bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨಁ")
        args = args[1:]
      elif str(CONFIG[bstack111llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಂ")]).lower() == bstack111llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಃ"):
        bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ಄")
        args = args[1:]
      elif str(CONFIG[bstack111llll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಅ")]).lower() == bstack111llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಆ"):
        bstack1l1l11111l_opy_ = bstack111llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨಇ")
        args = args[1:]
      else:
        os.environ[bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಈ")] = bstack1l1l11111l_opy_
        bstack1l1l1l111l_opy_(bstack1l11l1ll_opy_)
  os.environ[bstack111llll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫಉ")] = bstack1l1l11111l_opy_
  bstack11111lll1_opy_ = bstack1l1l11111l_opy_
  global bstack1l11lll1l1_opy_
  global bstack11l1l111_opy_
  if bstack1ll1l11ll1_opy_:
    try:
      os.environ[bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ಊ")] = bstack1l1l11111l_opy_
      bstack11lllll1l_opy_(bstack111ll1lll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l1l1l1lll_opy_.format(str(e)))
  global bstack1l1l1l11_opy_
  global bstack11lll11ll_opy_
  global bstack1lll11ll1_opy_
  global bstack11lll1l11_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1l11l11ll1_opy_
  global bstack1lll11ll1l_opy_
  global bstack1l11l111l_opy_
  global bstack1l11llll11_opy_
  global bstack11l11111l_opy_
  global bstack1l1l11l11l_opy_
  global bstack1l1ll1l1_opy_
  global bstack111l1llll_opy_
  global bstack1ll1lll1_opy_
  global bstack1l1lll1l1_opy_
  global bstack1l1lll11l1_opy_
  global bstack1l11l1ll1_opy_
  global bstack1ll1ll11l1_opy_
  global bstack1l1lllll11_opy_
  global bstack1l11l1l11_opy_
  global bstack1ll1l1111l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l1l11_opy_ = webdriver.Remote.__init__
    bstack11lll11ll_opy_ = WebDriver.quit
    bstack1l1ll1l1_opy_ = WebDriver.close
    bstack1l1lll1l1_opy_ = WebDriver.get
    bstack1ll1l1111l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l11lll1l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1l111lll_opy_
    bstack11l1l111_opy_ = bstack1l111lll_opy_()
  except Exception as e:
    pass
  try:
    global bstack111ll11l1_opy_
    from QWeb.keywords import browser
    bstack111ll11l1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll111l1l1_opy_(CONFIG) and bstack1ll1ll1l11_opy_():
    if bstack1lll111l1_opy_() < version.parse(bstack1l1l1l11l_opy_):
      logger.error(bstack1lll11l1ll_opy_.format(bstack1lll111l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1lll11l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l1111l1_opy_.format(str(e)))
  if not CONFIG.get(bstack111llll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧಋ"), False) and not bstack1ll1l11ll1_opy_:
    logger.info(bstack1llllll11l_opy_)
  if bstack1l1l11111l_opy_ != bstack111llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ಌ") or (bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ಍") and not bstack1ll1l11ll1_opy_):
    bstack1l11l1ll1l_opy_()
  if (bstack1l1l11111l_opy_ in [bstack111llll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧಎ"), bstack111llll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨಏ"), bstack111llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫಐ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll111lll1_opy_
        bstack1l11l11ll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1llllll1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1l1ll1ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1111lll_opy_ + str(e))
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1llllll1ll_opy_)
    if bstack1l1l11111l_opy_ != bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ಑"):
      bstack1l1111ll1l_opy_()
    bstack1lll11ll1_opy_ = Output.start_test
    bstack11lll1l11_opy_ = Output.end_test
    bstack1lll11ll1l_opy_ = TestStatus.__init__
    bstack1l11llll11_opy_ = pabot._run
    bstack11l11111l_opy_ = QueueItem.__init__
    bstack1l1l11l11l_opy_ = pabot._create_command_for_execution
    bstack1l1lllll11_opy_ = pabot._report_results
  if bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬಒ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1l111l111_opy_)
    bstack111l1llll_opy_ = Runner.run_hook
    bstack1ll1lll1_opy_ = Step.run
  if bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಓ"):
    try:
      from _pytest.config import Config
      bstack1l11l1ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack1ll1ll11l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11llllll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l11l1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111llll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨಔ"))
  try:
    framework_name = bstack111llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧಕ") if bstack1l1l11111l_opy_ in [bstack111llll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨಖ"), bstack111llll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಗ"), bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬಘ")] else bstack1l1ll1111l_opy_(bstack1l1l11111l_opy_)
    bstack1111ll1l_opy_ = {
      bstack111llll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ಙ"): bstack111llll_opy_ (u"࠭ࡻ࠱ࡿ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬಚ").format(framework_name) if bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧಛ") and bstack1ll11lll1l_opy_() else framework_name,
      bstack111llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಜ"): bstack1l11l11l1l_opy_(framework_name),
      bstack111llll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಝ"): __version__,
      bstack111llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫಞ"): bstack1l1l11111l_opy_
    }
    if bstack1l1l11111l_opy_ in bstack1lllllll11_opy_:
      if bstack111l111l1_opy_ and bstack111llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫಟ") in CONFIG and CONFIG[bstack111llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬಠ")] == True:
        if bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ಡ") in CONFIG:
          os.environ[bstack111llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨಢ")] = os.getenv(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩಣ"), json.dumps(CONFIG[bstack111llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩತ")]))
          CONFIG[bstack111llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪಥ")].pop(bstack111llll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩದ"), None)
          CONFIG[bstack111llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬಧ")].pop(bstack111llll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫನ"), None)
        bstack1111ll1l_opy_[bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ಩")] = {
          bstack111llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಪ"): bstack111llll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫಫ"),
          bstack111llll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫಬ"): str(bstack1lll111l1_opy_())
        }
    if bstack1l1l11111l_opy_ not in [bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬಭ")]:
      bstack1llll11lll_opy_ = bstack1l11l1lll_opy_.launch(CONFIG, bstack1111ll1l_opy_)
  except Exception as e:
    logger.debug(bstack11l111l1l_opy_.format(bstack111llll_opy_ (u"࡚ࠬࡥࡴࡶࡋࡹࡧ࠭ಮ"), str(e)))
  if bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ಯ"):
    bstack1lll1l1l11_opy_ = True
    if bstack1ll1l11ll1_opy_ and bstack11lllll1ll_opy_:
      bstack1l1lll1l_opy_ = CONFIG.get(bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫರ"), {}).get(bstack111llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಱ"))
      bstack1111ll111_opy_(bstack11ll1llll_opy_)
    elif bstack1ll1l11ll1_opy_:
      bstack1l1lll1l_opy_ = CONFIG.get(bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ಲ"), {}).get(bstack111llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಳ"))
      global bstack1l1111111l_opy_
      try:
        if bstack1ll1l111_opy_(bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ಴")]) and multiprocessing.current_process().name == bstack111llll_opy_ (u"ࠬ࠶ࠧವ"):
          bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩಶ")].remove(bstack111llll_opy_ (u"ࠧ࠮࡯ࠪಷ"))
          bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಸ")].remove(bstack111llll_opy_ (u"ࠩࡳࡨࡧ࠭ಹ"))
          bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭಺")] = bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ಻")][0]
          with open(bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ಼")], bstack111llll_opy_ (u"࠭ࡲࠨಽ")) as f:
            bstack11111ll1l_opy_ = f.read()
          bstack1ll11ll11_opy_ = bstack111llll_opy_ (u"ࠢࠣࠤࡩࡶࡴࡳࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡥ࡭ࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡁࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࠫࡿࢂ࠯࠻ࠡࡨࡵࡳࡲࠦࡰࡥࡤࠣ࡭ࡲࡶ࡯ࡳࡶࠣࡔࡩࡨ࠻ࠡࡱࡪࡣࡩࡨࠠ࠾ࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡥࡧࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯࠭ࡹࡥ࡭ࡨ࠯ࠤࡦࡸࡧ࠭ࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡃࠠ࠱ࠫ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡺࡦࡩࡵࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡥࡸࠦࡥ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡸࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫ࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥಾ").format(str(bstack1ll1l11ll1_opy_))
          bstack111lllll_opy_ = bstack1ll11ll11_opy_ + bstack11111ll1l_opy_
          bstack1lll111ll_opy_ = bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಿ")] + bstack111llll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡸࡪࡳࡰ࠯ࡲࡼࠫೀ")
          with open(bstack1lll111ll_opy_, bstack111llll_opy_ (u"ࠪࡻࠬು")):
            pass
          with open(bstack1lll111ll_opy_, bstack111llll_opy_ (u"ࠦࡼ࠱ࠢೂ")) as f:
            f.write(bstack111lllll_opy_)
          import subprocess
          bstack1l1ll1l11_opy_ = subprocess.run([bstack111llll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧೃ"), bstack1lll111ll_opy_])
          if os.path.exists(bstack1lll111ll_opy_):
            os.unlink(bstack1lll111ll_opy_)
          os._exit(bstack1l1ll1l11_opy_.returncode)
        else:
          if bstack1ll1l111_opy_(bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೄ")]):
            bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ೅")].remove(bstack111llll_opy_ (u"ࠨ࠯ࡰࠫೆ"))
            bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬೇ")].remove(bstack111llll_opy_ (u"ࠪࡴࡩࡨࠧೈ"))
            bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೉")] = bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨೊ")][0]
          bstack1111ll111_opy_(bstack11ll1llll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೋ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111llll_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩೌ")] = bstack111llll_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡ್ࠪ")
          mod_globals[bstack111llll_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ೎")] = os.path.abspath(bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭೏")])
          exec(open(bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೐")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111llll_opy_ (u"ࠬࡉࡡࡶࡩ࡫ࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠬ೑").format(str(e)))
          for driver in bstack1l1111111l_opy_:
            bstack1l1l1ll1l1_opy_.append({
              bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೒"): bstack1ll1l11ll1_opy_[bstack111llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ೓")],
              bstack111llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ೔"): str(e),
              bstack111llll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨೕ"): multiprocessing.current_process().name
            })
            bstack1l1l1lll_opy_(driver, bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪೖ"), bstack111llll_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ೗") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1111111l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l1l1l1l_opy_, CONFIG, logger)
      bstack1111l1l1l_opy_()
      bstack1lllll1lll_opy_()
      bstack1111llll1_opy_ = {
        bstack111llll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ೘"): args[0],
        bstack111llll_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭೙"): CONFIG,
        bstack111llll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ೚"): bstack11l111lll_opy_,
        bstack111llll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ೛"): bstack11l1l1l1l_opy_
      }
      percy.bstack1lllll1ll_opy_()
      if bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ೜") in CONFIG:
        bstack1ll1l11l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llllllll_opy_ = manager.list()
        if bstack1ll1l111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ೝ")]):
            if index == 0:
              bstack1111llll1_opy_[bstack111llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧೞ")] = args
            bstack1ll1l11l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111llll1_opy_, bstack1llllllll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack111llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೟")]):
            bstack1ll1l11l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1111llll1_opy_, bstack1llllllll_opy_)))
        for t in bstack1ll1l11l1_opy_:
          t.start()
        for t in bstack1ll1l11l1_opy_:
          t.join()
        bstack1ll1111ll1_opy_ = list(bstack1llllllll_opy_)
      else:
        if bstack1ll1l111_opy_(args):
          bstack1111llll1_opy_[bstack111llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೠ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1111llll1_opy_,))
          test.start()
          test.join()
        else:
          bstack1111ll111_opy_(bstack11ll1llll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111llll_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩೡ")] = bstack111llll_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪೢ")
          mod_globals[bstack111llll_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫೣ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ೤") or bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೥"):
    percy.init(bstack11l1l1l1l_opy_, CONFIG, logger)
    percy.bstack1lllll1ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1llllll1ll_opy_)
    bstack1111l1l1l_opy_()
    bstack1111ll111_opy_(bstack1l1l1ll11_opy_)
    if bstack111l111l1_opy_:
      bstack1l1llll1l_opy_(bstack1l1l1ll11_opy_, args)
      if bstack111llll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ೦") in args:
        i = args.index(bstack111llll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ೧"))
        args.pop(i)
        args.pop(i)
      if bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ೨") not in CONFIG:
        CONFIG[bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೩")] = [{}]
        bstack11l111111_opy_ = 1
      if bstack11ll1ll1l_opy_ == 0:
        bstack11ll1ll1l_opy_ = 1
      args.insert(0, str(bstack11ll1ll1l_opy_))
      args.insert(0, str(bstack111llll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ೪")))
    if bstack1l11l1lll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll1ll111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l111l1ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111llll_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ೫"),
        ).parse_args(bstack1ll1ll111_opy_)
        bstack11ll1l1l1_opy_ = args.index(bstack1ll1ll111_opy_[0]) if len(bstack1ll1ll111_opy_) > 0 else len(args)
        args.insert(bstack11ll1l1l1_opy_, str(bstack111llll_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ೬")))
        args.insert(bstack11ll1l1l1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ೭"))))
        if bstack1l11ll1lll_opy_(os.environ.get(bstack111llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ೮"))) and str(os.environ.get(bstack111llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ೯"), bstack111llll_opy_ (u"ࠨࡰࡸࡰࡱ࠭೰"))) != bstack111llll_opy_ (u"ࠩࡱࡹࡱࡲࠧೱ"):
          for bstack11l11l11l_opy_ in bstack1l111l1ll_opy_:
            args.remove(bstack11l11l11l_opy_)
          bstack1111l1111_opy_ = os.environ.get(bstack111llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧೲ")).split(bstack111llll_opy_ (u"ࠫ࠱࠭ೳ"))
          for bstack1llll1l1l_opy_ in bstack1111l1111_opy_:
            args.append(bstack1llll1l1l_opy_)
      except Exception as e:
        logger.error(bstack111llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣ೴").format(e))
    pabot.main(args)
  elif bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ೵"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1llllll1ll_opy_)
    for a in args:
      if bstack111llll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭೶") in a:
        bstack1lll1l1l_opy_ = int(a.split(bstack111llll_opy_ (u"ࠨ࠼ࠪ೷"))[1])
      if bstack111llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭೸") in a:
        bstack1l1lll1l_opy_ = str(a.split(bstack111llll_opy_ (u"ࠪ࠾ࠬ೹"))[1])
      if bstack111llll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫ೺") in a:
        bstack1l11ll11l1_opy_ = str(a.split(bstack111llll_opy_ (u"ࠬࡀࠧ೻"))[1])
    bstack1l11l11lll_opy_ = None
    if bstack111llll_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ೼") in args:
      i = args.index(bstack111llll_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭೽"))
      args.pop(i)
      bstack1l11l11lll_opy_ = args.pop(i)
    if bstack1l11l11lll_opy_ is not None:
      global bstack1lll11l11l_opy_
      bstack1lll11l11l_opy_ = bstack1l11l11lll_opy_
    bstack1111ll111_opy_(bstack1l1l1ll11_opy_)
    run_cli(args)
    if bstack111llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ೾") in multiprocessing.current_process().__dict__.keys():
      for bstack1l111lll11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1l1ll1l1_opy_.append(bstack1l111lll11_opy_)
  elif bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ೿"):
    percy.init(bstack11l1l1l1l_opy_, CONFIG, logger)
    percy.bstack1lllll1ll_opy_()
    bstack11ll1ll11_opy_ = bstack1l111ll11l_opy_(args, logger, CONFIG, bstack111l111l1_opy_)
    bstack11ll1ll11_opy_.bstack11111l1l_opy_()
    bstack1111l1l1l_opy_()
    bstack1ll11l1ll_opy_ = True
    bstack1ll11ll11l_opy_ = bstack11ll1ll11_opy_.bstack1l1llllll1_opy_()
    bstack11ll1ll11_opy_.bstack1111llll1_opy_(bstack111l1lll1_opy_)
    bstack11l1l11l1_opy_ = bstack11ll1ll11_opy_.bstack11lll1111_opy_(bstack1l111l1l1_opy_, {
      bstack111llll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫഀ"): bstack11l111lll_opy_,
      bstack111llll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ഁ"): bstack11l1l1l1l_opy_,
      bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨം"): bstack111l111l1_opy_
    })
    try:
      bstack1111l11l_opy_, bstack1lllll1l1l_opy_ = map(list, zip(*bstack11l1l11l1_opy_))
      bstack1llll1111l_opy_ = bstack1111l11l_opy_[0]
      for status_code in bstack1lllll1l1l_opy_:
        if status_code != 0:
          bstack11l1ll1ll_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦഃ").format(str(e)))
  elif bstack1l1l11111l_opy_ == bstack111llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧഄ"):
    try:
      from behave.__main__ import main as bstack11lllllll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1l111l111_opy_)
    bstack1111l1l1l_opy_()
    bstack1ll11l1ll_opy_ = True
    bstack11l1ll111_opy_ = 1
    if bstack111llll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨഅ") in CONFIG:
      bstack11l1ll111_opy_ = CONFIG[bstack111llll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩആ")]
    if bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ഇ") in CONFIG:
      bstack1ll1lll11l_opy_ = int(bstack11l1ll111_opy_) * int(len(CONFIG[bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഈ")]))
    else:
      bstack1ll1lll11l_opy_ = int(bstack11l1ll111_opy_)
    config = Configuration(args)
    bstack1l11l111_opy_ = config.paths
    if len(bstack1l11l111_opy_) == 0:
      import glob
      pattern = bstack111llll_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫഉ")
      bstack1ll1l111l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll1l111l_opy_)
      config = Configuration(args)
      bstack1l11l111_opy_ = config.paths
    bstack1l1l11l1ll_opy_ = [os.path.normpath(item) for item in bstack1l11l111_opy_]
    bstack1111ll1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1llll1l1_opy_ = [item for item in bstack1111ll1l1_opy_ if item not in bstack1l1l11l1ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack111llll_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧഊ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1l11l1ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l111l1_opy_)))
                    for bstack1l1l111l1_opy_ in bstack1l1l11l1ll_opy_]
    bstack1l1ll111l1_opy_ = []
    for spec in bstack1l1l11l1ll_opy_:
      bstack1l1llll1ll_opy_ = []
      bstack1l1llll1ll_opy_ += bstack1l1llll1l1_opy_
      bstack1l1llll1ll_opy_.append(spec)
      bstack1l1ll111l1_opy_.append(bstack1l1llll1ll_opy_)
    execution_items = []
    for bstack1l1llll1ll_opy_ in bstack1l1ll111l1_opy_:
      if bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪഋ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫഌ")]):
          item = {}
          item[bstack111llll_opy_ (u"ࠩࡤࡶ࡬࠭഍")] = bstack111llll_opy_ (u"ࠪࠤࠬഎ").join(bstack1l1llll1ll_opy_)
          item[bstack111llll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪഏ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111llll_opy_ (u"ࠬࡧࡲࡨࠩഐ")] = bstack111llll_opy_ (u"࠭ࠠࠨ഑").join(bstack1l1llll1ll_opy_)
        item[bstack111llll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ഒ")] = 0
        execution_items.append(item)
    bstack11l1l1111_opy_ = bstack1l1l11l111_opy_(execution_items, bstack1ll1lll11l_opy_)
    for execution_item in bstack11l1l1111_opy_:
      bstack1ll1l11l1_opy_ = []
      for item in execution_item:
        bstack1ll1l11l1_opy_.append(bstack1llll1l1ll_opy_(name=str(item[bstack111llll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧഓ")]),
                                             target=bstack11ll11ll1_opy_,
                                             args=(item[bstack111llll_opy_ (u"ࠩࡤࡶ࡬࠭ഔ")],)))
      for t in bstack1ll1l11l1_opy_:
        t.start()
      for t in bstack1ll1l11l1_opy_:
        t.join()
  else:
    bstack1l1l1l111l_opy_(bstack1l11l1ll_opy_)
  if not bstack1ll1l11ll1_opy_:
    bstack1l1111l11_opy_()
  bstack1ll1l1ll11_opy_.bstack111l1111_opy_()
def browserstack_initialize(bstack1l1ll11ll_opy_=None):
  run_on_browserstack(bstack1l1ll11ll_opy_, None, True)
def bstack1l1111l11_opy_():
  global CONFIG
  global bstack11111lll1_opy_
  global bstack11l1ll1ll_opy_
  global bstack1ll11llll_opy_
  global bstack1l111l11ll_opy_
  bstack1l11l1lll_opy_.stop()
  bstack1l1lll1111_opy_.bstack1l1ll11l1_opy_()
  [bstack11l1llll_opy_, bstack1l1111lll1_opy_] = get_build_link()
  if bstack11l1llll_opy_ is not None and bstack11lllll11_opy_() != -1:
    sessions = bstack1ll1ll11ll_opy_(bstack11l1llll_opy_)
    bstack1l11lllll_opy_(sessions, bstack1l1111lll1_opy_)
  if bstack11111lll1_opy_ == bstack111llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪക") and bstack11l1ll1ll_opy_ != 0:
    sys.exit(bstack11l1ll1ll_opy_)
  if bstack11111lll1_opy_ == bstack111llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഖ") and bstack1ll11llll_opy_ != 0:
    sys.exit(bstack1ll11llll_opy_)
def bstack1l1ll1111l_opy_(bstack1llllll11_opy_):
  if bstack1llllll11_opy_:
    return bstack1llllll11_opy_.capitalize()
  else:
    return bstack111llll_opy_ (u"ࠬ࠭ഗ")
def bstack1llll1l11l_opy_(bstack1ll1l1lll1_opy_):
  if bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫഘ") in bstack1ll1l1lll1_opy_ and bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬങ")] != bstack111llll_opy_ (u"ࠨࠩച"):
    return bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧഛ")]
  else:
    bstack1ll11l111l_opy_ = bstack111llll_opy_ (u"ࠥࠦജ")
    if bstack111llll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫഝ") in bstack1ll1l1lll1_opy_ and bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬഞ")] != None:
      bstack1ll11l111l_opy_ += bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ട")] + bstack111llll_opy_ (u"ࠢ࠭ࠢࠥഠ")
      if bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠨࡱࡶࠫഡ")] == bstack111llll_opy_ (u"ࠤ࡬ࡳࡸࠨഢ"):
        bstack1ll11l111l_opy_ += bstack111llll_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣണ")
      bstack1ll11l111l_opy_ += (bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨത")] or bstack111llll_opy_ (u"ࠬ࠭ഥ"))
      return bstack1ll11l111l_opy_
    else:
      bstack1ll11l111l_opy_ += bstack1l1ll1111l_opy_(bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧദ")]) + bstack111llll_opy_ (u"ࠢࠡࠤധ") + (
              bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪന")] or bstack111llll_opy_ (u"ࠩࠪഩ")) + bstack111llll_opy_ (u"ࠥ࠰ࠥࠨപ")
      if bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠫࡴࡹࠧഫ")] == bstack111llll_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨബ"):
        bstack1ll11l111l_opy_ += bstack111llll_opy_ (u"ࠨࡗࡪࡰࠣࠦഭ")
      bstack1ll11l111l_opy_ += bstack1ll1l1lll1_opy_[bstack111llll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫമ")] or bstack111llll_opy_ (u"ࠨࠩയ")
      return bstack1ll11l111l_opy_
def bstack1l11ll111l_opy_(bstack1ll11l1l11_opy_):
  if bstack1ll11l1l11_opy_ == bstack111llll_opy_ (u"ࠤࡧࡳࡳ࡫ࠢര"):
    return bstack111llll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭റ")
  elif bstack1ll11l1l11_opy_ == bstack111llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦല"):
    return bstack111llll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨള")
  elif bstack1ll11l1l11_opy_ == bstack111llll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨഴ"):
    return bstack111llll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧവ")
  elif bstack1ll11l1l11_opy_ == bstack111llll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢശ"):
    return bstack111llll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫഷ")
  elif bstack1ll11l1l11_opy_ == bstack111llll_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦസ"):
    return bstack111llll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩഹ")
  elif bstack1ll11l1l11_opy_ == bstack111llll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨഺ"):
    return bstack111llll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄ഻ࠧ")
  else:
    return bstack111llll_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁ഼ࠫ") + bstack1l1ll1111l_opy_(
      bstack1ll11l1l11_opy_) + bstack111llll_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧഽ")
def bstack1l1lll1l1l_opy_(session):
  return bstack111llll_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩാ").format(
    session[bstack111llll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧി")], bstack1llll1l11l_opy_(session), bstack1l11ll111l_opy_(session[bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪീ")]),
    bstack1l11ll111l_opy_(session[bstack111llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬു")]),
    bstack1l1ll1111l_opy_(session[bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧൂ")] or session[bstack111llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧൃ")] or bstack111llll_opy_ (u"ࠨࠩൄ")) + bstack111llll_opy_ (u"ࠤࠣࠦ൅") + (session[bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬെ")] or bstack111llll_opy_ (u"ࠫࠬേ")),
    session[bstack111llll_opy_ (u"ࠬࡵࡳࠨൈ")] + bstack111llll_opy_ (u"ࠨࠠࠣ൉") + session[bstack111llll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫൊ")], session[bstack111llll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪോ")] or bstack111llll_opy_ (u"ࠩࠪൌ"),
    session[bstack111llll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺ്ࠧ")] if session[bstack111llll_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨൎ")] else bstack111llll_opy_ (u"ࠬ࠭൏"))
def bstack1l11lllll_opy_(sessions, bstack1l1111lll1_opy_):
  try:
    bstack1l11ll1l1l_opy_ = bstack111llll_opy_ (u"ࠨࠢ൐")
    if not os.path.exists(bstack11ll111ll_opy_):
      os.mkdir(bstack11ll111ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111llll_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ൑")), bstack111llll_opy_ (u"ࠨࡴࠪ൒")) as f:
      bstack1l11ll1l1l_opy_ = f.read()
    bstack1l11ll1l1l_opy_ = bstack1l11ll1l1l_opy_.replace(bstack111llll_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭൓"), str(len(sessions)))
    bstack1l11ll1l1l_opy_ = bstack1l11ll1l1l_opy_.replace(bstack111llll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪൔ"), bstack1l1111lll1_opy_)
    bstack1l11ll1l1l_opy_ = bstack1l11ll1l1l_opy_.replace(bstack111llll_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬൕ"),
                                              sessions[0].get(bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩൖ")) if sessions[0] else bstack111llll_opy_ (u"࠭ࠧൗ"))
    with open(os.path.join(bstack11ll111ll_opy_, bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ൘")), bstack111llll_opy_ (u"ࠨࡹࠪ൙")) as stream:
      stream.write(bstack1l11ll1l1l_opy_.split(bstack111llll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭൚"))[0])
      for session in sessions:
        stream.write(bstack1l1lll1l1l_opy_(session))
      stream.write(bstack1l11ll1l1l_opy_.split(bstack111llll_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ൛"))[1])
    logger.info(bstack111llll_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧ൜").format(bstack11ll111ll_opy_));
  except Exception as e:
    logger.debug(bstack1l11l1llll_opy_.format(str(e)))
def bstack1ll1ll11ll_opy_(bstack11l1llll_opy_):
  global CONFIG
  try:
    host = bstack111llll_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ൝") if bstack111llll_opy_ (u"࠭ࡡࡱࡲࠪ൞") in CONFIG else bstack111llll_opy_ (u"ࠧࡢࡲ࡬ࠫൟ")
    user = CONFIG[bstack111llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪൠ")]
    key = CONFIG[bstack111llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬൡ")]
    bstack1l1111l1ll_opy_ = bstack111llll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩൢ") if bstack111llll_opy_ (u"ࠫࡦࡶࡰࠨൣ") in CONFIG else bstack111llll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ൤")
    url = bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫ൥").format(user, key, host, bstack1l1111l1ll_opy_,
                                                                                bstack11l1llll_opy_)
    headers = {
      bstack111llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭൦"): bstack111llll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ൧"),
    }
    proxies = bstack1lllll11ll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack111llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ൨")], response.json()))
  except Exception as e:
    logger.debug(bstack1lll11l1l1_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1l11l1l1l_opy_
  try:
    if bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭൩") in CONFIG:
      host = bstack111llll_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧ൪") if bstack111llll_opy_ (u"ࠬࡧࡰࡱࠩ൫") in CONFIG else bstack111llll_opy_ (u"࠭ࡡࡱ࡫ࠪ൬")
      user = CONFIG[bstack111llll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ൭")]
      key = CONFIG[bstack111llll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ൮")]
      bstack1l1111l1ll_opy_ = bstack111llll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ൯") if bstack111llll_opy_ (u"ࠪࡥࡵࡶࠧ൰") in CONFIG else bstack111llll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭൱")
      url = bstack111llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬ൲").format(user, key, host, bstack1l1111l1ll_opy_)
      headers = {
        bstack111llll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ൳"): bstack111llll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ൴"),
      }
      if bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ൵") in CONFIG:
        params = {bstack111llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ൶"): CONFIG[bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭൷")], bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ൸"): CONFIG[bstack111llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ൹")]}
      else:
        params = {bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫൺ"): CONFIG[bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪൻ")]}
      proxies = bstack1lllll11ll_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll1111ll_opy_ = response.json()[0][bstack111llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫർ")]
        if bstack1ll1111ll_opy_:
          bstack1l1111lll1_opy_ = bstack1ll1111ll_opy_[bstack111llll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ൽ")].split(bstack111llll_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩൾ"))[0] + bstack111llll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬൿ") + bstack1ll1111ll_opy_[
            bstack111llll_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ඀")]
          logger.info(bstack1lll111l_opy_.format(bstack1l1111lll1_opy_))
          bstack1l11l1l1l_opy_ = bstack1ll1111ll_opy_[bstack111llll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩඁ")]
          bstack1l1l1l1ll1_opy_ = CONFIG[bstack111llll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪං")]
          if bstack111llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪඃ") in CONFIG:
            bstack1l1l1l1ll1_opy_ += bstack111llll_opy_ (u"ࠩࠣࠫ඄") + CONFIG[bstack111llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬඅ")]
          if bstack1l1l1l1ll1_opy_ != bstack1ll1111ll_opy_[bstack111llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩආ")]:
            logger.debug(bstack1lllll11l1_opy_.format(bstack1ll1111ll_opy_[bstack111llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඇ")], bstack1l1l1l1ll1_opy_))
          return [bstack1ll1111ll_opy_[bstack111llll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩඈ")], bstack1l1111lll1_opy_]
    else:
      logger.warn(bstack1111l1ll_opy_)
  except Exception as e:
    logger.debug(bstack1l11l111l1_opy_.format(str(e)))
  return [None, None]
def bstack1l1lllllll_opy_(url, bstack1l1ll11l1l_opy_=False):
  global CONFIG
  global bstack1l111l1ll1_opy_
  if not bstack1l111l1ll1_opy_:
    hostname = bstack11l11l11_opy_(url)
    is_private = bstack11111111l_opy_(hostname)
    if (bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫඉ") in CONFIG and not bstack1l11ll1lll_opy_(CONFIG[bstack111llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬඊ")])) and (is_private or bstack1l1ll11l1l_opy_):
      bstack1l111l1ll1_opy_ = hostname
def bstack11l11l11_opy_(url):
  return urlparse(url).hostname
def bstack11111111l_opy_(hostname):
  for bstack11l1l1l11_opy_ in bstack1l1llll111_opy_:
    regex = re.compile(bstack11l1l1l11_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l111111l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1lll1l1l_opy_
  bstack1l1l1l11ll_opy_ = not (bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭උ"), None) and bstack1llll11l1l_opy_(
          threading.current_thread(), bstack111llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩඌ"), None))
  bstack111llll1l_opy_ = getattr(driver, bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫඍ"), None) != True
  if not bstack1l1111ll_opy_.bstack1l111l11_opy_(CONFIG, bstack1lll1l1l_opy_) or (bstack111llll1l_opy_ and bstack1l1l1l11ll_opy_):
    logger.warning(bstack111llll_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣඎ"))
    return {}
  try:
    logger.debug(bstack111llll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪඏ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1l111l_opy_.bstack1l1111ll11_opy_)
    return results
  except Exception:
    logger.error(bstack111llll_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤඐ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1lll1l1l_opy_
  bstack1l1l1l11ll_opy_ = not (bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬඑ"), None) and bstack1llll11l1l_opy_(
          threading.current_thread(), bstack111llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨඒ"), None))
  bstack111llll1l_opy_ = getattr(driver, bstack111llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪඓ"), None) != True
  if not bstack1l1111ll_opy_.bstack1l111l11_opy_(CONFIG, bstack1lll1l1l_opy_) or (bstack111llll1l_opy_ and bstack1l1l1l11ll_opy_):
    logger.warning(bstack111llll_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣඔ"))
    return {}
  try:
    logger.debug(bstack111llll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪඕ"))
    logger.debug(perform_scan(driver))
    bstack1lll1lll11_opy_ = driver.execute_async_script(bstack1l1l111l_opy_.bstack111111l1l_opy_)
    return bstack1lll1lll11_opy_
  except Exception:
    logger.error(bstack111llll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢඖ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1lll1l1l_opy_
  bstack1l1l1l11ll_opy_ = not (bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ඗"), None) and bstack1llll11l1l_opy_(
          threading.current_thread(), bstack111llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ඘"), None))
  bstack111llll1l_opy_ = getattr(driver, bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ඙"), None) != True
  if not bstack1l1111ll_opy_.bstack1l111l11_opy_(CONFIG, bstack1lll1l1l_opy_) or (bstack111llll1l_opy_ and bstack1l1l1l11ll_opy_):
    logger.warning(bstack111llll_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡹࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠧක"))
    return {}
  try:
    bstack1l1l1lll1_opy_ = driver.execute_async_script(bstack1l1l111l_opy_.perform_scan, {bstack111llll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫඛ"): kwargs.get(bstack111llll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡩ࡯࡮࡯ࡤࡲࡩ࠭ග"), None) or bstack111llll_opy_ (u"࠭ࠧඝ")})
    return bstack1l1l1lll1_opy_
  except Exception:
    logger.error(bstack111llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨඞ"))
    return {}