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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111l1ll1ll_opy_, bstack111ll11l11_opy_
import tempfile
import json
bstack1lllll1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩᒥ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111llll_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᒦ"),
      datefmt=bstack111llll_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫᒧ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll1llll_opy_():
  global bstack1lllll1l111_opy_
  if os.path.exists(bstack1lllll1l111_opy_):
    os.remove(bstack1lllll1l111_opy_)
def bstack111l1111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11llll1ll_opy_(config, log_level):
  bstack1llllll1l1l_opy_ = log_level
  if bstack111llll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᒨ") in config and config[bstack111llll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᒩ")] in bstack111l1ll1ll_opy_:
    bstack1llllll1l1l_opy_ = bstack111l1ll1ll_opy_[config[bstack111llll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᒪ")]]
  if config.get(bstack111llll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᒫ"), False):
    logging.getLogger().setLevel(bstack1llllll1l1l_opy_)
    return bstack1llllll1l1l_opy_
  global bstack1lllll1l111_opy_
  bstack111l1111_opy_()
  bstack1lllll1lll1_opy_ = logging.Formatter(
    fmt=bstack111llll_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬᒬ"),
    datefmt=bstack111llll_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪᒭ")
  )
  bstack1lllll1l1l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllll1l111_opy_)
  file_handler.setFormatter(bstack1lllll1lll1_opy_)
  bstack1lllll1l1l1_opy_.setFormatter(bstack1lllll1lll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllll1l1l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111llll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᒮ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllll1l1l1_opy_.setLevel(bstack1llllll1l1l_opy_)
  logging.getLogger().addHandler(bstack1lllll1l1l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1llllll1l1l_opy_
def bstack1lllll1l11l_opy_(config):
  try:
    bstack1llllll1l11_opy_ = set(bstack111ll11l11_opy_)
    bstack1llllll111l_opy_ = bstack111llll_opy_ (u"ࠪࠫᒯ")
    with open(bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᒰ")) as bstack1llllll1111_opy_:
      bstack1llllll11l1_opy_ = bstack1llllll1111_opy_.read()
      bstack1llllll111l_opy_ = re.sub(bstack111llll_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᒱ"), bstack111llll_opy_ (u"࠭ࠧᒲ"), bstack1llllll11l1_opy_, flags=re.M)
      bstack1llllll111l_opy_ = re.sub(
        bstack111llll_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᒳ") + bstack111llll_opy_ (u"ࠨࡾࠪᒴ").join(bstack1llllll1l11_opy_) + bstack111llll_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᒵ"),
        bstack111llll_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᒶ"),
        bstack1llllll111l_opy_, flags=re.M | re.I
      )
    def bstack1lllll1ll11_opy_(dic):
      bstack1llllll11ll_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llllll1l11_opy_:
          bstack1llllll11ll_opy_[key] = bstack111llll_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᒷ")
        else:
          if isinstance(value, dict):
            bstack1llllll11ll_opy_[key] = bstack1lllll1ll11_opy_(value)
          else:
            bstack1llllll11ll_opy_[key] = value
      return bstack1llllll11ll_opy_
    bstack1llllll11ll_opy_ = bstack1lllll1ll11_opy_(config)
    return {
      bstack111llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᒸ"): bstack1llllll111l_opy_,
      bstack111llll_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᒹ"): json.dumps(bstack1llllll11ll_opy_)
    }
  except Exception as e:
    return {}
def bstack11l1l111l_opy_(config):
  global bstack1lllll1l111_opy_
  try:
    if config.get(bstack111llll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᒺ"), False):
      return
    uuid = os.getenv(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᒻ"))
    if not uuid or uuid == bstack111llll_opy_ (u"ࠩࡱࡹࡱࡲࠧᒼ"):
      return
    bstack1lllll1l1ll_opy_ = [bstack111llll_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭ᒽ"), bstack111llll_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬᒾ"), bstack111llll_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭ᒿ"), bstack1lllll1l111_opy_]
    bstack111l1111_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬᓀ") + uuid + bstack111llll_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᓁ"))
    with tarfile.open(output_file, bstack111llll_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᓂ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllll1l1ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll1l11l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lllll1ll1l_opy_ = data.encode()
        tarinfo.size = len(bstack1lllll1ll1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lllll1ll1l_opy_))
    bstack1l1ll1lll1_opy_ = MultipartEncoder(
      fields= {
        bstack111llll_opy_ (u"ࠩࡧࡥࡹࡧࠧᓃ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111llll_opy_ (u"ࠪࡶࡧ࠭ᓄ")), bstack111llll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᓅ")),
        bstack111llll_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᓆ"): uuid
      }
    )
    response = requests.post(
      bstack111llll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࡶࡲ࡯ࡳࡦࡪ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣᓇ"),
      data=bstack1l1ll1lll1_opy_,
      headers={bstack111llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᓈ"): bstack1l1ll1lll1_opy_.content_type},
      auth=(config[bstack111llll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᓉ")], config[bstack111llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᓊ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩᓋ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪᓌ") + str(e))
  finally:
    try:
      bstack1lllll1llll_opy_()
    except:
      pass