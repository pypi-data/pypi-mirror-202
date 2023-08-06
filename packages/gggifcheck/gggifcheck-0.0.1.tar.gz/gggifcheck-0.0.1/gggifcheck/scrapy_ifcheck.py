# -*- coding:utf-8 -*-
# author: kusen
# email: 1194542196@qq.com
# date: 2023/4/13


import scrapy
from gggifcheck.items import CheckItem


class ScrapyCheckItem(scrapy.Item, CheckItem):

    def __getitem__(self, key):
        if key in self.fields and key not in self._values:
            value = None
            for field1, field2 in self.relate_process_default:
                value = self[field2]
                break
            self[key] = value
        return self._values[key]

    def __setitem__(self, key, value):
        if key in self.fields:
            field = self.fields[key]['check_field']
            field.input(key, value)
            self._values[key] = field.value
        else:
            raise KeyError(
                f"{self.__class__.__name__} does not support field: {key}")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            raise AttributeError(
                f"Use item[{name!r}] = {value!r} to set field value")

    def keys(self):
        self._process_and_check()
        _ = [self[field] for field in self.fields]  # 进行所有字段检查
        return self._values.keys()
