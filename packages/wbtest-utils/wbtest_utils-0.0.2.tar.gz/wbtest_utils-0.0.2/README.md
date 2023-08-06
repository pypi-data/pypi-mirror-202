# 仓库简介
这是Android基础架构组alpha和release阶段自动化测试库， 包含alpha和release阶段的UI、日志、接口等case。

## 1. case_suite
case_suite目录下保存各个业务的测试case，目前实现了UG日志下S0级别1339的case。

## 2. 环境配置
配置文件位于根目录的`config.yaml`文件中，并在`case_suite/common.air/common.py`中进行读取和初始化。可根据测试环境的不同，自定义`config.yaml`中的内容

## 3. 模块导入
在使用Pycharm运行相关case脚本时，如果需要引入其他脚本，需要使用airtest框架中的using特性并且using方法和python的from导包顺序不能调换。


```python
from airtest.core.api import *

auto_setup(__file__)
using("../utils/release.air")
from release import goto_language
```

## 4. 连接设备
在使用Pycharm运行case前需要连接硬件设备，并且在auto_setup中详细指定设备的平台、IP地址、端口号等信息。否则在Pycharm中运行会报错。

```python
from airtest.core.api import *
auto_setup(__file__, devices=[DEVICE_INFO])
```

## 5. 运行case
如果想要运行相关case，可以使用AirTestIDE、Pycharm等集成开发环境运行。在AirTest中，脚本后缀名是air，其本质是一个.py文件并附带一些图片资源。
.air文件在AirTestIDE中可以直接运行。

## 6. 捞取日志
日志测试case是通过adb命令先将app运行过程中的日志文件复制到本地测试环境后，再对日志内容进行测试，因此拉取日志会有一定时间的延迟，此外app端生成日志文件也会有一定的延迟。
为了避免在测试期间由于日志文件读写时机引发的异常，需要在捞取日志之前等待一段时间用于日志文件的生成和读写。日志文件的生成和读写逻辑位于`android_utils.py`脚本中。