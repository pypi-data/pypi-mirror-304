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
from uuid import uuid4
from bstack_utils.helper import bstack1ll1llllll_opy_, bstack111l11ll11_opy_
from bstack_utils.bstack1l11ll1111_opy_ import bstack1lll11l11l1_opy_
class bstack11ll11111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11lll11l11_opy_=None, framework=None, tags=[], scope=[], bstack1ll1lll1l11_opy_=None, bstack1ll1ll1llll_opy_=True, bstack1ll1ll1l1ll_opy_=None, bstack11ll1lll1_opy_=None, result=None, duration=None, bstack11ll111ll1_opy_=None, meta={}):
        self.bstack11ll111ll1_opy_ = bstack11ll111ll1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1ll1llll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11lll11l11_opy_ = bstack11lll11l11_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1lll1l11_opy_ = bstack1ll1lll1l11_opy_
        self.bstack1ll1ll1l1ll_opy_ = bstack1ll1ll1l1ll_opy_
        self.bstack11ll1lll1_opy_ = bstack11ll1lll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack11l1ll1l1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11lll1llll_opy_(self, meta):
        self.meta = meta
    def bstack11ll1llll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1ll1ll1l111_opy_(self):
        bstack1ll1ll11l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack111llll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᘗ"): bstack1ll1ll11l11_opy_,
            bstack111llll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᘘ"): bstack1ll1ll11l11_opy_,
            bstack111llll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᘙ"): bstack1ll1ll11l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack111llll_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴ࠻ࠢࠥᘚ") + key)
            setattr(self, key, val)
    def bstack1ll1ll1lll1_opy_(self):
        return {
            bstack111llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᘛ"): self.name,
            bstack111llll_opy_ (u"ࠫࡧࡵࡤࡺࠩᘜ"): {
                bstack111llll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᘝ"): bstack111llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᘞ"),
                bstack111llll_opy_ (u"ࠧࡤࡱࡧࡩࠬᘟ"): self.code
            },
            bstack111llll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᘠ"): self.scope,
            bstack111llll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᘡ"): self.tags,
            bstack111llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᘢ"): self.framework,
            bstack111llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᘣ"): self.bstack11lll11l11_opy_
        }
    def bstack1ll1ll1l1l1_opy_(self):
        return {
         bstack111llll_opy_ (u"ࠬࡳࡥࡵࡣࠪᘤ"): self.meta
        }
    def bstack1ll1lll11l1_opy_(self):
        return {
            bstack111llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᘥ"): {
                bstack111llll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᘦ"): self.bstack1ll1lll1l11_opy_
            }
        }
    def bstack1ll1ll111ll_opy_(self, bstack1ll1ll11lll_opy_, details):
        step = next(filter(lambda st: st[bstack111llll_opy_ (u"ࠨ࡫ࡧࠫᘧ")] == bstack1ll1ll11lll_opy_, self.meta[bstack111llll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᘨ")]), None)
        step.update(details)
    def bstack1lll1llll1_opy_(self, bstack1ll1ll11lll_opy_):
        step = next(filter(lambda st: st[bstack111llll_opy_ (u"ࠪ࡭ࡩ࠭ᘩ")] == bstack1ll1ll11lll_opy_, self.meta[bstack111llll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᘪ")]), None)
        step.update({
            bstack111llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᘫ"): bstack1ll1llllll_opy_()
        })
    def bstack11lll11ll1_opy_(self, bstack1ll1ll11lll_opy_, result, duration=None):
        bstack1ll1ll1l1ll_opy_ = bstack1ll1llllll_opy_()
        if bstack1ll1ll11lll_opy_ is not None and self.meta.get(bstack111llll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᘬ")):
            step = next(filter(lambda st: st[bstack111llll_opy_ (u"ࠧࡪࡦࠪᘭ")] == bstack1ll1ll11lll_opy_, self.meta[bstack111llll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᘮ")]), None)
            step.update({
                bstack111llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘯ"): bstack1ll1ll1l1ll_opy_,
                bstack111llll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᘰ"): duration if duration else bstack111l11ll11_opy_(step[bstack111llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᘱ")], bstack1ll1ll1l1ll_opy_),
                bstack111llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᘲ"): result.result,
                bstack111llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᘳ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1ll11l1l_opy_):
        if self.meta.get(bstack111llll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᘴ")):
            self.meta[bstack111llll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᘵ")].append(bstack1ll1ll11l1l_opy_)
        else:
            self.meta[bstack111llll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᘶ")] = [ bstack1ll1ll11l1l_opy_ ]
    def bstack1ll1lll11ll_opy_(self):
        return {
            bstack111llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘷ"): self.bstack11l1ll1l1l_opy_(),
            **self.bstack1ll1ll1lll1_opy_(),
            **self.bstack1ll1ll1l111_opy_(),
            **self.bstack1ll1ll1l1l1_opy_()
        }
    def bstack1ll1lll1l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack111llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘸ"): self.bstack1ll1ll1l1ll_opy_,
            bstack111llll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᘹ"): self.duration,
            bstack111llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘺ"): self.result.result
        }
        if data[bstack111llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘻ")] == bstack111llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᘼ"):
            data[bstack111llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᘽ")] = self.result.bstack11l11ll1l1_opy_()
            data[bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᘾ")] = [{bstack111llll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᘿ"): self.result.bstack1111l1l1l1_opy_()}]
        return data
    def bstack1ll1ll1ll11_opy_(self):
        return {
            bstack111llll_opy_ (u"ࠬࡻࡵࡪࡦࠪᙀ"): self.bstack11l1ll1l1l_opy_(),
            **self.bstack1ll1ll1lll1_opy_(),
            **self.bstack1ll1ll1l111_opy_(),
            **self.bstack1ll1lll1l1l_opy_(),
            **self.bstack1ll1ll1l1l1_opy_()
        }
    def bstack11l1lllll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack111llll_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧᙁ") in event:
            return self.bstack1ll1lll11ll_opy_()
        elif bstack111llll_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᙂ") in event:
            return self.bstack1ll1ll1ll11_opy_()
    def bstack11ll111l11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1ll1l1ll_opy_ = time if time else bstack1ll1llllll_opy_()
        self.duration = duration if duration else bstack111l11ll11_opy_(self.bstack11lll11l11_opy_, self.bstack1ll1ll1l1ll_opy_)
        if result:
            self.result = result
class bstack11llll1l1l_opy_(bstack11ll11111l_opy_):
    def __init__(self, hooks=[], bstack11lll1l1l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11lll1l1l1_opy_ = bstack11lll1l1l1_opy_
        super().__init__(*args, **kwargs, bstack11ll1lll1_opy_=bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᙃ"))
    @classmethod
    def bstack1ll1ll1ll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111llll_opy_ (u"ࠩ࡬ࡨࠬᙄ"): id(step),
                bstack111llll_opy_ (u"ࠪࡸࡪࡾࡴࠨᙅ"): step.name,
                bstack111llll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᙆ"): step.keyword,
            })
        return bstack11llll1l1l_opy_(
            **kwargs,
            meta={
                bstack111llll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᙇ"): {
                    bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙈ"): feature.name,
                    bstack111llll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᙉ"): feature.filename,
                    bstack111llll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᙊ"): feature.description
                },
                bstack111llll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᙋ"): {
                    bstack111llll_opy_ (u"ࠪࡲࡦࡳࡥࠨᙌ"): scenario.name
                },
                bstack111llll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᙍ"): steps,
                bstack111llll_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᙎ"): bstack1lll11l11l1_opy_(test)
            }
        )
    def bstack1ll1lll111l_opy_(self):
        return {
            bstack111llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᙏ"): self.hooks
        }
    def bstack1ll1ll1l11l_opy_(self):
        if self.bstack11lll1l1l1_opy_:
            return {
                bstack111llll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᙐ"): self.bstack11lll1l1l1_opy_
            }
        return {}
    def bstack1ll1ll1ll11_opy_(self):
        return {
            **super().bstack1ll1ll1ll11_opy_(),
            **self.bstack1ll1lll111l_opy_()
        }
    def bstack1ll1lll11ll_opy_(self):
        return {
            **super().bstack1ll1lll11ll_opy_(),
            **self.bstack1ll1ll1l11l_opy_()
        }
    def bstack11ll111l11_opy_(self):
        return bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᙑ")
class bstack11llll1lll_opy_(bstack11ll11111l_opy_):
    def __init__(self, hook_type, *args,bstack11lll1l1l1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1ll11ll1_opy_ = None
        self.bstack11lll1l1l1_opy_ = bstack11lll1l1l1_opy_
        super().__init__(*args, **kwargs, bstack11ll1lll1_opy_=bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᙒ"))
    def bstack11ll1l1l1l_opy_(self):
        return self.hook_type
    def bstack1ll1lll1111_opy_(self):
        return {
            bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᙓ"): self.hook_type
        }
    def bstack1ll1ll1ll11_opy_(self):
        return {
            **super().bstack1ll1ll1ll11_opy_(),
            **self.bstack1ll1lll1111_opy_()
        }
    def bstack1ll1lll11ll_opy_(self):
        return {
            **super().bstack1ll1lll11ll_opy_(),
            bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᙔ"): self.bstack1ll1ll11ll1_opy_,
            **self.bstack1ll1lll1111_opy_()
        }
    def bstack11ll111l11_opy_(self):
        return bstack111llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᙕ")
    def bstack11llll111l_opy_(self, bstack1ll1ll11ll1_opy_):
        self.bstack1ll1ll11ll1_opy_ = bstack1ll1ll11ll1_opy_