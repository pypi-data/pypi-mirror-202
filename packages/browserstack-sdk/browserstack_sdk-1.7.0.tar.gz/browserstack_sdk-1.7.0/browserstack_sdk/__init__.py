# coding: UTF-8
import sys
bstack11l_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1l1_opy_ = 7
def bstack111_opy_ (bstackl_opy_):
    global bstack1_opy_
    stringNr = ord (bstackl_opy_ [-1])
    bstack1ll_opy_ = bstackl_opy_ [:-1]
    bstack11_opy_ = stringNr % len (bstack1ll_opy_)
    bstack1ll1_opy_ = bstack1ll_opy_ [:bstack11_opy_] + bstack1ll_opy_ [bstack11_opy_:]
    if bstack11l_opy_:
        bstack1l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l_opy_ + stringNr) % bstack1l1_opy_) for bstack1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1l_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l_opy_ + stringNr) % bstack1l1_opy_) for bstack1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1l_opy_)
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
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1l1l1l11_opy_ = {
	bstack111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstack111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstack111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstack111_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstack111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstack111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstack111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstack111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstack111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstack111_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstack111_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstack111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstack111_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstack111_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstack111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstack111_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstack111_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstack111_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstack111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstack111_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstack111_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstack111_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstack111_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstack111_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstack111_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstack111_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstack111_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstack111_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstack111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstack111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstack111_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstack111_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstack111_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstack111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstack111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstack111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstack111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstack111_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack1l1l1111l_opy_ = [
  bstack111_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack111_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack111_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack111_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack1l1l1_opy_ = {
  bstack111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩࡐ"): [bstack111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩࡑ"), bstack111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡎࡂࡏࡈࠫࡒ")],
  bstack111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡓ"): bstack111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧࡔ"),
  bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࡕ"): bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩࡖ"),
  bstack111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࡗ"): bstack111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊ࠭ࡘ"),
  bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࡙ࠫ"): bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࡚ࠬ"),
  bstack111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰ࡛ࠫ"): bstack111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑ࡙࡟ࡑࡇࡕࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭࡜"),
  bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ࡝"): bstack111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ࡞"),
  bstack111_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬ࡟"): bstack111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ࡠ"),
  bstack111_opy_ (u"ࠪࡥࡵࡶࠧࡡ"): bstack111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ"),
  bstack111_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1l1llllll_opy_ = {
  bstack111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack111_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack111_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1lll1111_opy_ = {
  bstack111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack111_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack111_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack111_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack111_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack111_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack11ll1l_opy_ = [
  bstack111_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack111_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack111_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack111_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack111_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack111_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack111_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack111_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack1l111ll_opy_ = [
  bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack111_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
]
bstack1l1l11_opy_ = [
  bstack111_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬࢫ"),
  bstack111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪࢬ"),
  bstack111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࢭ"),
  bstack111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࢮ"),
  bstack111_opy_ (u"ࠫࡹ࡫ࡳࡵࡒࡵ࡭ࡴࡸࡩࡵࡻࠪࢯ"),
  bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨࢰ"),
  bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡧࡧࠨࢱ"),
  bstack111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬࢲ"),
  bstack111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢳ"),
  bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧࢴ"),
  bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫࢵ"),
  bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪࢶ"),
  bstack111_opy_ (u"ࠬࡵࡳࠨࢷ"),
  bstack111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢸ"),
  bstack111_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭ࢹ"),
  bstack111_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪࢺ"),
  bstack111_opy_ (u"ࠩࡵࡩ࡬࡯࡯࡯ࠩࢻ"),
  bstack111_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬࢼ"),
  bstack111_opy_ (u"ࠫࡲࡧࡣࡩ࡫ࡱࡩࠬࢽ"),
  bstack111_opy_ (u"ࠬࡸࡥࡴࡱ࡯ࡹࡹ࡯࡯࡯ࠩࢾ"),
  bstack111_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࢿ"),
  bstack111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡏࡳ࡫ࡨࡲࡹࡧࡴࡪࡱࡱࠫࣀ"),
  bstack111_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࠧࣁ"),
  bstack111_opy_ (u"ࠩࡱࡳࡕࡧࡧࡦࡎࡲࡥࡩ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ࣂ"),
  bstack111_opy_ (u"ࠪࡦ࡫ࡩࡡࡤࡪࡨࠫࣃ"),
  bstack111_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪࣄ"),
  bstack111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩࣅ"),
  bstack111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧࣆ"),
  bstack111_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫࣇ"),
  bstack111_opy_ (u"ࠨࡰࡲࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠬࣈ"),
  bstack111_opy_ (u"ࠩࡦ࡬ࡪࡩ࡫ࡖࡔࡏࠫࣉ"),
  bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊"),
  bstack111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡇࡴࡵ࡫ࡪࡧࡶࠫ࣋"),
  bstack111_opy_ (u"ࠬࡩࡡࡱࡶࡸࡶࡪࡉࡲࡢࡵ࡫ࠫ࣌"),
  bstack111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ࣍"),
  bstack111_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ࣎"),
  bstack111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡛࡫ࡲࡴ࡫ࡲࡲ࣏ࠬ"),
  bstack111_opy_ (u"ࠩࡱࡳࡇࡲࡡ࡯࡭ࡓࡳࡱࡲࡩ࡯ࡩ࣐ࠪ"),
  bstack111_opy_ (u"ࠪࡱࡦࡹ࡫ࡔࡧࡱࡨࡐ࡫ࡹࡴ࣑ࠩ"),
  bstack111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡐࡴ࡭ࡳࠨ࣒"),
  bstack111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡎࡪ࣓ࠧ"),
  bstack111_opy_ (u"࠭ࡤࡦࡦ࡬ࡧࡦࡺࡥࡥࡆࡨࡺ࡮ࡩࡥࠨࣔ"),
  bstack111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡐࡢࡴࡤࡱࡸ࠭ࣕ"),
  bstack111_opy_ (u"ࠨࡲ࡫ࡳࡳ࡫ࡎࡶ࡯ࡥࡩࡷ࠭ࣖ"),
  bstack111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࣗ"),
  bstack111_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡐࡲࡷ࡭ࡴࡴࡳࠨࣘ"),
  bstack111_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩࣙ"),
  bstack111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬࣚ"),
  bstack111_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲࡒ࡯ࡨࡵࠪࣛ"),
  bstack111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡂࡪࡱࡰࡩࡹࡸࡩࡤࠩࣜ"),
  bstack111_opy_ (u"ࠨࡸ࡬ࡨࡪࡵࡖ࠳ࠩࣝ"),
  bstack111_opy_ (u"ࠩࡰ࡭ࡩ࡙ࡥࡴࡵ࡬ࡳࡳࡏ࡮ࡴࡶࡤࡰࡱࡇࡰࡱࡵࠪࣞ"),
  bstack111_opy_ (u"ࠪࡩࡸࡶࡲࡦࡵࡶࡳࡘ࡫ࡲࡷࡧࡵࠫࣟ"),
  bstack111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪ࣠"),
  bstack111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡃࡥࡲࠪ࣡"),
  bstack111_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭࣢"),
  bstack111_opy_ (u"ࠧࡴࡻࡱࡧ࡙࡯࡭ࡦ࡙࡬ࡸ࡭ࡔࡔࡑࣣࠩ"),
  bstack111_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ࣤ"),
  bstack111_opy_ (u"ࠩࡪࡴࡸࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack111_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡔࡷࡵࡦࡪ࡮ࡨࣦࠫ"),
  bstack111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫࣧ"),
  bstack111_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡇ࡭ࡧ࡮ࡨࡧࡍࡥࡷ࠭ࣨ"),
  bstack111_opy_ (u"࠭ࡸ࡮ࡵࡍࡥࡷࣩ࠭"),
  bstack111_opy_ (u"ࠧࡹ࡯ࡻࡎࡦࡸࠧ࣪"),
  bstack111_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ࣫"),
  bstack111_opy_ (u"ࠩࡰࡥࡸࡱࡂࡢࡵ࡬ࡧࡆࡻࡴࡩࠩ࣬"),
  bstack111_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷ࣭ࠫ"),
  bstack111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡈࡵࡲࡴࡔࡨࡷࡹࡸࡩࡤࡶ࡬ࡳࡳࡹ࣮ࠧ"),
  bstack111_opy_ (u"ࠬࡧࡰࡱࡘࡨࡶࡸ࡯࡯࡯࣯ࠩ"),
  bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࣰࠬ"),
  bstack111_opy_ (u"ࠧࡳࡧࡶ࡭࡬ࡴࡁࡱࡲࣱࠪ"),
  bstack111_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࡷࣲࠬ"),
  bstack111_opy_ (u"ࠩࡦࡥࡳࡧࡲࡺࠩࣳ"),
  bstack111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫࣴ"),
  bstack111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫࣵ"),
  bstack111_opy_ (u"ࠬ࡯ࡥࠨࣶ"),
  bstack111_opy_ (u"࠭ࡥࡥࡩࡨࠫࣷ"),
  bstack111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧࣸ"),
  bstack111_opy_ (u"ࠨࡳࡸࡩࡺ࡫ࣹࠧ"),
  bstack111_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࣺࠫ"),
  bstack111_opy_ (u"ࠪࡥࡵࡶࡓࡵࡱࡵࡩࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠫࣻ"),
  bstack111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡇࡦࡳࡥࡳࡣࡌࡱࡦ࡭ࡥࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪࣼ"),
  bstack111_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࡈࡼࡨࡲࡵࡥࡧࡋࡳࡸࡺࡳࠨࣽ"),
  bstack111_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡍࡳࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack111_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡁࡱࡲࡖࡩࡹࡺࡩ࡯ࡩࡶࠫࣿ"),
  bstack111_opy_ (u"ࠨࡴࡨࡷࡪࡸࡶࡦࡆࡨࡺ࡮ࡩࡥࠨऀ"),
  bstack111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩँ"),
  bstack111_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬं"),
  bstack111_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡔࡦࡹࡳࡤࡱࡧࡩࠬः"),
  bstack111_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡎࡵࡳࡅࡧࡹ࡭ࡨ࡫ࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨऄ"),
  bstack111_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡵࡥ࡫ࡲࡍࡳࡰࡥࡤࡶ࡬ࡳࡳ࠭अ"),
  bstack111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡱࡲ࡯ࡩࡕࡧࡹࠨआ"),
  bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩइ"),
  bstack111_opy_ (u"ࠩࡺࡨ࡮ࡵࡓࡦࡴࡹ࡭ࡨ࡫ࠧई"),
  bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬउ"),
  bstack111_opy_ (u"ࠫࡵࡸࡥࡷࡧࡱࡸࡈࡸ࡯ࡴࡵࡖ࡭ࡹ࡫ࡔࡳࡣࡦ࡯࡮ࡴࡧࠨऊ"),
  bstack111_opy_ (u"ࠬ࡮ࡩࡨࡪࡆࡳࡳࡺࡲࡢࡵࡷࠫऋ"),
  bstack111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡖࡲࡦࡨࡨࡶࡪࡴࡣࡦࡵࠪऌ"),
  bstack111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡓࡪ࡯ࠪऍ"),
  bstack111_opy_ (u"ࠨࡵ࡬ࡱࡔࡶࡴࡪࡱࡱࡷࠬऎ"),
  bstack111_opy_ (u"ࠩࡵࡩࡲࡵࡶࡦࡋࡒࡗࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࡎࡲࡧࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠧए"),
  bstack111_opy_ (u"ࠪ࡬ࡴࡹࡴࡏࡣࡰࡩࠬऐ"),
  bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ"),
  bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧऒ"),
  bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬओ"),
  bstack111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩऔ"),
  bstack111_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫक"),
  bstack111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨख"),
  bstack111_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬग"),
  bstack111_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧघ")
]
bstack11111111_opy_ = {
  bstack111_opy_ (u"ࠬࡼࠧङ"): bstack111_opy_ (u"࠭ࡶࠨच"),
  bstack111_opy_ (u"ࠧࡧࠩछ"): bstack111_opy_ (u"ࠨࡨࠪज"),
  bstack111_opy_ (u"ࠩࡩࡳࡷࡩࡥࠨझ"): bstack111_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"),
  bstack111_opy_ (u"ࠫࡴࡴ࡬ࡺࡣࡸࡸࡴࡳࡡࡵࡧࠪट"): bstack111_opy_ (u"ࠬࡵ࡮࡭ࡻࡄࡹࡹࡵ࡭ࡢࡶࡨࠫठ"),
  bstack111_opy_ (u"࠭ࡦࡰࡴࡦࡩࡱࡵࡣࡢ࡮ࠪड"): bstack111_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"),
  bstack111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫण"): bstack111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬत"),
  bstack111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭थ"): bstack111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧद"),
  bstack111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨध"): bstack111_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩन"),
  bstack111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶࡡࡴࡵࠪऩ"): bstack111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫप"),
  bstack111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾ࡮࡯ࡴࡶࠪफ"): bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡈࡰࡵࡷࠫब"),
  bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡱࡵࡸࠬभ"): bstack111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭म"),
  bstack111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧय"): bstack111_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩर"),
  bstack111_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡻࡳࡦࡴࠪऱ"): bstack111_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡕࡴࡧࡵࠫल"),
  bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫळ"): bstack111_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ऴ"),
  bstack111_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧव"): bstack111_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡔࡦࡹࡳࠨश"),
  bstack111_opy_ (u"ࠧࡣ࡫ࡱࡥࡷࡿࡰࡢࡶ࡫ࠫष"): bstack111_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"),
  bstack111_opy_ (u"ࠩࡳࡥࡨ࡬ࡩ࡭ࡧࠪह"): bstack111_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ऺ"),
  bstack111_opy_ (u"ࠫࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ऻ"): bstack111_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨ़"),
  bstack111_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"): bstack111_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"),
  bstack111_opy_ (u"ࠨ࡮ࡲ࡫࡫࡯࡬ࡦࠩि"): bstack111_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"),
  bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬु"): bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"),
}
bstack111l1l1l_opy_ = bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ृ")
bstack1111ll1_opy_ = bstack111_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩॄ")
bstack1ll1ll1l1_opy_ = {
  bstack111_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩॅ"): 50,
  bstack111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧॆ"): 40,
  bstack111_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪे"): 30,
  bstack111_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨै"): 20,
  bstack111_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪॉ"): 10
}
DEFAULT_LOG_LEVEL = bstack1ll1ll1l1_opy_[bstack111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ")]
bstack1l111l11_opy_ = bstack111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬो")
bstack1l1lll_opy_ = bstack111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬौ")
bstack11l111ll_opy_ = bstack111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1l1l11l1_opy_ = bstack111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨॎ")
bstack111ll1ll_opy_ = [bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫॏ"), bstack111_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫॐ")]
bstack1lllll1l_opy_ = [bstack111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ॑"), bstack111_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ॒")]
bstack111l_opy_ = [
  bstack111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡒࡦࡳࡥࠨ॓"),
  bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ॔"),
  bstack111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ॕ"),
  bstack111_opy_ (u"ࠪࡲࡪࡽࡃࡰ࡯ࡰࡥࡳࡪࡔࡪ࡯ࡨࡳࡺࡺࠧॖ"),
  bstack111_opy_ (u"ࠫࡦࡶࡰࠨॗ"),
  bstack111_opy_ (u"ࠬࡻࡤࡪࡦࠪक़"),
  bstack111_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨख़"),
  bstack111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࠧग़"),
  bstack111_opy_ (u"ࠨࡱࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭ज़"),
  bstack111_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࠧड़"),
  bstack111_opy_ (u"ࠪࡲࡴࡘࡥࡴࡧࡷࠫढ़"), bstack111_opy_ (u"ࠫ࡫ࡻ࡬࡭ࡔࡨࡷࡪࡺࠧफ़"),
  bstack111_opy_ (u"ࠬࡩ࡬ࡦࡣࡵࡗࡾࡹࡴࡦ࡯ࡉ࡭ࡱ࡫ࡳࠨय़"),
  bstack111_opy_ (u"࠭ࡥࡷࡧࡱࡸ࡙࡯࡭ࡪࡰࡪࡷࠬॠ"),
  bstack111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡐࡦࡴࡩࡳࡷࡳࡡ࡯ࡥࡨࡐࡴ࡭ࡧࡪࡰࡪࠫॡ"),
  bstack111_opy_ (u"ࠨࡱࡷ࡬ࡪࡸࡁࡱࡲࡶࠫॢ"),
  bstack111_opy_ (u"ࠩࡳࡶ࡮ࡴࡴࡑࡣࡪࡩࡘࡵࡵࡳࡥࡨࡓࡳࡌࡩ࡯ࡦࡉࡥ࡮ࡲࡵࡳࡧࠪॣ"),
  bstack111_opy_ (u"ࠪࡥࡵࡶࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨ।"), bstack111_opy_ (u"ࠫࡦࡶࡰࡑࡣࡦ࡯ࡦ࡭ࡥࠨ॥"), bstack111_opy_ (u"ࠬࡧࡰࡱ࡙ࡤ࡭ࡹࡇࡣࡵ࡫ࡹ࡭ࡹࡿࠧ०"), bstack111_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡐࡢࡥ࡮ࡥ࡬࡫ࠧ१"), bstack111_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡅࡷࡵࡥࡹ࡯࡯࡯ࠩ२"),
  bstack111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭३"),
  bstack111_opy_ (u"ࠩࡤࡰࡱࡵࡷࡕࡧࡶࡸࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭४"),
  bstack111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡇࡴࡼࡥࡳࡣࡪࡩࠬ५"), bstack111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪࡋ࡮ࡥࡋࡱࡸࡪࡴࡴࠨ६"),
  bstack111_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡊࡥࡷ࡫ࡦࡩࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪ७"),
  bstack111_opy_ (u"࠭ࡡࡥࡤࡓࡳࡷࡺࠧ८"),
  bstack111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡓࡰࡥ࡮ࡩࡹ࠭९"),
  bstack111_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡋࡱࡷࡹࡧ࡬࡭ࡖ࡬ࡱࡪࡵࡵࡵࠩ॰"),
  bstack111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡓࡥࡹ࡮ࠧॱ"),
  bstack111_opy_ (u"ࠪࡥࡻࡪࠧॲ"), bstack111_opy_ (u"ࠫࡦࡼࡤࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧॳ"), bstack111_opy_ (u"ࠬࡧࡶࡥࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧॴ"), bstack111_opy_ (u"࠭ࡡࡷࡦࡄࡶ࡬ࡹࠧॵ"),
  bstack111_opy_ (u"ࠧࡶࡵࡨࡏࡪࡿࡳࡵࡱࡵࡩࠬॶ"), bstack111_opy_ (u"ࠨ࡭ࡨࡽࡸࡺ࡯ࡳࡧࡓࡥࡹ࡮ࠧॷ"), bstack111_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡹࡳࡸࡱࡵࡨࠬॸ"),
  bstack111_opy_ (u"ࠪ࡯ࡪࡿࡁ࡭࡫ࡤࡷࠬॹ"), bstack111_opy_ (u"ࠫࡰ࡫ࡹࡑࡣࡶࡷࡼࡵࡲࡥࠩॺ"),
  bstack111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧॻ"), bstack111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡆࡸࡧࡴࠩॼ"), bstack111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࡆ࡬ࡶࠬॽ"), bstack111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡃࡩࡴࡲࡱࡪࡓࡡࡱࡲ࡬ࡲ࡬ࡌࡩ࡭ࡧࠪॾ"), bstack111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡖࡵࡨࡗࡾࡹࡴࡦ࡯ࡈࡼࡪࡩࡵࡵࡣࡥࡰࡪ࠭ॿ"),
  bstack111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡒࡲࡶࡹ࠭ঀ"), bstack111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࡳࠨঁ"),
  bstack111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡈ࡮ࡹࡡࡣ࡮ࡨࡆࡺ࡯࡬ࡥࡅ࡫ࡩࡨࡱࠧং"),
  bstack111_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡪࡨࡶࡪࡧࡺࡘ࡮ࡳࡥࡰࡷࡷࠫঃ"),
  bstack111_opy_ (u"ࠧࡪࡰࡷࡩࡳࡺࡁࡤࡶ࡬ࡳࡳ࠭঄"), bstack111_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡄࡣࡷࡩ࡬ࡵࡲࡺࠩঅ"), bstack111_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡈ࡯ࡥ࡬ࡹࠧআ"), bstack111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡤࡰࡎࡴࡴࡦࡰࡷࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ই"),
  bstack111_opy_ (u"ࠫࡩࡵ࡮ࡵࡕࡷࡳࡵࡇࡰࡱࡑࡱࡖࡪࡹࡥࡵࠩঈ"),
  bstack111_opy_ (u"ࠬࡻ࡮ࡪࡥࡲࡨࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧউ"), bstack111_opy_ (u"࠭ࡲࡦࡵࡨࡸࡐ࡫ࡹࡣࡱࡤࡶࡩ࠭ঊ"),
  bstack111_opy_ (u"ࠧ࡯ࡱࡖ࡭࡬ࡴࠧঋ"),
  bstack111_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࡖࡰ࡬ࡱࡵࡵࡲࡵࡣࡱࡸ࡛࡯ࡥࡸࡵࠪঌ"),
  bstack111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲࡩࡸ࡯ࡪࡦ࡚ࡥࡹࡩࡨࡦࡴࡶࠫ঍"),
  bstack111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ঎"),
  bstack111_opy_ (u"ࠫࡷ࡫ࡣࡳࡧࡤࡸࡪࡉࡨࡳࡱࡰࡩࡉࡸࡩࡷࡧࡵࡗࡪࡹࡳࡪࡱࡱࡷࠬএ"),
  bstack111_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫঐ"),
  bstack111_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡓࡤࡴࡨࡩࡳࡹࡨࡰࡶࡓࡥࡹ࡮ࠧ঑"),
  bstack111_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡔࡲࡨࡩࡩ࠭঒"),
  bstack111_opy_ (u"ࠨࡩࡳࡷࡊࡴࡡࡣ࡮ࡨࡨࠬও"),
  bstack111_opy_ (u"ࠩ࡬ࡷࡍ࡫ࡡࡥ࡮ࡨࡷࡸ࠭ঔ"),
  bstack111_opy_ (u"ࠪࡥࡩࡨࡅࡹࡧࡦࡘ࡮ࡳࡥࡰࡷࡷࠫক"),
  bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡨࡗࡨࡸࡩࡱࡶࠪখ"),
  bstack111_opy_ (u"ࠬࡹ࡫ࡪࡲࡇࡩࡻ࡯ࡣࡦࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠩগ"),
  bstack111_opy_ (u"࠭ࡡࡶࡶࡲࡋࡷࡧ࡮ࡵࡒࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠭ঘ"),
  bstack111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡏࡣࡷࡹࡷࡧ࡬ࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬঙ"),
  bstack111_opy_ (u"ࠨࡵࡼࡷࡹ࡫࡭ࡑࡱࡵࡸࠬচ"),
  bstack111_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡧࡦࡍࡵࡳࡵࠩছ"),
  bstack111_opy_ (u"ࠪࡷࡰ࡯ࡰࡖࡰ࡯ࡳࡨࡱࠧজ"), bstack111_opy_ (u"ࠫࡺࡴ࡬ࡰࡥ࡮ࡘࡾࡶࡥࠨঝ"), bstack111_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯ࡐ࡫ࡹࠨঞ"),
  bstack111_opy_ (u"࠭ࡡࡶࡶࡲࡐࡦࡻ࡮ࡤࡪࠪট"),
  bstack111_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡤࡣࡷࡇࡦࡶࡴࡶࡴࡨࠫঠ"),
  bstack111_opy_ (u"ࠨࡷࡱ࡭ࡳࡹࡴࡢ࡮࡯ࡓࡹ࡮ࡥࡳࡒࡤࡧࡰࡧࡧࡦࡵࠪড"),
  bstack111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧ࡚࡭ࡳࡪ࡯ࡸࡃࡱ࡭ࡲࡧࡴࡪࡱࡱࠫঢ"),
  bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡲࡳࡱࡹࡖࡦࡴࡶ࡭ࡴࡴࠧণ"),
  bstack111_opy_ (u"ࠫࡪࡴࡦࡰࡴࡦࡩࡆࡶࡰࡊࡰࡶࡸࡦࡲ࡬ࠨত"),
  bstack111_opy_ (u"ࠬ࡫࡮ࡴࡷࡵࡩ࡜࡫ࡢࡷ࡫ࡨࡻࡸࡎࡡࡷࡧࡓࡥ࡬࡫ࡳࠨথ"), bstack111_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࡄࡦࡸࡷࡳࡴࡲࡳࡑࡱࡵࡸࠬদ"), bstack111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡄࡦࡶࡤ࡭ࡱࡹࡃࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠪধ"),
  bstack111_opy_ (u"ࠨࡴࡨࡱࡴࡺࡥࡂࡲࡳࡷࡈࡧࡣࡩࡧࡏ࡭ࡲ࡯ࡴࠨন"),
  bstack111_opy_ (u"ࠩࡦࡥࡱ࡫࡮ࡥࡣࡵࡊࡴࡸ࡭ࡢࡶࠪ঩"),
  bstack111_opy_ (u"ࠪࡦࡺࡴࡤ࡭ࡧࡌࡨࠬপ"),
  bstack111_opy_ (u"ࠫࡱࡧࡵ࡯ࡥ࡫ࡘ࡮ࡳࡥࡰࡷࡷࠫফ"),
  bstack111_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࡓࡦࡴࡹ࡭ࡨ࡫ࡳࡆࡰࡤࡦࡱ࡫ࡤࠨব"), bstack111_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡃࡸࡸ࡭ࡵࡲࡪࡼࡨࡨࠬভ"),
  bstack111_opy_ (u"ࠧࡢࡷࡷࡳࡆࡩࡣࡦࡲࡷࡅࡱ࡫ࡲࡵࡵࠪম"), bstack111_opy_ (u"ࠨࡣࡸࡸࡴࡊࡩࡴ࡯࡬ࡷࡸࡇ࡬ࡦࡴࡷࡷࠬয"),
  bstack111_opy_ (u"ࠩࡱࡥࡹ࡯ࡶࡦࡋࡱࡷࡹࡸࡵ࡮ࡧࡱࡸࡸࡒࡩࡣࠩর"),
  bstack111_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧ࡚ࡩࡧ࡚ࡡࡱࠩ঱"),
  bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡍࡳ࡯ࡴࡪࡣ࡯࡙ࡷࡲࠧল"), bstack111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡆࡲ࡬ࡰࡹࡓࡳࡵࡻࡰࡴࠩ঳"), bstack111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏࡧ࡯ࡱࡵࡩࡋࡸࡡࡶࡦ࡚ࡥࡷࡴࡩ࡯ࡩࠪ঴"), bstack111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡧࡱࡐ࡮ࡴ࡫ࡴࡋࡱࡆࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠧ঵"),
  bstack111_opy_ (u"ࠨ࡭ࡨࡩࡵࡑࡥࡺࡅ࡫ࡥ࡮ࡴࡳࠨশ"),
  bstack111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡪࡼࡤࡦࡱ࡫ࡓࡵࡴ࡬ࡲ࡬ࡹࡄࡪࡴࠪষ"),
  bstack111_opy_ (u"ࠪࡴࡷࡵࡣࡦࡵࡶࡅࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭স"),
  bstack111_opy_ (u"ࠫ࡮ࡴࡴࡦࡴࡎࡩࡾࡊࡥ࡭ࡣࡼࠫহ"),
  bstack111_opy_ (u"ࠬࡹࡨࡰࡹࡌࡓࡘࡒ࡯ࡨࠩ঺"),
  bstack111_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡓࡵࡴࡤࡸࡪ࡭ࡹࠨ঻"),
  bstack111_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡒࡦࡵࡳࡳࡳࡹࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ়"), bstack111_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸ࡜ࡧࡩࡵࡖ࡬ࡱࡪࡵࡵࡵࠩঽ"),
  bstack111_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡆࡨࡦࡺ࡭ࡐࡳࡱࡻࡽࠬা"),
  bstack111_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡷࡾࡴࡣࡆࡺࡨࡧࡺࡺࡥࡇࡴࡲࡱࡍࡺࡴࡱࡵࠪি"),
  bstack111_opy_ (u"ࠫࡸࡱࡩࡱࡎࡲ࡫ࡈࡧࡰࡵࡷࡵࡩࠬী"),
  bstack111_opy_ (u"ࠬࡽࡥࡣ࡭࡬ࡸࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࡑࡱࡵࡸࠬু"),
  bstack111_opy_ (u"࠭ࡦࡶ࡮࡯ࡇࡴࡴࡴࡦࡺࡷࡐ࡮ࡹࡴࠨূ"),
  bstack111_opy_ (u"ࠧࡸࡣ࡬ࡸࡋࡵࡲࡂࡲࡳࡗࡨࡸࡩࡱࡶࠪৃ"),
  bstack111_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡅࡲࡲࡳ࡫ࡣࡵࡔࡨࡸࡷ࡯ࡥࡴࠩৄ"),
  bstack111_opy_ (u"ࠩࡤࡴࡵࡔࡡ࡮ࡧࠪ৅"),
  bstack111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡗࡑࡉࡥࡳࡶࠪ৆"),
  bstack111_opy_ (u"ࠫࡹࡧࡰࡘ࡫ࡷ࡬ࡘ࡮࡯ࡳࡶࡓࡶࡪࡹࡳࡅࡷࡵࡥࡹ࡯࡯࡯ࠩে"),
  bstack111_opy_ (u"ࠬࡹࡣࡢ࡮ࡨࡊࡦࡩࡴࡰࡴࠪৈ"),
  bstack111_opy_ (u"࠭ࡷࡥࡣࡏࡳࡨࡧ࡬ࡑࡱࡵࡸࠬ৉"),
  bstack111_opy_ (u"ࠧࡴࡪࡲࡻ࡝ࡩ࡯ࡥࡧࡏࡳ࡬࠭৊"),
  bstack111_opy_ (u"ࠨ࡫ࡲࡷࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡵࡴࡧࠪো"),
  bstack111_opy_ (u"ࠩࡻࡧࡴࡪࡥࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠫৌ"),
  bstack111_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡳࡴࡹࡲࡶࡩ্࠭"),
  bstack111_opy_ (u"ࠫࡺࡹࡥࡑࡴࡨࡦࡺ࡯࡬ࡵ࡙ࡇࡅࠬৎ"),
  bstack111_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹ࡝ࡄࡂࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠭৏"),
  bstack111_opy_ (u"࠭ࡷࡦࡤࡇࡶ࡮ࡼࡥࡳࡃࡪࡩࡳࡺࡕࡳ࡮ࠪ৐"),
  bstack111_opy_ (u"ࠧ࡬ࡧࡼࡧ࡭ࡧࡩ࡯ࡒࡤࡸ࡭࠭৑"),
  bstack111_opy_ (u"ࠨࡷࡶࡩࡓ࡫ࡷࡘࡆࡄࠫ৒"),
  bstack111_opy_ (u"ࠩࡺࡨࡦࡒࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ৓"), bstack111_opy_ (u"ࠪࡻࡩࡧࡃࡰࡰࡱࡩࡨࡺࡩࡰࡰࡗ࡭ࡲ࡫࡯ࡶࡶࠪ৔"),
  bstack111_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡒࡶ࡬ࡏࡤࠨ৕"), bstack111_opy_ (u"ࠬࡾࡣࡰࡦࡨࡗ࡮࡭࡮ࡪࡰࡪࡍࡩ࠭৖"),
  bstack111_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪࡗࡅࡃࡅࡹࡳࡪ࡬ࡦࡋࡧࠫৗ"),
  bstack111_opy_ (u"ࠧࡳࡧࡶࡩࡹࡕ࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡶࡹࡕ࡮࡭ࡻࠪ৘"),
  bstack111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࡵࠪ৙"),
  bstack111_opy_ (u"ࠩࡺࡨࡦ࡙ࡴࡢࡴࡷࡹࡵࡘࡥࡵࡴ࡬ࡩࡸ࠭৚"), bstack111_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵࡽࡎࡴࡴࡦࡴࡹࡥࡱ࠭৛"),
  bstack111_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࡍࡧࡲࡥࡹࡤࡶࡪࡑࡥࡺࡤࡲࡥࡷࡪࠧড়"),
  bstack111_opy_ (u"ࠬࡳࡡࡹࡖࡼࡴ࡮ࡴࡧࡇࡴࡨࡵࡺ࡫࡮ࡤࡻࠪঢ়"),
  bstack111_opy_ (u"࠭ࡳࡪ࡯ࡳࡰࡪࡏࡳࡗ࡫ࡶ࡭ࡧࡲࡥࡄࡪࡨࡧࡰ࠭৞"),
  bstack111_opy_ (u"ࠧࡶࡵࡨࡇࡦࡸࡴࡩࡣࡪࡩࡘࡹ࡬ࠨয়"),
  bstack111_opy_ (u"ࠨࡵ࡫ࡳࡺࡲࡤࡖࡵࡨࡗ࡮ࡴࡧ࡭ࡧࡷࡳࡳ࡚ࡥࡴࡶࡐࡥࡳࡧࡧࡦࡴࠪৠ"),
  bstack111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡊ࡙ࡇࡔࠬৡ"),
  bstack111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡲࡹࡨ࡮ࡉࡥࡇࡱࡶࡴࡲ࡬ࠨৢ"),
  bstack111_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࡌ࡮ࡪࡤࡦࡰࡄࡴ࡮ࡖ࡯࡭࡫ࡦࡽࡊࡸࡲࡰࡴࠪৣ"),
  bstack111_opy_ (u"ࠬࡳ࡯ࡤ࡭ࡏࡳࡨࡧࡴࡪࡱࡱࡅࡵࡶࠧ৤"),
  bstack111_opy_ (u"࠭࡬ࡰࡩࡦࡥࡹࡌ࡯ࡳ࡯ࡤࡸࠬ৥"), bstack111_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡪ࡮ࡷࡩࡷ࡙ࡰࡦࡥࡶࠫ০"),
  bstack111_opy_ (u"ࠨࡣ࡯ࡰࡴࡽࡄࡦ࡮ࡤࡽࡆࡪࡢࠨ১")
]
bstack1l11l111_opy_ = bstack111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡷࡳࡰࡴࡧࡤࠨ২")
bstack1lll111l_opy_ = [bstack111_opy_ (u"ࠪ࠲ࡦࡶ࡫ࠨ৩"), bstack111_opy_ (u"ࠫ࠳ࡧࡡࡣࠩ৪"), bstack111_opy_ (u"ࠬ࠴ࡩࡱࡣࠪ৫")]
bstack1l1ll1_opy_ = [bstack111_opy_ (u"࠭ࡩࡥࠩ৬"), bstack111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৭"), bstack111_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ৮"), bstack111_opy_ (u"ࠩࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤࠨ৯")]
bstack1lll11111_opy_ = {
  bstack111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪৰ"): bstack111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩৱ"),
  bstack111_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৲"): bstack111_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack111_opy_ (u"ࠧࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ৴"): bstack111_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৵"),
  bstack111_opy_ (u"ࠩ࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ৶"): bstack111_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৷"),
  bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࡓࡵࡺࡩࡰࡰࡶࠫ৸"): bstack111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭৹")
}
bstack1ll11llll_opy_ = [
  bstack111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৺"),
  bstack111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ৻"),
  bstack111_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩৼ"),
  bstack111_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ৽"),
  bstack111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ৾"),
]
bstack1l1l1ll1l_opy_ = bstack1l111ll_opy_ + bstack1l1l11_opy_ + bstack111l_opy_
bstack1lll11_opy_ = [
  bstack111_opy_ (u"ࠫࡣࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴࠥࠩ৿"),
  bstack111_opy_ (u"ࠬࡤࡢࡴ࠯࡯ࡳࡨࡧ࡬࠯ࡥࡲࡱࠩ࠭਀"),
  bstack111_opy_ (u"࠭࡞࠲࠴࠺࠲ࠬਁ"),
  bstack111_opy_ (u"ࠧ࡟࠳࠳࠲ࠬਂ"),
  bstack111_opy_ (u"ࠨࡠ࠴࠻࠷࠴࠱࡜࠸࠰࠽ࡢ࠴ࠧਃ"),
  bstack111_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠳࡝࠳࠱࠾ࡣ࠮ࠨ਄"),
  bstack111_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠵࡞࠴࠲࠷࡝࠯ࠩਅ"),
  bstack111_opy_ (u"ࠫࡣ࠷࠹࠳࠰࠴࠺࠽࠴ࠧਆ")
]
bstack1llllll1_opy_ = bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾࠩਇ")
bstack111llll_opy_ = bstack111_opy_ (u"࠭ࡳࡥ࡭࠲ࡺ࠶࠵ࡥࡷࡧࡱࡸࠬਈ")
bstack1l1l1l1ll_opy_ = [ bstack111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩਉ") ]
bstack1ll1lllll_opy_ = [ bstack111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧਊ") ]
bstack1lll1llll_opy_ = [ bstack111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ਋") ]
bstack11l11l_opy_ = bstack111_opy_ (u"ࠪࡗࡉࡑࡓࡦࡶࡸࡴࠬ਌")
bstack1ll1ll1ll_opy_ = bstack111_opy_ (u"ࠫࡘࡊࡋࡕࡧࡶࡸࡆࡺࡴࡦ࡯ࡳࡸࡪࡪࠧ਍")
bstack1lll11l1l_opy_ = bstack111_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹ࡙ࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠩ਎")
bstack1l1l1llll_opy_ = bstack111_opy_ (u"࠭࠴࠯࠲࠱࠴ࠬਏ")
bstack11l11lll_opy_ = bstack111_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠽ࠤࢀࢃࠧਐ")
bstack1ll1l111_opy_ = bstack111_opy_ (u"ࠨࡅࡲࡱࡵࡲࡥࡵࡧࡧࠤࡸ࡫ࡴࡶࡲࠤࠫ਑")
bstack1llll1l1_opy_ = bstack111_opy_ (u"ࠩࡓࡥࡷࡹࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠫ਒")
bstack1lll111l1_opy_ = bstack111_opy_ (u"ࠪࡗࡦࡴࡩࡵ࡫ࡽࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠨਓ")
bstack1l11ll11_opy_ = bstack111_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣ࡬ࡺࡨࠠࡶࡴ࡯࠾ࠥࢁࡽࠨਔ")
bstack1lllll1_opy_ = bstack111_opy_ (u"࡙ࠬࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࡾࢁࠬਕ")
bstack1ll11l11l_opy_ = bstack111_opy_ (u"࠭ࡒࡦࡥࡨ࡭ࡻ࡫ࡤࠡ࡫ࡱࡸࡪࡸࡲࡶࡲࡷ࠰ࠥ࡫ࡸࡪࡶ࡬ࡲ࡬࠭ਖ")
bstack1ll11l1l_opy_ = bstack111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬਗ")
bstack11l11l11_opy_ = bstack111_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡤࡲࡩࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡲࡤࡧࡰࡧࡧࡦࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡴࡾࡺࡥࡴࡶ࠰ࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭ਘ")
bstack1l1lll1l_opy_ = bstack111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵ࠮ࠣࡴࡦࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࡵࡧࡲࡢ࡮࡯ࡩࡱ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡲࡤࡦࡴࡺࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࡣࠫਙ")
bstack1llllll11_opy_ = bstack111_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࡣࠫਚ")
bstack1llll11_opy_ = bstack111_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡧࡰࡱ࡫ࡸࡱ࠲ࡩ࡬ࡪࡧࡱࡸࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡆࡶࡰࡪࡷࡰ࠱ࡕࡿࡴࡩࡱࡱ࠱ࡈࡲࡩࡦࡰࡷࡤࠬਛ")
bstack1l11lll1l_opy_ = bstack111_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡦࠧਜ")
bstack111lll_opy_ = bstack111_opy_ (u"࠭ࡈࡢࡰࡧࡰ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡰࡴࡹࡥࠨਝ")
bstack1ll1l1lll_opy_ = bstack111_opy_ (u"ࠧࡂ࡮࡯ࠤࡩࡵ࡮ࡦࠣࠪਞ")
bstack1l1ll1ll_opy_ = bstack111_opy_ (u"ࠨࡅࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࠠࡢࡶࠣࡥࡳࡿࠠࡱࡣࡵࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡳ࡫ࠦࠢࡼࡿࠥ࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡤ࡮ࡸࡨࡪࠦࡡࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠡࡨ࡬ࡰࡪࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡧࡶࡸࡸ࠴ࠧਟ")
bstack11l1ll1l_opy_ = bstack111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡵࡩࡩ࡫࡮ࡵ࡫ࡤࡰࡸࠦ࡮ࡰࡶࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡡࡥࡦࠣࡸ࡭࡫࡭ࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩࠥࡧࡳࠡࠤࡸࡷࡪࡸࡎࡢ࡯ࡨࠦࠥࡧ࡮ࡥࠢࠥࡥࡨࡩࡥࡴࡵࡎࡩࡾࠨࠠࡰࡴࠣࡷࡪࡺࠠࡵࡪࡨࡱࠥࡧࡳࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴ࠼ࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧࠦࡡ࡯ࡦࠣࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠢࠨਠ")
bstack1l1l11l1l_opy_ = bstack111_opy_ (u"ࠪࡑࡦࡲࡦࡰࡴࡰࡩࡩࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠾ࠧࢁࡽࠣࠩਡ")
bstack1ll11_opy_ = bstack111_opy_ (u"ࠫࡊࡴࡣࡰࡷࡱࡸࡪࡸࡥࡥࠢࡨࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࠤ࠲ࠦࡻࡾࠩਢ")
bstack1l11lll1_opy_ = bstack111_opy_ (u"࡙ࠬࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠬਣ")
bstack1111ll_opy_ = bstack111_opy_ (u"࠭ࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ਤ")
bstack1ll1l1ll_opy_ = bstack111_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡌࡰࡥࡤࡰࠥ࡯ࡳࠡࡰࡲࡻࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠧࠧਥ")
bstack1lll1l11l_opy_ = bstack111_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࠣࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡏࡳࡨࡧ࡬࠻ࠢࡾࢁࠬਦ")
bstack11l1ll11_opy_ = bstack111_opy_ (u"ࠩࡖࡸࡦࡸࡴࡪࡰࡪࠤࡱࡵࡣࡢ࡮ࠣࡦ࡮ࡴࡡࡳࡻࠣࡻ࡮ࡺࡨࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࡿࢂ࠭ਧ")
bstack11ll1l1_opy_ = bstack111_opy_ (u"࡙ࠪࡵࡪࡡࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠫਨ")
bstack1ll11lll_opy_ = bstack111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠪ਩")
bstack111ll1_opy_ = bstack111_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࠦࡡ࡯ࠢࡤࡴࡵࡸ࡯ࡱࡴ࡬ࡥࡹ࡫ࠠࡇ࡙ࠣࠬࡷࡵࡢࡰࡶ࠲ࡴࡦࡨ࡯ࡵࠫࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨ࠰ࠥࡹ࡫ࡪࡲࠣࡸ࡭࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡯ࡪࡿࠠࡪࡰࠣࡧࡴࡴࡦࡪࡩࠣ࡭࡫ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡴ࡫ࡰࡴࡱ࡫ࠠࡱࡻࡷ࡬ࡴࡴࠠࡴࡥࡵ࡭ࡵࡺࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡣࡱࡽࠥࡌࡗ࠯ࠩਪ")
bstack1ll1l_opy_ = bstack111_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡩࡶࡷࡴࡕࡸ࡯ࡹࡻ࠲࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠠࡪࡵࠣࡲࡴࡺࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡳࡳࠦࡣࡶࡴࡵࡩࡳࡺ࡬ࡺࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࡯ࡧࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࠭ࢁࡽࠪ࠮ࠣࡴࡱ࡫ࡡࡴࡧࠣࡹࡵ࡭ࡲࡢࡦࡨࠤࡹࡵࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡀࡀ࠸࠳࠶࠮࠱ࠢࡲࡶࠥࡸࡥࡧࡧࡵࠤࡹࡵࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡰࡪࡴࡩࡶ࡯࠲ࡶࡺࡴ࠭ࡵࡧࡶࡸࡸ࠳ࡢࡦࡪ࡬ࡲࡩ࠳ࡰࡳࡱࡻࡽࠨࡶࡹࡵࡪࡲࡲࠥ࡬࡯ࡳࠢࡤࠤࡼࡵࡲ࡬ࡣࡵࡳࡺࡴࡤ࠯ࠩਫ")
bstack11ll11_opy_ = bstack111_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡽࡲࡲࠠࡧ࡫࡯ࡩ࠳࠴ࠧਬ")
bstack11l1111l_opy_ = bstack111_opy_ (u"ࠨࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡨࡧࡱࡩࡷࡧࡴࡦࡦࠣࡸ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧ࡫࡯ࡩࠦ࠭ਭ")
bstack11l11ll1_opy_ = bstack111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡪࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥ࠯ࠢࡾࢁࠬਮ")
bstack1ll1llll_opy_ = bstack111_opy_ (u"ࠪࡉࡽࡶࡥࡤࡶࡨࡨࠥࡧࡴࠡ࡮ࡨࡥࡸࡺࠠ࠲ࠢ࡬ࡲࡵࡻࡴ࠭ࠢࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࠵࠭ਯ")
bstack1lll1l_opy_ = bstack111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡨࡺࡸࡩ࡯ࡩࠣࡅࡵࡶࠠࡶࡲ࡯ࡳࡦࡪ࠮ࠡࡽࢀࠫਰ")
bstack1l1lll1l1_opy_ = bstack111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡃࡳࡴ࠳ࠦࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࢁࡽ࠯ࠩ਱")
bstack111ll1l1_opy_ = bstack111_opy_ (u"࠭ࡋࡦࡻࡶࠤࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࠭ࡦࡺ࡬ࡷࡹࠦࡡࡴࠢࡤࡴࡵࠦࡶࡢ࡮ࡸࡩࡸ࠲ࠠࡶࡵࡨࠤࡦࡴࡹࠡࡱࡱࡩࠥࡶࡲࡰࡲࡨࡶࡹࡿࠠࡧࡴࡲࡱࠥࢁࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡵࡧࡴࡩ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡨࡻࡳࡵࡱࡰࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡶ࡬ࡦࡸࡥࡢࡤ࡯ࡩࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿ࡿ࠯ࠤࡴࡴ࡬ࡺࠢࠥࡴࡦࡺࡨࠣࠢࡤࡲࡩࠦࠢࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠥࠤࡨࡧ࡮ࠡࡥࡲ࠱ࡪࡾࡩࡴࡶࠣࡸࡴ࡭ࡥࡵࡪࡨࡶ࠳࠭ਲ")
bstack1lll11l1_opy_ = bstack111_opy_ (u"ࠧ࡜ࡋࡱࡺࡦࡲࡩࡥࠢࡤࡴࡵࠦࡰࡳࡱࡳࡩࡷࡺࡹ࡞ࠢࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠢࡤࡶࡪࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩਲ਼")
bstack111l11ll_opy_ = bstack111_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡗࡺࡶࡰࡰࡴࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࡸࠦ࡯ࡧࠢࡤࡴࡵࠦࡡࡳࡧࠣࡳ࡫ࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠲ࠥࡌ࡯ࡳࠢࡰࡳࡷ࡫ࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡲ࡯ࡩࡦࡹࡥࠡࡸ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡦࡲࡧࡸ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡱ࡫ࡸࡱ࠴ࡹࡥࡵ࠯ࡸࡴ࠲ࡺࡥࡴࡶࡶ࠳ࡸࡶࡥࡤ࡫ࡩࡽ࠲ࡧࡰࡱࠩ਴")
bstack11111_opy_ = bstack111_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡵࡶࠠࡪࡦࠣࡿࢂࠦࡦࡰࡴࠣ࡬ࡦࡹࡨࠡ࠼ࠣࡿࢂ࠴ࠧਵ")
bstack1l1ll1ll1_opy_ = bstack111_opy_ (u"ࠪࡅࡵࡶࠠࡖࡲ࡯ࡳࡦࡪࡥࡥࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠢࡌࡈࠥࡀࠠࡼࡿࠪਸ਼")
bstack1l11l11l_opy_ = bstack111_opy_ (u"࡚ࠫࡹࡩ࡯ࡩࠣࡅࡵࡶࠠ࠻ࠢࡾࢁ࠳࠭਷")
bstack11lllll_opy_ = bstack111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡲࡶࠥࡼࡡ࡯࡫࡯ࡰࡦࠦࡰࡺࡶ࡫ࡳࡳࠦࡴࡦࡵࡷࡷ࠱ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶࡡࡳࡣ࡯ࡰࡪࡲࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠤࡂࠦ࠱ࠨਸ")
bstack111lll1_opy_ = bstack111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࠿ࠦࡻࡾࠩਹ")
bstack11111ll1_opy_ = bstack111_opy_ (u"ࠧࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴ࠽ࠤࢀࢃࠧ਺")
bstack11lll11l_opy_ = bstack111_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤ࡬࡫ࡴࠡࡴࡨࡥࡸࡵ࡮ࠡࡨࡲࡶࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫࠮ࠡࡽࢀࠫ਻")
bstack1ll1l11l1_opy_ = bstack111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡣࡳ࡭ࠥࡩࡡ࡭࡮࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࢀࢃ਼ࠧ")
bstack1111l1ll_opy_ = bstack111_opy_ (u"࡙ࠪࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡩࡱࡺࠤࡧࡻࡩ࡭ࡦ࡙ࠣࡗࡒࠬࠡࡣࡶࠤࡧࡻࡩ࡭ࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠࡪࡵࠣࡲࡴࡺࠠࡶࡵࡨࡨ࠳࠭਽")
bstack11llll1l_opy_ = bstack111_opy_ (u"ࠫࡘ࡫ࡲࡷࡧࡵࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡶࡥࡲ࡫ࠠࡢࡵࠣࡧࡱ࡯ࡥ࡯ࡶࠣࡷ࡮ࡪࡥࠡࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠬࢀࢃࠩࠨਾ")
bstack1ll1111l_opy_ = bstack111_opy_ (u"ࠬ࡜ࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡲࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡩࡧࡳࡩࡤࡲࡥࡷࡪ࠺ࠡࡽࢀࠫਿ")
bstack1lll11ll1_opy_ = bstack111_opy_ (u"࠭ࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡤࡧࡨ࡫ࡳࡴࠢࡤࠤࡵࡸࡩࡷࡣࡷࡩࠥࡪ࡯࡮ࡣ࡬ࡲ࠿ࠦࡻࡾࠢ࠱ࠤࡘ࡫ࡴࠡࡶ࡫ࡩࠥ࡬࡯࡭࡮ࡲࡻ࡮ࡴࡧࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡱࠤࡾࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠽ࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠤࡡࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯࠾ࠥࡺࡲࡶࡧࠣࡠࡳ࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯ࠪੀ")
bstack1lll1lll1_opy_ = bstack111_opy_ (u"ࠧࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡪࡩࡹࡥ࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࡣࡪࡸࡲࡰࡴࠣ࠾ࠥࢁࡽࠨੁ")
bstack1l1llll1_opy_ = bstack111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡴࡤࡠࡣࡰࡴࡱ࡯ࡴࡶࡦࡨࡣࡪࡼࡥ࡯ࡶࠣࡪࡴࡸࠠࡔࡆࡎࡗࡪࡺࡵࡱࠢࡾࢁࠧੂ")
bstack1llll1ll_opy_ = bstack111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠤࢀࢃࠢ੃")
bstack11ll1ll_opy_ = bstack111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠦࡻࡾࠤ੄")
bstack1ll11111_opy_ = bstack111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡴࡨࡣࡷ࡫ࡱࡶࡧࡶࡸࠥࢁࡽࠣ੅")
bstack111lll1l_opy_ = bstack111_opy_ (u"ࠧࡖࡏࡔࡖࠣࡉࡻ࡫࡮ࡵࠢࡾࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠ࠻ࠢࡾࢁࠧ੆")
bstack1lllll_opy_ = bstack111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡶࡲࡰࡺࡼࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪੇ")
bstack1ll11111l_opy_ = bstack111_opy_ (u"ࠧࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠠࠡ࡫ࡩࠬࡵࡧࡧࡦࠢࡀࡁࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠠࡼ࡞ࡱࠤࠥࠦࡴࡳࡻࡾࡠࡳࠦࡣࡰࡰࡶࡸࠥ࡬ࡳࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࡡ࠭ࡦࡴ࡞ࠪ࠭ࡀࡢ࡮ࠡࠢࠣࠤࠥ࡬ࡳ࠯ࡣࡳࡴࡪࡴࡤࡇ࡫࡯ࡩࡘࡿ࡮ࡤࠪࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠬࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡳࡣ࡮ࡴࡤࡦࡺࠬࠤ࠰ࠦࠢ࠻ࠤࠣ࠯ࠥࡐࡓࡐࡐ࠱ࡷࡹࡸࡩ࡯ࡩ࡬ࡪࡾ࠮ࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࠬࡦࡽࡡࡪࡶࠣࡲࡪࡽࡐࡢࡩࡨ࠶࠳࡫ࡶࡢ࡮ࡸࡥࡹ࡫ࠨࠣࠪࠬࠤࡂࡄࠠࡼࡿࠥ࠰ࠥࡢࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦࢂࡢࠧࠪࠫࠬ࡟ࠧ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠣ࡟ࠬࠤ࠰ࠦࠢ࠭࡞࡟ࡲࠧ࠯࡜࡯ࠢࠣࠤࠥࢃࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡽ࡝ࡰࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵ࠧੈ")
bstack1l1lllll1_opy_ = bstack111_opy_ (u"ࠨ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࡤࡱࡱࡷࡹࠦࡢࡴࡶࡤࡧࡰࡥࡰࡢࡶ࡫ࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳࡞࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠴ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡶ࡟ࡪࡰࡧࡩࡽࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠴ࡠࡠࡳࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡹ࡬ࡪࡥࡨࠬ࠵࠲ࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࠬࡠࡳࡩ࡯࡯ࡵࡷࠤ࡮ࡳࡰࡰࡴࡷࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠵ࡡࡥࡷࡹࡧࡣ࡬ࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ࠭ࡀࡢ࡮ࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮࡭ࡣࡸࡲࡨ࡮ࠠ࠾ࠢࡤࡷࡾࡴࡣࠡࠪ࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴࠫࠣࡁࡃࠦࡻ࡝ࡰ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࡡࡴࡴࡳࡻࠣࡿࡡࡴࡣࡢࡲࡶࠤࡂࠦࡊࡔࡑࡑ࠲ࡵࡧࡲࡴࡧࠫࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠪ࡞ࡱࠤࠥࢃࠠࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࠣࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡣࡺࡥ࡮ࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯࠳ࡩࡨࡳࡱࡰ࡭ࡺࡳ࠮ࡤࡱࡱࡲࡪࡩࡴࠩࡽ࡟ࡲࠥࠦࠠࠡࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸ࠿ࠦࡠࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠦࡾࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪࡿࡣ࠰ࡡࡴࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࡢ࡮ࠡࠢࢀ࠭ࡡࡴࡽ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࠧ੉")
from ._version import __version__
bstack1ll111l1l_opy_ = None
CONFIG = {}
bstack1ll1lll_opy_ = {}
bstack1l1l111_opy_ = {}
bstack1l11ll_opy_ = None
bstack1l1111l1_opy_ = None
bstack1l11111l_opy_ = None
bstack11llll1_opy_ = -1
bstack11111l11_opy_ = DEFAULT_LOG_LEVEL
bstack1ll1ll11_opy_ = 1
bstack1l1l1l1l1_opy_ = False
bstack1l111_opy_ = bstack111_opy_ (u"ࠩࠪ੊")
bstack1llll1l11_opy_ = bstack111_opy_ (u"ࠪࠫੋ")
bstack1l11l_opy_ = False
bstack1ll1l1l1l_opy_ = True
bstack1ll1l1111_opy_ = bstack111_opy_ (u"ࠫࠬੌ")
bstack1l11l1l1_opy_ = None
bstack1l1l11ll_opy_ = None
bstack1l11ll1l_opy_ = None
bstack1l1ll1l11_opy_ = None
bstack11lllll1_opy_ = None
bstack1ll1ll1_opy_ = None
bstack1l1111ll_opy_ = None
bstack1l1ll111_opy_ = None
bstack1l1ll11_opy_ = None
bstack111l111l_opy_ = None
bstack1111l1_opy_ = None
bstack11l1l1l1_opy_ = bstack111_opy_ (u"ࠧࠨ੍")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11111l11_opy_,
                    format=bstack111_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫ੎"),
                    datefmt=bstack111_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੏"))
def bstack1l1l11l_opy_():
  global CONFIG
  global bstack11111l11_opy_
  if bstack111_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ੐") in CONFIG:
    bstack11111l11_opy_ = bstack1ll1ll1l1_opy_[CONFIG[bstack111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫੑ")]]
    logging.getLogger().setLevel(bstack11111l11_opy_)
def bstack1ll1ll111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l111l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11ll11l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111_opy_ (u"ࠥ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡧࡴࡴࡦࡪࡩࡩ࡭ࡱ࡫ࠢ੒") == args[i].lower() or bstack111_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡯ࡨ࡬࡫ࠧ੓") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll1l1111_opy_
      bstack1ll1l1111_opy_ += bstack111_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࡋ࡯࡬ࡦࠢࠪ੔") + path
      return path
  return None
def bstack1l1l1l_opy_():
  bstack1l11lll_opy_ = bstack11ll11l_opy_()
  if bstack1l11lll_opy_ and os.path.exists(os.path.abspath(bstack1l11lll_opy_)):
    fileName = bstack1l11lll_opy_
  if bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪ੕") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ੖")])) and not bstack111_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ੗") in locals():
    fileName = os.environ[bstack111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࡠࡈࡌࡐࡊ࠭੘")]
  if bstack111_opy_ (u"ࠪࡪ࡮ࡲࡥࡏࡣࡰࡩࠬਖ਼") in locals():
    bstack111lllll_opy_ = os.path.abspath(fileName)
  else:
    bstack111lllll_opy_ = bstack111_opy_ (u"ࠫࠬਗ਼")
  bstack1ll11lll1_opy_ = os.getcwd()
  bstack11111ll_opy_ = bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨਜ਼")
  bstack1ll1llll1_opy_ = bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿࡡ࡮࡮ࠪੜ")
  while (not os.path.exists(bstack111lllll_opy_)) and bstack1ll11lll1_opy_ != bstack111_opy_ (u"ࠢࠣ੝"):
    bstack111lllll_opy_ = os.path.join(bstack1ll11lll1_opy_, bstack11111ll_opy_)
    if not os.path.exists(bstack111lllll_opy_):
      bstack111lllll_opy_ = os.path.join(bstack1ll11lll1_opy_, bstack1ll1llll1_opy_)
    if bstack1ll11lll1_opy_ != os.path.dirname(bstack1ll11lll1_opy_):
      bstack1ll11lll1_opy_ = os.path.dirname(bstack1ll11lll1_opy_)
    else:
      bstack1ll11lll1_opy_ = bstack111_opy_ (u"ࠣࠤਫ਼")
  if not os.path.exists(bstack111lllll_opy_):
    bstack11lll1l1_opy_(
      bstack1l1ll1ll_opy_.format(os.getcwd()))
  with open(bstack111lllll_opy_, bstack111_opy_ (u"ࠩࡵࠫ੟")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack11lll1l1_opy_(bstack1l1l11l1l_opy_.format(str(exc)))
def bstack1ll1l11l_opy_(config):
  bstack1lll11ll_opy_ = bstack111l111_opy_(config)
  for option in list(bstack1lll11ll_opy_):
    if option.lower() in bstack11111111_opy_ and option != bstack11111111_opy_[option.lower()]:
      bstack1lll11ll_opy_[bstack11111111_opy_[option.lower()]] = bstack1lll11ll_opy_[option]
      del bstack1lll11ll_opy_[option]
  return config
def bstack1ll11ll11_opy_():
  global bstack1l1l111_opy_
  for key, bstack111111ll_opy_ in bstack1l1l1_opy_.items():
    if isinstance(bstack111111ll_opy_, list):
      for var in bstack111111ll_opy_:
        if var in os.environ:
          bstack1l1l111_opy_[key] = os.environ[var]
          break
    elif bstack111111ll_opy_ in os.environ:
      bstack1l1l111_opy_[key] = os.environ[bstack111111ll_opy_]
  if bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ੠") in os.environ:
    bstack1l1l111_opy_[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ੡")] = {}
    bstack1l1l111_opy_[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੢")][bstack111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੣")] = os.environ[bstack111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ੤")]
def bstack11ll1111_opy_():
  global bstack1ll1lll_opy_
  global bstack1ll1l1111_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack111_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ੥").lower() == val.lower():
      bstack1ll1lll_opy_[bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੦")] = {}
      bstack1ll1lll_opy_[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ੧")][bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੨")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1l1l11ll1_opy_ in bstack1l1llllll_opy_.items():
    if isinstance(bstack1l1l11ll1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1l11ll1_opy_:
          if idx<len(sys.argv) and bstack111_opy_ (u"ࠬ࠳࠭ࠨ੩") + var.lower() == val.lower() and not key in bstack1ll1lll_opy_:
            bstack1ll1lll_opy_[key] = sys.argv[idx+1]
            bstack1ll1l1111_opy_ += bstack111_opy_ (u"࠭ࠠ࠮࠯ࠪ੪") + var + bstack111_opy_ (u"ࠧࠡࠩ੫") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack111_opy_ (u"ࠨ࠯࠰ࠫ੬") + bstack1l1l11ll1_opy_.lower() == val.lower() and not key in bstack1ll1lll_opy_:
          bstack1ll1lll_opy_[key] = sys.argv[idx+1]
          bstack1ll1l1111_opy_ += bstack111_opy_ (u"ࠩࠣ࠱࠲࠭੭") + bstack1l1l11ll1_opy_ + bstack111_opy_ (u"ࠪࠤࠬ੮") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1111l1l_opy_(config):
  bstack1l1lllll_opy_ = config.keys()
  for bstack111111l_opy_, bstack111ll11_opy_ in bstack1l1l1l11_opy_.items():
    if bstack111ll11_opy_ in bstack1l1lllll_opy_:
      config[bstack111111l_opy_] = config[bstack111ll11_opy_]
      del config[bstack111ll11_opy_]
  for bstack111111l_opy_, bstack111ll11_opy_ in bstack1lll1111_opy_.items():
    if isinstance(bstack111ll11_opy_, list):
      for bstack111l11_opy_ in bstack111ll11_opy_:
        if bstack111l11_opy_ in bstack1l1lllll_opy_:
          config[bstack111111l_opy_] = config[bstack111l11_opy_]
          del config[bstack111l11_opy_]
          break
    elif bstack111ll11_opy_ in bstack1l1lllll_opy_:
        config[bstack111111l_opy_] = config[bstack111ll11_opy_]
        del config[bstack111ll11_opy_]
  for bstack111l11_opy_ in list(config):
    for bstack11l1lll_opy_ in bstack1l1l1ll1l_opy_:
      if bstack111l11_opy_.lower() == bstack11l1lll_opy_.lower() and bstack111l11_opy_ != bstack11l1lll_opy_:
        config[bstack11l1lll_opy_] = config[bstack111l11_opy_]
        del config[bstack111l11_opy_]
  bstack1111l1l1_opy_ = []
  if bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ੯") in config:
    bstack1111l1l1_opy_ = config[bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨੰ")]
  for platform in bstack1111l1l1_opy_:
    for bstack111l11_opy_ in list(platform):
      for bstack11l1lll_opy_ in bstack1l1l1ll1l_opy_:
        if bstack111l11_opy_.lower() == bstack11l1lll_opy_.lower() and bstack111l11_opy_ != bstack11l1lll_opy_:
          platform[bstack11l1lll_opy_] = platform[bstack111l11_opy_]
          del platform[bstack111l11_opy_]
  for bstack111111l_opy_, bstack111ll11_opy_ in bstack1lll1111_opy_.items():
    for platform in bstack1111l1l1_opy_:
      if isinstance(bstack111ll11_opy_, list):
        for bstack111l11_opy_ in bstack111ll11_opy_:
          if bstack111l11_opy_ in platform:
            platform[bstack111111l_opy_] = platform[bstack111l11_opy_]
            del platform[bstack111l11_opy_]
            break
      elif bstack111ll11_opy_ in platform:
        platform[bstack111111l_opy_] = platform[bstack111ll11_opy_]
        del platform[bstack111ll11_opy_]
  for bstack1l1l1l111_opy_ in bstack1lll11111_opy_:
    if bstack1l1l1l111_opy_ in config:
      if not bstack1lll11111_opy_[bstack1l1l1l111_opy_] in config:
        config[bstack1lll11111_opy_[bstack1l1l1l111_opy_]] = {}
      config[bstack1lll11111_opy_[bstack1l1l1l111_opy_]].update(config[bstack1l1l1l111_opy_])
      del config[bstack1l1l1l111_opy_]
  for platform in bstack1111l1l1_opy_:
    for bstack1l1l1l111_opy_ in bstack1lll11111_opy_:
      if bstack1l1l1l111_opy_ in list(platform):
        if not bstack1lll11111_opy_[bstack1l1l1l111_opy_] in platform:
          platform[bstack1lll11111_opy_[bstack1l1l1l111_opy_]] = {}
        platform[bstack1lll11111_opy_[bstack1l1l1l111_opy_]].update(platform[bstack1l1l1l111_opy_])
        del platform[bstack1l1l1l111_opy_]
  config = bstack1ll1l11l_opy_(config)
  return config
def bstack1l11l1_opy_(config):
  global bstack1llll1l11_opy_
  if bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪੱ") in config and str(config[bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫੲ")]).lower() != bstack111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧੳ"):
    if not bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ੴ") in config:
      config[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧੵ")] = {}
    if not bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੶") in config[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੷")]:
      current_time = datetime.datetime.now()
      bstack11lll111_opy_ = current_time.strftime(bstack111_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪ੸"))
      hostname = socket.gethostname()
      bstack1l111l1l_opy_ = bstack111_opy_ (u"ࠧࠨ੹").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪ੺").format(bstack11lll111_opy_, hostname, bstack1l111l1l_opy_)
      config[bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੻")][bstack111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੼")] = identifier
    bstack1llll1l11_opy_ = config[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ੽")][bstack111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੾")]
  return config
def bstack11l1l111_opy_():
  if (
    isinstance(os.getenv(bstack111_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫ੿")), str) and len(os.getenv(bstack111_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠬ઀"))) > 0
  ) or (
    isinstance(os.getenv(bstack111_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧઁ")), str) and len(os.getenv(bstack111_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠨં"))) > 0
  ):
    return os.getenv(bstack111_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩઃ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠫࡈࡏࠧ઄"))).lower() == bstack111_opy_ (u"ࠬࡺࡲࡶࡧࠪઅ") and str(os.getenv(bstack111_opy_ (u"࠭ࡃࡊࡔࡆࡐࡊࡉࡉࠨઆ"))).lower() == bstack111_opy_ (u"ࠧࡵࡴࡸࡩࠬઇ"):
    return os.getenv(bstack111_opy_ (u"ࠨࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠫઈ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠩࡆࡍࠬઉ"))).lower() == bstack111_opy_ (u"ࠪࡸࡷࡻࡥࠨઊ") and str(os.getenv(bstack111_opy_ (u"࡙ࠫࡘࡁࡗࡋࡖࠫઋ"))).lower() == bstack111_opy_ (u"ࠬࡺࡲࡶࡧࠪઌ"):
    return os.getenv(bstack111_opy_ (u"࠭ࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬઍ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠧࡄࡋࠪ઎"))).lower() == bstack111_opy_ (u"ࠨࡶࡵࡹࡪ࠭એ") and str(os.getenv(bstack111_opy_ (u"ࠩࡆࡍࡤࡔࡁࡎࡇࠪઐ"))).lower() == bstack111_opy_ (u"ࠪࡧࡴࡪࡥࡴࡪ࡬ࡴࠬઑ"):
    return 0 # bstack1ll1l11ll_opy_ bstack1ll111l1_opy_ not set build number env
  if os.getenv(bstack111_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠧ઒")) and os.getenv(bstack111_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠨઓ")):
    return os.getenv(bstack111_opy_ (u"࠭ࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨઔ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠧࡄࡋࠪક"))).lower() == bstack111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ખ") and str(os.getenv(bstack111_opy_ (u"ࠩࡇࡖࡔࡔࡅࠨગ"))).lower() == bstack111_opy_ (u"ࠪࡸࡷࡻࡥࠨઘ"):
    return os.getenv(bstack111_opy_ (u"ࠫࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩઙ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠬࡉࡉࠨચ"))).lower() == bstack111_opy_ (u"࠭ࡴࡳࡷࡨࠫછ") and str(os.getenv(bstack111_opy_ (u"ࠧࡔࡇࡐࡅࡕࡎࡏࡓࡇࠪજ"))).lower() == bstack111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ઝ"):
    return os.getenv(bstack111_opy_ (u"ࠩࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠬઞ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠪࡇࡎ࠭ટ"))).lower() == bstack111_opy_ (u"ࠫࡹࡸࡵࡦࠩઠ") and str(os.getenv(bstack111_opy_ (u"ࠬࡍࡉࡕࡎࡄࡆࡤࡉࡉࠨડ"))).lower() == bstack111_opy_ (u"࠭ࡴࡳࡷࡨࠫઢ"):
    return os.getenv(bstack111_opy_ (u"ࠧࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠪણ"), 0)
  if str(os.getenv(bstack111_opy_ (u"ࠨࡅࡌࠫત"))).lower() == bstack111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧથ") and str(os.getenv(bstack111_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡍࡌࡘࡊ࠭દ"))).lower() == bstack111_opy_ (u"ࠫࡹࡸࡵࡦࠩધ"):
    return os.getenv(bstack111_opy_ (u"ࠬࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧન"), 0)
  if str(os.getenv(bstack111_opy_ (u"࠭ࡔࡇࡡࡅ࡙ࡎࡒࡄࠨ઩"))).lower() == bstack111_opy_ (u"ࠧࡵࡴࡸࡩࠬપ"):
    return os.getenv(bstack111_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨફ"), 0)
  return -1
def bstack1ll111ll1_opy_(bstack1l11ll1_opy_):
  global CONFIG
  if not bstack111_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫબ") in CONFIG[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬભ")]:
    return
  CONFIG[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭મ")] = CONFIG[bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧય")].replace(
    bstack111_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨર"),
    str(bstack1l11ll1_opy_)
  )
