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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11ll111lll_opy_ import RobotHandler
from bstack_utils.capture import bstack11lll1l1ll_opy_
from bstack_utils.bstack11lll1lll1_opy_ import bstack11ll11111l_opy_, bstack11llll1lll_opy_, bstack11llll1l1l_opy_
from bstack_utils.bstack1lll1ll11_opy_ import bstack1l1lll1111_opy_
from bstack_utils.bstack111lll1ll_opy_ import bstack1l11l1lll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1llll11l1l_opy_, bstack1ll1llllll_opy_, Result, \
    bstack11ll1ll111_opy_, bstack11l1ll11l1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩณ"): [],
        bstack111llll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬด"): [],
        bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫต"): []
    }
    bstack11l1ll1l11_opy_ = []
    bstack11ll11llll_opy_ = []
    @staticmethod
    def bstack11llll11l1_opy_(log):
        if not (log[bstack111llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩถ")] and log[bstack111llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪท")].strip()):
            return
        active = bstack1l1lll1111_opy_.bstack11lll1l111_opy_()
        log = {
            bstack111llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩธ"): log[bstack111llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪน")],
            bstack111llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨบ"): bstack11l1ll11l1_opy_().isoformat() + bstack111llll_opy_ (u"࡚࠭ࠨป"),
            bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨผ"): log[bstack111llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩฝ")],
        }
        if active:
            if active[bstack111llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧพ")] == bstack111llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨฟ"):
                log[bstack111llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫภ")] = active[bstack111llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬม")]
            elif active[bstack111llll_opy_ (u"࠭ࡴࡺࡲࡨࠫย")] == bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࠬร"):
                log[bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨฤ")] = active[bstack111llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩล")]
        bstack1l11l1lll_opy_.bstack11l1l111l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11ll1l111l_opy_ = None
        self._11l1lll1l1_opy_ = None
        self._11ll11ll1l_opy_ = OrderedDict()
        self.bstack11lll111l1_opy_ = bstack11lll1l1ll_opy_(self.bstack11llll11l1_opy_)
    @bstack11ll1ll111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11ll11ll11_opy_()
        if not self._11ll11ll1l_opy_.get(attrs.get(bstack111llll_opy_ (u"ࠪ࡭ࡩ࠭ฦ")), None):
            self._11ll11ll1l_opy_[attrs.get(bstack111llll_opy_ (u"ࠫ࡮ࡪࠧว"))] = {}
        bstack11l1ll11ll_opy_ = bstack11llll1l1l_opy_(
                bstack11ll111ll1_opy_=attrs.get(bstack111llll_opy_ (u"ࠬ࡯ࡤࠨศ")),
                name=name,
                bstack11lll11l11_opy_=bstack1ll1llllll_opy_(),
                file_path=os.path.relpath(attrs[bstack111llll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ษ")], start=os.getcwd()) if attrs.get(bstack111llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧส")) != bstack111llll_opy_ (u"ࠨࠩห") else bstack111llll_opy_ (u"ࠩࠪฬ"),
                framework=bstack111llll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩอ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111llll_opy_ (u"ࠫ࡮ࡪࠧฮ"), None)
        self._11ll11ll1l_opy_[attrs.get(bstack111llll_opy_ (u"ࠬ࡯ࡤࠨฯ"))][bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩะ")] = bstack11l1ll11ll_opy_
    @bstack11ll1ll111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11ll1111ll_opy_()
        self._11ll1l1l11_opy_(messages)
        for bstack11l1l1ll1l_opy_ in self.bstack11l1ll1l11_opy_:
            bstack11l1l1ll1l_opy_[bstack111llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩั")][bstack111llll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧา")].extend(self.store[bstack111llll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨำ")])
            bstack1l11l1lll_opy_.bstack11ll1l1111_opy_(bstack11l1l1ll1l_opy_)
        self.bstack11l1ll1l11_opy_ = []
        self.store[bstack111llll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩิ")] = []
    @bstack11ll1ll111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11lll111l1_opy_.start()
        if not self._11ll11ll1l_opy_.get(attrs.get(bstack111llll_opy_ (u"ࠫ࡮ࡪࠧี")), None):
            self._11ll11ll1l_opy_[attrs.get(bstack111llll_opy_ (u"ࠬ࡯ࡤࠨึ"))] = {}
        driver = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬื"), None)
        bstack11lll1lll1_opy_ = bstack11llll1l1l_opy_(
            bstack11ll111ll1_opy_=attrs.get(bstack111llll_opy_ (u"ࠧࡪࡦุࠪ")),
            name=name,
            bstack11lll11l11_opy_=bstack1ll1llllll_opy_(),
            file_path=os.path.relpath(attrs[bstack111llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨู")], start=os.getcwd()),
            scope=RobotHandler.bstack11ll111l1l_opy_(attrs.get(bstack111llll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦฺࠩ"), None)),
            framework=bstack111llll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ฻"),
            tags=attrs[bstack111llll_opy_ (u"ࠫࡹࡧࡧࡴࠩ฼")],
            hooks=self.store[bstack111llll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ฽")],
            bstack11lll1l1l1_opy_=bstack1l11l1lll_opy_.bstack11lll11111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111llll_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣ฾").format(bstack111llll_opy_ (u"ࠢࠡࠤ฿").join(attrs[bstack111llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭เ")]), name) if attrs[bstack111llll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧแ")] else name
        )
        self._11ll11ll1l_opy_[attrs.get(bstack111llll_opy_ (u"ࠪ࡭ࡩ࠭โ"))][bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧใ")] = bstack11lll1lll1_opy_
        threading.current_thread().current_test_uuid = bstack11lll1lll1_opy_.bstack11l1ll1l1l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111llll_opy_ (u"ࠬ࡯ࡤࠨไ"), None)
        self.bstack11llll11ll_opy_(bstack111llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧๅ"), bstack11lll1lll1_opy_)
    @bstack11ll1ll111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11lll111l1_opy_.reset()
        bstack11l1llll1l_opy_ = bstack11ll1l11l1_opy_.get(attrs.get(bstack111llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧๆ")), bstack111llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ็"))
        self._11ll11ll1l_opy_[attrs.get(bstack111llll_opy_ (u"ࠩ࡬ࡨ่ࠬ"))][bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ้࠭")].stop(time=bstack1ll1llllll_opy_(), duration=int(attrs.get(bstack111llll_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦ๊ࠩ"), bstack111llll_opy_ (u"ࠬ࠶๋ࠧ"))), result=Result(result=bstack11l1llll1l_opy_, exception=attrs.get(bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ์")), bstack11llll1111_opy_=[attrs.get(bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨํ"))]))
        self.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ๎"), self._11ll11ll1l_opy_[attrs.get(bstack111llll_opy_ (u"ࠩ࡬ࡨࠬ๏"))][bstack111llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭๐")], True)
        self.store[bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ๑")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11ll1ll111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11ll11ll11_opy_()
        current_test_id = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ๒"), None)
        bstack11l1llllll_opy_ = current_test_id if bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ๓"), None) else bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ๔"), None)
        if attrs.get(bstack111llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭๕"), bstack111llll_opy_ (u"ࠩࠪ๖")).lower() in [bstack111llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ๗"), bstack111llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭๘")]:
            hook_type = bstack11l1lll111_opy_(attrs.get(bstack111llll_opy_ (u"ࠬࡺࡹࡱࡧࠪ๙")), bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ๚"), None))
            hook_name = bstack111llll_opy_ (u"ࠧࡼࡿࠪ๛").format(attrs.get(bstack111llll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ๜"), bstack111llll_opy_ (u"ࠩࠪ๝")))
            if hook_type in [bstack111llll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ๞"), bstack111llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ๟")]:
                hook_name = bstack111llll_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭๠").format(bstack11l1lll1ll_opy_.get(hook_type), attrs.get(bstack111llll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭๡"), bstack111llll_opy_ (u"ࠧࠨ๢")))
            bstack11ll1lll11_opy_ = bstack11llll1lll_opy_(
                bstack11ll111ll1_opy_=bstack11l1llllll_opy_ + bstack111llll_opy_ (u"ࠨ࠯ࠪ๣") + attrs.get(bstack111llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๤"), bstack111llll_opy_ (u"ࠪࠫ๥")).lower(),
                name=hook_name,
                bstack11lll11l11_opy_=bstack1ll1llllll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111llll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ๦")), start=os.getcwd()),
                framework=bstack111llll_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ๧"),
                tags=attrs[bstack111llll_opy_ (u"࠭ࡴࡢࡩࡶࠫ๨")],
                scope=RobotHandler.bstack11ll111l1l_opy_(attrs.get(bstack111llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ๩"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11ll1lll11_opy_.bstack11l1ll1l1l_opy_()
            threading.current_thread().current_hook_id = bstack11l1llllll_opy_ + bstack111llll_opy_ (u"ࠨ࠯ࠪ๪") + attrs.get(bstack111llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๫"), bstack111llll_opy_ (u"ࠪࠫ๬")).lower()
            self.store[bstack111llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ๭")] = [bstack11ll1lll11_opy_.bstack11l1ll1l1l_opy_()]
            if bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ๮"), None):
                self.store[bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ๯")].append(bstack11ll1lll11_opy_.bstack11l1ll1l1l_opy_())
            else:
                self.store[bstack111llll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭๰")].append(bstack11ll1lll11_opy_.bstack11l1ll1l1l_opy_())
            if bstack11l1llllll_opy_:
                self._11ll11ll1l_opy_[bstack11l1llllll_opy_ + bstack111llll_opy_ (u"ࠨ࠯ࠪ๱") + attrs.get(bstack111llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ๲"), bstack111llll_opy_ (u"ࠪࠫ๳")).lower()] = { bstack111llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ๴"): bstack11ll1lll11_opy_ }
            bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭๵"), bstack11ll1lll11_opy_)
        else:
            bstack11llll1l11_opy_ = {
                bstack111llll_opy_ (u"࠭ࡩࡥࠩ๶"): uuid4().__str__(),
                bstack111llll_opy_ (u"ࠧࡵࡧࡻࡸࠬ๷"): bstack111llll_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧ๸").format(attrs.get(bstack111llll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ๹")), attrs.get(bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ๺"), bstack111llll_opy_ (u"ࠫࠬ๻"))) if attrs.get(bstack111llll_opy_ (u"ࠬࡧࡲࡨࡵࠪ๼"), []) else attrs.get(bstack111llll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭๽")),
                bstack111llll_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧ๾"): attrs.get(bstack111llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭๿"), []),
                bstack111llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭຀"): bstack1ll1llllll_opy_(),
                bstack111llll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪກ"): bstack111llll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬຂ"),
                bstack111llll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ຃"): attrs.get(bstack111llll_opy_ (u"࠭ࡤࡰࡥࠪຄ"), bstack111llll_opy_ (u"ࠧࠨ຅"))
            }
            if attrs.get(bstack111llll_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩຆ"), bstack111llll_opy_ (u"ࠩࠪງ")) != bstack111llll_opy_ (u"ࠪࠫຈ"):
                bstack11llll1l11_opy_[bstack111llll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬຉ")] = attrs.get(bstack111llll_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ຊ"))
            if not self.bstack11ll11llll_opy_:
                self._11ll11ll1l_opy_[self._11ll1111l1_opy_()][bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ຋")].add_step(bstack11llll1l11_opy_)
                threading.current_thread().current_step_uuid = bstack11llll1l11_opy_[bstack111llll_opy_ (u"ࠧࡪࡦࠪຌ")]
            self.bstack11ll11llll_opy_.append(bstack11llll1l11_opy_)
    @bstack11ll1ll111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11ll1111ll_opy_()
        self._11ll1l1l11_opy_(messages)
        current_test_id = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪຍ"), None)
        bstack11l1llllll_opy_ = current_test_id if current_test_id else bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬຎ"), None)
        bstack11l1l1lll1_opy_ = bstack11ll1l11l1_opy_.get(attrs.get(bstack111llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪຏ")), bstack111llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬຐ"))
        bstack11l1ll1ll1_opy_ = attrs.get(bstack111llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຑ"))
        if bstack11l1l1lll1_opy_ != bstack111llll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧຒ") and not attrs.get(bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຓ")) and self._11ll1l111l_opy_:
            bstack11l1ll1ll1_opy_ = self._11ll1l111l_opy_
        bstack11lll1ll11_opy_ = Result(result=bstack11l1l1lll1_opy_, exception=bstack11l1ll1ll1_opy_, bstack11llll1111_opy_=[bstack11l1ll1ll1_opy_])
        if attrs.get(bstack111llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ດ"), bstack111llll_opy_ (u"ࠩࠪຕ")).lower() in [bstack111llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩຖ"), bstack111llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ທ")]:
            bstack11l1llllll_opy_ = current_test_id if current_test_id else bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨຘ"), None)
            if bstack11l1llllll_opy_:
                bstack11lll1111l_opy_ = bstack11l1llllll_opy_ + bstack111llll_opy_ (u"ࠨ࠭ࠣນ") + attrs.get(bstack111llll_opy_ (u"ࠧࡵࡻࡳࡩࠬບ"), bstack111llll_opy_ (u"ࠨࠩປ")).lower()
                self._11ll11ll1l_opy_[bstack11lll1111l_opy_][bstack111llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຜ")].stop(time=bstack1ll1llllll_opy_(), duration=int(attrs.get(bstack111llll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨຝ"), bstack111llll_opy_ (u"ࠫ࠵࠭ພ"))), result=bstack11lll1ll11_opy_)
                bstack1l11l1lll_opy_.bstack11llll11ll_opy_(bstack111llll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧຟ"), self._11ll11ll1l_opy_[bstack11lll1111l_opy_][bstack111llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩຠ")])
        else:
            bstack11l1llllll_opy_ = current_test_id if current_test_id else bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩມ"), None)
            if bstack11l1llllll_opy_ and len(self.bstack11ll11llll_opy_) == 1:
                current_step_uuid = bstack1llll11l1l_opy_(threading.current_thread(), bstack111llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬຢ"), None)
                self._11ll11ll1l_opy_[bstack11l1llllll_opy_][bstack111llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຣ")].bstack11lll11ll1_opy_(current_step_uuid, duration=int(attrs.get(bstack111llll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨ຤"), bstack111llll_opy_ (u"ࠫ࠵࠭ລ"))), result=bstack11lll1ll11_opy_)
            else:
                self.bstack11ll11l111_opy_(attrs)
            self.bstack11ll11llll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111llll_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪ຦"), bstack111llll_opy_ (u"࠭࡮ࡰࠩວ")) == bstack111llll_opy_ (u"ࠧࡺࡧࡶࠫຨ"):
                return
            self.messages.push(message)
            bstack11l1ll1111_opy_ = []
            if bstack1l1lll1111_opy_.bstack11lll1l111_opy_():
                bstack11l1ll1111_opy_.append({
                    bstack111llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫຩ"): bstack1ll1llllll_opy_(),
                    bstack111llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪສ"): message.get(bstack111llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຫ")),
                    bstack111llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪຬ"): message.get(bstack111llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫອ")),
                    **bstack1l1lll1111_opy_.bstack11lll1l111_opy_()
                })
                if len(bstack11l1ll1111_opy_) > 0:
                    bstack1l11l1lll_opy_.bstack11l1l111l_opy_(bstack11l1ll1111_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l11l1lll_opy_.bstack11ll1l11ll_opy_()
    def bstack11ll11l111_opy_(self, bstack11ll1ll1ll_opy_):
        if not bstack1l1lll1111_opy_.bstack11lll1l111_opy_():
            return
        kwname = bstack111llll_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬຮ").format(bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧຯ")), bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ະ"), bstack111llll_opy_ (u"ࠩࠪັ"))) if bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨາ"), []) else bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫຳ"))
        error_message = bstack111llll_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦິ").format(kwname, bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ີ")), str(bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຶ"))))
        bstack11l1ll1lll_opy_ = bstack111llll_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢື").format(kwname, bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴຸࠩ")))
        bstack11ll11l1ll_opy_ = error_message if bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨູࠫ")) else bstack11l1ll1lll_opy_
        bstack11l1l1llll_opy_ = {
            bstack111llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶ຺ࠧ"): self.bstack11ll11llll_opy_[-1].get(bstack111llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩົ"), bstack1ll1llllll_opy_()),
            bstack111llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຼ"): bstack11ll11l1ll_opy_,
            bstack111llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຽ"): bstack111llll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ຾") if bstack11ll1ll1ll_opy_.get(bstack111llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ຿")) == bstack111llll_opy_ (u"ࠪࡊࡆࡏࡌࠨເ") else bstack111llll_opy_ (u"ࠫࡎࡔࡆࡐࠩແ"),
            **bstack1l1lll1111_opy_.bstack11lll1l111_opy_()
        }
        bstack1l11l1lll_opy_.bstack11l1l111l_opy_([bstack11l1l1llll_opy_])
    def _11ll1111l1_opy_(self):
        for bstack11ll111ll1_opy_ in reversed(self._11ll11ll1l_opy_):
            bstack11l1lll11l_opy_ = bstack11ll111ll1_opy_
            data = self._11ll11ll1l_opy_[bstack11ll111ll1_opy_][bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨໂ")]
            if isinstance(data, bstack11llll1lll_opy_):
                if not bstack111llll_opy_ (u"࠭ࡅࡂࡅࡋࠫໃ") in data.bstack11ll1l1l1l_opy_():
                    return bstack11l1lll11l_opy_
            else:
                return bstack11l1lll11l_opy_
    def _11ll1l1l11_opy_(self, messages):
        try:
            bstack11ll11l11l_opy_ = BuiltIn().get_variable_value(bstack111llll_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨໄ")) in (bstack11ll1l1ll1_opy_.DEBUG, bstack11ll1l1ll1_opy_.TRACE)
            for message, bstack11ll11l1l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໅"))
                level = message.get(bstack111llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨໆ"))
                if level == bstack11ll1l1ll1_opy_.FAIL:
                    self._11ll1l111l_opy_ = name or self._11ll1l111l_opy_
                    self._11l1lll1l1_opy_ = bstack11ll11l1l1_opy_.get(bstack111llll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ໇")) if bstack11ll11l11l_opy_ and bstack11ll11l1l1_opy_ else self._11l1lll1l1_opy_
        except:
            pass
    @classmethod
    def bstack11llll11ll_opy_(self, event: str, bstack11ll1l1lll_opy_: bstack11ll11111l_opy_, bstack11l1ll111l_opy_=False):
        if event == bstack111llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ່࠭"):
            bstack11ll1l1lll_opy_.set(hooks=self.store[bstack111llll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴ້ࠩ")])
        if event == bstack111llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪ໊ࠧ"):
            event = bstack111llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥ໋ࠩ")
        if bstack11l1ll111l_opy_:
            bstack11ll11lll1_opy_ = {
                bstack111llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ໌"): event,
                bstack11ll1l1lll_opy_.bstack11ll111l11_opy_(): bstack11ll1l1lll_opy_.bstack11l1lllll1_opy_(event)
            }
            self.bstack11l1ll1l11_opy_.append(bstack11ll11lll1_opy_)
        else:
            bstack1l11l1lll_opy_.bstack11llll11ll_opy_(event, bstack11ll1l1lll_opy_)
class Messages:
    def __init__(self):
        self._11ll1ll11l_opy_ = []
    def bstack11ll11ll11_opy_(self):
        self._11ll1ll11l_opy_.append([])
    def bstack11ll1111ll_opy_(self):
        return self._11ll1ll11l_opy_.pop() if self._11ll1ll11l_opy_ else list()
    def push(self, message):
        self._11ll1ll11l_opy_[-1].append(message) if self._11ll1ll11l_opy_ else self._11ll1ll11l_opy_.append([message])
class bstack11ll1l1ll1_opy_:
    FAIL = bstack111llll_opy_ (u"ࠩࡉࡅࡎࡒࠧໍ")
    ERROR = bstack111llll_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩ໎")
    WARNING = bstack111llll_opy_ (u"ࠫ࡜ࡇࡒࡏࠩ໏")
    bstack11ll111111_opy_ = bstack111llll_opy_ (u"ࠬࡏࡎࡇࡑࠪ໐")
    DEBUG = bstack111llll_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬ໑")
    TRACE = bstack111llll_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭໒")
    bstack11ll1lll1l_opy_ = [FAIL, ERROR]
def bstack11ll1ll1l1_opy_(bstack11l1llll11_opy_):
    if not bstack11l1llll11_opy_:
        return None
    if bstack11l1llll11_opy_.get(bstack111llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໓"), None):
        return getattr(bstack11l1llll11_opy_[bstack111llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໔")], bstack111llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ໕"), None)
    return bstack11l1llll11_opy_.get(bstack111llll_opy_ (u"ࠫࡺࡻࡩࡥࠩ໖"), None)
def bstack11l1lll111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ໗"), bstack111llll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ໘")]:
        return
    if hook_type.lower() == bstack111llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭໙"):
        if current_test_uuid is None:
            return bstack111llll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ໚")
        else:
            return bstack111llll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ໛")
    elif hook_type.lower() == bstack111llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬໜ"):
        if current_test_uuid is None:
            return bstack111llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧໝ")
        else:
            return bstack111llll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩໞ")