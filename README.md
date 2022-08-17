# psychCode
这个仓库用于存放一些在研究生期间用python编写的代码。

### FaceRating

用psychopy写的一个面孔评定程序。代码很简陋，是为了上课交作业。

### behaviorData

处理实验中的行为数据。

### eyemoveData

处理实验中的眼动数据。

### crossSpatialCueingTask

跨通道空间线索任务。

### SmoothPursuitTask

平滑追踪任务。包括两种：

- 基于正弦波的平滑追踪（Lissajous curve）
- 基于八个方向的直线追踪任务

眼动部分使用的EyeLink眼动仪。使用Psychopy和pylink连接。

感谢王志国老师@[zhiguo-eyelab](https://github.com/zhiguo-eyelab)的帮助。

### edf2asc.py
把eyelink的.edf文件批量转为.asc文件。使用前，需要到eyelink官网安装**EyeLink Developers Kit** 

### transFile.py
一个在windows下转移文件的小脚本

### fixtion_erp.m
使用ERPLAB批处理数据

## Updata Log

- 二〇一九年五月十六日 22:05:52，更新eyemoveData
- 二〇一九年六月二日 11:00:37，添加crossSpatialCueingTask
- 2021年4月12日 20:07:01，更新SmoothPursuitTask
- 2022-08-15 更新README.MD
- 2022-08-17 上传fixation_erp.m
