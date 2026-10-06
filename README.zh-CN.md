<div align="center">

# RVC for Colab

[English](./README.md) | **简体中文**

在 Google Colab 或 Kaggle 上运行官方 [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)，训练自己的声音模型并进行变声，无需本地 GPU。

[![RVC](https://img.shields.io/badge/RVC-2.3%20(81eed5e)-black?logo=github)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/tree/81eed5e8f68b6bed1789f682fe78cdd324495afc)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

## 选择笔记本

| 笔记本 | 功能 | 运行平台 |
| --- | --- | --- |
| [`RVC_CLI.ipynb`](./RVC_CLI.ipynb) | 纯命令行：训练模型、转换音频，不启动 WebUI | [![在 Colab 中打开](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_CLI.ipynb) [![在 Kaggle 中打开](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_CLI.ipynb) |
| [`RVC_For_Colab.ipynb`](./RVC_For_Colab.ipynb) | 完整的 RVC WebUI，通过 Gradio 公网链接或 ngrok 访问 | [![在 Colab 中打开](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_For_Colab.ipynb) **需要计算单元或 Colab Pro** |

> [!WARNING]
> **WebUI 版需要付费的 Colab。** 在 Colab 免费版上运行时会显示“受限代码”警告，运行时可能中途被断开。运行 WebUI 需要计算单元（按量付费）或 Colab Pro。没有的话请使用 `RVC_CLI.ipynb`，可以在 Colab 上运行，也可以在 Kaggle 上运行（每周 30 小时免费 GPU）。
>
> 命令行版在 Colab 免费版上也可能被提示受限，遇到这种情况请改用 Kaggle。

## 项目简介

笔记本会克隆官方 [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) 的固定提交，配置好环境并运行。具体来说：

- 用 [uv](https://github.com/astral-sh/uv) 单独创建 **Python 3.12** 环境。RVC 2.3 需要 Python 3.12 和 `numpy<2`，而 Colab 和 Kaggle 现在的系统 Python 是 3.13，在 3.13 上装不了这些依赖。
- 安装上游要求的 Torch 版本（2.7.1，CUDA 12.8），并改用 PyPI 安装依赖，不走上游 requirements 中写死的国内镜像
- 按上游要求的目录结构下载 HuBERT、RMVPE、底模，以及可选的 PyMSS 模型
- 借助谷歌云盘（Colab）或 `/kaggle/working`（Kaggle）备份和恢复模型

默认使用上游 2026-08-04 的 main（[`81eed5e`](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/commit/81eed5e8f68b6bed1789f682fe78cdd324495afc)）。`2.3.260718` 这个 git tag 打在 2026-07-20，早于 release 说明中列出的部分更新（例如人声分离从 UVR5 换成 PyMSS）。固定在之后的提交可以拿到全部更新，另外还包含多说话人训练。

### 为什么不再 fork RVC 官方仓库

2026 年 10 月之前，本仓库是一个 fork，自带一份为 Colab 修改过的 RVC 2.2 代码。现在改为直接运行官方代码，原因如下：

- **fork 已经无法同步。** 上游在 2026 年 7 月从零重建了 `main`，新历史和旧历史没有任何共同提交。
- **原来的补丁不再需要。** 本仓库原来的改动是适配 Python 3.11，并修复 fairseq、matplotlib、Gradio 的兼容问题。RVC 2.3 已经自行解决了这些问题，并官方支持 Linux 和 Python 3.12。
- **用户拿到的就是官方代码。** 升级只需修改 `RVC_REF`。笔记本只负责配置环境，不会修改 RVC 的代码。

本仓库只维护笔记本，RVC 本身的 bug 请提交到 [上游](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/issues)。旧代码保存在 [`legacy-2.2`](https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/tree/legacy-2.2) tag 中。

## 环境要求

- 一个 Google 账号（用于 Colab），或者一个已验证手机号的 Kaggle 账号（使用 GPU 和联网需要验证）。
- 目标声音的数据集：尽量干净、背景噪音小的录音。建议 10–30 分钟的说话或演唱，越多越好，推荐 `.wav` 格式。

## 快速开始

1. 点击上方徽章打开笔记本。
   - **Colab：** 先 `文件 > 在云端硬盘中保存一份副本` 以保留修改，再选择 GPU 运行时：`代码执行程序 > 更改运行时类型 > T4 GPU`。
   - **Kaggle：** 在右侧设置中把加速器设为 `GPU T4 x2`，并打开 Internet。先把数据集上传为 Kaggle Dataset，再通过 `Add Input` 添加到笔记本。
2. 按顺序运行 **准备环境** 中的单元格：
   1. 克隆 RVC 官方仓库，`RVC_REF` 指定上游的 tag、分支或提交
   2. 在 Python 3.12 环境中安装依赖，需要几分钟
   3. 下载模型：v2 底模（40k / 48k）必定下载，v1 底模和 PyMSS 人声分离模型（约 2 GB）可选
   4. 准备数据集：zip 文件或文件夹，音频直接放在顶层。Colab 填谷歌云盘路径（会自动挂载云盘），Kaggle 填 `/kaggle/input/` 下的路径
   5. 恢复备份（可选）

### 命令行版

按顺序运行 **训练** 中的单元格，命令参考上游的 [CLI 文档](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/cn/cli.md)：

| 单元格 | 作用 |
| --- | --- |
| 音频预处理 | `train/preprocess.py`：切分并重采样数据集，输出到 `logs/<模型名>` |
| 提取音高与特征 | `train/dataset/extract_f0.py`（推荐 `rmvpe_gpu`）和 `extract_hubert_feature.py` |
| 训练模型 | 按 WebUI 的方式生成 `filelist.txt` / `config.json`，然后运行 `train/train.py` |
| 训练特征索引 | `train/train_index.py`：生成推理时使用的 faiss 索引 |
| 转换音频 | `infer/cli.py`：转换单个文件，或文件夹中的全部文件 |

所有单元格中的模型名、采样率和版本需保持一致。转换后的音频默认保存在 `rvc_output`（Colab 为 `/content/rvc_output`，Kaggle 为 `/kaggle/working/rvc_output`），也可以通过 `OUTPUT` 指定。

### WebUI 版

- **方案一** 使用 Gradio 公网链接（`*.gradio.live`）启动 WebUI，打开输出中的链接即可。
- **方案二** 通过 ngrok 暴露 WebUI，需先在 <https://dashboard.ngrok.com> 获取 Authtoken 并填入。

在 WebUI 的训练页中把训练集路径填为 `/content/dataset`，然后依次执行各步骤（或点击“一键训练”）。

### RVC 2.3 的变化

RVC 2.3 移除了一些旧选项：训练只支持 40k 和 48k，训练用的音高提取只支持 `rmvpe` 和 `pm`（harvest、dio、crepe 已移除）。推理时 WebUI 额外支持 `fcpe`，命令行的 `infer/cli.py` 支持 `rmvpe` 和 `pm`。

### 备份与恢复

- **备份** 会把 `G_*.pth` / `D_*.pth`、`config.json`、索引以及 `assets/weights` 中导出的模型复制到 `<BACKUP_DIR>/<模型名>`。默认位置：Colab 为 `MyDrive/RVC_backup`，Kaggle 为 `/kaggle/working/RVC_backup`。在 Kaggle 上需要保存一个笔记本版本才能保留 `/kaggle/working`，或者直接下载该文件夹。
- **恢复** 会把这些文件复制回来，用于继续训练或推理。在 Kaggle 上，请把备份添加为输入，并把 `BACKUP_DIR` 设为它在 `/kaggle/input/` 下的路径。
- 如果训练时开启了“仅保存最新”（默认开启），检查点的 epoch 为 `2333333`。
- 2025 年版笔记本的备份直接放在 MyDrive 根目录，且 G/D 文件名是互换的，恢复这类备份时请勾选 `LEGACY_BACKUP`。

## 升级到更新的 RVC 版本

把第一个单元格中的 `RVC_REF` 改为上游的 tag、分支（如 `main`）或完整的提交 SHA。笔记本只针对默认值适配过，如果新版本无法运行，欢迎提 Issue。

## 注意事项

- **GPU 时长限制：** 免费 GPU 的使用时长有限，长时间训练可能被中断，请定期备份。
- **临时存储：** 运行时停止后，备份目录以外的文件都会被删除。数据集和模型请保存在谷歌云盘或 Kaggle Dataset 中。
- **数据集质量** 对效果影响最大。请使用无混响、无伴奏、无噪音的干净录音，可以先用 WebUI 的人声分离页（PyMSS）去除伴奏和混响。
- **调参：** 可以尝试增加 epoch、推理时换一种音高算法，或调整 `index_rate`。

## 问题排查

- **Colab 提示“受限代码”：** 见顶部的警告。WebUI 版需要计算单元或 Colab Pro；免费版请使用命令行版，或改在 Kaggle 上运行。
- **“GPU 不可用”或已断开连接：** 确认已选择 GPU 运行时。也可能是达到了使用上限，请稍后再试。
- **依赖安装出错：** 重新运行安装单元格。如果 uv 无法下载 Python 3.12，请检查运行时能否联网（Kaggle 需要打开 Internet）。
- **提示底模不存在（pretrained model not exist）：** 请运行下载单元格，模型必须位于 `assets/` 目录下。
- **找不到文件：** 检查填写的路径，尤其是数据集和备份目录。

## 合理使用

未经本人明确同意，请勿使用变声技术冒充他人或制作误导性内容。使用者需对自己生成和传播的音频负责。

## 贡献者

笔记本维护者：[@juksentang](https://github.com/juksentang)

本仓库保留了作为 fork 时的提交历史，所以下方列表中也包括本仓库以前所含代码的 RVC 作者。

<a href="https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juksentang/RVC-Retrieval-based-Voice-Conversion-Colab" alt="Contributors" />
</a>

RVC 本身由 [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) 及其 [贡献者](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors) 开发。笔记本相关的 Issue 和 PR 欢迎提交到本仓库，RVC 本身的 bug 请提交到 [上游](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/issues)。

## 许可证

笔记本以 [MIT 协议](./LICENSE) 开源。RVC 及其下载的模型遵循上游的 [协议与使用条款](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE)。
