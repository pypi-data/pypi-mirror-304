# -*- coding: utf-8 -*-
# @Project: 芒果测试平台# @Description: # @Time   : 2023-07-07 10:14
# @Author : 毛鹏
from .mango_error import MangoKitError


class UiError(MangoKitError):
    pass


class ReplaceElementLocatorError(UiError):
    pass
