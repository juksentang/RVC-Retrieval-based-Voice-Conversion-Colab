<div align="center">

# RVC for Colab

**English** | [简体中文](./README.zh-CN.md)

Train your own voice model and convert voices with the official [RVC WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) on Google Colab, no local GPU needed.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_For_Colab.ipynb)
[![RVC](https://img.shields.io/badge/RVC-2.3.260718-black?logo=github)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/releases/tag/2.3.260718)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

## Overview

This repository holds a single Colab notebook, [`RVC_For_Colab.ipynb`](./RVC_For_Colab.ipynb). It clones the official [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) at a pinned release (currently **2.3.260718**), sets up the environment on Colab, and runs it.

The notebook:

- installs the Torch version upstream requires (2.7.1, CUDA 12.8) in place of the one Colab ships, and installs the dependencies from PyPI instead of the mirror pinned in upstream's requirements file
- downloads the HuBERT, RMVPE, pretrained and UVR5 models into the layout upstream expects
- starts the WebUI through a Gradio share link or an ngrok tunnel
- offers command-line training cells for when Colab refuses to run the WebUI
- backs up and restores models with Google Drive

> Before 2026-10, this repository was a fork that carried a copy of the RVC 2.2 code. That version is kept as the [`legacy-2.2`](https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/tree/legacy-2.2) tag.

## Requirements

- A Google account (for Colab and Google Drive).
- A dataset of the target voice: clean recordings with as little background noise as possible. 10–30 minutes of speech or singing is a good start; more helps. `.wav` is recommended.

## Quick start

1. Click the **Open in Colab** badge above, then `File > Save a copy in Drive` so your changes are kept.
2. Select a GPU runtime: `Runtime > Change runtime type > T4 GPU`.
3. Run the cells under **Setup** in order:
   1. Clone the official RVC repository. `RVC_REF` picks the upstream tag or branch.
   2. Install dependencies. This takes a few minutes.
   3. Download models. v2 pretrained models are always downloaded; v1 and UVR5 are optional.
   4. Mount Google Drive.
   5. Unzip your dataset to `/content/dataset`. Put the audio files at the top level of the zip.
4. Pick one of the two options below.

### Option 1: WebUI

- **Plan A** starts the WebUI with a Gradio share link (`*.gradio.live`). Open the link printed in the output.
- **Plan B** exposes the WebUI through ngrok. Fill in your authtoken from <https://dashboard.ngrok.com> first.

In the WebUI's training tab, set the training folder to `/content/dataset`, then run the steps in order (or click "One-click training"). Trained models are written to `assets/weights`, indexes to `logs/<model name>`.

### Option 2: command-line training

Colab's free tier may block the WebUI. In that case, use the cells under **Option 2**. They follow upstream's [CLI guide](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/en/cli.md):

| Cell | What it does |
| --- | --- |
| Preprocess audio | `train/preprocess.py`: slices and resamples the dataset into `logs/<model>` |
| Extract pitch and features | `train/dataset/extract_f0.py` (`rmvpe_gpu` recommended) and `extract_hubert_feature.py` |
| Train the model | Writes `filelist.txt` / `config.json` the same way the WebUI does, then runs `train/train.py` |
| Train the feature index | `train/train_index.py`: builds the faiss index used at inference time |

Keep the model name, sample rate and version the same in every cell.

### Backup and restore

- **Back up** copies `G_*.pth` / `D_*.pth`, `config.json`, the index and the exported model in `assets/weights` to `MyDrive/RVC_backup/<model>`.
- **Restore** copies them back so you can resume training or run inference.
- If you trained with "only save latest" (the default), the checkpoint epoch is `2333333`.
- Backups made by the 2025 notebook stored files in the root of MyDrive with the G/D names swapped. Tick `LEGACY_BACKUP` to restore those.

## Updating to a newer RVC release

Set `RVC_REF` in the first cell to a newer [upstream tag](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/tags), or to `main`. The notebook is tested with the default value only. If a newer release breaks it, please open an issue.

## Tips

- **Colab limits:** free GPU time is limited and sessions may disconnect during long training runs. Back up to Drive regularly.
- **Temporary storage:** everything under `/content` is deleted when the runtime disconnects. Keep datasets and models in Drive.
- **Dataset quality** matters most. Use clean recordings without reverb, accompaniment or noise. The UVR5 tab can separate vocals first.
- **Tuning:** try more epochs, or adjust `index_rate` at inference time.

## Troubleshooting

- **"GPU not available" / disconnected:** check that a GPU runtime is selected. You may have hit Colab's usage limit, so try again later or upgrade.
- **Python version warning:** RVC 2.3 targets Python 3.12. If Colab moves to a different version, dependency installation may fail; please open an issue.
- **Dependency install errors:** restart the runtime (`Runtime > Restart session`) and run the install cell again.
- **"Pretrained model not exist":** run the download cell. The models must live under `assets/`.
- **File not found:** check the paths you filled in, especially the dataset zip and the backup folder on Drive.

## Ethical use

Do not use voice conversion to impersonate anyone, or to make misleading content, without their explicit consent. You are responsible for the audio you create and share.

## Contributors

Notebook maintainer: [@juksentang](https://github.com/juksentang)

<a href="https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juksentang/RVC-Retrieval-based-Voice-Conversion-Colab" alt="Contributors" />
</a>

RVC itself is developed by [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) and its [contributors](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors). Issues and pull requests for the notebook are welcome here; bugs in RVC itself belong [upstream](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/issues).

## License

The notebook is released under the [MIT License](./LICENSE). RVC and the models it downloads are covered by upstream's [license and terms](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE).
