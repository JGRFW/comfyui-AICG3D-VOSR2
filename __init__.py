# Copyright (C) 2026 AICG3D
# SPDX-License-Identifier: GPL-3.0-or-later
# -*- coding: utf-8 -*-
"""AICG3D-VOSR2 —— VOSR2 图像 / 视频超分辨率放大的 ComfyUI 加速节点。"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

# 底层 .pyd 里的品牌字符串是「等长替换」的：改短了会破坏文件内部地址偏移，
# 所以短出来的字节用空格补在尾部。这里统一去掉首尾空格，
# 让节点菜单和分类里显示的名字干净。
for _cls in NODE_CLASS_MAPPINGS.values():
    _cat = getattr(_cls, "CATEGORY", None)
    if isinstance(_cat, str):
        _cls.CATEGORY = _cat.strip()

NODE_DISPLAY_NAME_MAPPINGS = {
    _k: (_v.strip() if isinstance(_v, str) else _v)
    for _k, _v in NODE_DISPLAY_NAME_MAPPINGS.items()
}
