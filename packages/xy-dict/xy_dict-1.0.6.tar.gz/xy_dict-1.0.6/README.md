# xy_dict


- [简体中文](readme/README_zh_CN.md)
- [繁体中文](readme/README_zh_TW.md)
- [English](readme/README_en.md)


## 说明
字典工具。

## 源码仓库

- <a href="https://github.com/xy-base/xy_dict.git" target="_blank">Github地址</a>  
- <a href="https://gitee.com/xy-base/xy_dict.git" target="_blank">Gitee地址</a>


## 安装

```bash
pip install xy_dict
```

## 使用

```python

from xy_dict.utils import is_empty_dict, dict_get

object_map_0 = {}
is_empty_dict(object_map_0)
# True

object_map_1 = {"key_0":"object_0"}
is_empty_dict(object_map_1)
# False

dict_get(object_map_1, "key_0")
# object_0

dict_get(object_map_0, "key_0")
# None

from xy_dict.Dict import Dict

object_map_2 = {"key_0":"object_0", "key_1":{"key_2":"object_2"}, "key_3":["object_3"]}
object_dict = Dict(object_map_2)

object_dict.search_k("key_0")
object_dict.key_map
# {'key_0': 'object_0'}

object_dict.search_k("key_1")
object_dict.key_map
# {'key_1': {'key_2': 'object_2'}}

object_dict.search_v("object_0")
object_dict.key_map
# {'key_0': 'object_0'}

object_dict.search_v({"key_2":"object_2"})
object_dict.key_map
# {'key_1': {'key_2': 'object_2'}}

object_dict.search_kv('key_0', 'object_0')
object_dict.key_map
# {'key_0': 'object_0'}

object_dict.search_kv('key_0', 'object_0')
object_dict.key_map
# {'key_0': 'object_0'}

object_dict.search_kv('key_0', 'object_01')
object_dict.key_map
# {}

```

## 许可证
xy_dict 根据 <木兰宽松许可证, 第2版> 获得许可。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 捐赠

如果小伙伴们觉得这些工具还不错的话，能否请咱喝一杯咖啡呢?  
  
![Pay-Total](./readme/Pay-Total.png)

## 联系方式

```
微信: yuyangiit
邮箱: yuyangit.0515@qq.com
```