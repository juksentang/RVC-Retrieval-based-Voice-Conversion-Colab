<div align="center">

# RVC for Colab

**English** | [简体中文](./README.zh-CN.md)

Train your own voice model and convert voices with the official [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) on Google Colab or Kaggle, no local GPU needed.

[![RVC](https://img.shields.io/badge/RVC-2.3%20(81eed5e)-black?logo=github)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/tree/81eed5e8f68b6bed1789f682fe78cdd324495afc)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

</div>

## Choose a notebook

| Notebook | What it does | Where it runs |
| --- | --- | --- |
| [`RVC_CLI.ipynb`](./RVC_CLI.ipynb) | Command line only: train a model and convert audio, no WebUI | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_CLI.ipynb) [![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_CLI.ipynb) |
| [`RVC_For_Colab.ipynb`](./RVC_For_Colab.ipynb) | The full RVC WebUI, via a Gradio share link or ngrok | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/blob/main/RVC_For_Colab.ipynb) **needs compute units or Colab Pro** |

> [!WARNING]
> **The WebUI notebook needs a paid Colab plan.** On the free tier, Colab shows a "restricted code" warning for it and may disconnect the runtime partway through. Running a WebUI needs compute units (pay as you go) or Colab Pro. Without them, use `RVC_CLI.ipynb`, on Colab or on Kaggle (30 free GPU hours a week).
>
> The free tier may also flag the command-line notebook. If it does, run it on Kaggle.

## Overview

The notebooks clone the official [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) at a pinned commit, set up the environment, and run it. They:

- create a separate **Python 3.12** environment with [uv](https://github.com/astral-sh/uv). RVC 2.3 requires Python 3.12 and `numpy<2`, but Colab and Kaggle now run Python 3.13, where these dependencies cannot be installed.
- install the Torch version upstream requires (2.7.1, CUDA 12.8), and install the dependencies from PyPI instead of the mirror pinned in upstream's requirements file
- download the HuBERT, RMVPE, pretrained and (optionally) PyMSS models into the layout upstream expects
- back up and restore models with Google Drive (Colab) or `/kaggle/working` (Kaggle)

The default RVC version is upstream main as of 2026-08-04 ([`81eed5e`](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/commit/81eed5e8f68b6bed1789f682fe78cdd324495afc)). The `2.3.260718` git tag was created on 2026-07-20, before several changes the release notes list, such as switching vocal separation from UVR5 to PyMSS. Pinning the later commit gets all of them, plus multi-speaker training.

### Why this is no longer a fork of RVC

Until 2026-10, this repository was a fork that carried its own copy of the RVC 2.2 code, patched to run on Colab. It now runs the official code directly, because:

- **The fork can no longer sync.** In 2026-07 upstream rebuilt `main` from scratch, so the new history shares no commits with the old one.
- **The patches are no longer needed.** This fork adapted RVC to Python 3.11 and fixed compatibility issues with fairseq, matplotlib and Gradio. RVC 2.3 fixes these itself and officially supports Linux and Python 3.12.
- **Users get the official code.** Upgrading only means changing `RVC_REF`. The notebooks set up the environment but never modify RVC's code.

This repository only maintains the notebooks. Please report bugs in RVC itself [upstream](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/issues). The old code is kept as the [`legacy-2.2`](https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/tree/legacy-2.2) tag.

## Requirements

- A Google account for Colab, or a Kaggle account with a verified phone number (needed for GPU and Internet access).
- A dataset of the target voice: clean recordings with as little background noise as possible. 10–30 minutes of speech or singing is a good start; more helps. `.wav` is recommended.

## Quick start

1. Open a notebook with one of the badges above.
   - **Colab:** `File > Save a copy in Drive` so your changes are kept, then select a GPU runtime: `Runtime > Change runtime type > T4 GPU`.
   - **Kaggle:** in the side panel, set the accelerator to `GPU T4 x2` and turn Internet on. Upload your dataset as a Kaggle Dataset and add it to the notebook with `Add Input`.
2. Run the cells under **Setup** in order:
   1. Clone the official RVC repository. `RVC_REF` picks the upstream tag, branch or commit.
   2. Install dependencies into the Python 3.12 environment. This takes a few minutes.
   3. Download models. v2 pretrained models (40k / 48k) are always downloaded; v1 and the PyMSS vocal separation models (about 2 GB) are optional.
   4. Prepare the dataset: a zip file or folder with the audio at the top level. On Colab use a Google Drive path (Drive is mounted automatically); on Kaggle use a path under `/kaggle/input/`.
   5. Restore a backup (optional).

### Command-line notebook

Run the **Training** cells in order. They follow upstream's [CLI guide](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/en/cli.md):

| Cell | What it does |
| --- | --- |
| Preprocess audio | `train/preprocess.py`: slices and resamples the dataset into `logs/<model>` |
| Extract pitch and features | `train/dataset/extract_f0.py` (`rmvpe_gpu` recommended) and `extract_hubert_feature.py` |
| Train the model | Writes `filelist.txt` / `config.json` the same way the WebUI does, then runs `train/train.py` |
| Train the feature index | `train/train_index.py`: builds the faiss index used at inference time |
| Convert audio | `infer/cli.py`: converts one file, or every file in a folder |

Keep the model name, sample rate and version the same in every cell. Converted audio is saved to `rvc_output` (`/content/rvc_output` on Colab, `/kaggle/working/rvc_output` on Kaggle) unless you set `OUTPUT`.

### WebUI notebook

- **Plan A** starts the WebUI with a Gradio share link (`*.gradio.live`). Open the link printed in the output.
- **Plan B** exposes the WebUI through ngrok. Fill in your authtoken from <https://dashboard.ngrok.com> first.

In the WebUI's training tab, set the training folder to `/content/dataset`, then run the steps in order (or click "One-click training").

### What changed in RVC 2.3

RVC 2.3 removed several older options. Training supports 40k and 48k only, and pitch extraction for training supports `rmvpe` and `pm` only (harvest, dio and crepe are gone). For inference, the WebUI also offers `fcpe`; the command-line `infer/cli.py` supports `rmvpe` and `pm`.

### Backup and restore

- **Back up** copies `G_*.pth` / `D_*.pth`, `config.json`, the index and the exported model in `assets/weights` to `<BACKUP_DIR>/<model>`. By default that is `MyDrive/RVC_backup` on Colab and `/kaggle/working/RVC_backup` on Kaggle. On Kaggle, save a notebook version to keep `/kaggle/working`, or download the folder.
- **Restore** copies them back so you can resume training or run inference. On Kaggle, add your backup as an input and set `BACKUP_DIR` to its path under `/kaggle/input/`.
- If you trained with "only save latest" (the default), the checkpoint epoch is `2333333`.
- Backups made by the 2025 notebook stored files in the root of MyDrive with the G/D names swapped. Tick `LEGACY_BACKUP` to restore those.

## Updating to a newer RVC release

Set `RVC_REF` in the first cell to an upstream tag, a branch such as `main`, or a full commit SHA. The notebooks are written for the default value only. If a newer release breaks them, please open an issue.

## Tips

- **GPU time limits:** free GPU time is limited and sessions may disconnect during long training runs. Back up regularly.
- **Temporary storage:** files outside your backup folder are deleted when the runtime stops. Keep datasets and models in Drive or a Kaggle Dataset.
- **Dataset quality** matters most. Use clean recordings without reverb, accompaniment or noise. The WebUI's vocal separation tab (PyMSS) can remove accompaniment and reverb first.
- **Tuning:** try more epochs, a different pitch method at inference time, or adjust `index_rate`.

## Troubleshooting

- **"Restricted code" warning on Colab:** see the warning at the top. The WebUI notebook needs compute units or Colab Pro; on the free tier, use the command-line notebook, or run it on Kaggle.
- **"GPU not available" / disconnected:** check that a GPU runtime is selected. You may have hit the usage limit, so try again later.
- **Dependency install errors:** run the install cell again. If uv cannot download Python 3.12, check that the runtime has Internet access (on Kaggle, turn Internet on).
- **"Pretrained model not exist":** run the download cell. The models must live under `assets/`.
- **File not found:** check the paths you filled in, especially the dataset and the backup folder.

## Ethical use

Do not use voice conversion to impersonate anyone, or to make misleading content, without their explicit consent. You are responsible for the audio you create and share.

## Contributors

Notebook maintainer: [@juksentang](https://github.com/juksentang)

This repository keeps the commit history from when it was a fork, so the list below also includes the RVC authors whose code it used to carry.

<a href="https://github.com/juksentang/RVC-Retrieval-based-Voice-Conversion-Colab/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juksentang/RVC-Retrieval-based-Voice-Conversion-Colab" alt="Contributors" />
</a>

RVC itself is developed by [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) and its [contributors](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors). Issues and pull requests for the notebooks are welcome here; bugs in RVC itself belong [upstream](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/issues).

## License

The notebooks are released under the [MIT License](./LICENSE). RVC and the models it downloads are covered by upstream's [license and terms](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/LICENSE).
