## 眼动数据处理

此文件夹用于存储处理**眼动**数据的代码

### eye_process.py

**说明**：

此程序适用于使用[psychopy_tobii_controller](<https://github.com/hsogo/psychopy_tobii_controller>)生成的眼动文件

**目的分析**：

1. 由于眼动程序生成的文件格式是tsv (tobii支持)，为了excel处理方便
   在源代码中改成了xls，但excel不能正常打开，所以不能直接使用pandas。
   解决思路：通过`with open`打开，通过数据格式处理，转为pandas支持的数据框。
2. 输出的眼动文件中，以屏幕中心为0点。但为了方便计算，需要改成以左上角为0点。
   解决思路：显示器分辨率为`1920*1080`，因此，`x + 960`, `y + 540`
3. 在`Event`列，输出的眼动文件中，只在每一事件开始时的一行写`trigger`。为了后续
   分析方面，需要连续写入相同`trigger`，直到该事件结束。
   解决思路：
       1) 使用`fillna(method='ffill')`，以前一个`trigger`为准，填充空值
       2) 使用`fillna('Event')`填充其他空值
4. 原眼动文件中空值的标记方式是`np.nan`,为了方便后续在`matlab`中计算眼动，需改成"-1"
   解决思路：在`Event`列处理完成后通过`fillna(-1)`实现
5. 删除特定行，如`Event==1`, `Event=='Event'`等
   解决思路：获取特定行的`index`，使用`tolist()`转为列表，通过`drop()`删除
6. 将TimeStamp列时间递增。即第二个试次的开始时间为第一个试次的结束时间。


### ns_el_pre.m 
脑电和眼动结合批处理脚本
用于分析基于eeglab和eye-eeg联合数据的预处理脚本，具体使用方法可以参考：[csdn博客](https://blog.csdn.net/zjjoebloggs/article/details/126346626?csdn_share_tail=%7B%22type%22%3A%22blog%22%2C%22rType%22%3A%22article%22%2C%22rId%22%3A%22126346626%22%2C%22source%22%3A%22zjjoebloggs%22%7D)
该脚本处理的脑电数据是neuroScan产生的，眼动文件是eyelink产生

### BP_pre.m
和ns_el_pre一样，只不过脑电文件时BrainProduct产生

### position_gain.py
用于计算positon gain。眼动文件由eyelink中的dataViewer导出

### compute-mean-std-checkpoint.ipynb
计算眼动数据的平均数和标准差。眼动文件由eyelink中的dataViewer导出

## Update Log

- 二〇一九年五月十六日 21:44:19，创建README
- 二〇一九年五月十六日 21:59:04，上传 `eye_process.py`并添加说明
- 二〇一九年五月三十一日 15:01:48，添加add_time()
- 2019-10-31 22:18:47，**大更新**：
  - 更新原有计算中的bug
  - 优化代码
 - 2022-08-15 更新README.MD
