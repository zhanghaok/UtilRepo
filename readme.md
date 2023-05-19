## 一些工具函数


## Tensorboard的使用
使用Tensorboard可视化训练过程的Loss曲线是PyTorch中非常常见的操作。以下是一些步骤：

1. 安装Tensorboard

首先，确保你已经安装了Tensorboard。如果你还没有安装它，可以通过以下命令在终端中安装：

```
pip install tensorboard
```

2. 导入Tensorboard和其他必要的库

在你的PyTorch项目中，首先需要导入Tensorboard和其他必要的库。例如：

```python
from torch.utils.tensorboard import SummaryWriter
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
import torch
```

3. 初始化SummaryWriter

在训练过程中，你需要将数据写入Tensorboard的摘要（summary）文件。因此，需要初始化一个`SummaryWriter`对象。这个对象将在训练过程中记录摘要信息。

```python
writer = SummaryWriter()
```

4. 写入Loss的摘要信息

在训练循环中，你可以使用`writer.add_scalar`方法将Loss的摘要信息写入摘要文件。例如：

```python
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data

        optimizer.zero_grad()

        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i % 1000 == 999:
            # 记录每1000个batch的loss
            writer.add_scalar('training loss',
                              running_loss / 1000,
                              epoch * len(trainloader) + i)
            running_loss = 0.0
```

在上面的代码中，`writer.add_scalar`方法需要三个参数：

- `tag`：摘要信息的标签。在这个例子中，我们使用了`training loss`作为标签。这个标签将在Tensorboard中显示。
- `scalar_value`：摘要信息的值。在这个例子中，我们使用了`running_loss / 1000`作为值。这个值将作为Loss曲线的y轴值。
- `global_step`：全局步数。在这个例子中，我们使用了`epoch * len(trainloader) + i`作为全局步数。这个全局步数将作为Loss曲线的x轴值。

5. 启动Tensorboard

在终端中运行以下命令，启动Tensorboard：

```
tensorboard --logdir=runs
```

6. 查看Loss曲线

在浏览器中打开`http://localhost:6006`，你应该可以看到Tensorboard的界面。在左侧导航栏中选择`Scalars`，你应该可以看到训练过程中Loss曲线的图表。
## plot工具包画图
```python
data = "../roberta-pretain/May18_11-17-09_xjtuPC6.csv"
import pandas as pd

df = pd.read_csv(data)
df
```
```python
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# X和Y轴数据
x = df["Step"]
y = df["Value"]

# 用Matplotlib绘制折线图
# 创建一个新的图形
fig, ax = plt.subplots()
# 绘制数据
ax.plot(x, y,color="red")
# 定义刻度格式化器函数
def format_func(value, tick_number):
    # 将刻度值除以1000，并添加"k"表示千
    return f"{value/1000:.0f}k"
# 将格式化器应用于横坐标轴
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))
# 添加水平线
ax.axhline(y=0.6, color='gray', linestyle='--', linewidth=1)
ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=1)
ax.axhline(y=0.7, color='gray', linestyle='--', linewidth=1)
ax.axhline(y=0.8, color='gray', linestyle='--', linewidth=1)

# 添加垂直线
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1)
ax.axvline(x=20000, color='gray', linestyle='--', linewidth=1)
ax.axvline(x=40000, color='gray', linestyle='--', linewidth=1)
ax.axvline(x=60000, color='gray', linestyle='--', linewidth=1)
ax.axvline(x=80000, color='gray', linestyle='--', linewidth=1)
ax.axvline(x=100000, color='gray', linestyle='--', linewidth=1)
ax.axvline(x=120000, color='gray', linestyle='--', linewidth=1)
ax.axvline(x=140000, color='gray', linestyle='--', linewidth=1)


# 添加底色
# plt.rcParams['axes.facecolor']='snow'
plt.rcParams['axes.facecolor']='#ecd9c0'
# 添加标题和标签
plt.title("Tax domain-adaptive pre-training on RoBERTa")
plt.xlabel("Step")
plt.ylabel("Pretrain Loss(MLM)")

# 显示图形
plt.show()
```