def bstack11ll1l11_opy_():
  global CONFIG
  if not bstack111_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭઱") in CONFIG[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")]:
    return
  current_time = datetime.datetime.now()
  bstack11lll111_opy_ = current_time.strftime(bstack111_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧળ"))
  CONFIG[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ઴")] = CONFIG[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭વ")].replace(
    bstack111_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫશ"),
    bstack11lll111_opy_
  )
def bstack1lllllll_opy_():
  global CONFIG
  if bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨષ") in CONFIG and not bool(CONFIG[bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")]):
    del CONFIG[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪહ")]
    return
  if not bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ઺") in CONFIG:
    CONFIG[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ઻")] = bstack111_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃ઼ࠧ")
  if bstack111_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫઽ") in CONFIG[bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨા")]:
    bstack11ll1l11_opy_()
    os.environ[bstack111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫિ")] = CONFIG[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪી")]
  if not bstack111_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫુ") in CONFIG[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૂ")]:
    return
  bstack1l11ll1_opy_ = bstack111_opy_ (u"ࠫࠬૃ")
  bstack1l11llll_opy_ = bstack11l1l111_opy_()
  if bstack1l11llll_opy_ != -1:
    bstack1l11ll1_opy_ = bstack111_opy_ (u"ࠬࡉࡉࠡࠩૄ") + str(bstack1l11llll_opy_)
  if bstack1l11ll1_opy_ == bstack111_opy_ (u"࠭ࠧૅ"):
    bstack1ll11ll1l_opy_ = bstack1lll1ll11_opy_(CONFIG[bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ૆")])
    if bstack1ll11ll1l_opy_ != -1:
      bstack1l11ll1_opy_ = str(bstack1ll11ll1l_opy_)
  if bstack1l11ll1_opy_:
    bstack1ll111ll1_opy_(bstack1l11ll1_opy_)
    os.environ[bstack111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬે")] = CONFIG[bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫૈ")]
def bstack11l1lll1_opy_(bstack1l1l1lll_opy_, bstack111l11l_opy_, path):
  bstack1l111ll1_opy_ = {
    bstack111_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૉ"): bstack111l11l_opy_
  }
  if os.path.exists(path):
    bstack1lll1ll1_opy_ = json.load(open(path, bstack111_opy_ (u"ࠫࡷࡨࠧ૊")))
  else:
    bstack1lll1ll1_opy_ = {}
  bstack1lll1ll1_opy_[bstack1l1l1lll_opy_] = bstack1l111ll1_opy_
  with open(path, bstack111_opy_ (u"ࠧࡽࠫࠣો")) as outfile:
    json.dump(bstack1lll1ll1_opy_, outfile)
def bstack1lll1ll11_opy_(bstack1l1l1lll_opy_):
  bstack1l1l1lll_opy_ = str(bstack1l1l1lll_opy_)
  bstack111llll1_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"࠭ࡾࠨૌ")), bstack111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ્ࠧ"))
  try:
    if not os.path.exists(bstack111llll1_opy_):
      os.makedirs(bstack111llll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠨࢀࠪ૎")), bstack111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ૏"), bstack111_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬૐ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111_opy_ (u"ࠫࡼ࠭૑")):
        pass
      with open(file_path, bstack111_opy_ (u"ࠧࡽࠫࠣ૒")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111_opy_ (u"࠭ࡲࠨ૓")) as bstack1ll111l_opy_:
      bstack111111l1_opy_ = json.load(bstack1ll111l_opy_)
    if bstack1l1l1lll_opy_ in bstack111111l1_opy_:
      bstack1111lll1_opy_ = bstack111111l1_opy_[bstack1l1l1lll_opy_][bstack111_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૔")]
      bstack1lll1l1_opy_ = int(bstack1111lll1_opy_) + 1
      bstack11l1lll1_opy_(bstack1l1l1lll_opy_, bstack1lll1l1_opy_, file_path)
      return bstack1lll1l1_opy_
    else:
      bstack11l1lll1_opy_(bstack1l1l1lll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111lll1_opy_.format(str(e)))
    return -1
def bstack11lll1l_opy_(config):
  if not config[bstack111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ૕")] or not config[bstack111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ૖")]:
    return True
  else:
    return False
