<div align="center">

# RVC for Colab

[English](./README.md) | **简体中文**

在 Google Colab 上运行官方 [RVC WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)，训练自己的声音模型并进行变声，无需本地 GPU。

[![在 Colab 中打开](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_For_Colab.ipynb)
[![RVC](https://img.shields.io/badge/RVC-2.3.260718-black?logo=github)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/releases/tag/2.3.260718)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

## 项目简介

本仓库只包含一个 Colab 笔记本 [`RVC_For_Colab.ipynb`](./RVC_For_Colab.ipynb)。它会克隆官方 [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) 的固定 release（当前为 **2.3.260718**），在 Colab 上配置好环境并运行。

笔记本会：

- 把 Colab 自带的 Torch 换成上游要求的版本（2.7.1，CUDA 12.8），并改用 PyPI 安装依赖，不走上游 requirements 中写死的国内镜像
- 按上游要求的目录结构下载 HuBERT、RMVPE、底模和 UVR5 模型
- 通过 Gradio 公网链接或 ngrok 隧道启动 WebUI
- 在 Colab 禁止运行 WebUI 时，提供命令行训练单元格
- 借助谷歌云盘备份和恢复模型

> 2026 年 10 月之前，本仓库是一个包含 RVC 2.2 代码副本的 fork。该版本保存在 [`legacy-2.2`](https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/tree/legacy-2.2) tag 中。

## 环境要求

- 一个 Google 账号（用于 Colab 和谷歌云盘）。
- 目标声音的数据集：尽量干净、背景噪音小的录音。建议 10–30 分钟的说话或演唱，越多越好，推荐 `.wav` 格式。

## 快速开始

1. 点击上方 **Open in Colab** 徽章，然后 `文件 > 在云端硬盘中保存一份副本`，以便保留修改。
2. 选择 GPU 运行时：`代码执行程序 > 更改运行时类型 > T4 GPU`。
3. 按顺序运行 **准备环境** 中的单元格：
   1. 克隆 RVC 官方仓库，`RVC_REF` 指定上游的 tag 或分支
   2. 安装依赖，需要几分钟
   3. 下载模型：v2 底模必定下载，v1 底模和 UVR5 可选
   4. 挂载谷歌云盘
   5. 将数据集解压到 `/content/dataset`，zip 内直接放音频文件即可
4. 从下面两种方式中任选一种。

### 方式一：WebUI

- **方案一** 使用 Gradio 公网链接（`*.gradio.live`）启动 WebUI，打开输出中的链接即可。
- **方案二** 通过 ngrok 暴露 WebUI，需先在 <https://dashboard.ngrok.com> 获取 Authtoken 并填入。

在 WebUI 的训练页中把训练集路径填为 `/content/dataset`，然后依次执行各步骤（或点击“一键训练”）。训练好的模型保存在 `assets/weights`，索引保存在 `logs/<模型名>`。

### 方式二：命令行训练

免费版 Colab 可能会禁止运行 WebUI，此时可使用 **方式二** 中的单元格，命令参考上游的 [CLI 文档](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/cn/cli.md)：

| 单元格 | 作用 |
| --- | --- |
| 音频预处理 | `train/preprocess.py`：切分并重采样数据集，输出到 `logs/<模型名>` |
| 提取音高与特征 | `train/dataset/extract_f0.py`（推荐 `rmvpe_gpu`）和 `extract_hubert_feature.py` |
| 训练模型 | 按 WebUI 的方式生成 `filelist.txt` / `config.json`，然后运行 `train/train.py` |
| 训练特征索引 | `train/train_index.py`：生成推理时使用的 faiss 索引 |

所有单元格中的模型名、采样率和版本需保持一致。

### 备份与恢复

- **备份** 会把 `G_*.pth` / `D_*.pth`、`config.json`、索引以及 `assets/weights` 中导出的模型复制到 `MyDrive/RVC_backup/<模型名>`。
- **恢复** 会把这些文件复制回来，用于继续训练或推理。
- 如果训练时开启了“仅保存最新”（默认开启），检查点的 epoch 为 `2333333`。
- 2025 年版笔记本的备份直接放在 MyDrive 根目录，且 G/D 文件名是互换的，恢复这类备份时请勾选 `LEGACY_BACKUP`。

## 升级到更新的 RVC 版本

把第一个单元格中的 `RVC_REF` 改为更新的 [上游 tag](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/tags) 或 `main`。笔记本只针对默认值测试过，如果新版本无法运行，欢迎提 Issue。

## 注意事项

- **Colab 限制：** 免费 GPU 有使用时长限制，长时间训练可能被中断，请定期备份到云盘。
- **临时存储：** `/content` 下的文件会在运行时断开后被删除，数据集和模型请保存在云盘中。
- **数据集质量** 对效果影响最大。请使用无混响、无伴奏、无噪音的干净录音，可以先用 UVR5 分离人声。
- **调参：** 可以尝试增加 epoch，或在推理时调整 `index_rate`。

## 问题排查

- **“GPU 不可用”或已断开连接：** 确认已选择 GPU 运行时。也可能是达到了 Colab 的使用上限，请稍后再试或升级。
- **Python 版本警告：** RVC 2.3 面向 Python 3.12。如果 Colab 换成了其他版本，依赖安装可能失败，欢迎提 Issue。
- **依赖安装出错：** 重启运行时（`代码执行程序 > 重启会话`）后重新运行安装单元格。
- **提示底模不存在（pretrained model not exist）：** 请运行下载单元格，模型必须位于 `assets/` 目录下。
- **找不到文件：** 检查填写的路径，尤其是数据集 zip 和云盘备份目录。

## 合理使用

未经本人明确同意，请勿使用变声技术冒充他人或制作误导性内容。使用者需对自己生成和传播的音频负责。

## 贡献者

笔记本维护者：[@juksentang](https://github.com/juksentang)

<a href="https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juksentang/RVC-Retrieval-based-Voice-Conversion-Colab" alt="Contributors" />
</a>

RVC 本身由 [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) 及其 [贡献者](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors) 开发。笔记本相关的 Issue 和 PR 欢迎提交到本仓库，RVC 本身的 bug 请提交到 [上游](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/issues)。

## 许可证

笔记本以 [MIT 协议](./LICENSE) 开源。RVC 及其下载的模型遵循上游的 [协议与使用条款](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)。
