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
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack111llll1_opy_, bstack111l1l1ll_opy_, update, bstack1ll1llll1_opy_,
                                       bstack1111l11ll_opy_, bstack1ll11111l1_opy_, bstack11ll1l1ll_opy_, bstack1ll11lllll_opy_,
                                       bstack11ll11111_opy_, bstack1l11llll_opy_, bstack11l1l1l1_opy_, bstack1l11l11111_opy_,
                                       bstack11lll1lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11l1ll11_opy_)
from browserstack_sdk.bstack1l11lll1ll_opy_ import bstack1l111ll11l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1l1ll11_opy_
from bstack_utils.capture import bstack11lll1l1ll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1lll111l_opy_, bstack1l1l1l11l_opy_, bstack1llll1l1_opy_, \
    bstack111l11l1_opy_
from bstack_utils.helper import bstack1llll11l1l_opy_, bstack1111l11lll_opy_, bstack11l1ll11l1_opy_, bstack1ll1ll1l11_opy_, bstack1111llll11_opy_, bstack1ll1llllll_opy_, \
    bstack111111l11l_opy_, \
    bstack1111l1l11l_opy_, bstack1lll111l1_opy_, bstack1llll1ll1l_opy_, bstack1111lll1l1_opy_, bstack1ll11lll1l_opy_, Notset, \
    bstack1ll1ll1lll_opy_, bstack111l11ll11_opy_, bstack1111lll111_opy_, Result, bstack1111ll111l_opy_, bstack1111ll1ll1_opy_, bstack11ll1ll111_opy_, \
    bstack1l1l1l1ll_opy_, bstack1ll1lllll1_opy_, bstack1l11ll1lll_opy_, bstack1111l11l1l_opy_
from bstack_utils.bstack1lllllllll1_opy_ import bstack1llllll1lll_opy_
from bstack_utils.messages import bstack1l1l111ll_opy_, bstack1l1l1111l1_opy_, bstack111llll11_opy_, bstack1l1l1ll11l_opy_, bstack1l11llllll_opy_, \
    bstack11l1111l1_opy_, bstack1lll11l1ll_opy_, bstack1lll1111ll_opy_, bstack1111ll1ll_opy_, bstack1llllll1l_opy_, \
    bstack1lll11l1l_opy_, bstack1l11ll11ll_opy_
from bstack_utils.proxy import bstack1ll11lll11_opy_, bstack1l1l11ll1l_opy_
from bstack_utils.bstack1l11ll1111_opy_ import bstack1lll11l11ll_opy_, bstack1lll11l1lll_opy_, bstack1lll111llll_opy_, bstack1lll11l1l1l_opy_, \
    bstack1lll11l111l_opy_, bstack1lll11l1ll1_opy_, bstack1lll11l1l11_opy_, bstack1llllllll1_opy_, bstack1lll111l1ll_opy_
from bstack_utils.bstack1l11111l1l_opy_ import bstack1lll1l1ll1_opy_
from bstack_utils.bstack1l1l111111_opy_ import bstack111l1ll1l_opy_, bstack1l1lllllll_opy_, bstack11llllllll_opy_, \
    bstack1l1l1lll_opy_, bstack1l1l11ll_opy_
from bstack_utils.bstack11lll1lll1_opy_ import bstack11llll1l1l_opy_
from bstack_utils.bstack1lll1ll11_opy_ import bstack1l1lll1111_opy_
import bstack_utils.bstack1lll111l11_opy_ as bstack1l1111ll_opy_
from bstack_utils.bstack111lll1ll_opy_ import bstack1l11l1lll_opy_
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1l111l_opy_
bstack1l1l1l11_opy_ = None
bstack11lll11ll_opy_ = None
bstack1lll11ll1l_opy_ = None
bstack1l11l111l_opy_ = None
bstack11l11111l_opy_ = None
bstack1l1l11l11l_opy_ = None
bstack1l1lll11l1_opy_ = None
bstack1l1ll1l1_opy_ = None
bstack1l1lll1l1_opy_ = None
bstack1l11lll1l1_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack1ll1ll11l1_opy_ = None
bstack1l11l1l11_opy_ = None
bstack11lll111l_opy_ = bstack111llll_opy_ (u"ࠫࠬឝ")
CONFIG = {}
bstack11l1l1l1l_opy_ = False
bstack11l111lll_opy_ = bstack111llll_opy_ (u"ࠬ࠭ឞ")
bstack1l1lll1l_opy_ = bstack111llll_opy_ (u"࠭ࠧស")
bstack1lll1l1l11_opy_ = False
bstack1l1111111l_opy_ = []
bstack1llll111_opy_ = bstack1l1lll111l_opy_
bstack1ll111lll1l_opy_ = bstack111llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧហ")
bstack1llll1l11_opy_ = {}
bstack11ll11lll_opy_ = False
logger = bstack1ll1l1ll11_opy_.get_logger(__name__, bstack1llll111_opy_)
store = {
    bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬឡ"): []
}
bstack1ll11l1llll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11ll11ll1l_opy_ = {}
current_test_uuid = None
def bstack111ll111l_opy_(page, bstack1l11111ll_opy_):
    try:
        page.evaluate(bstack111llll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥអ"),
                      bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧឣ") + json.dumps(
                          bstack1l11111ll_opy_) + bstack111llll_opy_ (u"ࠦࢂࢃࠢឤ"))
    except Exception as e:
        print(bstack111llll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥឥ"), e)
def bstack1ll1l11111_opy_(page, message, level):
    try:
        page.evaluate(bstack111llll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢឦ"), bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬឧ") + json.dumps(
            message) + bstack111llll_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫឨ") + json.dumps(level) + bstack111llll_opy_ (u"ࠩࢀࢁࠬឩ"))
    except Exception as e:
        print(bstack111llll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨឪ"), e)
def pytest_configure(config):
    bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
    config.args = bstack1l1lll1111_opy_.bstack1ll11lll111_opy_(config.args)
    bstack1l111l11ll_opy_.bstack1lll1l1lll_opy_(bstack1l11ll1lll_opy_(config.getoption(bstack111llll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨឫ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll11l11lll_opy_ = item.config.getoption(bstack111llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឬ"))
    plugins = item.config.getoption(bstack111llll_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢឭ"))
    report = outcome.get_result()
    bstack1ll11l1111l_opy_(item, call, report)
    if bstack111llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧឮ") not in plugins or bstack1ll11lll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack111llll_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤឯ"), None)
    page = getattr(item, bstack111llll_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣឰ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll111lllll_opy_(item, report, summary, bstack1ll11l11lll_opy_)
    if (page is not None):
        bstack1ll11l111ll_opy_(item, report, summary, bstack1ll11l11lll_opy_)
def bstack1ll111lllll_opy_(item, report, summary, bstack1ll11l11lll_opy_):
    if report.when == bstack111llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩឱ") and report.skipped:
        bstack1lll111l1ll_opy_(report)
    if report.when in [bstack111llll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥឲ"), bstack111llll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢឳ")]:
        return
    if not bstack1111llll11_opy_():
        return
    try:
        if (str(bstack1ll11l11lll_opy_).lower() != bstack111llll_opy_ (u"࠭ࡴࡳࡷࡨࠫ឴")):
            item._driver.execute_script(
                bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ឵") + json.dumps(
                    report.nodeid) + bstack111llll_opy_ (u"ࠨࡿࢀࠫា"))
        os.environ[bstack111llll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬិ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111llll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥី").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111llll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨឹ")))
    bstack11lll11l1_opy_ = bstack111llll_opy_ (u"ࠧࠨឺ")
    bstack1lll111l1ll_opy_(report)
    if not passed:
        try:
            bstack11lll11l1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111llll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨុ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11lll11l1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111llll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤូ")))
        bstack11lll11l1_opy_ = bstack111llll_opy_ (u"ࠣࠤួ")
        if not passed:
            try:
                bstack11lll11l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111llll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤើ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11lll11l1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧឿ")
                    + json.dumps(bstack111llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧៀ"))
                    + bstack111llll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣេ")
                )
            else:
                item._driver.execute_script(
                    bstack111llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫែ")
                    + json.dumps(str(bstack11lll11l1_opy_))
                    + bstack111llll_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥៃ")
                )
        except Exception as e:
            summary.append(bstack111llll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨោ").format(e))
def bstack1ll111l1l11_opy_(test_name, error_message):
    try:
        bstack1ll11l1ll1l_opy_ = []
        bstack1lll1l1ll_opy_ = os.environ.get(bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩៅ"), bstack111llll_opy_ (u"ࠪ࠴ࠬំ"))
        bstack1ll1ll11l_opy_ = {bstack111llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩះ"): test_name, bstack111llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫៈ"): error_message, bstack111llll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ៉"): bstack1lll1l1ll_opy_}
        bstack1ll111l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111llll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ៊"))
        if os.path.exists(bstack1ll111l1ll1_opy_):
            with open(bstack1ll111l1ll1_opy_) as f:
                bstack1ll11l1ll1l_opy_ = json.load(f)
        bstack1ll11l1ll1l_opy_.append(bstack1ll1ll11l_opy_)
        with open(bstack1ll111l1ll1_opy_, bstack111llll_opy_ (u"ࠨࡹࠪ់")) as f:
            json.dump(bstack1ll11l1ll1l_opy_, f)
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ៌") + str(e))
def bstack1ll11l111ll_opy_(item, report, summary, bstack1ll11l11lll_opy_):
    if report.when in [bstack111llll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ៍"), bstack111llll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ៎")]:
        return
    if (str(bstack1ll11l11lll_opy_).lower() != bstack111llll_opy_ (u"ࠬࡺࡲࡶࡧࠪ៏")):
        bstack111ll111l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111llll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ័")))
    bstack11lll11l1_opy_ = bstack111llll_opy_ (u"ࠢࠣ៑")
    bstack1lll111l1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11lll11l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111llll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽ្ࠣ").format(e)
                )
        try:
            if passed:
                bstack1l1l11ll_opy_(getattr(item, bstack111llll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ៓"), None), bstack111llll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ។"))
            else:
                error_message = bstack111llll_opy_ (u"ࠫࠬ៕")
                if bstack11lll11l1_opy_:
                    bstack1ll1l11111_opy_(item._page, str(bstack11lll11l1_opy_), bstack111llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ៖"))
                    bstack1l1l11ll_opy_(getattr(item, bstack111llll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬៗ"), None), bstack111llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ៘"), str(bstack11lll11l1_opy_))
                    error_message = str(bstack11lll11l1_opy_)
                else:
                    bstack1l1l11ll_opy_(getattr(item, bstack111llll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ៙"), None), bstack111llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ៚"))
                bstack1ll111l1l11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111llll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ៛").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack111llll_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣៜ"), default=bstack111llll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ៝"), help=bstack111llll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ៞"))
    parser.addoption(bstack111llll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ៟"), default=bstack111llll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ០"), help=bstack111llll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ១"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111llll_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ២"), action=bstack111llll_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ៣"), default=bstack111llll_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ៤"),
                         help=bstack111llll_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ៥"))