def bstack1llllll1l_opy_(config):
  if bstack11l111l_opy_() < version.parse(bstack111_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩ૗")):
    return False
  if bstack11l111l_opy_() >= version.parse(bstack111_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪ૘")):
    return True
  if bstack111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ૙") in config and config[bstack111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭૚")] == False:
    return False
  else:
    return True
def bstack111l1l11_opy_(config, index = 0):
  global bstack1l11l_opy_
  bstack1lll11l_opy_ = {}
  caps = bstack1l111ll_opy_ + bstack11ll1l_opy_
  if bstack1l11l_opy_:
    caps += bstack111l_opy_
  for key in config:
    if key in caps + [bstack111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૛")]:
      continue
    bstack1lll11l_opy_[key] = config[key]
  if bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૜") in config:
    for bstack1l1llll1l_opy_ in config[bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૝")][index]:
      if bstack1l1llll1l_opy_ in caps + [bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૞"), bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૟")]:
        continue
      bstack1lll11l_opy_[bstack1l1llll1l_opy_] = config[bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ")][index][bstack1l1llll1l_opy_]
  bstack1lll11l_opy_[bstack111_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨૡ")] = socket.gethostname()
  if bstack111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨૢ") in bstack1lll11l_opy_:
    del(bstack1lll11l_opy_[bstack111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩૣ")])
  return bstack1lll11l_opy_
def bstack111l1_opy_(config):
  global bstack1l11l_opy_
  bstack1llll111_opy_ = {}
  caps = bstack11ll1l_opy_
  if bstack1l11l_opy_:
    caps+= bstack111l_opy_
  for key in caps:
    if key in config:
      bstack1llll111_opy_[key] = config[key]
  return bstack1llll111_opy_
def bstack111ll111_opy_(bstack1lll11l_opy_, bstack1llll111_opy_):
  bstack1llll1l_opy_ = {}
  for key in bstack1lll11l_opy_.keys():
    if key in bstack1l1l1l11_opy_:
      bstack1llll1l_opy_[bstack1l1l1l11_opy_[key]] = bstack1lll11l_opy_[key]
    else:
      bstack1llll1l_opy_[key] = bstack1lll11l_opy_[key]
  for key in bstack1llll111_opy_:
    if key in bstack1l1l1l11_opy_:
      bstack1llll1l_opy_[bstack1l1l1l11_opy_[key]] = bstack1llll111_opy_[key]
    else:
      bstack1llll1l_opy_[key] = bstack1llll111_opy_[key]
  return bstack1llll1l_opy_
def bstack11lll1ll_opy_(config, index = 0):
  global bstack1l11l_opy_
  caps = {}
  bstack1llll111_opy_ = bstack111l1_opy_(config)
  bstack11llllll_opy_ = bstack11ll1l_opy_
  bstack11llllll_opy_ += bstack1ll11llll_opy_
  if bstack1l11l_opy_:
    bstack11llllll_opy_ += bstack111l_opy_
  if bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૤") in config:
    if bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ૥") in config[bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૦")][index]:
      caps[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ૧")] = config[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨")][index][bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૩")]
    if bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ૪") in config[bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૫")][index]:
      caps[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ૬")] = str(config[bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૭")][index][bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૮")])
    bstack1l11_opy_ = {}
    for bstack1ll1l1ll1_opy_ in bstack11llllll_opy_:
      if bstack1ll1l1ll1_opy_ in config[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૯")][index]:
        if bstack1ll1l1ll1_opy_ == bstack111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ૰"):
          bstack1l11_opy_[bstack1ll1l1ll1_opy_] = str(config[bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૱")][index][bstack1ll1l1ll1_opy_] * 1.0)
        else:
          bstack1l11_opy_[bstack1ll1l1ll1_opy_] = config[bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૲")][index][bstack1ll1l1ll1_opy_]
        del(config[bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૳")][index][bstack1ll1l1ll1_opy_])
    bstack1llll111_opy_ = update(bstack1llll111_opy_, bstack1l11_opy_)
  bstack1lll11l_opy_ = bstack111l1l11_opy_(config, index)
  for bstack111l11_opy_ in bstack11ll1l_opy_ + [bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ૴"), bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭૵")]:
    if bstack111l11_opy_ in bstack1lll11l_opy_:
      bstack1llll111_opy_[bstack111l11_opy_] = bstack1lll11l_opy_[bstack111l11_opy_]
      del(bstack1lll11l_opy_[bstack111l11_opy_])
  if bstack1llllll1l_opy_(config):
    bstack1lll11l_opy_[bstack111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭૶")] = True
    caps.update(bstack1llll111_opy_)
    caps[bstack111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ૷")] = bstack1lll11l_opy_
  else:
    bstack1lll11l_opy_[bstack111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ૸")] = False
    caps.update(bstack111ll111_opy_(bstack1lll11l_opy_, bstack1llll111_opy_))
    if bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧૹ") in caps:
      caps[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫૺ")] = caps[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩૻ")]
      del(caps[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪૼ")])
    if bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ૽") in caps:
      caps[bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ૾")] = caps[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ૿")]
      del(caps[bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ଀")])
  return caps
def bstack1111ll1l_opy_():
  if bstack11l111l_opy_() <= version.parse(bstack111_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪଁ")):
    return bstack1111ll1_opy_
  return bstack111l1l1l_opy_
def bstack11ll_opy_(options):
  return hasattr(options, bstack111_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬଂ"))
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
def bstack1l11lllll_opy_(options, bstack1l1ll_opy_):
  for bstack111l1ll_opy_ in bstack1l1ll_opy_:
    if bstack111l1ll_opy_ in [bstack111_opy_ (u"ࠬࡧࡲࡨࡵࠪଃ"), bstack111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ଄")]:
      next
    if bstack111l1ll_opy_ in options._experimental_options:
      options._experimental_options[bstack111l1ll_opy_]= update(options._experimental_options[bstack111l1ll_opy_], bstack1l1ll_opy_[bstack111l1ll_opy_])
    else:
      options.add_experimental_option(bstack111l1ll_opy_, bstack1l1ll_opy_[bstack111l1ll_opy_])
  if bstack111_opy_ (u"ࠧࡢࡴࡪࡷࠬଅ") in bstack1l1ll_opy_:
    for arg in bstack1l1ll_opy_[bstack111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ଆ")]:
      options.add_argument(arg)
    del(bstack1l1ll_opy_[bstack111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧଇ")])
  if bstack111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧଈ") in bstack1l1ll_opy_:
    for ext in bstack1l1ll_opy_[bstack111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨଉ")]:
      options.add_extension(ext)
    del(bstack1l1ll_opy_[bstack111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩଊ")])
def bstack1ll1ll11l_opy_(options, bstack11ll1ll1_opy_):
  if bstack111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬଋ") in bstack11ll1ll1_opy_:
    for bstack1ll1ll_opy_ in bstack11ll1ll1_opy_[bstack111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ଌ")]:
      if bstack1ll1ll_opy_ in options._preferences:
        options._preferences[bstack1ll1ll_opy_] = update(options._preferences[bstack1ll1ll_opy_], bstack11ll1ll1_opy_[bstack111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ଍")][bstack1ll1ll_opy_])
      else:
        options.set_preference(bstack1ll1ll_opy_, bstack11ll1ll1_opy_[bstack111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ଎")][bstack1ll1ll_opy_])
  if bstack111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଏ") in bstack11ll1ll1_opy_:
    for arg in bstack11ll1ll1_opy_[bstack111_opy_ (u"ࠫࡦࡸࡧࡴࠩଐ")]:
      options.add_argument(arg)
def bstack1ll11ll_opy_(options, bstack1l111l1_opy_):
  if bstack111_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭଑") in bstack1l111l1_opy_:
    options.use_webview(bool(bstack1l111l1_opy_[bstack111_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧ଒")]))
  bstack1l11lllll_opy_(options, bstack1l111l1_opy_)
def bstack11llll11_opy_(options, bstack1ll1111_opy_):
  for bstack1ll1l1l1_opy_ in bstack1ll1111_opy_:
    if bstack1ll1l1l1_opy_ in [bstack111_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫଓ"), bstack111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ଔ")]:
      next
    options.set_capability(bstack1ll1l1l1_opy_, bstack1ll1111_opy_[bstack1ll1l1l1_opy_])
  if bstack111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧକ") in bstack1ll1111_opy_:
    for arg in bstack1ll1111_opy_[bstack111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଖ")]:
      options.add_argument(arg)
  if bstack111_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨଗ") in bstack1ll1111_opy_:
    options.use_technology_preview(bool(bstack1ll1111_opy_[bstack111_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩଘ")]))
def bstack1lll1l1l_opy_(options, bstack1l1lll11l_opy_):
  for bstack11l1l_opy_ in bstack1l1lll11l_opy_:
    if bstack11l1l_opy_ in [bstack111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪଙ"), bstack111_opy_ (u"ࠧࡢࡴࡪࡷࠬଚ")]:
      next
    options._options[bstack11l1l_opy_] = bstack1l1lll11l_opy_[bstack11l1l_opy_]
  if bstack111_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬଛ") in bstack1l1lll11l_opy_:
    for bstack1111l11l_opy_ in bstack1l1lll11l_opy_[bstack111_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ଜ")]:
      options.add_additional_option(
          bstack1111l11l_opy_, bstack1l1lll11l_opy_[bstack111_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧଝ")][bstack1111l11l_opy_])
  if bstack111_opy_ (u"ࠫࡦࡸࡧࡴࠩଞ") in bstack1l1lll11l_opy_:
    for arg in bstack1l1lll11l_opy_[bstack111_opy_ (u"ࠬࡧࡲࡨࡵࠪଟ")]:
      options.add_argument(arg)
def bstack1ll11l1_opy_(options, caps):
  if not hasattr(options, bstack111_opy_ (u"࠭ࡋࡆ࡛ࠪଠ")):
    return
  if options.KEY == bstack111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬଡ") and options.KEY in caps:
    bstack1l11lllll_opy_(options, caps[bstack111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ଢ")])
  elif options.KEY == bstack111_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧଣ") and options.KEY in caps:
    bstack1ll1ll11l_opy_(options, caps[bstack111_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨତ")])
  elif options.KEY == bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬଥ") and options.KEY in caps:
    bstack11llll11_opy_(options, caps[bstack111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ଦ")])
  elif options.KEY == bstack111_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧଧ") and options.KEY in caps:
    bstack1ll11ll_opy_(options, caps[bstack111_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨନ")])
  elif options.KEY == bstack111_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ଩") and options.KEY in caps:
    bstack1lll1l1l_opy_(options, caps[bstack111_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨପ")])
def bstack11l1ll_opy_(caps):
  global bstack1l11l_opy_
  if bstack1l11l_opy_:
    if bstack1ll1ll111_opy_() < version.parse(bstack111_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩଫ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫବ")
    if bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଭ") in caps:
      browser = caps[bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫମ")]
    elif bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨଯ") in caps:
      browser = caps[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩର")]
    browser = str(browser).lower()
    if browser == bstack111_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩ଱") or browser == bstack111_opy_ (u"ࠪ࡭ࡵࡧࡤࠨଲ"):
      browser = bstack111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫଳ")
    if browser == bstack111_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭଴"):
      browser = bstack111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ଵ")
    if browser not in [bstack111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧଶ"), bstack111_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ଷ"), bstack111_opy_ (u"ࠩ࡬ࡩࠬସ"), bstack111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪହ"), bstack111_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ଺")]:
      return None
    try:
      package = bstack111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ଻").format(browser)
      name = bstack111_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹ଼ࠧ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll_opy_(options):
        return None
      for bstack111l11_opy_ in caps.keys():
        options.set_capability(bstack111l11_opy_, caps[bstack111l11_opy_])
      bstack1ll11l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll111ll_opy_(options, bstack1lllllll1_opy_):
  if not bstack11ll_opy_(options):
    return
  for bstack111l11_opy_ in bstack1lllllll1_opy_.keys():
    if bstack111l11_opy_ in bstack1ll11llll_opy_:
      next
    if bstack111l11_opy_ in options._caps and type(options._caps[bstack111l11_opy_]) in [dict, list]:
      options._caps[bstack111l11_opy_] = update(options._caps[bstack111l11_opy_], bstack1lllllll1_opy_[bstack111l11_opy_])
    else:
      options.set_capability(bstack111l11_opy_, bstack1lllllll1_opy_[bstack111l11_opy_])
  bstack1ll11l1_opy_(options, bstack1lllllll1_opy_)
  if bstack111_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ଽ") in options._caps:
    if options._caps[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ା")] and options._caps[bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧି")].lower() != bstack111_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫୀ"):
      del options._caps[bstack111_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪୁ")]
def bstack1l1ll1l1_opy_(proxy_config):
  if bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩୂ") in proxy_config:
    proxy_config[bstack111_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨୃ")] = proxy_config[bstack111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫୄ")]
    del(proxy_config[bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ୅")])
  if bstack111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ୆") in proxy_config and proxy_config[bstack111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭େ")].lower() != bstack111_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫୈ"):
    proxy_config[bstack111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ୉")] = bstack111_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭୊")
  if bstack111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬୋ") in proxy_config:
    proxy_config[bstack111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫୌ")] = bstack111_opy_ (u"ࠩࡳࡥࡨ୍࠭")
  return proxy_config
def bstack1ll1ll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ୎") in config:
    return proxy
  config[bstack111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ୏")] = bstack1l1ll1l1_opy_(config[bstack111_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ୐")])
  if proxy == None:
    proxy = Proxy(config[bstack111_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ୑")])
  return proxy
def bstack1l1l1ll_opy_(self):
  global CONFIG
  global bstack1l1ll111_opy_
  if bstack111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ୒") in CONFIG:
    return CONFIG[bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ୓")]
  elif bstack111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭୔") in CONFIG:
    return CONFIG[bstack111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ୕")]
  else:
    return bstack1l1ll111_opy_(self)
def bstack1ll1l111l_opy_():
  global CONFIG
  return bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧୖ") in CONFIG or bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩୗ") in CONFIG
def bstack1llll1l1l_opy_(config):
  if not bstack1ll1l111l_opy_():
    return
  if config.get(bstack111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ୘")):
    return config.get(bstack111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ୙"))
  if config.get(bstack111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ୚")):
    return config.get(bstack111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭୛"))
def bstack1111_opy_():
  return bstack1ll1l111l_opy_() and bstack11l111l_opy_() >= version.parse(bstack1l1l1llll_opy_)
def bstack111l111_opy_(config):
  if bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧଡ଼") in config:
    return config[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଢ଼")]
  if bstack111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୞") in config:
    return config[bstack111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬୟ")]
  return {}
def bstack1llllll_opy_(caps):
  global bstack1llll1l11_opy_
  if bstack111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨୠ") in caps:
    caps[bstack111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩୡ")][bstack111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨୢ")] = True
    if bstack1llll1l11_opy_:
      caps[bstack111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫୣ")][bstack111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୤")] = bstack1llll1l11_opy_
  else:
    caps[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ୥")] = True
    if bstack1llll1l11_opy_:
      caps[bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ୦")] = bstack1llll1l11_opy_
def bstack1l1l1l1_opy_():
  global CONFIG
  if bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ୧") in CONFIG and CONFIG[bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ୨")]:
    bstack1lll11ll_opy_ = bstack111l111_opy_(CONFIG)
    bstack111l1l1_opy_(CONFIG[bstack111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ୩")], bstack1lll11ll_opy_)
def bstack111l1l1_opy_(key, bstack1lll11ll_opy_):
  global bstack1ll111l1l_opy_
  logger.info(bstack1l11lll1_opy_)
  try:
    bstack1ll111l1l_opy_ = Local()
    bstack1l11l1ll_opy_ = {bstack111_opy_ (u"ࠪ࡯ࡪࡿࠧ୪"): key}
    bstack1l11l1ll_opy_.update(bstack1lll11ll_opy_)
    logger.debug(bstack11l1ll11_opy_.format(str(bstack1l11l1ll_opy_)))
    bstack1ll111l1l_opy_.start(**bstack1l11l1ll_opy_)
    if bstack1ll111l1l_opy_.isRunning():
      logger.info(bstack1ll1l1ll_opy_)
  except Exception as e:
    bstack11lll1l1_opy_(bstack1lll1l11l_opy_.format(str(e)))
def bstack1111111l_opy_():
  global bstack1ll111l1l_opy_
  if bstack1ll111l1l_opy_.isRunning():
    logger.info(bstack1111ll_opy_)
    bstack1ll111l1l_opy_.stop()
  bstack1ll111l1l_opy_ = None
def bstack111ll_opy_():
  global bstack11l1l1l1_opy_
  if bstack11l1l1l1_opy_:
    logger.warning(bstack1lll11ll1_opy_.format(str(bstack11l1l1l1_opy_)))
  logger.info(bstack111lll_opy_)
  global bstack1ll111l1l_opy_
  if bstack1ll111l1l_opy_:
    bstack1111111l_opy_()
  logger.info(bstack1ll1l1lll_opy_)
  bstack11111l_opy_()
def bstack1l11111_opy_(self, *args):
  logger.error(bstack1ll11l11l_opy_)
  bstack111ll_opy_()
  sys.exit(1)
def bstack11lll1l1_opy_(err):
  logger.critical(bstack1ll11_opy_.format(str(err)))
  bstack11111l_opy_(bstack1ll11_opy_.format(str(err)))
  atexit.unregister(bstack111ll_opy_)
  sys.exit(1)
def bstack1llll111l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11111l_opy_(message)
  atexit.unregister(bstack111ll_opy_)
  sys.exit(1)
def bstack111l1ll1_opy_():
  global CONFIG
  global bstack1ll1lll_opy_
  global bstack1l1l111_opy_
  global bstack1ll1l1l1l_opy_
  CONFIG = bstack1l1l1l_opy_()
  bstack1ll11ll11_opy_()
  bstack11ll1111_opy_()
  CONFIG = bstack1111l1l_opy_(CONFIG)
  update(CONFIG, bstack1l1l111_opy_)
  update(CONFIG, bstack1ll1lll_opy_)
  CONFIG = bstack1l11l1_opy_(CONFIG)
  if bstack111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ୫") in CONFIG and str(CONFIG[bstack111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ୬")]).lower() == bstack111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ୭"):
    bstack1ll1l1l1l_opy_ = False
  if (bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ୮") in CONFIG and bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ୯") in bstack1ll1lll_opy_) or (bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ୰") in CONFIG and bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ୱ") not in bstack1l1l111_opy_):
    if os.getenv(bstack111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨ୲")):
      CONFIG[bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ୳")] = os.getenv(bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ୴"))
    else:
      bstack1lllllll_opy_()
  elif (bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ୵") not in CONFIG and bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୶") in CONFIG) or (bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ୷") in bstack1l1l111_opy_ and bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭୸") not in bstack1ll1lll_opy_):
    del(CONFIG[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭୹")])
  if bstack11lll1l_opy_(CONFIG):
    bstack11lll1l1_opy_(bstack11l1ll1l_opy_)
  bstack111l1l_opy_()
  bstack1l1llll11_opy_()
  if bstack1l11l_opy_:
    CONFIG[bstack111_opy_ (u"ࠬࡧࡰࡱࠩ୺")] = bstack1ll11l1ll_opy_(CONFIG)
    logger.info(bstack1l11l11l_opy_.format(CONFIG[bstack111_opy_ (u"࠭ࡡࡱࡲࠪ୻")]))
def bstack1l1llll11_opy_():
  global CONFIG
  global bstack1l11l_opy_
  if bstack111_opy_ (u"ࠧࡢࡲࡳࠫ୼") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1llll11_opy_)
    bstack1l11l_opy_ = True
def bstack1ll11l1ll_opy_(config):
  bstack1l1lll111_opy_ = bstack111_opy_ (u"ࠨࠩ୽")
  app = config[bstack111_opy_ (u"ࠩࡤࡴࡵ࠭୾")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lll111l_opy_:
      if os.path.exists(app):
        bstack1l1lll111_opy_ = bstack1l1lll11_opy_(config, app)
      elif bstack1ll111_opy_(app):
        bstack1l1lll111_opy_ = app
      else:
        bstack11lll1l1_opy_(bstack1l1lll1l1_opy_.format(app))
    else:
      if bstack1ll111_opy_(app):
        bstack1l1lll111_opy_ = app
      elif os.path.exists(app):
        bstack1l1lll111_opy_ = bstack1l1lll11_opy_(app)
      else:
        bstack11lll1l1_opy_(bstack111l11ll_opy_)
  else:
    if len(app) > 2:
      bstack11lll1l1_opy_(bstack111ll1l1_opy_)
    elif len(app) == 2:
      if bstack111_opy_ (u"ࠪࡴࡦࡺࡨࠨ୿") in app and bstack111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ஀") in app:
        if os.path.exists(app[bstack111_opy_ (u"ࠬࡶࡡࡵࡪࠪ஁")]):
          bstack1l1lll111_opy_ = bstack1l1lll11_opy_(config, app[bstack111_opy_ (u"࠭ࡰࡢࡶ࡫ࠫஂ")], app[bstack111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪஃ")])
        else:
          bstack11lll1l1_opy_(bstack1l1lll1l1_opy_.format(app))
      else:
        bstack11lll1l1_opy_(bstack111ll1l1_opy_)
    else:
      for key in app:
        if key in bstack1l1ll1_opy_:
          if key == bstack111_opy_ (u"ࠨࡲࡤࡸ࡭࠭஄"):
            if os.path.exists(app[key]):
              bstack1l1lll111_opy_ = bstack1l1lll11_opy_(config, app[key])
            else:
              bstack11lll1l1_opy_(bstack1l1lll1l1_opy_.format(app))
          else:
            bstack1l1lll111_opy_ = app[key]
        else:
          bstack11lll1l1_opy_(bstack1lll11l1_opy_)
  return bstack1l1lll111_opy_
def bstack1ll111_opy_(bstack1l1lll111_opy_):
  import re
  bstack1l11l1l_opy_ = re.compile(bstack111_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤஅ"))
  bstack1l1lll1ll_opy_ = re.compile(bstack111_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢஆ"))
  if bstack111_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪஇ") in bstack1l1lll111_opy_ or re.fullmatch(bstack1l11l1l_opy_, bstack1l1lll111_opy_) or re.fullmatch(bstack1l1lll1ll_opy_, bstack1l1lll111_opy_):
    return True
  else:
    return False
def bstack1l1lll11_opy_(config, path, bstack1111l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111_opy_ (u"ࠬࡸࡢࠨஈ")).read()).hexdigest()
  bstack11l1l1ll_opy_ = bstack1llll1111_opy_(md5_hash)
  bstack1l1lll111_opy_ = None
  if bstack11l1l1ll_opy_:
    logger.info(bstack11111_opy_.format(bstack11l1l1ll_opy_, md5_hash))
    return bstack11l1l1ll_opy_
  bstack1lll1l111_opy_ = MultipartEncoder(
    fields={
        bstack111_opy_ (u"࠭ࡦࡪ࡮ࡨࠫஉ"): (os.path.basename(path), open(os.path.abspath(path), bstack111_opy_ (u"ࠧࡳࡤࠪஊ")), bstack111_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ஋")),
        bstack111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ஌"): bstack1111l_opy_
    }
  )
  response = requests.post(bstack1l11l111_opy_, data=bstack1lll1l111_opy_,
                         headers={bstack111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ஍"): bstack1lll1l111_opy_.content_type}, auth=(config[bstack111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭எ")], config[bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஏ")]))
  try:
    res = json.loads(response.text)
    bstack1l1lll111_opy_ = res[bstack111_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧஐ")]
    logger.info(bstack1l1ll1ll1_opy_.format(bstack1l1lll111_opy_))
    bstack1lll1l11_opy_(md5_hash, bstack1l1lll111_opy_)
  except ValueError as err:
    bstack11lll1l1_opy_(bstack1lll1l_opy_.format(str(err)))
  return bstack1l1lll111_opy_
def bstack111l1l_opy_():
  global CONFIG
  global bstack1ll1ll11_opy_
  bstack1l1l1l1l_opy_ = 0
  bstack1l1l111l1_opy_ = 1
  if bstack111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ஑") in CONFIG:
    bstack1l1l111l1_opy_ = CONFIG[bstack111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨஒ")]
  if bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬஓ") in CONFIG:
    bstack1l1l1l1l_opy_ = len(CONFIG[bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஔ")])
  bstack1ll1ll11_opy_ = int(bstack1l1l111l1_opy_) * int(bstack1l1l1l1l_opy_)
def bstack1llll1111_opy_(md5_hash):
  bstack1ll1l1l_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠫࢃ࠭க")), bstack111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ஖"), bstack111_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ஗"))
  if os.path.exists(bstack1ll1l1l_opy_):
    bstack11lll_opy_ = json.load(open(bstack1ll1l1l_opy_,bstack111_opy_ (u"ࠧࡳࡤࠪ஘")))
    if md5_hash in bstack11lll_opy_:
      bstack111ll11l_opy_ = bstack11lll_opy_[md5_hash]
      bstack1l1l1l11l_opy_ = datetime.datetime.now()
      bstack1111l11_opy_ = datetime.datetime.strptime(bstack111ll11l_opy_[bstack111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫங")], bstack111_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ச"))
      if (bstack1l1l1l11l_opy_ - bstack1111l11_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack111ll11l_opy_[bstack111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ஛")]):
        return None
      return bstack111ll11l_opy_[bstack111_opy_ (u"ࠫ࡮ࡪࠧஜ")]
  else:
    return None
def bstack1lll1l11_opy_(md5_hash, bstack1l1lll111_opy_):
  bstack111llll1_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠬࢄࠧ஝")), bstack111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ஞ"))
  if not os.path.exists(bstack111llll1_opy_):
    os.makedirs(bstack111llll1_opy_)
  bstack1ll1l1l_opy_ = os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠧࡿࠩட")), bstack111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ஠"), bstack111_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ஡"))
  bstack11ll111l_opy_ = {
    bstack111_opy_ (u"ࠪ࡭ࡩ࠭஢"): bstack1l1lll111_opy_,
    bstack111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧண"): datetime.datetime.strftime(datetime.datetime.now(), bstack111_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩத")),
    bstack111_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ஥"): str(__version__)
  }
  if os.path.exists(bstack1ll1l1l_opy_):
    bstack11lll_opy_ = json.load(open(bstack1ll1l1l_opy_,bstack111_opy_ (u"ࠧࡳࡤࠪ஦")))
  else:
    bstack11lll_opy_ = {}
  bstack11lll_opy_[md5_hash] = bstack11ll111l_opy_
  with open(bstack1ll1l1l_opy_, bstack111_opy_ (u"ࠣࡹ࠮ࠦ஧")) as outfile:
    json.dump(bstack11lll_opy_, outfile)
def bstack1ll1111ll_opy_(self):
  return
def bstack1llll1ll1_opy_(self):
  return
def bstack11llll_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1l1ll11_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11ll_opy_
  global bstack11llll1_opy_
  global bstack1l11111l_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l111_opy_
  global bstack1l11l1l1_opy_
  CONFIG[bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫந")] = str(bstack1l111_opy_) + str(__version__)
  command_executor = bstack1111ll1l_opy_()
  logger.debug(bstack1l11ll11_opy_.format(command_executor))
  proxy = bstack1ll1ll1l_opy_(CONFIG, proxy)
  bstack1ll1l11_opy_ = 0 if bstack11llll1_opy_ < 0 else bstack11llll1_opy_
  if bstack1l1l1l1l1_opy_ is True:
    bstack1ll1l11_opy_ = int(threading.current_thread().getName())
  bstack1lllllll1_opy_ = bstack11lll1ll_opy_(CONFIG, bstack1ll1l11_opy_)
  logger.debug(bstack1llll1l1_opy_.format(str(bstack1lllllll1_opy_)))
  if bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧன") in CONFIG and CONFIG[bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨப")]:
    bstack1llllll_opy_(bstack1lllllll1_opy_)
  if desired_capabilities:
    bstack1ll11l_opy_ = bstack1111l1l_opy_(desired_capabilities)
    bstack1ll11l_opy_[bstack111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ஫")] = bstack1llllll1l_opy_(CONFIG)
    bstack1lllll1l1_opy_ = bstack11lll1ll_opy_(bstack1ll11l_opy_)
    if bstack1lllll1l1_opy_:
      bstack1lllllll1_opy_ = update(bstack1lllll1l1_opy_, bstack1lllllll1_opy_)
    desired_capabilities = None
  if options:
    bstack1lll111ll_opy_(options, bstack1lllllll1_opy_)
  if not options:
    options = bstack11l1ll_opy_(bstack1lllllll1_opy_)
  if options and bstack11l111l_opy_() >= version.parse(bstack111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ஬")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack11l111l_opy_() < version.parse(bstack111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭஭")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lllllll1_opy_)
  logger.info(bstack1ll1l111_opy_)
  if bstack11l111l_opy_() >= version.parse(bstack111_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧம")):
    bstack1l11l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l111l_opy_() >= version.parse(bstack111_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩய")):
    bstack1l11l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l11l1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack1l11ll_opy_ = self.session_id
  if bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ர") in CONFIG and bstack111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩற") in CONFIG[bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨல")][bstack1ll1l11_opy_]:
    bstack1l11111l_opy_ = CONFIG[bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩள")][bstack1ll1l11_opy_][bstack111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬழ")]
  logger.debug(bstack1lllll1_opy_.format(bstack1l11ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack111ll1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      if(bstack111_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥவ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠩࢁࠫஶ")), bstack111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪஷ"), bstack111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ஸ")), bstack111_opy_ (u"ࠬࡽࠧஹ")) as fp:
          fp.write(bstack111_opy_ (u"ࠨࠢ஺"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ஻")))):
          with open(args[1], bstack111_opy_ (u"ࠨࡴࠪ஼")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ஽") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll11111l_opy_)
            lines.insert(1, bstack1l1lllll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧா")), bstack111_opy_ (u"ࠫࡼ࠭ி")) as bstack1lll1_opy_:
              bstack1lll1_opy_.writelines(lines)
        CONFIG[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧீ")] = str(bstack1l111_opy_) + str(__version__)
        bstack1ll1l11_opy_ = 0 if bstack11llll1_opy_ < 0 else bstack11llll1_opy_
        if bstack1l1l1l1l1_opy_ is True:
          bstack1ll1l11_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack111_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨு")] = False
        bstack1lllllll1_opy_ = bstack11lll1ll_opy_(CONFIG, bstack1ll1l11_opy_)
        logger.debug(bstack1llll1l1_opy_.format(str(bstack1lllllll1_opy_)))
        if CONFIG[bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫூ")]:
          bstack1llllll_opy_(bstack1lllllll1_opy_)
        if bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௃") in CONFIG and bstack111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ௄") in CONFIG[bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௅")][bstack1ll1l11_opy_]:
          bstack1l11111l_opy_ = CONFIG[bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧெ")][bstack1ll1l11_opy_][bstack111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪே")]
        args.append(os.path.join(os.path.expanduser(bstack111_opy_ (u"࠭ࡾࠨை")), bstack111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ௉"), bstack111_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪொ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lllllll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦோ"))
      return bstack1111l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    logger.debug(bstack1l11lll1l_opy_ + str(e))
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1lll1111l_opy_(self,
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
    global bstack1l11ll_opy_
    global bstack11llll1_opy_
    global bstack1l11111l_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1l111_opy_
    global bstack1l11l1l1_opy_
    CONFIG[bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬௌ")] = str(bstack1l111_opy_) + str(__version__)
    bstack1ll1l11_opy_ = 0 if bstack11llll1_opy_ < 0 else bstack11llll1_opy_
    if bstack1l1l1l1l1_opy_ is True:
      bstack1ll1l11_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack111_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆ்ࠦ")] = False
    bstack1lllllll1_opy_ = bstack11lll1ll_opy_(CONFIG, bstack1ll1l11_opy_)
    logger.debug(bstack1llll1l1_opy_.format(str(bstack1lllllll1_opy_)))
    if CONFIG[bstack111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௎")]:
      bstack1llllll_opy_(bstack1lllllll1_opy_)
    if bstack111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ௏") in CONFIG and bstack111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬௐ") in CONFIG[bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௑")][bstack1ll1l11_opy_]:
      bstack1l11111l_opy_ = CONFIG[bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")][bstack1ll1l11_opy_][bstack111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ௓")]
    import urllib
    import json
    bstack1l11llll1_opy_ = bstack111_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭௔") + urllib.parse.quote(json.dumps(bstack1lllllll1_opy_))
    browser = self.connect(bstack1l11llll1_opy_)
    return browser
except Exception as e:
    logger.debug(bstack1l11lll1l_opy_ + str(e))
def bstack1ll1lll11_opy_():
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll1111l_opy_
    except Exception as e:
        logger.debug(bstack1l11lll1l_opy_ + str(e))
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack111ll1l_opy_
    except Exception as e:
      logger.debug(bstack1l11lll1l_opy_ + str(e))
def bstack11ll1lll_opy_(context, bstack1ll11l11_opy_):
  try:
    context.page.evaluate(bstack111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ௕"), bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ௖")+ json.dumps(bstack1ll11l11_opy_) + bstack111_opy_ (u"ࠢࡾࡿࠥௗ"))
  except Exception as e:
    logger.debug(bstack111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ௘"), e)
def bstack11111lll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ௙"), bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ௚") + json.dumps(message) + bstack111_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ௛") + json.dumps(level) + bstack111_opy_ (u"ࠬࢃࡽࠨ௜"))
  except Exception as e:
    logger.debug(bstack111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ௝"), e)
def bstack1l1l11111_opy_(context, status, message = bstack111_opy_ (u"ࠢࠣ௞")):
  try:
    if(status == bstack111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ௟")):
      context.page.evaluate(bstack111_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ௠"), bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠫ௡") + json.dumps(bstack111_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࠨ௢") + str(message)) + bstack111_opy_ (u"ࠬ࠲ࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩ௣") + json.dumps(status) + bstack111_opy_ (u"ࠨࡽࡾࠤ௤"))
    else:
      context.page.evaluate(bstack111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ௥"), bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩ௦") + json.dumps(status) + bstack111_opy_ (u"ࠤࢀࢁࠧ௧"))
  except Exception as e:
    logger.debug(bstack111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢ௨"), e)
def bstack11l1l11l_opy_(self, url):
  global bstack111l111l_opy_
  try:
    bstack1l1ll11l1_opy_(url)
  except Exception as err:
    logger.debug(bstack1lll1lll1_opy_.format(str(err)))
  try:
    bstack111l111l_opy_(self, url)
  except Exception as e:
    try:
      bstack11l11ll_opy_ = str(e)
      if bstack111_opy_ (u"ࠫࡊࡘࡒࡠࡐࡄࡑࡊࡥࡎࡐࡖࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࠬ௩") in bstack11l11ll_opy_ or bstack111_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡒࡆࡈࡘࡗࡊࡊࠧ௪") in bstack11l11ll_opy_ or bstack111_opy_ (u"࠭ࡅࡓࡔࡢࡘ࡚ࡔࡎࡆࡎࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧ௫") in bstack11l11ll_opy_:
        bstack1l1ll11l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lll1lll1_opy_.format(str(err)))
    raise e
def bstack11ll1l1l_opy_(self, test):
  global CONFIG
  global bstack1l11ll_opy_
  global bstack1l1111l1_opy_
  global bstack1l11111l_opy_
  global bstack1l1l11ll_opy_
  try:
    if not bstack1l11ll_opy_:
      with open(os.path.join(os.path.expanduser(bstack111_opy_ (u"ࠧࡿࠩ௬")), bstack111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ௭"), bstack111_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ௮"))) as f:
        bstack1llll11l_opy_ = json.loads(bstack111_opy_ (u"ࠥࡿࠧ௯") + f.read().strip() + bstack111_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭௰") + bstack111_opy_ (u"ࠧࢃࠢ௱"))
        bstack1l11ll_opy_ = bstack1llll11l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l11ll_opy_:
    try:
      data = {}
      bstack1lll11lll_opy_ = None
      if test:
        bstack1lll11lll_opy_ = str(test.data)
      if bstack1lll11lll_opy_ and not bstack1l11111l_opy_:
        data[bstack111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ௲")] = bstack1lll11lll_opy_
      if bstack1l1111l1_opy_:
        if bstack1l1111l1_opy_.status == bstack111_opy_ (u"ࠧࡑࡃࡖࡗࠬ௳"):
          data[bstack111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ௴")] = bstack111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ௵")
        elif bstack1l1111l1_opy_.status == bstack111_opy_ (u"ࠪࡊࡆࡏࡌࠨ௶"):
          data[bstack111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ௷")] = bstack111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ௸")
          if bstack1l1111l1_opy_.message:
            data[bstack111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭௹")] = str(bstack1l1111l1_opy_.message)
      user = CONFIG[bstack111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ௺")]
      key = CONFIG[bstack111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ௻")]
      url = bstack111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ௼").format(user, key, bstack1l11ll_opy_)
      headers = {
        bstack111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ௽"): bstack111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ௾"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll11lll_opy_.format(str(e)))
  bstack1l1l11ll_opy_(self, test)
def bstack1ll1lll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l11ll1l_opy_
  bstack1l11ll1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1111l1_opy_
  bstack1l1111l1_opy_ = self._test
def bstack1l111111_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack111_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠧ௿"), bstack111_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠥఀ"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack111_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࡤࡪࡴࠥఁ"), bstack111_opy_ (u"ࠣ࠰ࠥం")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack111_opy_ (u"ࠤ࠭࠲ࡽࡳ࡬ࠣః"))))
  if not files:
    pabot._write(bstack111_opy_ (u"࡛ࠪࡆࡘࡎ࠻ࠢࡑࡳࠥࡵࡵࡵࡲࡸࡸࠥ࡬ࡩ࡭ࡧࡶࠤ࡮ࡴࠠࠣࠧࡶࠦࠬఄ") % outs_dir, pabot.Color.YELLOW)
    return bstack111_opy_ (u"ࠦࠧఅ")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack11lll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack111_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤఆ") in options:
    del options[bstack111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥఇ")]
  if ROBOT_VERSION < bstack111_opy_ (u"ࠢ࠵࠰࠳ࠦఈ"):
    stats = {
      bstack111_opy_ (u"ࠣࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠥఉ"): {bstack111_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣఊ"): 0, bstack111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఋ"): 0, bstack111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఌ"): 0},
      bstack111_opy_ (u"ࠧࡧ࡬࡭ࠤ఍"): {bstack111_opy_ (u"ࠨࡴࡰࡶࡤࡰࠧఎ"): 0, bstack111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢఏ"): 0, bstack111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣఐ"): 0},
    }
  else:
    stats = {
      bstack111_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣ఑"): 0,
      bstack111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఒ"): 0,
      bstack111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఓ"): 0,
      bstack111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨఔ"): 0,
    }
  if pabot_args[bstack111_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧక")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack111_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨఖ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack111_opy_ (u"ࠣࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠦగ")], pabot_args[bstack111_opy_ (u"ࠤࡤࡶࡹ࡯ࡦࡢࡥࡷࡷ࡮ࡴࡳࡶࡤࡩࡳࡱࡪࡥࡳࡵࠥఘ")]
      )
      outputs += [
        bstack1l111111_opy_(
          os.path.join(outs_dir, str(index)+ bstack111_opy_ (u"ࠥ࠳ࠧఙ")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack111_opy_ (u"ࠦࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠦచ"), bstack111_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠪࡹ࠮ࡹ࡯࡯ࠦఛ") % index),
        )
      ]
    if bstack111_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹࠨజ") not in options:
      options[bstack111_opy_ (u"ࠢࡰࡷࡷࡴࡺࡺࠢఝ")] = bstack111_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠧఞ")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11lll1_opy_(self, ff_profile_dir):
  global bstack1l1ll1l11_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll1l11_opy_(self, ff_profile_dir)
def bstack1ll111l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1llll1l11_opy_
  bstack1l1ll11l_opy_ = []
  if bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬట") in CONFIG:
    bstack1l1ll11l_opy_ = CONFIG[bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఠ")]
  bstack1ll1l1_opy_ = len(suite_group) * len(pabot_args[bstack111_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦడ")] or [(bstack111_opy_ (u"ࠧࠨఢ"), None)]) * len(bstack1l1ll11l_opy_)
  pabot_args[bstack111_opy_ (u"ࠨࡂࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡠࡔࡘࡒࠧణ")] = []
  for q in range(bstack1ll1l1_opy_):
    pabot_args[bstack111_opy_ (u"ࠢࡃࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡡࡕ࡙ࡓࠨత")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤథ")],
      pabot_args[bstack111_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥద")],
      argfile,
      pabot_args.get(bstack111_opy_ (u"ࠥ࡬࡮ࡼࡥࠣధ")),
      pabot_args[bstack111_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠢన")],
      platform[0],
      bstack1llll1l11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧ఩")] or [(bstack111_opy_ (u"ࠨࠢప"), None)]
    for platform in enumerate(bstack1l1ll11l_opy_)
  ]
def bstack1l1ll1111_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1ll11l111_opy_=bstack111_opy_ (u"ࠧࠨఫ")):
  global bstack1ll1ll1_opy_
  self.platform_index = platform_index
  self.bstack11l1llll_opy_ = bstack1ll11l111_opy_
  bstack1ll1ll1_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack111111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1111ll_opy_
  global bstack1ll1l1111_opy_
  if not bstack111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪబ") in item.options:
    item.options[bstack111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫభ")] = []
  for v in item.options[bstack111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬమ")]:
    if bstack111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪయ") in v:
      item.options[bstack111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧర")].remove(v)
    if bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ఱ") in v:
      item.options[bstack111_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩల")].remove(v)
  item.options[bstack111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪళ")].insert(0, bstack111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫఴ").format(item.platform_index))
  item.options[bstack111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬవ")].insert(0, bstack111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫశ").format(item.bstack11l1llll_opy_))
  if bstack1ll1l1111_opy_:
    item.options[bstack111_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧష")].insert(0, bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩస").format(bstack1ll1l1111_opy_))
  return bstack1l1111ll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1llll11l1_opy_(command):
  global bstack1ll1l1111_opy_
  if bstack1ll1l1111_opy_:
    command[0] = command[0].replace(bstack111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭హ"), bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠭఺") + bstack1ll1l1111_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ఻"), bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲ఼ࠧ"), 1)
def bstack11ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11lllll1_opy_
  bstack1llll11l1_opy_(command)
  return bstack11lllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11lllll1_opy_
  bstack1llll11l1_opy_(command)
  return bstack11lllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llllllll_opy_(self, runner, quiet=False, capture=True):
  global bstack1llll1lll_opy_
  bstack11l11l1_opy_ = bstack1llll1lll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack111_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫఽ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩా")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11l11l1_opy_
def bstack11l1ll1_opy_(self, name, context, *args):
  global bstack1111111_opy_
  if name in [bstack111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧి"), bstack111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩీ")]:
    bstack1111111_opy_(self, name, context, *args)
  if name == bstack111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩు"):
    try:
      bstack1ll11l11_opy_ = str(self.feature.name)
      bstack11ll1lll_opy_(context, bstack1ll11l11_opy_)
      context.browser.execute_script(bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧూ") + json.dumps(bstack1ll11l11_opy_) + bstack111_opy_ (u"ࠪࢁࢂ࠭ృ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫౄ").format(str(e)))
  if name == bstack111_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ౅"):
    try:
      if not hasattr(self, bstack111_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨె")):
        self.driver_before_scenario = True
      bstack1lll1ll_opy_ = args[0].name
      bstack1111lll_opy_ = bstack1ll11l11_opy_ = str(self.feature.name)
      bstack1ll11l11_opy_ = bstack1111lll_opy_ + bstack111_opy_ (u"ࠧࠡ࠯ࠣࠫే") + bstack1lll1ll_opy_
      if self.driver_before_scenario:
        bstack11ll1lll_opy_(context, bstack1ll11l11_opy_)
        context.browser.execute_script(bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ై") + json.dumps(bstack1ll11l11_opy_) + bstack111_opy_ (u"ࠩࢀࢁࠬ౉"))
    except Exception as e:
      logger.debug(bstack111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫొ").format(str(e)))
  if name == bstack111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬో"):
    try:
      bstack1lll1lll_opy_ = args[0].status.name
      if str(bstack1lll1lll_opy_).lower() == bstack111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬౌ"):
        bstack11l11111_opy_ = bstack111_opy_ (u"్࠭ࠧ")
        bstack1ll1l1l11_opy_ = bstack111_opy_ (u"ࠧࠨ౎")
        bstack1lll1ll1l_opy_ = bstack111_opy_ (u"ࠨࠩ౏")
        try:
          import traceback
          bstack11l11111_opy_ = self.exception.__class__.__name__
          bstack11ll11l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1ll1l1l11_opy_ = bstack111_opy_ (u"ࠩࠣࠫ౐").join(bstack11ll11l1_opy_)
          bstack1lll1ll1l_opy_ = bstack11ll11l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack11lll11l_opy_.format(str(e)))
        bstack11l11111_opy_ += bstack1lll1ll1l_opy_
        bstack11111lll_opy_(context, json.dumps(str(args[0].name) + bstack111_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤ౑") + str(bstack1ll1l1l11_opy_)), bstack111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ౒"))
        if self.driver_before_scenario:
          bstack1l1l11111_opy_(context, bstack111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ౓"), bstack11l11111_opy_)
        context.browser.execute_script(bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ౔") + json.dumps(str(args[0].name) + bstack111_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨౕ") + str(bstack1ll1l1l11_opy_)) + bstack111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨౖ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ౗") + json.dumps(bstack111_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢౘ") + str(bstack11l11111_opy_)) + bstack111_opy_ (u"ࠫࢂࢃࠧౙ"))
      else:
        bstack11111lll_opy_(context, bstack111_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨౚ"), bstack111_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ౛"))
        if self.driver_before_scenario:
          bstack1l1l11111_opy_(context, bstack111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౜"))
        context.browser.execute_script(bstack111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ౝ") + json.dumps(str(args[0].name) + bstack111_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨ౞")) + bstack111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩ౟"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧࡶࡡࡴࡵࡨࡨࠧࢃࡽࠨౠ"))
    except Exception as e:
      logger.debug(bstack111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧౡ").format(str(e)))
  if name == bstack111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ౢ"):
    try:
      if context.failed is True:
        bstack1l1l1111_opy_ = []
        bstack1lllll111_opy_ = []
        bstack111l1111_opy_ = []
        bstack1l1l11lll_opy_ = bstack111_opy_ (u"ࠧࠨౣ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1l1111_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack11ll11l1_opy_ = traceback.format_tb(exc_tb)
            bstack1lllll11_opy_ = bstack111_opy_ (u"ࠨࠢࠪ౤").join(bstack11ll11l1_opy_)
            bstack1lllll111_opy_.append(bstack1lllll11_opy_)
            bstack111l1111_opy_.append(bstack11ll11l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack11lll11l_opy_.format(str(e)))
        bstack11l11111_opy_ = bstack111_opy_ (u"ࠩࠪ౥")
        for i in range(len(bstack1l1l1111_opy_)):
          bstack11l11111_opy_ += bstack1l1l1111_opy_[i] + bstack111l1111_opy_[i] + bstack111_opy_ (u"ࠪࡠࡳ࠭౦")
        bstack1l1l11lll_opy_ = bstack111_opy_ (u"ࠫࠥ࠭౧").join(bstack1lllll111_opy_)
        if not self.driver_before_scenario:
          bstack11111lll_opy_(context, bstack1l1l11lll_opy_, bstack111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ౨"))
          bstack1l1l11111_opy_(context, bstack111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౩"), bstack11l11111_opy_)
          context.browser.execute_script(bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ౪") + json.dumps(bstack1l1l11lll_opy_) + bstack111_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ౫"))
          context.browser.execute_script(bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ౬") + json.dumps(bstack111_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ౭") + str(bstack11l11111_opy_)) + bstack111_opy_ (u"ࠫࢂࢃࠧ౮"))
      else:
        if not self.driver_before_scenario:
          bstack11111lll_opy_(context, bstack111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ౯") + str(self.feature.name) + bstack111_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ౰"), bstack111_opy_ (u"ࠢࡪࡰࡩࡳࠧ౱"))
          bstack1l1l11111_opy_(context, bstack111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ౲"))
          context.browser.execute_script(bstack111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౳") + json.dumps(bstack111_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ౴") + str(self.feature.name) + bstack111_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ౵")) + bstack111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ౶"))
          context.browser.execute_script(bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ౷"))
    except Exception as e:
      logger.debug(bstack111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ౸").format(str(e)))
  if name in [bstack111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ౹"), bstack111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ౺")]:
    bstack1111111_opy_(self, name, context, *args)
def bstack1l1ll1l1l_opy_(bstack1ll1lll1l_opy_):
  global bstack1l111_opy_
  bstack1l111_opy_ = bstack1ll1lll1l_opy_
  logger.info(bstack11l11lll_opy_.format(bstack1l111_opy_.split(bstack111_opy_ (u"ࠪ࠱ࠬ౻"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack1ll11l1l_opy_ + str(e))
  Service.start = bstack1ll1111ll_opy_
  Service.stop = bstack1llll1ll1_opy_
  webdriver.Remote.__init__ = bstack1l1l1ll11_opy_
  webdriver.Remote.get = bstack11l1l11l_opy_
  WebDriver.close = bstack11llll_opy_
  bstack1ll1lll11_opy_()
  if bstack1111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1l1ll_opy_
    except Exception as e:
      logger.error(bstack1lllll_opy_.format(str(e)))
  if (bstack111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౼") in str(bstack1ll1lll1l_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11lll1_opy_
      except Exception as e:
        logger.warn(bstack1l1lll1l_opy_ + str(e))
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1l1lll1l_opy_)
    Output.end_test = bstack11ll1l1l_opy_
    TestStatus.__init__ = bstack1ll1lll1_opy_
    QueueItem.__init__ = bstack1l1ll1111_opy_
    pabot._create_items = bstack1ll111l11_opy_
    try:
      from pabot import __version__ as bstack1l1llll_opy_
      if version.parse(bstack1l1llll_opy_) >= version.parse(bstack111_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬ౽")):
        pabot._run = bstack1l11l11_opy_
      else:
        pabot._run = bstack11ll11ll_opy_
    except Exception as e:
      pabot._run = bstack11ll11ll_opy_
    pabot._create_command_for_execution = bstack111111_opy_
    pabot._report_results = bstack11lll11_opy_
  if bstack111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭౾") in str(bstack1ll1lll1l_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1llllll11_opy_)
    Runner.run_hook = bstack11l1ll1_opy_
    Step.run = bstack1llllllll_opy_
def bstack1l1ll1l_opy_():
  global CONFIG
  if bstack111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ౿") in CONFIG and int(CONFIG[bstack111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಀ")]) > 1:
    logger.warn(bstack11lllll_opy_)
def bstack1l1ll1lll_opy_(bstack1ll11ll1_opy_, index):
  bstack1l1ll1l1l_opy_(bstack1l111l11_opy_)
  exec(open(bstack1ll11ll1_opy_).read())
def bstack11l1l1_opy_(arg):
  global CONFIG
  bstack1l1ll1l1l_opy_(bstack1l1l11l1_opy_)
  os.environ[bstack111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪಁ")] = CONFIG[bstack111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬಂ")]
  os.environ[bstack111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧಃ")] = CONFIG[bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ಄")]
  from _pytest.config import main as bstack1ll111ll_opy_
  bstack1ll111ll_opy_(arg)
def bstack1l1l11l11_opy_(arg):
  bstack1l1ll1l1l_opy_(bstack11l111ll_opy_)
  from behave.__main__ import main as bstack11ll1_opy_
  bstack11ll1_opy_(arg)
def bstack1llll_opy_():
  logger.info(bstack11ll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬಅ"), help=bstack111_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨಆ"))
  parser.add_argument(bstack111_opy_ (u"ࠨ࠯ࡸࠫಇ"), bstack111_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭ಈ"), help=bstack111_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩಉ"))
  parser.add_argument(bstack111_opy_ (u"ࠫ࠲ࡱࠧಊ"), bstack111_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫಋ"), help=bstack111_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧಌ"))
  parser.add_argument(bstack111_opy_ (u"ࠧ࠮ࡨࠪ಍"), bstack111_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಎ"), help=bstack111_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨಏ"))
  bstack1l1l111l_opy_ = parser.parse_args()
  try:
    bstack1l1ll111l_opy_ = bstack111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧಐ")
    if bstack1l1l111l_opy_.framework and bstack1l1l111l_opy_.framework not in (bstack111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ಑"), bstack111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ಒ")):
      bstack1l1ll111l_opy_ = bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬಓ")
    bstack1ll11l1l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll111l_opy_)
    bstack111l1lll_opy_ = open(bstack1ll11l1l1_opy_, bstack111_opy_ (u"ࠧࡳࠩಔ"))
    bstack11l1_opy_ = bstack111l1lll_opy_.read()
    bstack111l1lll_opy_.close()
    if bstack1l1l111l_opy_.username:
      bstack11l1_opy_ = bstack11l1_opy_.replace(bstack111_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨಕ"), bstack1l1l111l_opy_.username)
    if bstack1l1l111l_opy_.key:
      bstack11l1_opy_ = bstack11l1_opy_.replace(bstack111_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫಖ"), bstack1l1l111l_opy_.key)
    if bstack1l1l111l_opy_.framework:
      bstack11l1_opy_ = bstack11l1_opy_.replace(bstack111_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಗ"), bstack1l1l111l_opy_.framework)
    file_name = bstack111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧಘ")
    file_path = os.path.abspath(file_name)
    bstack11ll111_opy_ = open(file_path, bstack111_opy_ (u"ࠬࡽࠧಙ"))
    bstack11ll111_opy_.write(bstack11l1_opy_)
    bstack11ll111_opy_.close()
    logger.info(bstack11l1111l_opy_)
    try:
      os.environ[bstack111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಚ")] = bstack1l1l111l_opy_.framework if bstack1l1l111l_opy_.framework != None else bstack111_opy_ (u"ࠢࠣಛ")
      config = yaml.safe_load(bstack11l1_opy_)
      config[bstack111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨಜ")] = bstack111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨಝ")
      bstack11111l1_opy_(bstack11l11l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1llll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l11ll1_opy_.format(str(e)))
def bstack11111l1_opy_(bstack1l111lll_opy_, config, bstack1111ll11_opy_ = {}):
  global bstack1ll1l1l1l_opy_
  if not config:
    return
  bstack111lll11_opy_ = bstack1lll1llll_opy_ if not bstack1ll1l1l1l_opy_ else ( bstack1ll1lllll_opy_ if bstack111_opy_ (u"ࠪࡥࡵࡶࠧಞ") in config else bstack1l1l1l1ll_opy_ )
  data = {
    bstack111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ಟ"): config[bstack111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧಠ")],
    bstack111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩಡ"): config[bstack111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪಢ")],
    bstack111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬಣ"): bstack1l111lll_opy_,
    bstack111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬತ"): {
      bstack111_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨಥ"): str(config[bstack111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫದ")]) if bstack111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬಧ") in config else bstack111_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢನ"),
      bstack111_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩ಩"): bstack11l111_opy_(os.getenv(bstack111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥಪ"), bstack111_opy_ (u"ࠤࠥಫ"))),
      bstack111_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬಬ"): bstack111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫಭ"),
      bstack111_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ಮ"): bstack111lll11_opy_,
      bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩಯ"): config[bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪರ")]if config[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಱ")] else bstack111_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥಲ"),
      bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಳ"): str(config[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭಴")]) if bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧವ") in config else bstack111_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢಶ"),
      bstack111_opy_ (u"ࠧࡰࡵࠪಷ"): sys.platform,
      bstack111_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪಸ"): socket.gethostname()
    }
  }
  update(data[bstack111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬಹ")], bstack1111ll11_opy_)
  try:
    response = bstack1l111l_opy_(bstack111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ಺"), bstack111llll_opy_, data, config)
    if response:
      logger.debug(bstack111lll1l_opy_.format(bstack1l111lll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll11111_opy_.format(str(e)))
def bstack1l111l_opy_(type, url, data, config):
  bstack1lll111_opy_ = bstack1llllll1_opy_.format(url)
  proxy = bstack1llll1l1l_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstack111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ಻")):
    proxies = {
      bstack111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ಼ࠫ"): proxy
    }
  if config.get(bstack111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪಽ")):
    proxies = {
      bstack111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ಾ"): proxy
    }
  if type == bstack111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ಿ"):
    response = requests.post(bstack1lll111_opy_, json=data,
                    headers={bstack111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨೀ"): bstack111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ು")}, auth=(config[bstack111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೂ")], config[bstack111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨೃ")]), proxies=proxies)
  return response
def bstack11l111_opy_(framework):
  return bstack111_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥೄ").format(str(framework), __version__) if framework else bstack111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ೅").format(__version__)
def bstack1llll11ll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack111l1ll1_opy_()
  logger.debug(bstack1lll111l1_opy_.format(str(CONFIG)))
  bstack1l1l11l_opy_()
  sys.excepthook = bstack1l1111l_opy_
  atexit.register(bstack111ll_opy_)
  signal.signal(signal.SIGINT, bstack1l11111_opy_)
  signal.signal(signal.SIGTERM, bstack1l11111_opy_)
def bstack1l1111l_opy_(exctype, value, traceback):
  bstack11111l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
def bstack11111l_opy_(message = bstack111_opy_ (u"ࠨࠩೆ")):
  global CONFIG
  try:
    if message:
      bstack1111ll11_opy_ = {
        bstack111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨೇ"): str(message)
      }
      bstack11111l1_opy_(bstack1lll11l1l_opy_, CONFIG, bstack1111ll11_opy_)
    else:
      bstack11111l1_opy_(bstack1lll11l1l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11ll1ll_opy_.format(str(e)))
def bstack1ll111lll_opy_(bstack1lllll1ll_opy_, size):
  bstack1l1lll1_opy_ = []
  while len(bstack1lllll1ll_opy_) > size:
    bstack11l11l1l_opy_ = bstack1lllll1ll_opy_[:size]
    bstack1l1lll1_opy_.append(bstack11l11l1l_opy_)
    bstack1lllll1ll_opy_   = bstack1lllll1ll_opy_[size:]
  bstack1l1lll1_opy_.append(bstack1lllll1ll_opy_)
  return bstack1l1lll1_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1llll_opy_)
    return
  if sys.argv[1] == bstack111_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ೈ")  or sys.argv[1] == bstack111_opy_ (u"ࠫ࠲ࡼࠧ೉"):
    logger.info(bstack111_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬೊ").format(__version__))
    return
  if sys.argv[1] == bstack111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬೋ"):
    bstack1llll_opy_()
    return
  args = sys.argv
  bstack1llll11ll_opy_()
  global CONFIG
  global bstack1ll1ll11_opy_
  global bstack1l1l1l1l1_opy_
  global bstack11llll1_opy_
  global bstack1llll1l11_opy_
  global bstack1ll1l1111_opy_
  bstack11111l1l_opy_ = bstack111_opy_ (u"ࠧࠨೌ")
  if args[1] == bstack111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ್") or args[1] == bstack111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ೎"):
    bstack11111l1l_opy_ = bstack111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ೏")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೐"):
    bstack11111l1l_opy_ = bstack111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೑")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ೒"):
    bstack11111l1l_opy_ = bstack111_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭೓")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ೔"):
    bstack11111l1l_opy_ = bstack111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪೕ")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೖ"):
    bstack11111l1l_opy_ = bstack111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ೗")
    args = args[2:]
  elif args[1] == bstack111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ೘"):
    bstack11111l1l_opy_ = bstack111_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭೙")
    args = args[2:]
  else:
    if not bstack111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೚") in CONFIG or str(CONFIG[bstack111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ೛")]).lower() in [bstack111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ೜"), bstack111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫೝ")]:
      bstack11111l1l_opy_ = bstack111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫೞ")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ೟")]).lower() == bstack111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬೠ"):
      bstack11111l1l_opy_ = bstack111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ೡ")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫೢ")]).lower() == bstack111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨೣ"):
      bstack11111l1l_opy_ = bstack111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ೤")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ೥")]).lower() == bstack111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ೦"):
      bstack11111l1l_opy_ = bstack111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭೧")
      args = args[1:]
    elif str(CONFIG[bstack111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ೨")]).lower() == bstack111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೩"):
      bstack11111l1l_opy_ = bstack111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ೪")
      args = args[1:]
    else:
      os.environ[bstack111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ೫")] = bstack11111l1l_opy_
      bstack11lll1l1_opy_(bstack111ll1_opy_)
  global bstack1111l1_opy_
  try:
    os.environ[bstack111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೬")] = bstack11111l1l_opy_
    bstack11111l1_opy_(bstack1ll1ll1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11ll1ll_opy_.format(str(e)))
  global bstack1l11l1l1_opy_
  global bstack1l1l11ll_opy_
  global bstack1l11ll1l_opy_
  global bstack1l1ll1l11_opy_
  global bstack11lllll1_opy_
  global bstack1ll1ll1_opy_
  global bstack1l1111ll_opy_
  global bstack1l1ll11_opy_
  global bstack1111111_opy_
  global bstack1llll1lll_opy_
  global bstack111l111l_opy_
  global bstack1l1ll111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack1ll11l1l_opy_ + str(e))
  bstack1l11l1l1_opy_ = webdriver.Remote.__init__
  bstack1l1ll11_opy_ = WebDriver.close
  try:
    import Browser
    from subprocess import Popen
    bstack1111l1_opy_ = Popen.__init__
  except Exception as e:
    logger.debug(bstack1l11lll1l_opy_ + str(e))
  bstack111l111l_opy_ = WebDriver.get
  if bstack1ll1l111l_opy_():
    if bstack11l111l_opy_() < version.parse(bstack1l1l1llll_opy_):
      logger.error(bstack1ll1l_opy_.format(bstack11l111l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1ll111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1lllll_opy_.format(str(e)))
  if (bstack11111l1l_opy_ in [bstack111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೭"), bstack111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೮"), bstack111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ೯")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11lll1_opy_
      except Exception as e:
        logger.warn(bstack1l1lll1l_opy_ + str(e))
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1l1lll1l_opy_)
    bstack1l1l11ll_opy_ = Output.end_test
    bstack1l11ll1l_opy_ = TestStatus.__init__
    bstack11lllll1_opy_ = pabot._run
    bstack1ll1ll1_opy_ = QueueItem.__init__
    bstack1l1111ll_opy_ = pabot._create_command_for_execution
  if bstack11111l1l_opy_ == bstack111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ೰"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1llllll11_opy_)
    bstack1111111_opy_ = Runner.run_hook
    bstack1llll1lll_opy_ = Step.run
  if bstack11111l1l_opy_ == bstack111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩೱ"):
    bstack1l1l1l1_opy_()
    bstack1l1ll1l_opy_()
    if bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ೲ") in CONFIG:
      bstack1l1l1l1l1_opy_ = True
      bstack1l1111_opy_ = []
      for index, platform in enumerate(CONFIG[bstack111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧೳ")]):
        bstack1l1111_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1l1ll1lll_opy_, args=(args[0], index)))
      for t in bstack1l1111_opy_:
        t.start()
      for t in bstack1l1111_opy_:
        t.join()
    else:
      bstack1l1ll1l1l_opy_(bstack1l111l11_opy_)
      exec(open(args[0]).read())
  elif bstack11111l1l_opy_ == bstack111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೴") or bstack11111l1l_opy_ == bstack111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೵"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1l1lll1l_opy_)
    bstack1l1l1l1_opy_()
    bstack1l1ll1l1l_opy_(bstack1l1lll_opy_)
    if bstack111_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ೶") in args:
      i = args.index(bstack111_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭೷"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1ll1ll11_opy_))
    args.insert(0, str(bstack111_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ೸")))
    pabot.main(args)
  elif bstack11111l1l_opy_ == bstack111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ೹"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1l1lll1l_opy_)
    for a in args:
      if bstack111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ೺") in a:
        bstack11llll1_opy_ = int(a.split(bstack111_opy_ (u"ࠬࡀࠧ೻"))[1])
      if bstack111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ೼") in a:
        bstack1llll1l11_opy_ = str(a.split(bstack111_opy_ (u"ࠧ࠻ࠩ೽"))[1])
      if bstack111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ೾") in a:
        bstack1ll1l1111_opy_ = str(a.split(bstack111_opy_ (u"ࠩ࠽ࠫ೿"))[1])
    bstack1l1ll1l1l_opy_(bstack1l1lll_opy_)
    run_cli(args)
  elif bstack11111l1l_opy_ == bstack111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪഀ"):
    try:
      from _pytest.config import _prepareconfig
      import importlib
      bstack11l1l11_opy_ = importlib.find_loader(bstack111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ഁ"))
      if bstack11l1l11_opy_ is None:
        bstack1llll111l_opy_(e, bstack11l11l11_opy_)
    except Exception as e:
      bstack1llll111l_opy_(e, bstack11l11l11_opy_)
    bstack1l1l1l1_opy_()
    try:
      if bstack111_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧം") in args:
        i = args.index(bstack111_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨഃ"))
        args.pop(i+1)
        args.pop(i)
      if bstack111_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪഄ") in args:
        i = args.index(bstack111_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫഅ"))
        args.pop(i+1)
        args.pop(i)
      if bstack111_opy_ (u"ࠩ࠰ࡴࠬആ") in args:
        i = args.index(bstack111_opy_ (u"ࠪ࠱ࡵ࠭ഇ"))
        args.pop(i+1)
        args.pop(i)
      if bstack111_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬഈ") in args:
        i = args.index(bstack111_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ഉ"))
        args.pop(i+1)
        args.pop(i)
      if bstack111_opy_ (u"࠭࠭࡯ࠩഊ") in args:
        i = args.index(bstack111_opy_ (u"ࠧ࠮ࡰࠪഋ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1lll11l11_opy_ = config.args
    bstack1lll1l1ll_opy_ = config.invocation_params.args
    bstack1lll1l1ll_opy_ = list(bstack1lll1l1ll_opy_)
    bstack1l1l111ll_opy_ = []
    for arg in bstack1lll1l1ll_opy_:
      for spec in bstack1lll11l11_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1l1l111ll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack111_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩഌ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll11l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l1lll1_opy_)))
                    for bstack1l1l1lll1_opy_ in bstack1lll11l11_opy_]
    bstack1l1l111ll_opy_.append(bstack111_opy_ (u"ࠩ࠰ࡴࠬ഍"))
    bstack1l1l111ll_opy_.append(bstack111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨഎ"))
    bstack1l1l111ll_opy_.append(bstack111_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ഏ"))
    bstack1l1l111ll_opy_.append(bstack111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬഐ"))
    bstack11l11_opy_ = []
    for spec in bstack1lll11l11_opy_:
      bstack1llll1_opy_ = []
      bstack1llll1_opy_.append(spec)
      bstack1llll1_opy_ += bstack1l1l111ll_opy_
      bstack11l11_opy_.append(bstack1llll1_opy_)
    bstack1l1l1l1l1_opy_ = True
    bstack111l11l1_opy_ = 1
    if bstack111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭഑") in CONFIG:
      bstack111l11l1_opy_ = CONFIG[bstack111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧഒ")]
    bstack1lll1l1l1_opy_ = int(bstack111l11l1_opy_)*int(len(CONFIG[bstack111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫഓ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬഔ")]):
      for bstack1llll1_opy_ in bstack11l11_opy_:
        item = {}
        item[bstack111_opy_ (u"ࠪࡥࡷ࡭ࠧക")] = bstack1llll1_opy_
        item[bstack111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪഖ")] = index
        execution_items.append(item)
    bstack1ll111111_opy_ = bstack1ll111lll_opy_(execution_items, bstack1lll1l1l1_opy_)
    for execution_item in bstack1ll111111_opy_:
      bstack1l1111_opy_ = []
      for item in execution_item:
        bstack1l1111_opy_.append(threading.Thread(name=str(item[bstack111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫഗ")]),
                                            target=bstack11l1l1_opy_,
                                            args=(item[bstack111_opy_ (u"࠭ࡡࡳࡩࠪഘ")],)))
      for t in bstack1l1111_opy_:
        t.start()
      for t in bstack1l1111_opy_:
        t.join()
  elif bstack11111l1l_opy_ == bstack111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧങ"):
    try:
      from behave.__main__ import main as bstack11ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1llll111l_opy_(e, bstack1llllll11_opy_)
    bstack1l1l1l1_opy_()
    bstack1l1l1l1l1_opy_ = True
    bstack111l11l1_opy_ = 1
    if bstack111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨച") in CONFIG:
      bstack111l11l1_opy_ = CONFIG[bstack111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഛ")]
    bstack1lll1l1l1_opy_ = int(bstack111l11l1_opy_)*int(len(CONFIG[bstack111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ജ")]))
    config = Configuration(args)
    bstack1lll11l11_opy_ = config.paths
    bstack11l1111_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1lll11l11_opy_:
        bstack11l1111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack111_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬഝ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll11l11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l1lll1_opy_)))
                    for bstack1l1l1lll1_opy_ in bstack1lll11l11_opy_]
    bstack11l11_opy_ = []
    for spec in bstack1lll11l11_opy_:
      bstack1llll1_opy_ = []
      bstack1llll1_opy_ += bstack11l1111_opy_
      bstack1llll1_opy_.append(spec)
      bstack11l11_opy_.append(bstack1llll1_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨഞ")]):
      for bstack1llll1_opy_ in bstack11l11_opy_:
        item = {}
        item[bstack111_opy_ (u"࠭ࡡࡳࡩࠪട")] = bstack111_opy_ (u"ࠧࠡࠩഠ").join(bstack1llll1_opy_)
        item[bstack111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧഡ")] = index
        execution_items.append(item)
    bstack1ll111111_opy_ = bstack1ll111lll_opy_(execution_items, bstack1lll1l1l1_opy_)
    for execution_item in bstack1ll111111_opy_:
      bstack1l1111_opy_ = []
      for item in execution_item:
        bstack1l1111_opy_.append(threading.Thread(name=str(item[bstack111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨഢ")]),
                                            target=bstack1l1l11l11_opy_,
                                            args=(item[bstack111_opy_ (u"ࠪࡥࡷ࡭ࠧണ")],)))
      for t in bstack1l1111_opy_:
        t.start()
      for t in bstack1l1111_opy_:
        t.join()
  else:
    bstack11lll1l1_opy_(bstack111ll1_opy_)
  bstack1l1ll11ll_opy_()
def bstack1l1ll11ll_opy_():
  global CONFIG
  try:
    if bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧത") in CONFIG:
      host = bstack111_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨഥ") if bstack111_opy_ (u"࠭ࡡࡱࡲࠪദ") in CONFIG else bstack111_opy_ (u"ࠧࡢࡲ࡬ࠫധ")
      user = CONFIG[bstack111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪന")]
      key = CONFIG[bstack111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬഩ")]
      bstack11l1l1l_opy_ = bstack111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩപ") if bstack111_opy_ (u"ࠫࡦࡶࡰࠨഫ") in CONFIG else bstack111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧബ")
      url = bstack111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭ഭ").format(user, key, host, bstack11l1l1l_opy_)
      headers = {
        bstack111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭മ"): bstack111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫയ"),
      }
      if bstack111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫര") in CONFIG:
        params = {bstack111_opy_ (u"ࠪࡲࡦࡳࡥࠨറ"):CONFIG[bstack111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧല")], bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨള"):CONFIG[bstack111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨഴ")]}
      else:
        params = {bstack111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬവ"):CONFIG[bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫശ")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1111llll_opy_ = response.json()[0][bstack111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬഷ")]
        if bstack1111llll_opy_:
          bstack1111l111_opy_ = bstack1111llll_opy_[bstack111_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧസ")].split(bstack111_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪഹ"))[0] + bstack111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ഺ") + bstack1111llll_opy_[bstack111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥ഻ࠩ")]
          logger.info(bstack1ll1111l_opy_.format(bstack1111l111_opy_))
          bstack1l1l1ll1_opy_ = CONFIG[bstack111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ഼ࠪ")]
          if bstack111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪഽ") in CONFIG:
            bstack1l1l1ll1_opy_ += bstack111_opy_ (u"ࠩࠣࠫാ") + CONFIG[bstack111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬി")]
          if bstack1l1l1ll1_opy_!= bstack1111llll_opy_[bstack111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩീ")]:
            logger.debug(bstack11llll1l_opy_.format(bstack1111llll_opy_[bstack111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪു")], bstack1l1l1ll1_opy_))
    else:
      logger.warn(bstack1111l1ll_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l11l1_opy_.format(str(e)))
def bstack1l1ll11l1_opy_(url, bstack1lllll11l_opy_=False):
  global CONFIG
  global bstack11l1l1l1_opy_
  if not bstack11l1l1l1_opy_:
    hostname = bstack1l11lll11_opy_(url)
    is_private = bstack1ll1111l1_opy_(hostname)
    if (bstack111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪൂ") in CONFIG and not CONFIG[bstack111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫൃ")]) and (is_private or bstack1lllll11l_opy_):
      bstack11l1l1l1_opy_ = hostname
def bstack1l11lll11_opy_(url):
  return urlparse(url).hostname
def bstack1ll1111l1_opy_(hostname):
  for bstack11l111l1_opy_ in bstack1lll11_opy_:
    regex = re.compile(bstack11l111l1_opy_)
    if regex.match(hostname):
      return True
  return False