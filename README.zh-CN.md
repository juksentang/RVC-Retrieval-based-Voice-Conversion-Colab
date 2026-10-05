<div align="center">

# RVC for Colab

[English](./README.md) | **简体中文**

在 Google Colab 上用 RVC（Retrieval-based Voice Conversion，基于检索的语音转换）训练自己的声音模型并进行变声，无需本地 GPU。

[![在 Colab 中打开](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_For_Colab.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Upstream](https://img.shields.io/badge/upstream-RVC--Project-black?logo=github)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

</div>

## 项目简介

本仓库 fork 自 [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)，提供一个开箱即用的 Colab 笔记本。笔记本适配了 Colab 当前的 **Python 3.11** 环境，并修复了原 Colab 流程中的若干 bug。

主要功能：

- 完全在 Google Colab 中运行，本地无需任何配置。
- 通过 Gradio 公网链接或 ngrok 隧道使用 RVC WebUI 进行训练和推理。
- 当免费版 Colab 禁止运行 WebUI 时，可改用命令行训练。
- 借助谷歌云盘备份和恢复模型。
- 附带 UVR5 人声 / 伴奏分离模型。

## 环境要求

- 一个 Google 账号（用于 Colab 和谷歌云盘）。
- 目标声音的数据集：尽量干净、背景噪音小的录音。建议 10–30 分钟的说话或演唱，越多越好，推荐 `.wav` 格式。

## 快速开始

1. 点击上方 **Open in Colab** 徽章，然后 `文件 > 在云端硬盘中保存一份副本`，以便保留修改。
2. 选择 GPU 运行时：`代码执行程序 > 更改运行时类型 > T4 GPU`。
3. 按顺序运行 **准备环境** 中的单元格：
   1. 克隆仓库
   2. 安装依赖
   3. 下载预训练模型（下载到 `assets/pretrained_v2`、`assets/uvr5_weights`、`assets/hubert`、`assets/rmvpe`）
   4. 挂载谷歌云盘
   5. 将数据集解压到 `/content/dataset`，zip 内直接放音频文件即可
4. 从下面两种方式中任选一种。

### 方式一：WebUI

- **方案一** 使用 Gradio 公网链接（`*.gradio.live`）启动 WebUI，打开输出中的链接即可。
- **方案二** 通过 ngrok 暴露 WebUI，需先在 <https://dashboard.ngrok.com> 获取 Authtoken 并填入。

在 WebUI 的训练页中把训练集路径填为 `/content/dataset`，然后依次执行各步骤（或点击“一键训练”）。训练好的模型保存在 `assets/weights`，索引保存在 `logs/<模型名>`。

### 方式二：命令行训练

免费版 Colab 可能会禁止运行 WebUI，此时可使用 **方式二** 中的单元格：

| 单元格 | 作用 |
| --- | --- |
| 音频预处理 | 切分并重采样数据集，输出到 `logs/<模型名>` |
| 提取音高与特征 | 提取音高（推荐 `rmvpe_gpu`）和 HuBERT 特征 |
| 训练模型 | 生成 filelist / config，并基于 v2 底模训练 |
| 训练特征索引 | 生成推理时使用的 faiss 索引 |

所有单元格中的模型名、采样率和版本需保持一致。

### 备份与恢复

- **备份** 会把 `G_*.pth` / `D_*.pth`、`config.json`、索引以及 `assets/weights` 中导出的模型复制到 `MyDrive/RVC_backup/<模型名>`。
- **恢复** 会把这些文件复制回来，用于继续训练或推理。旧版笔记本的备份直接放在 MyDrive 根目录，且 G/D 文件名是互换的，恢复这类备份时请勾选 `LEGACY_BACKUP`。
- 如果训练时开启了“仅保存最新”，检查点的 epoch 为 `2333333`。

## 注意事项

- **Colab 限制：** 免费 GPU 有使用时长限制，长时间训练可能被中断，请定期备份到云盘。
- **临时存储：** `/content` 下的文件会在运行时断开后被删除，数据集和模型请保存在云盘中。
- **数据集质量** 对效果影响最大。请使用无混响、无伴奏、无噪音的干净录音，可以先用 UVR5 分离人声。
- **调参：** 可以尝试增加 epoch、更换音高提取算法（`rmvpe` 通常效果最好），或在推理时调整 `index_rate`。

## 问题排查

- **“GPU 不可用”或已断开连接：** 确认已选择 GPU 运行时。也可能是达到了 Colab 的使用上限，请稍后再试或升级。
- **依赖安装出错：** 本笔记本面向 Python 3.11。请重启运行时（`代码执行程序 > 重启会话`）后重新运行安装单元格。
- **提示底模不存在（pretrained model not exist）：** 请运行下载单元格，模型必须位于 `assets/` 目录下。
- **找不到文件：** 检查填写的路径，尤其是数据集 zip 和云盘备份目录。

## 合理使用

未经本人明确同意，请勿使用变声技术冒充他人或制作误导性内容。使用者需对自己生成和传播的音频负责。

## 贡献者

维护者：[@juksentang](https://github.com/juksentang)

本项目建立在 [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) 全体贡献者的工作之上，仓库中保留了上游项目的提交历史。

<a href="https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juksentang/RVC-Retrieval-based-Voice-Conversion-Colab" alt="Contributors" />
</a>

上游贡献者：<https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors>

欢迎提交 Issue 和 Pull Request。

## 致谢

- [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- [ContentVec](https://github.com/auspicious3000/contentvec)、[VITS](https://github.com/jaywalnut310/vits)、[HiFi-GAN](https://github.com/jik876/hifi-gan)、[RMVPE](https://github.com/Dream-High/RMVPE)、[Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)、[audio-slicer](https://github.com/openvpi/audio-slicer)、[Gradio](https://github.com/gradio-app/gradio)

## 许可证

[MIT](./LICENSE)，与上游项目一致。使用条款及引用库的协议见 [MIT协议暨相关引用库协议](./MIT协议暨相关引用库协议)。