def bstack11llll11l1_opy_(log):
    if not (log[bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៦")] and log[bstack111llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ៧")].strip()):
        return
    active = bstack11lll1l111_opy_()
    log = {
        bstack111llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ៨"): log[bstack111llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ៩")],
        bstack111llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ៪"): bstack11l1ll11l1_opy_().isoformat() + bstack111llll_opy_ (u"ࠬࡠࠧ៫"),
        bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ៬"): log[bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៭")],
    }
    if active:
        if active[bstack111llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭៮")] == bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ៯"):
            log[bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៰")] = active[bstack111llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៱")]
        elif active[bstack111llll_opy_ (u"ࠬࡺࡹࡱࡧࠪ៲")] == bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࠫ៳"):
            log[bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៴")] = active[bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៵")]
    bstack1l11l1lll_opy_.bstack11l1l111l_opy_([log])
def bstack11lll1l111_opy_():
    if len(store[bstack111llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭៶")]) > 0 and store[bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ៷")][-1]:
        return {
            bstack111llll_opy_ (u"ࠫࡹࡿࡰࡦࠩ៸"): bstack111llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ៹"),
            bstack111llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭៺"): store[bstack111llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ៻")][-1]
        }
    if store.get(bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ៼"), None):
        return {
            bstack111llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ៽"): bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࠨ៾"),
            bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៿"): store[bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ᠀")]
        }
    return None
