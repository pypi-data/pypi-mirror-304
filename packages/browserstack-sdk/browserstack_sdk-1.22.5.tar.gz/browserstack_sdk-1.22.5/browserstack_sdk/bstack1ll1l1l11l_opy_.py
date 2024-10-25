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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11lll1lll1_opy_ import bstack11llll1lll_opy_, bstack11llll1l1l_opy_
from bstack_utils.bstack1lll1ll11_opy_ import bstack1l1lll1111_opy_
from bstack_utils.helper import bstack1llll11l1l_opy_, bstack1ll1llllll_opy_, Result
from bstack_utils.bstack111lll1ll_opy_ import bstack1l11l1lll_opy_
from bstack_utils.capture import bstack11lll1l1ll_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll1l1l11l_opy_:
    def __init__(self):
        self.bstack11lll111l1_opy_ = bstack11lll1l1ll_opy_(self.bstack11llll11l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack11llll11l1_opy_(log):
        if not (log[bstack111llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ෆ")] and log[bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෇")].strip()):
            return
        active = bstack1l1lll1111_opy_.bstack11lll1l111_opy_()
        log = {
            bstack111llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭෈"): log[bstack111llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ෉")],
            bstack111llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴ්ࠬ"): bstack1ll1llllll_opy_(),
            bstack111llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෋"): log[bstack111llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෌")],
        }
        if active:
            if active[bstack111llll_opy_ (u"ࠬࡺࡹࡱࡧࠪ෍")] == bstack111llll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ෎"):
                log[bstack111llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧා")] = active[bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨැ")]
            elif active[bstack111llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧෑ")] == bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࠨි"):
                log[bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫී")] = active[bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬු")]
        bstack1l11l1lll_opy_.bstack11l1l111l_opy_([log])
    def start_test(self, attrs):
        bstack11ll1lllll_opy_ = uuid4().__str__()
        self.tests[bstack11ll1lllll_opy_] = {}
        self.bstack11lll111l1_opy_.start()
        driver = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ෕"), None)
        bstack11lll1lll1_opy_ = bstack11llll1l1l_opy_(
            name=attrs.scenario.name,
            uuid=bstack11ll1lllll_opy_,
            bstack11lll11l11_opy_=bstack1ll1llllll_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111llll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣූ"),
            framework=bstack111llll_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨ෗"),
            scope=[attrs.feature.name],
            bstack11lll1l1l1_opy_=bstack1l11l1lll_opy_.bstack11lll11111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11ll1lllll_opy_][bstack111llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬෘ")] = bstack11lll1lll1_opy_
        threading.current_thread().current_test_uuid = bstack11ll1lllll_opy_
        bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫෙ"), bstack11lll1lll1_opy_)
    def end_test(self, attrs):
        bstack11lll1l11l_opy_ = {
            bstack111llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤේ"): attrs.feature.name,
            bstack111llll_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥෛ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11lll1lll1_opy_ = self.tests[current_test_uuid][bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩො")]
        meta = {
            bstack111llll_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣෝ"): bstack11lll1l11l_opy_,
            bstack111llll_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢෞ"): bstack11lll1lll1_opy_.meta.get(bstack111llll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨෟ"), []),
            bstack111llll_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ෠"): {
                bstack111llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ෡"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11lll1lll1_opy_.bstack11lll1llll_opy_(meta)
        bstack11lll1lll1_opy_.bstack11ll1llll1_opy_(bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ෢"), []))
        bstack11lll111ll_opy_, exception = self._11llll1ll1_opy_(attrs)
        bstack11lll1ll11_opy_ = Result(result=attrs.status.name, exception=exception, bstack11llll1111_opy_=[bstack11lll111ll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෣")].stop(time=bstack1ll1llllll_opy_(), duration=int(attrs.duration)*1000, result=bstack11lll1ll11_opy_)
        bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ෤"), self.tests[threading.current_thread().current_test_uuid][bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ෥")])
    def bstack1lll1llll1_opy_(self, attrs):
        bstack11llll1l11_opy_ = {
            bstack111llll_opy_ (u"ࠩ࡬ࡨࠬ෦"): uuid4().__str__(),
            bstack111llll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ෧"): attrs.keyword,
            bstack111llll_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ෨"): [],
            bstack111llll_opy_ (u"ࠬࡺࡥࡹࡶࠪ෩"): attrs.name,
            bstack111llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ෪"): bstack1ll1llllll_opy_(),
            bstack111llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ෫"): bstack111llll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ෬"),
            bstack111llll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ෭"): bstack111llll_opy_ (u"ࠪࠫ෮")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ෯")].add_step(bstack11llll1l11_opy_)
        threading.current_thread().current_step_uuid = bstack11llll1l11_opy_[bstack111llll_opy_ (u"ࠬ࡯ࡤࠨ෰")]
    def bstack1l11l1111_opy_(self, attrs):
        current_test_id = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ෱"), None)
        current_step_uuid = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫෲ"), None)
        bstack11lll111ll_opy_, exception = self._11llll1ll1_opy_(attrs)
        bstack11lll1ll11_opy_ = Result(result=attrs.status.name, exception=exception, bstack11llll1111_opy_=[bstack11lll111ll_opy_])
        self.tests[current_test_id][bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫෳ")].bstack11lll11ll1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11lll1ll11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l11111l_opy_(self, name, attrs):
        try:
            bstack11lll1ll1l_opy_ = uuid4().__str__()
            self.tests[bstack11lll1ll1l_opy_] = {}
            self.bstack11lll111l1_opy_.start()
            scopes = []
            driver = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ෴"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ෵")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11lll1ll1l_opy_)
            if name in [bstack111llll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ෶"), bstack111llll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ෷")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ෸"), bstack111llll_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ෹")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack111llll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ෺")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11llll1lll_opy_(
                name=name,
                uuid=bstack11lll1ll1l_opy_,
                bstack11lll11l11_opy_=bstack1ll1llllll_opy_(),
                file_path=file_path,
                framework=bstack111llll_opy_ (u"ࠤࡅࡩ࡭ࡧࡶࡦࠤ෻"),
                bstack11lll1l1l1_opy_=bstack1l11l1lll_opy_.bstack11lll11111_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack111llll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ෼"),
                hook_type=name
            )
            self.tests[bstack11lll1ll1l_opy_][bstack111llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠢ෽")] = hook_data
            current_test_id = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤ෾"), None)
            if current_test_id:
                hook_data.bstack11llll111l_opy_(current_test_id)
            if name == bstack111llll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ෿"):
                threading.current_thread().before_all_hook_uuid = bstack11lll1ll1l_opy_
            threading.current_thread().current_hook_uuid = bstack11lll1ll1l_opy_
            bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠢࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠣ฀"), hook_data)
        except Exception as e:
            logger.debug(bstack111llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤ࡭ࡵ࡯࡬ࠢࡨࡺࡪࡴࡴࡴ࠮ࠣ࡬ࡴࡵ࡫ࠡࡰࡤࡱࡪࡀࠠࠦࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠪࡹࠢก"), name, e)
    def bstack1l1l11llll_opy_(self, attrs):
        bstack11lll1111l_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ข"), None)
        hook_data = self.tests[bstack11lll1111l_opy_][bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ฃ")]
        status = bstack111llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦค")
        exception = None
        bstack11lll111ll_opy_ = None
        if hook_data.name == bstack111llll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣฅ"):
            self.bstack11lll111l1_opy_.reset()
            bstack11lll11l1l_opy_ = self.tests[bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ฆ"), None)][bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪง")].result.result
            if bstack11lll11l1l_opy_ == bstack111llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣจ"):
                if attrs.hook_failures == 1:
                    status = bstack111llll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤฉ")
                elif attrs.hook_failures == 2:
                    status = bstack111llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥช")
            elif attrs.bstack11lll11lll_opy_:
                status = bstack111llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦซ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩฌ") and attrs.hook_failures == 1:
                status = bstack111llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨญ")
            elif hasattr(attrs, bstack111llll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧฎ")) and attrs.error_message:
                status = bstack111llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣฏ")
            bstack11lll111ll_opy_, exception = self._11llll1ll1_opy_(attrs)
        bstack11lll1ll11_opy_ = Result(result=status, exception=exception, bstack11llll1111_opy_=[bstack11lll111ll_opy_])
        hook_data.stop(time=bstack1ll1llllll_opy_(), duration=0, result=bstack11lll1ll11_opy_)
        bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫฐ"), self.tests[bstack11lll1111l_opy_][bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ฑ")])
        threading.current_thread().current_hook_uuid = None
    def _11llll1ll1_opy_(self, attrs):
        try:
            import traceback
            bstack11ll111l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11lll111ll_opy_ = bstack11ll111l_opy_[-1] if bstack11ll111l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣฒ"))
            bstack11lll111ll_opy_ = None
            exception = None
        return bstack11lll111ll_opy_, exception