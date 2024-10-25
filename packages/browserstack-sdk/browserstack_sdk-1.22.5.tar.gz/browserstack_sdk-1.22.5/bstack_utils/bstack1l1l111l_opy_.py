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
class bstack111lll1l11_opy_(object):
  bstack1ll1llll11_opy_ = os.path.join(os.path.expanduser(bstack111llll_opy_ (u"ࠬࢄࠧྰ")), bstack111llll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ྱ"))
  bstack111lll1l1l_opy_ = os.path.join(bstack1ll1llll11_opy_, bstack111llll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴ࠰࡭ࡷࡴࡴࠧྲ"))
  bstack111lll1lll_opy_ = None
  perform_scan = None
  bstack1l1111ll11_opy_ = None
  bstack111111l1l_opy_ = None
  bstack111llll111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111llll_opy_ (u"ࠨ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠪླ")):
      cls.instance = super(bstack111lll1l11_opy_, cls).__new__(cls)
      cls.instance.bstack111lll1ll1_opy_()
    return cls.instance
  def bstack111lll1ll1_opy_(self):
    try:
      with open(self.bstack111lll1l1l_opy_, bstack111llll_opy_ (u"ࠩࡵࠫྴ")) as bstack1l111ll1_opy_:
        bstack111lll11l1_opy_ = bstack1l111ll1_opy_.read()
        data = json.loads(bstack111lll11l1_opy_)
        if bstack111llll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬྵ") in data:
          self.bstack11l1111ll1_opy_(data[bstack111llll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ྶ")])
        if bstack111llll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ྷ") in data:
          self.bstack11l111lll1_opy_(data[bstack111llll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧྸ")])
    except:
      pass
  def bstack11l111lll1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack111llll_opy_ (u"ࠧࡴࡥࡤࡲࠬྐྵ")]
      self.bstack1l1111ll11_opy_ = scripts[bstack111llll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬྺ")]
      self.bstack111111l1l_opy_ = scripts[bstack111llll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ྻ")]
      self.bstack111llll111_opy_ = scripts[bstack111llll_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨྼ")]
  def bstack11l1111ll1_opy_(self, bstack111lll1lll_opy_):
    if bstack111lll1lll_opy_ != None and len(bstack111lll1lll_opy_) != 0:
      self.bstack111lll1lll_opy_ = bstack111lll1lll_opy_
  def store(self):
    try:
      with open(self.bstack111lll1l1l_opy_, bstack111llll_opy_ (u"ࠫࡼ࠭྽")) as file:
        json.dump({
          bstack111llll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢ྾"): self.bstack111lll1lll_opy_,
          bstack111llll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ྿"): {
            bstack111llll_opy_ (u"ࠢࡴࡥࡤࡲࠧ࿀"): self.perform_scan,
            bstack111llll_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ࿁"): self.bstack1l1111ll11_opy_,
            bstack111llll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ࿂"): self.bstack111111l1l_opy_,
            bstack111llll_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ࿃"): self.bstack111llll111_opy_
          }
        }, file)
    except:
      pass
  def bstack111l111l_opy_(self, bstack111lll11ll_opy_):
    try:
      return any(command.get(bstack111llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ࿄")) == bstack111lll11ll_opy_ for command in self.bstack111lll1lll_opy_)
    except:
      return False
bstack1l1l111l_opy_ = bstack111lll1l11_opy_()