bstack11lll111l1_opy_ = bstack11lll1l1ll_opy_(bstack11llll11l1_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        item._1ll11ll1111_opy_ = True
        bstack1l111ll1l_opy_ = bstack1l1111ll_opy_.bstack11111ll1_opy_(bstack1111l1l11l_opy_(item.own_markers))
        item._a11y_test_case = bstack1l111ll1l_opy_
        if bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᠁"), None):
            driver = getattr(item, bstack111llll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᠂"), None)
            item._a11y_started = bstack1l1111ll_opy_.bstack11llllll11_opy_(driver, bstack1l111ll1l_opy_)
        if not bstack1l11l1lll_opy_.on() or bstack1ll111lll1l_opy_ != bstack111llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᠃"):
            return
        global current_test_uuid, bstack11lll111l1_opy_
        bstack11lll111l1_opy_.start()
        bstack11l1llll11_opy_ = {
            bstack111llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᠄"): uuid4().__str__(),
            bstack111llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᠅"): bstack11l1ll11l1_opy_().isoformat() + bstack111llll_opy_ (u"ࠫ࡟࠭᠆")
        }
        current_test_uuid = bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᠇")]
        store[bstack111llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ᠈")] = bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᠉")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11ll11ll1l_opy_[item.nodeid] = {**_11ll11ll1l_opy_[item.nodeid], **bstack11l1llll11_opy_}
        bstack1ll11l1l1ll_opy_(item, _11ll11ll1l_opy_[item.nodeid], bstack111llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ᠊"))
    except Exception as err:
        print(bstack111llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫ᠋"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll11l1llll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111lll1l1_opy_():
        atexit.register(bstack1l11ll11l_opy_)
        if not bstack1ll11l1llll_opy_:
            try:
                bstack1ll111l1l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1111l11l1l_opy_():
                    bstack1ll111l1l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll111l1l1l_opy_:
                    signal.signal(s, bstack1ll111ll1l1_opy_)
                bstack1ll11l1llll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦ᠌") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll11l11ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᠍")
    try:
        if not bstack1l11l1lll_opy_.on():
            return
        bstack11lll111l1_opy_.start()
        uuid = uuid4().__str__()
        bstack11l1llll11_opy_ = {
            bstack111llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᠎"): uuid,
            bstack111llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᠏"): bstack11l1ll11l1_opy_().isoformat() + bstack111llll_opy_ (u"࡛ࠧࠩ᠐"),
            bstack111llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭᠑"): bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᠒"),
            bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭᠓"): bstack111llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ᠔"),
            bstack111llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ᠕"): bstack111llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ᠖")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack111llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᠗")] = item
        store[bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ᠘")] = [uuid]
        if not _11ll11ll1l_opy_.get(item.nodeid, None):
            _11ll11ll1l_opy_[item.nodeid] = {bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᠙"): [], bstack111llll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ᠚"): []}
        _11ll11ll1l_opy_[item.nodeid][bstack111llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᠛")].append(bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ᠜")])
        _11ll11ll1l_opy_[item.nodeid + bstack111llll_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭᠝")] = bstack11l1llll11_opy_
        bstack1ll111l1lll_opy_(item, bstack11l1llll11_opy_, bstack111llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᠞"))
    except Exception as err:
        print(bstack111llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ᠟"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1llll1l11_opy_
        bstack1lll1l1ll_opy_ = 0
        if bstack1lll1l1l11_opy_ is True:
            bstack1lll1l1ll_opy_ = int(os.environ.get(bstack111llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᠠ")))
        if bstack111llllll_opy_.bstack1llll111l_opy_() == bstack111llll_opy_ (u"ࠥࡸࡷࡻࡥࠣᠡ"):
            if bstack111llllll_opy_.bstack1111111l1_opy_() == bstack111llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᠢ"):
                bstack1ll11l11ll1_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᠣ"), None)
                bstack1lll1l1l1l_opy_ = bstack1ll11l11ll1_opy_ + bstack111llll_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤᠤ")
                driver = getattr(item, bstack111llll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᠥ"), None)
                bstack1l1l11l1_opy_ = getattr(item, bstack111llll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᠦ"), None)
                bstack111lll11_opy_ = getattr(item, bstack111llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᠧ"), None)
                PercySDK.screenshot(driver, bstack1lll1l1l1l_opy_, bstack1l1l11l1_opy_=bstack1l1l11l1_opy_, bstack111lll11_opy_=bstack111lll11_opy_, bstack1ll1ll11_opy_=bstack1lll1l1ll_opy_)
        if getattr(item, bstack111llll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪᠨ"), False):
            bstack1l111ll11l_opy_.bstack1ll111ll11_opy_(getattr(item, bstack111llll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᠩ"), None), bstack1llll1l11_opy_, logger, item)
        if not bstack1l11l1lll_opy_.on():
            return
        bstack11l1llll11_opy_ = {
            bstack111llll_opy_ (u"ࠬࡻࡵࡪࡦࠪᠪ"): uuid4().__str__(),
            bstack111llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᠫ"): bstack11l1ll11l1_opy_().isoformat() + bstack111llll_opy_ (u"࡛ࠧࠩᠬ"),
            bstack111llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᠭ"): bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᠮ"),
            bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᠯ"): bstack111llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᠰ"),
            bstack111llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᠱ"): bstack111llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᠲ")
        }
        _11ll11ll1l_opy_[item.nodeid + bstack111llll_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᠳ")] = bstack11l1llll11_opy_
        bstack1ll111l1lll_opy_(item, bstack11l1llll11_opy_, bstack111llll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᠴ"))
    except Exception as err:
        print(bstack111llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨᠵ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l11l1lll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lll11l1l1l_opy_(fixturedef.argname):
        store[bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᠶ")] = request.node
    elif bstack1lll11l111l_opy_(fixturedef.argname):
        store[bstack111llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᠷ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack111llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᠸ"): fixturedef.argname,
            bstack111llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᠹ"): bstack111111l11l_opy_(outcome),
            bstack111llll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᠺ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᠻ")]
        if not _11ll11ll1l_opy_.get(current_test_item.nodeid, None):
            _11ll11ll1l_opy_[current_test_item.nodeid] = {bstack111llll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᠼ"): []}
        _11ll11ll1l_opy_[current_test_item.nodeid][bstack111llll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᠽ")].append(fixture)
    except Exception as err:
        logger.debug(bstack111llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᠾ"), str(err))
if bstack1ll11lll1l_opy_() and bstack1l11l1lll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11ll11ll1l_opy_[request.node.nodeid][bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᠿ")].bstack1lll1llll1_opy_(id(step))
        except Exception as err:
            print(bstack111llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫᡀ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11ll11ll1l_opy_[request.node.nodeid][bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᡁ")].bstack11lll11ll1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᡂ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11lll1lll1_opy_: bstack11llll1l1l_opy_ = _11ll11ll1l_opy_[request.node.nodeid][bstack111llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᡃ")]
            bstack11lll1lll1_opy_.bstack11lll11ll1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᡄ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111lll1l_opy_
        try:
            if not bstack1l11l1lll_opy_.on() or bstack1ll111lll1l_opy_ != bstack111llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᡅ"):
                return
            global bstack11lll111l1_opy_
            bstack11lll111l1_opy_.start()
            driver = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᡆ"), None)
            if not _11ll11ll1l_opy_.get(request.node.nodeid, None):
                _11ll11ll1l_opy_[request.node.nodeid] = {}
            bstack11lll1lll1_opy_ = bstack11llll1l1l_opy_.bstack1ll1ll1ll1l_opy_(
                scenario, feature, request.node,
                name=bstack1lll11l1ll1_opy_(request.node, scenario),
                bstack11lll11l11_opy_=bstack1ll1llllll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111llll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᡇ"),
                tags=bstack1lll11l1l11_opy_(feature, scenario),
                bstack11lll1l1l1_opy_=bstack1l11l1lll_opy_.bstack11lll11111_opy_(driver) if driver and driver.session_id else {}
            )
            _11ll11ll1l_opy_[request.node.nodeid][bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᡈ")] = bstack11lll1lll1_opy_
            bstack1ll11l1l111_opy_(bstack11lll1lll1_opy_.uuid)
            bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᡉ"), bstack11lll1lll1_opy_)
        except Exception as err:
            print(bstack111llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫᡊ"), str(err))
def bstack1ll11l1lll1_opy_(bstack11lll1ll1l_opy_):
    if bstack11lll1ll1l_opy_ in store[bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᡋ")]:
        store[bstack111llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᡌ")].remove(bstack11lll1ll1l_opy_)
def bstack1ll11l1l111_opy_(bstack11ll1lllll_opy_):
    store[bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᡍ")] = bstack11ll1lllll_opy_
    threading.current_thread().current_test_uuid = bstack11ll1lllll_opy_
@bstack1l11l1lll_opy_.bstack1ll1l1lllll_opy_
def bstack1ll11l1111l_opy_(item, call, report):
    global bstack1ll111lll1l_opy_
    bstack1l11111ll1_opy_ = bstack1ll1llllll_opy_()
    if hasattr(report, bstack111llll_opy_ (u"࠭ࡳࡵࡱࡳࠫᡎ")):
        bstack1l11111ll1_opy_ = bstack1111ll111l_opy_(report.stop)
    elif hasattr(report, bstack111llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭ᡏ")):
        bstack1l11111ll1_opy_ = bstack1111ll111l_opy_(report.start)
    try:
        if getattr(report, bstack111llll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᡐ"), bstack111llll_opy_ (u"ࠩࠪᡑ")) == bstack111llll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᡒ"):
            bstack11lll111l1_opy_.reset()
        if getattr(report, bstack111llll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᡓ"), bstack111llll_opy_ (u"ࠬ࠭ᡔ")) == bstack111llll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᡕ"):
            if bstack1ll111lll1l_opy_ == bstack111llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᡖ"):
                _11ll11ll1l_opy_[item.nodeid][bstack111llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᡗ")] = bstack1l11111ll1_opy_
                bstack1ll11l1l1ll_opy_(item, _11ll11ll1l_opy_[item.nodeid], bstack111llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᡘ"), report, call)
                store[bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᡙ")] = None
            elif bstack1ll111lll1l_opy_ == bstack111llll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᡚ"):
                bstack11lll1lll1_opy_ = _11ll11ll1l_opy_[item.nodeid][bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᡛ")]
                bstack11lll1lll1_opy_.set(hooks=_11ll11ll1l_opy_[item.nodeid].get(bstack111llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᡜ"), []))
                exception, bstack11llll1111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11llll1111_opy_ = [call.excinfo.exconly(), getattr(report, bstack111llll_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭ᡝ"), bstack111llll_opy_ (u"ࠨࠩᡞ"))]
                bstack11lll1lll1_opy_.stop(time=bstack1l11111ll1_opy_, result=Result(result=getattr(report, bstack111llll_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᡟ"), bstack111llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᡠ")), exception=exception, bstack11llll1111_opy_=bstack11llll1111_opy_))
                bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᡡ"), _11ll11ll1l_opy_[item.nodeid][bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᡢ")])
        elif getattr(report, bstack111llll_opy_ (u"࠭ࡷࡩࡧࡱࠫᡣ"), bstack111llll_opy_ (u"ࠧࠨᡤ")) in [bstack111llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᡥ"), bstack111llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᡦ")]:
            bstack11lll1111l_opy_ = item.nodeid + bstack111llll_opy_ (u"ࠪ࠱ࠬᡧ") + getattr(report, bstack111llll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᡨ"), bstack111llll_opy_ (u"ࠬ࠭ᡩ"))
            if getattr(report, bstack111llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᡪ"), False):
                hook_type = bstack111llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᡫ") if getattr(report, bstack111llll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᡬ"), bstack111llll_opy_ (u"ࠩࠪᡭ")) == bstack111llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᡮ") else bstack111llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᡯ")
                _11ll11ll1l_opy_[bstack11lll1111l_opy_] = {
                    bstack111llll_opy_ (u"ࠬࡻࡵࡪࡦࠪᡰ"): uuid4().__str__(),
                    bstack111llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᡱ"): bstack1l11111ll1_opy_,
                    bstack111llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᡲ"): hook_type
                }
            _11ll11ll1l_opy_[bstack11lll1111l_opy_][bstack111llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᡳ")] = bstack1l11111ll1_opy_
            bstack1ll11l1lll1_opy_(_11ll11ll1l_opy_[bstack11lll1111l_opy_][bstack111llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᡴ")])
            bstack1ll111l1lll_opy_(item, _11ll11ll1l_opy_[bstack11lll1111l_opy_], bstack111llll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᡵ"), report, call)
            if getattr(report, bstack111llll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᡶ"), bstack111llll_opy_ (u"ࠬ࠭ᡷ")) == bstack111llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᡸ"):
                if getattr(report, bstack111llll_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ᡹"), bstack111llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᡺")) == bstack111llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᡻"):
                    bstack11l1llll11_opy_ = {
                        bstack111llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᡼"): uuid4().__str__(),
                        bstack111llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᡽"): bstack1ll1llllll_opy_(),
                        bstack111llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᡾"): bstack1ll1llllll_opy_()
                    }
                    _11ll11ll1l_opy_[item.nodeid] = {**_11ll11ll1l_opy_[item.nodeid], **bstack11l1llll11_opy_}
                    bstack1ll11l1l1ll_opy_(item, _11ll11ll1l_opy_[item.nodeid], bstack111llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ᡿"))
                    bstack1ll11l1l1ll_opy_(item, _11ll11ll1l_opy_[item.nodeid], bstack111llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᢀ"), report, call)
    except Exception as err:
        print(bstack111llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭ᢁ"), str(err))
def bstack1ll111ll111_opy_(test, bstack11l1llll11_opy_, result=None, call=None, bstack11ll1lll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11lll1lll1_opy_ = {
        bstack111llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢂ"): bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᢃ")],
        bstack111llll_opy_ (u"ࠫࡹࡿࡰࡦࠩᢄ"): bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࠪᢅ"),
        bstack111llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᢆ"): test.name,
        bstack111llll_opy_ (u"ࠧࡣࡱࡧࡽࠬᢇ"): {
            bstack111llll_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᢈ"): bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᢉ"),
            bstack111llll_opy_ (u"ࠪࡧࡴࡪࡥࠨᢊ"): inspect.getsource(test.obj)
        },
        bstack111llll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᢋ"): test.name,
        bstack111llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᢌ"): test.name,
        bstack111llll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᢍ"): bstack1l1lll1111_opy_.bstack11ll111l1l_opy_(test),
        bstack111llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᢎ"): file_path,
        bstack111llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᢏ"): file_path,
        bstack111llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᢐ"): bstack111llll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᢑ"),
        bstack111llll_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᢒ"): file_path,
        bstack111llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᢓ"): bstack11l1llll11_opy_[bstack111llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᢔ")],
        bstack111llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᢕ"): bstack111llll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᢖ"),
        bstack111llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᢗ"): {
            bstack111llll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᢘ"): test.nodeid
        },
        bstack111llll_opy_ (u"ࠫࡹࡧࡧࡴࠩᢙ"): bstack1111l1l11l_opy_(test.own_markers)
    }
    if bstack11ll1lll1_opy_ in [bstack111llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᢚ"), bstack111llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᢛ")]:
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᢜ")] = {
            bstack111llll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᢝ"): bstack11l1llll11_opy_.get(bstack111llll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᢞ"), [])
        }
    if bstack11ll1lll1_opy_ == bstack111llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᢟ"):
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᢠ")] = bstack111llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᢡ")
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᢢ")] = bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢣ")]
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᢤ")] = bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᢥ")]
    if result:
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢦ")] = result.outcome
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᢧ")] = result.duration * 1000
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢨ")] = bstack11l1llll11_opy_[bstack111llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷᢩࠫ")]
        if result.failed:
            bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᢪ")] = bstack1l11l1lll_opy_.bstack11l11ll1l1_opy_(call.excinfo.typename)
            bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ᢫")] = bstack1l11l1lll_opy_.bstack1ll1l1l11ll_opy_(call.excinfo, result)
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᢬")] = bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᢭")]
    if outcome:
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᢮")] = bstack111111l11l_opy_(outcome)
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭᢯")] = 0
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᢰ")] = bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᢱ")]
        if bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᢲ")] == bstack111llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᢳ"):
            bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᢴ")] = bstack111llll_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬᢵ")  # bstack1ll111lll11_opy_
            bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᢶ")] = [{bstack111llll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᢷ"): [bstack111llll_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫᢸ")]}]
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᢹ")] = bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᢺ")]
    return bstack11lll1lll1_opy_
def bstack1ll111ll11l_opy_(test, bstack11ll1lll11_opy_, bstack11ll1lll1_opy_, result, call, outcome, bstack1ll11l1ll11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᢻ")]
    hook_name = bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᢼ")]
    hook_data = {
        bstack111llll_opy_ (u"ࠬࡻࡵࡪࡦࠪᢽ"): bstack11ll1lll11_opy_[bstack111llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᢾ")],
        bstack111llll_opy_ (u"ࠧࡵࡻࡳࡩࠬᢿ"): bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᣀ"),
        bstack111llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᣁ"): bstack111llll_opy_ (u"ࠪࡿࢂ࠭ᣂ").format(bstack1lll11l1lll_opy_(hook_name)),
        bstack111llll_opy_ (u"ࠫࡧࡵࡤࡺࠩᣃ"): {
            bstack111llll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᣄ"): bstack111llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᣅ"),
            bstack111llll_opy_ (u"ࠧࡤࡱࡧࡩࠬᣆ"): None
        },
        bstack111llll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧᣇ"): test.name,
        bstack111llll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᣈ"): bstack1l1lll1111_opy_.bstack11ll111l1l_opy_(test, hook_name),
        bstack111llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᣉ"): file_path,
        bstack111llll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᣊ"): file_path,
        bstack111llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᣋ"): bstack111llll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᣌ"),
        bstack111llll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᣍ"): file_path,
        bstack111llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᣎ"): bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᣏ")],
        bstack111llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᣐ"): bstack111llll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ᣑ") if bstack1ll111lll1l_opy_ == bstack111llll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᣒ") else bstack111llll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᣓ"),
        bstack111llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᣔ"): hook_type
    }
    bstack1ll1ll11ll1_opy_ = bstack11ll1ll1l1_opy_(_11ll11ll1l_opy_.get(test.nodeid, None))
    if bstack1ll1ll11ll1_opy_:
        hook_data[bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭ᣕ")] = bstack1ll1ll11ll1_opy_
    if result:
        hook_data[bstack111llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᣖ")] = result.outcome
        hook_data[bstack111llll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᣗ")] = result.duration * 1000
        hook_data[bstack111llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᣘ")] = bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᣙ")]
        if result.failed:
            hook_data[bstack111llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᣚ")] = bstack1l11l1lll_opy_.bstack11l11ll1l1_opy_(call.excinfo.typename)
            hook_data[bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᣛ")] = bstack1l11l1lll_opy_.bstack1ll1l1l11ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣜ")] = bstack111111l11l_opy_(outcome)
        hook_data[bstack111llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᣝ")] = 100
        hook_data[bstack111llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣞ")] = bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᣟ")]
        if hook_data[bstack111llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᣠ")] == bstack111llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᣡ"):
            hook_data[bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᣢ")] = bstack111llll_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩᣣ")  # bstack1ll111lll11_opy_
            hook_data[bstack111llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᣤ")] = [{bstack111llll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᣥ"): [bstack111llll_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨᣦ")]}]
    if bstack1ll11l1ll11_opy_:
        hook_data[bstack111llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᣧ")] = bstack1ll11l1ll11_opy_.result
        hook_data[bstack111llll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᣨ")] = bstack111l11ll11_opy_(bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᣩ")], bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣪ")])
        hook_data[bstack111llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣫ")] = bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣬ")]
        if hook_data[bstack111llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣭ")] == bstack111llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᣮ"):
            hook_data[bstack111llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᣯ")] = bstack1l11l1lll_opy_.bstack11l11ll1l1_opy_(bstack1ll11l1ll11_opy_.exception_type)
            hook_data[bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᣰ")] = [{bstack111llll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᣱ"): bstack1111lll111_opy_(bstack1ll11l1ll11_opy_.exception)}]
    return hook_data
def bstack1ll11l1l1ll_opy_(test, bstack11l1llll11_opy_, bstack11ll1lll1_opy_, result=None, call=None, outcome=None):
    bstack11lll1lll1_opy_ = bstack1ll111ll111_opy_(test, bstack11l1llll11_opy_, result, call, bstack11ll1lll1_opy_, outcome)
    driver = getattr(test, bstack111llll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᣲ"), None)
    if bstack11ll1lll1_opy_ == bstack111llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᣳ") and driver:
        bstack11lll1lll1_opy_[bstack111llll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᣴ")] = bstack1l11l1lll_opy_.bstack11lll11111_opy_(driver)
    if bstack11ll1lll1_opy_ == bstack111llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᣵ"):
        bstack11ll1lll1_opy_ = bstack111llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ᣶")
    bstack11ll11lll1_opy_ = {
        bstack111llll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ᣷"): bstack11ll1lll1_opy_,
        bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ᣸"): bstack11lll1lll1_opy_
    }
    bstack1l11l1lll_opy_.bstack11ll1l1111_opy_(bstack11ll11lll1_opy_)
def bstack1ll111l1lll_opy_(test, bstack11l1llll11_opy_, bstack11ll1lll1_opy_, result=None, call=None, outcome=None, bstack1ll11l1ll11_opy_=None):
    hook_data = bstack1ll111ll11l_opy_(test, bstack11l1llll11_opy_, bstack11ll1lll1_opy_, result, call, outcome, bstack1ll11l1ll11_opy_)
    bstack11ll11lll1_opy_ = {
        bstack111llll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᣹"): bstack11ll1lll1_opy_,
        bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ᣺"): hook_data
    }
    bstack1l11l1lll_opy_.bstack11ll1l1111_opy_(bstack11ll11lll1_opy_)
def bstack11ll1ll1l1_opy_(bstack11l1llll11_opy_):
    if not bstack11l1llll11_opy_:
        return None
    if bstack11l1llll11_opy_.get(bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ᣻"), None):
        return getattr(bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ᣼")], bstack111llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᣽"), None)
    return bstack11l1llll11_opy_.get(bstack111llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᣾"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l11l1lll_opy_.on():
            return
        places = [bstack111llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ᣿"), bstack111llll_opy_ (u"ࠩࡦࡥࡱࡲࠧᤀ"), bstack111llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᤁ")]
        bstack11l1ll1111_opy_ = []
        for bstack1ll11ll111l_opy_ in places:
            records = caplog.get_records(bstack1ll11ll111l_opy_)
            bstack1ll11ll11l1_opy_ = bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᤂ") if bstack1ll11ll111l_opy_ == bstack111llll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᤃ") else bstack111llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᤄ")
            bstack1ll11l11l1l_opy_ = request.node.nodeid + (bstack111llll_opy_ (u"ࠧࠨᤅ") if bstack1ll11ll111l_opy_ == bstack111llll_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᤆ") else bstack111llll_opy_ (u"ࠩ࠰ࠫᤇ") + bstack1ll11ll111l_opy_)
            bstack11ll1lllll_opy_ = bstack11ll1ll1l1_opy_(_11ll11ll1l_opy_.get(bstack1ll11l11l1l_opy_, None))
            if not bstack11ll1lllll_opy_:
                continue
            for record in records:
                if bstack1111ll1ll1_opy_(record.message):
                    continue
                bstack11l1ll1111_opy_.append({
                    bstack111llll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᤈ"): bstack1111l11lll_opy_(record.created).isoformat() + bstack111llll_opy_ (u"ࠫ࡟࠭ᤉ"),
                    bstack111llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᤊ"): record.levelname,
                    bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᤋ"): record.message,
                    bstack1ll11ll11l1_opy_: bstack11ll1lllll_opy_
                })
        if len(bstack11l1ll1111_opy_) > 0:
            bstack1l11l1lll_opy_.bstack11l1l111l_opy_(bstack11l1ll1111_opy_)
    except Exception as err:
        print(bstack111llll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫᤌ"), str(err))
def bstack1l11lll1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11ll11lll_opy_
    bstack11111lll_opy_ = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᤍ"), None) and bstack1llll11l1l_opy_(
            threading.current_thread(), bstack111llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᤎ"), None)
    bstack1l111111ll_opy_ = getattr(driver, bstack111llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᤏ"), None) != None and getattr(driver, bstack111llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᤐ"), None) == True
    if sequence == bstack111llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᤑ") and driver != None:
      if not bstack11ll11lll_opy_ and bstack1111llll11_opy_() and bstack111llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᤒ") in CONFIG and CONFIG[bstack111llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᤓ")] == True and bstack1l1l111l_opy_.bstack111l111l_opy_(driver_command) and (bstack1l111111ll_opy_ or bstack11111lll_opy_) and not bstack11l1ll11_opy_(args):
        try:
          bstack11ll11lll_opy_ = True
          logger.debug(bstack111llll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪᤔ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack111llll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧᤕ").format(str(err)))
        bstack11ll11lll_opy_ = False
    if sequence == bstack111llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᤖ"):
        if driver_command == bstack111llll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᤗ"):
            bstack1l11l1lll_opy_.bstack11llllll1_opy_({
                bstack111llll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᤘ"): response[bstack111llll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᤙ")],
                bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᤚ"): store[bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᤛ")]
            })
