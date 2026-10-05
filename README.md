<div align="center">

# RVC for Colab

**English** | [简体中文](./README.zh-CN.md)

Train your own voice model and convert voices with RVC (Retrieval-based Voice Conversion) on Google Colab, no local GPU needed.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_For_Colab.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Upstream](https://img.shields.io/badge/upstream-RVC--Project-black?logo=github)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

</div>

## Overview

This repository is a fork of [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) with a ready-to-run Colab notebook. It is adapted to the **Python 3.11** runtime that Colab ships today and fixes several bugs in the original Colab workflow.

Features:

- Runs entirely in Google Colab, nothing to set up locally.
- Training and inference through the RVC WebUI, via a Gradio share link or an ngrok tunnel.
- A command-line training path for when Colab refuses to run the WebUI on the free tier.
- Back up and restore models with Google Drive.
- UVR5 vocal / accompaniment separation models included.

## Requirements

- A Google account (for Colab and Google Drive).
- A dataset of the target voice: clean recordings with as little background noise as possible. 10–30 minutes of speech or singing is a good start; more helps. `.wav` is recommended.

## Quick start

1. Click the **Open in Colab** badge above, then `File > Save a copy in Drive` so your changes are kept.
2. Select a GPU runtime: `Runtime > Change runtime type > T4 GPU`.
3. Run the cells under **Setup** in order:
   1. Clone the repository
   2. Install dependencies
   3. Download pretrained models (into `assets/pretrained_v2`, `assets/uvr5_weights`, `assets/hubert`, `assets/rmvpe`)
   4. Mount Google Drive
   5. Unzip your dataset to `/content/dataset`. Put the audio files at the top level of the zip.
4. Pick one of the two options below.

### Option 1: WebUI

- **Plan A** starts the WebUI with a Gradio share link (`*.gradio.live`). Open the link printed in the output.
- **Plan B** exposes the WebUI through ngrok. Fill in your authtoken from <https://dashboard.ngrok.com> first.

In the WebUI's training tab, set the training folder to `/content/dataset`, then run the steps in order (or click "One-click training"). Trained models are written to `assets/weights`, indexes to `logs/<model name>`.

### Option 2: command-line training

Colab's free tier may block the WebUI. In that case, use the cells under **Option 2**:

| Cell | What it does |
| --- | --- |
| Preprocess audio | Slices and resamples the dataset into `logs/<model>` |
| Extract pitch and features | Pitch (`rmvpe_gpu` recommended) and HuBERT features |
| Train the model | Writes the filelist / config, then trains from the v2 pretrained models |
| Train the feature index | Builds the faiss index used at inference time |

Keep the model name, sample rate and version the same in every cell.

### Backup and restore

- **Back up** copies `G_*.pth` / `D_*.pth`, `config.json`, the index and the exported model in `assets/weights` to `MyDrive/RVC_backup/<model>`.
- **Restore** copies them back so you can resume training or run inference. Backups made by the old version of the notebook stored files in the root of MyDrive with the G/D names swapped. Tick `LEGACY_BACKUP` to restore those.
- If you trained with "only save latest", the checkpoint epoch is `2333333`.

## Tips

- **Colab limits:** free GPU time is limited and sessions may disconnect during long training runs. Back up to Drive regularly.
- **Temporary storage:** everything under `/content` is deleted when the runtime disconnects. Keep datasets and models in Drive.
- **Dataset quality** matters most. Use clean recordings without reverb, accompaniment or noise. The UVR5 tab can separate vocals first.
- **Tuning:** try more epochs, a different pitch extraction method (`rmvpe` usually works best), or adjust `index_rate` at inference time.

## Troubleshooting

- **"GPU not available" / disconnected:** check that a GPU runtime is selected. You may have hit Colab's usage limit, so try again later or upgrade.
- **Dependency install errors:** this notebook targets Python 3.11. Restart the runtime (`Runtime > Restart session`) and run the install cell again.
- **"Pretrained model not exist":** run the download cell. The models must live under `assets/`.
- **File not found:** check the paths you filled in, especially the dataset zip and the backup folder on Drive.

## Ethical use

Do not use voice conversion to impersonate anyone, or to make misleading content, without their explicit consent. You are responsible for the audio you create and share.

## Contributors

Maintainer: [@juksentang](https://github.com/juksentang)

This project builds on the work of everyone who contributed to [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI). The commit history of the upstream project is kept in this repository.

<a href="https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juksentang/RVC-Retrieval-based-Voice-Conversion-Colab" alt="Contributors" />
</a>

Upstream contributors: <https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors>

Issues and pull requests are welcome.

## Acknowledgements

- [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- [ContentVec](https://github.com/auspicious3000/contentvec), [VITS](https://github.com/jaywalnut310/vits), [HiFi-GAN](https://github.com/jik876/hifi-gan), [RMVPE](https://github.com/Dream-High/RMVPE), [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui), [audio-slicer](https://github.com/openvpi/audio-slicer), [Gradio](https://github.com/gradio-app/gradio)

## License

[MIT](./LICENSE), same as the upstream project. See [MIT协议暨相关引用库协议](./MIT协议暨相关引用库协议) for the terms of use and the licenses of the bundled libraries.