def bstack1l11ll11l_opy_():
    global bstack1l1111111l_opy_
    bstack1ll1l1ll11_opy_.bstack111l1111_opy_()
    logging.shutdown()
    bstack1l11l1lll_opy_.bstack11ll1l11ll_opy_()
    for driver in bstack1l1111111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll111ll1l1_opy_(*args):
    global bstack1l1111111l_opy_
    bstack1l11l1lll_opy_.bstack11ll1l11ll_opy_()
    for driver in bstack1l1111111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11ll1l1l_opy_(self, *args, **kwargs):
    bstack11ll1ll1_opy_ = bstack1l1l1l11_opy_(self, *args, **kwargs)
    bstack1l11l1lll_opy_.bstack1ll1lll111_opy_(self)
    return bstack11ll1ll1_opy_
def bstack1111ll111_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l111l11ll_opy_ = Config.bstack1ll1ll1l1_opy_()
    if bstack1l111l11ll_opy_.get_property(bstack111llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ᤜ")):
        return
    bstack1l111l11ll_opy_.bstack1ll11l1l1_opy_(bstack111llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧᤝ"), True)
    global bstack11lll111l_opy_
    global bstack1111l111_opy_
    bstack11lll111l_opy_ = framework_name
    logger.info(bstack1l11ll11ll_opy_.format(bstack11lll111l_opy_.split(bstack111llll_opy_ (u"ࠫ࠲࠭ᤞ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1111llll11_opy_():
            Service.start = bstack11ll1l1ll_opy_
            Service.stop = bstack1ll11lllll_opy_
            webdriver.Remote.__init__ = bstack1ll1l1ll_opy_
            webdriver.Remote.get = bstack1l11lllll1_opy_
            if not isinstance(os.getenv(bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭᤟")), str):
                return
            WebDriver.close = bstack11ll11111_opy_
            WebDriver.quit = bstack1ll11l11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1111llll11_opy_() and bstack1l11l1lll_opy_.on():
            webdriver.Remote.__init__ = bstack11ll1l1l_opy_
        bstack1111l111_opy_ = True
    except Exception as e:
        pass
    bstack11l11l1ll_opy_()
    if os.environ.get(bstack111llll_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᤠ")):
        bstack1111l111_opy_ = eval(os.environ.get(bstack111llll_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᤡ")))
    if not bstack1111l111_opy_:
        bstack11l1l1l1_opy_(bstack111llll_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᤢ"), bstack1lll11l1l_opy_)
    if bstack1l11ll1l11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1ll11l1l_opy_
        except Exception as e:
            logger.error(bstack11l1111l1_opy_.format(str(e)))
    if bstack111llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᤣ") in str(framework_name).lower():
        if not bstack1111llll11_opy_():
            return
        try:
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
def bstack1ll11l11_opy_(self):
    global bstack11lll111l_opy_
    global bstack1llll11111_opy_
    global bstack11lll11ll_opy_
    try:
        if bstack111llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᤤ") in bstack11lll111l_opy_ and self.session_id != None and bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᤥ"), bstack111llll_opy_ (u"ࠬ࠭ᤦ")) != bstack111llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᤧ"):
            bstack1l11l1lll1_opy_ = bstack111llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᤨ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111llll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᤩ")
            bstack1ll1lllll1_opy_(logger, True)
            if self != None:
                bstack1l1l1lll_opy_(self, bstack1l11l1lll1_opy_, bstack111llll_opy_ (u"ࠩ࠯ࠤࠬᤪ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack111llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᤫ"), None)
        if item is not None and bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᤬"), None):
            bstack1l111ll11l_opy_.bstack1ll111ll11_opy_(self, bstack1llll1l11_opy_, logger, item)
        threading.current_thread().testStatus = bstack111llll_opy_ (u"ࠬ࠭᤭")
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢ᤮") + str(e))
    bstack11lll11ll_opy_(self)
    self.session_id = None
def bstack1ll1l1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll11111_opy_
    global bstack11lll1ll1_opy_
    global bstack1lll1l1l11_opy_
    global bstack11lll111l_opy_
    global bstack1l1l1l11_opy_
    global bstack1l1111111l_opy_
    global bstack11l111lll_opy_
    global bstack1l1lll1l_opy_
    global bstack1llll1l11_opy_
    CONFIG[bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ᤯")] = str(bstack11lll111l_opy_) + str(__version__)
    command_executor = bstack1llll1ll1l_opy_(bstack11l111lll_opy_)
    logger.debug(bstack1l1l1ll11l_opy_.format(command_executor))
    proxy = bstack11lll1lll_opy_(CONFIG, proxy)
    bstack1lll1l1ll_opy_ = 0
    try:
        if bstack1lll1l1l11_opy_ is True:
            bstack1lll1l1ll_opy_ = int(os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᤰ")))
    except:
        bstack1lll1l1ll_opy_ = 0
    bstack1ll1ll1l_opy_ = bstack111llll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
    logger.debug(bstack1lll1111ll_opy_.format(str(bstack1ll1ll1l_opy_)))
    bstack1llll1l11_opy_ = CONFIG.get(bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᤱ"))[bstack1lll1l1ll_opy_]
    if bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᤲ") in CONFIG and CONFIG[bstack111llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᤳ")]:
        bstack11llllllll_opy_(bstack1ll1ll1l_opy_, bstack1l1lll1l_opy_)
    if bstack1l1111ll_opy_.bstack1l111l11_opy_(CONFIG, bstack1lll1l1ll_opy_) and bstack1l1111ll_opy_.bstack11l111ll_opy_(bstack1ll1ll1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        bstack1l1111ll_opy_.set_capabilities(bstack1ll1ll1l_opy_, CONFIG)
    if desired_capabilities:
        bstack11l11llll_opy_ = bstack111l1l1ll_opy_(desired_capabilities)
        bstack11l11llll_opy_[bstack111llll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᤴ")] = bstack1ll1ll1lll_opy_(CONFIG)
        bstack11l111ll1_opy_ = bstack111llll1_opy_(bstack11l11llll_opy_)
        if bstack11l111ll1_opy_:
            bstack1ll1ll1l_opy_ = update(bstack11l111ll1_opy_, bstack1ll1ll1l_opy_)
        desired_capabilities = None
    if options:
        bstack1l11llll_opy_(options, bstack1ll1ll1l_opy_)
    if not options:
        options = bstack1ll1llll1_opy_(bstack1ll1ll1l_opy_)
    if proxy and bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᤵ")):
        options.proxy(proxy)
    if options and bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᤶ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll111l1_opy_() < version.parse(bstack111llll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᤷ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1ll1l_opy_)
    logger.info(bstack111llll11_opy_)
    if bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᤸ")):
        bstack1l1l1l11_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠪ࠷࠳࠾࠮࠱᤹ࠩ")):
        bstack1l1l1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ᤺")):
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
        bstack1llll1llll_opy_ = bstack111llll_opy_ (u"᤻ࠬ࠭")
        if bstack1lll111l1_opy_() >= version.parse(bstack111llll_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ᤼")):
            bstack1llll1llll_opy_ = self.caps.get(bstack111llll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ᤽"))
        else:
            bstack1llll1llll_opy_ = self.capabilities.get(bstack111llll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ᤾"))
        if bstack1llll1llll_opy_:
            bstack1l1l1l1ll_opy_(bstack1llll1llll_opy_)
            if bstack1lll111l1_opy_() <= version.parse(bstack111llll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ᤿")):
                self.command_executor._url = bstack111llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ᥀") + bstack11l111lll_opy_ + bstack111llll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ᥁")
            else:
                self.command_executor._url = bstack111llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ᥂") + bstack1llll1llll_opy_ + bstack111llll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ᥃")
            logger.debug(bstack1l1l1111l1_opy_.format(bstack1llll1llll_opy_))
        else:
            logger.debug(bstack1l1l111ll_opy_.format(bstack111llll_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ᥄")))
    except Exception as e:
        logger.debug(bstack1l1l111ll_opy_.format(e))
    bstack1llll11111_opy_ = self.session_id
    if bstack111llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᥅") in bstack11lll111l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack111llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᥆"), None)
        if item:
            bstack1ll11l1l11l_opy_ = getattr(item, bstack111llll_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ᥇"), False)
            if not getattr(item, bstack111llll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ᥈"), None) and bstack1ll11l1l11l_opy_:
                setattr(store[bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᥉")], bstack111llll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ᥊"), self)
        bstack1l11l1lll_opy_.bstack1ll1lll111_opy_(self)
    bstack1l1111111l_opy_.append(self)
    if bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᥋") in CONFIG and bstack111llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᥌") in CONFIG[bstack111llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᥍")][bstack1lll1l1ll_opy_]:
        bstack11lll1ll1_opy_ = CONFIG[bstack111llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᥎")][bstack1lll1l1ll_opy_][bstack111llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᥏")]
    logger.debug(bstack1llllll1l_opy_.format(bstack1llll11111_opy_))
def bstack1l11lllll1_opy_(self, url):
    global bstack1l1lll1l1_opy_
    global CONFIG
    try:
        bstack1l1lllllll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1111ll1ll_opy_.format(str(err)))
    try:
        bstack1l1lll1l1_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll1l11l_opy_ = str(e)
            if any(err_msg in bstack1ll1l11l_opy_ for err_msg in bstack1llll1l1_opy_):
                bstack1l1lllllll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1111ll1ll_opy_.format(str(err)))
        raise e
def bstack1l111l11l_opy_(item, when):
    global bstack1ll1ll11l1_opy_
    try:
        bstack1ll1ll11l1_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll1lll_opy_(item, call, rep):
    global bstack1l11l1l11_opy_
    global bstack1l1111111l_opy_
    name = bstack111llll_opy_ (u"ࠬ࠭ᥐ")
    try:
        if rep.when == bstack111llll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᥑ"):
            bstack1llll11111_opy_ = threading.current_thread().bstackSessionId
            bstack1ll11l11lll_opy_ = item.config.getoption(bstack111llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᥒ"))
            try:
                if (str(bstack1ll11l11lll_opy_).lower() != bstack111llll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᥓ")):
                    name = str(rep.nodeid)
                    bstack111ll1ll_opy_ = bstack111l1ll1l_opy_(bstack111llll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᥔ"), name, bstack111llll_opy_ (u"ࠪࠫᥕ"), bstack111llll_opy_ (u"ࠫࠬᥖ"), bstack111llll_opy_ (u"ࠬ࠭ᥗ"), bstack111llll_opy_ (u"࠭ࠧᥘ"))
                    os.environ[bstack111llll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᥙ")] = name
                    for driver in bstack1l1111111l_opy_:
                        if bstack1llll11111_opy_ == driver.session_id:
                            driver.execute_script(bstack111ll1ll_opy_)
            except Exception as e:
                logger.debug(bstack111llll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᥚ").format(str(e)))
            try:
                bstack1llllllll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᥛ"):
                    status = bstack111llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᥜ") if rep.outcome.lower() == bstack111llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᥝ") else bstack111llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᥞ")
                    reason = bstack111llll_opy_ (u"࠭ࠧᥟ")
                    if status == bstack111llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᥠ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111llll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᥡ") if status == bstack111llll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᥢ") else bstack111llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᥣ")
                    data = name + bstack111llll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ᥤ") if status == bstack111llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᥥ") else name + bstack111llll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩᥦ") + reason
                    bstack1l1l1l1l1l_opy_ = bstack111l1ll1l_opy_(bstack111llll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᥧ"), bstack111llll_opy_ (u"ࠨࠩᥨ"), bstack111llll_opy_ (u"ࠩࠪᥩ"), bstack111llll_opy_ (u"ࠪࠫᥪ"), level, data)
                    for driver in bstack1l1111111l_opy_:
                        if bstack1llll11111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l1l1l1l_opy_)
            except Exception as e:
                logger.debug(bstack111llll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᥫ").format(str(e)))
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩᥬ").format(str(e)))
    bstack1l11l1l11_opy_(item, call, rep)
notset = Notset()
def bstack1llll1ll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l11l1ll1_opy_
    if str(name).lower() == bstack111llll_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ᥭ"):
        return bstack111llll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ᥮")
    else:
        return bstack1l11l1ll1_opy_(self, name, default, skip)
def bstack1ll11l1l_opy_(self):
    global CONFIG
    global bstack1l1lll11l1_opy_
    try:
        proxy = bstack1ll11lll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111llll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭᥯")):
                proxies = bstack1l1l11ll1l_opy_(proxy, bstack1llll1ll1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l111l1l_opy_ = proxies.popitem()
                    if bstack111llll_opy_ (u"ࠤ࠽࠳࠴ࠨᥰ") in bstack1l111l1l_opy_:
                        return bstack1l111l1l_opy_
                    else:
                        return bstack111llll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᥱ") + bstack1l111l1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣᥲ").format(str(e)))
    return bstack1l1lll11l1_opy_(self)
def bstack1l11ll1l11_opy_():
    return (bstack111llll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᥳ") in CONFIG or bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᥴ") in CONFIG) and bstack1ll1ll1l11_opy_() and bstack1lll111l1_opy_() >= version.parse(
        bstack1l1l1l11l_opy_)
def bstack1l11l1ll11_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11lll1ll1_opy_
    global bstack1lll1l1l11_opy_
    global bstack11lll111l_opy_
    CONFIG[bstack111llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ᥵")] = str(bstack11lll111l_opy_) + str(__version__)
    bstack1lll1l1ll_opy_ = 0
    try:
        if bstack1lll1l1l11_opy_ is True:
            bstack1lll1l1ll_opy_ = int(os.environ.get(bstack111llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᥶")))
    except:
        bstack1lll1l1ll_opy_ = 0
    CONFIG[bstack111llll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ᥷")] = True
    bstack1ll1ll1l_opy_ = bstack111llll1_opy_(CONFIG, bstack1lll1l1ll_opy_)
    logger.debug(bstack1lll1111ll_opy_.format(str(bstack1ll1ll1l_opy_)))
    if CONFIG.get(bstack111llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᥸")):
        bstack11llllllll_opy_(bstack1ll1ll1l_opy_, bstack1l1lll1l_opy_)
    if bstack111llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᥹") in CONFIG and bstack111llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᥺") in CONFIG[bstack111llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᥻")][bstack1lll1l1ll_opy_]:
        bstack11lll1ll1_opy_ = CONFIG[bstack111llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᥼")][bstack1lll1l1ll_opy_][bstack111llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᥽")]
    import urllib
    import json
    bstack1l1lll111_opy_ = bstack111llll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ᥾") + urllib.parse.quote(json.dumps(bstack1ll1ll1l_opy_))
    browser = self.connect(bstack1l1lll111_opy_)
    return browser
def bstack11l11l1ll_opy_():
    global bstack1111l111_opy_
    global bstack11lll111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1111l11_opy_
        if not bstack1111llll11_opy_():
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
def bstack1ll111llll1_opy_():
    global CONFIG
    global bstack11l1l1l1l_opy_
    global bstack11l111lll_opy_
    global bstack1l1lll1l_opy_
    global bstack1lll1l1l11_opy_
    global bstack1llll111_opy_
    CONFIG = json.loads(os.environ.get(bstack111llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ᥿")))
    bstack11l1l1l1l_opy_ = eval(os.environ.get(bstack111llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᦀ")))
    bstack11l111lll_opy_ = os.environ.get(bstack111llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬᦁ"))
    bstack1l11l11111_opy_(CONFIG, bstack11l1l1l1l_opy_)
    bstack1llll111_opy_ = bstack1ll1l1ll11_opy_.bstack11llll1ll_opy_(CONFIG, bstack1llll111_opy_)
    global bstack1l1l1l11_opy_
    global bstack11lll11ll_opy_
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
    except Exception as e:
        pass
    if (bstack111llll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᦂ") in CONFIG or bstack111llll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᦃ") in CONFIG) and bstack1ll1ll1l11_opy_():
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
        logger.debug(bstack111llll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩᦄ"))
    bstack1l1lll1l_opy_ = CONFIG.get(bstack111llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᦅ"), {}).get(bstack111llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᦆ"))
    bstack1lll1l1l11_opy_ = True
    bstack1111ll111_opy_(bstack111l11l1_opy_)
if (bstack1111lll1l1_opy_()):
    bstack1ll111llll1_opy_()
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll11l11111_opy_(hook_name, event, bstack1ll11l1l1l1_opy_=None):
    if hook_name not in [bstack111llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᦇ"), bstack111llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᦈ"), bstack111llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᦉ"), bstack111llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᦊ"), bstack111llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᦋ"), bstack111llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᦌ"), bstack111llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᦍ"), bstack111llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᦎ")]:
        return
    node = store[bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᦏ")]
    if hook_name in [bstack111llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᦐ"), bstack111llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᦑ")]:
        node = store[bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᦒ")]
    elif hook_name in [bstack111llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᦓ"), bstack111llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᦔ")]:
        node = store[bstack111llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᦕ")]
    if event == bstack111llll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᦖ"):
        hook_type = bstack1lll111llll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11ll1lll11_opy_ = {
            bstack111llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᦗ"): uuid,
            bstack111llll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᦘ"): bstack1ll1llllll_opy_(),
            bstack111llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᦙ"): bstack111llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᦚ"),
            bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᦛ"): hook_type,
            bstack111llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᦜ"): hook_name
        }
        store[bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᦝ")].append(uuid)
        bstack1ll11l11l11_opy_ = node.nodeid
        if hook_type == bstack111llll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᦞ"):
            if not _11ll11ll1l_opy_.get(bstack1ll11l11l11_opy_, None):
                _11ll11ll1l_opy_[bstack1ll11l11l11_opy_] = {bstack111llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᦟ"): []}
            _11ll11ll1l_opy_[bstack1ll11l11l11_opy_][bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᦠ")].append(bstack11ll1lll11_opy_[bstack111llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᦡ")])
        _11ll11ll1l_opy_[bstack1ll11l11l11_opy_ + bstack111llll_opy_ (u"ࠪ࠱ࠬᦢ") + hook_name] = bstack11ll1lll11_opy_
        bstack1ll111l1lll_opy_(node, bstack11ll1lll11_opy_, bstack111llll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᦣ"))
    elif event == bstack111llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᦤ"):
        bstack11lll1111l_opy_ = node.nodeid + bstack111llll_opy_ (u"࠭࠭ࠨᦥ") + hook_name
        _11ll11ll1l_opy_[bstack11lll1111l_opy_][bstack111llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᦦ")] = bstack1ll1llllll_opy_()
        bstack1ll11l1lll1_opy_(_11ll11ll1l_opy_[bstack11lll1111l_opy_][bstack111llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦧ")])
        bstack1ll111l1lll_opy_(node, _11ll11ll1l_opy_[bstack11lll1111l_opy_], bstack111llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᦨ"), bstack1ll11l1ll11_opy_=bstack1ll11l1l1l1_opy_)
def bstack1ll11l111l1_opy_():
    global bstack1ll111lll1l_opy_
    if bstack1ll11lll1l_opy_():
        bstack1ll111lll1l_opy_ = bstack111llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᦩ")
    else:
        bstack1ll111lll1l_opy_ = bstack111llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᦪ")
@bstack1l11l1lll_opy_.bstack1ll1l1lllll_opy_
def bstack1ll111ll1ll_opy_():
    bstack1ll11l111l1_opy_()
    if bstack1ll1ll1l11_opy_():
        bstack1lll1l1ll1_opy_(bstack1l11lll1l_opy_)
    try:
        bstack1llllll1lll_opy_(bstack1ll11l11111_opy_)
    except Exception as e:
        logger.debug(bstack111llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᦫ").format(e))
bstack1ll111ll1ll_opy_()