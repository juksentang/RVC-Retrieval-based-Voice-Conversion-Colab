"""
Helpers for the command-line training cells in RVC_For_Colab.ipynb.

The WebUI builds the training filelist / config and the faiss index inside
infer-web.py, which cannot be imported without starting the whole app. This
script does the same two steps from the command line.

Usage (run from the repository root):
    python tools/colab_train.py filelist <exp_name> <sr: 32k|40k|48k> <v1|v2> [--no-f0] [--spk-id 0]
    python tools/colab_train.py index <exp_name> <v1|v2>
"""

import argparse
import json
import os
import platform
import shutil
from random import shuffle

import numpy as np

now_dir = os.getcwd()


def write_filelist(exp_name, sr, version, if_f0, spk_id):
    exp_dir = os.path.join(now_dir, "logs", exp_name)
    gt_wavs_dir = "%s/0_gt_wavs" % exp_dir
    feature_dir = "%s/3_feature%s" % (exp_dir, 256 if version == "v1" else 768)
    f0_dir = "%s/2a_f0" % exp_dir
    f0nsf_dir = "%s/2b-f0nsf" % exp_dir

    def stems(path):
        return set(name.split(".")[0] for name in os.listdir(path))

    names = stems(gt_wavs_dir) & stems(feature_dir)
    if if_f0:
        names &= stems(f0_dir) & stems(f0nsf_dir)
    if not names:
        raise SystemExit(
            "No usable samples found in %s. Run preprocessing and feature extraction first."
            % exp_dir
        )

    opt = []
    for name in names:
        if if_f0:
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s/%s.wav.npy|%s/%s.wav.npy|%s"
                % (gt_wavs_dir, name, feature_dir, name, f0_dir, name, f0nsf_dir, name, spk_id)
            )
        else:
            opt.append(
                "%s/%s.wav|%s/%s.npy|%s" % (gt_wavs_dir, name, feature_dir, name, spk_id)
            )
    fea_dim = 256 if version == "v1" else 768
    mute_dir = "%s/logs/mute" % now_dir
    for _ in range(2):
        if if_f0:
            opt.append(
                "%s/0_gt_wavs/mute%s.wav|%s/3_feature%s/mute.npy|%s/2a_f0/mute.wav.npy|%s/2b-f0nsf/mute.wav.npy|%s"
                % (mute_dir, sr, mute_dir, fea_dim, mute_dir, mute_dir, spk_id)
            )
        else:
            opt.append(
                "%s/0_gt_wavs/mute%s.wav|%s/3_feature%s/mute.npy|%s"
                % (mute_dir, sr, mute_dir, fea_dim, spk_id)
            )
    shuffle(opt)
    with open("%s/filelist.txt" % exp_dir, "w") as f:
        f.write("\n".join(opt))
    print("Wrote %s/filelist.txt (%d samples)" % (exp_dir, len(names)))

    # Same rule as infer-web.py: there is no v2 40k config, v1/40k.json is used.
    config_file = "v1/%s.json" % sr if version == "v1" or sr == "40k" else "v2/%s.json" % sr
    config_src = "configs/inuse/%s" % config_file
    if not os.path.exists(config_src):
        config_src = "configs/%s" % config_file
    config_dst = os.path.join(exp_dir, "config.json")
    if not os.path.exists(config_dst):
        with open(config_src, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(config_dst, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
            f.write("\n")
        print("Wrote %s (from %s)" % (config_dst, config_src))


def train_index(exp_name, version):
    import faiss
    from sklearn.cluster import MiniBatchKMeans

    exp_dir = "logs/%s" % exp_name
    feature_dir = "%s/3_feature%s" % (exp_dir, 256 if version == "v1" else 768)
    if not os.path.isdir(feature_dir) or not os.listdir(feature_dir):
        raise SystemExit("Run feature extraction first: %s is empty." % feature_dir)

    npys = [np.load("%s/%s" % (feature_dir, name)) for name in sorted(os.listdir(feature_dir))]
    big_npy = np.concatenate(npys, 0)
    big_npy_idx = np.arange(big_npy.shape[0])
    np.random.shuffle(big_npy_idx)
    big_npy = big_npy[big_npy_idx]
    if big_npy.shape[0] > 2e5:
        print("Trying doing kmeans %s shape to 10k centers." % big_npy.shape[0])
        big_npy = (
            MiniBatchKMeans(
                n_clusters=10000,
                verbose=True,
                batch_size=256 * os.cpu_count(),
                compute_labels=False,
                init="random",
            )
            .fit(big_npy)
            .cluster_centers_
        )

    np.save("%s/total_fea.npy" % exp_dir, big_npy)
    n_ivf = min(int(16 * np.sqrt(big_npy.shape[0])), big_npy.shape[0] // 39)
    print(big_npy.shape, n_ivf)
    index = faiss.index_factory(256 if version == "v1" else 768, "IVF%s,Flat" % n_ivf)
    index_ivf = faiss.extract_index_ivf(index)
    index_ivf.nprobe = 1
    print("training")
    index.train(big_npy)
    suffix = "IVF%s_Flat_nprobe_%s_%s_%s.index" % (n_ivf, index_ivf.nprobe, exp_name, version)
    faiss.write_index(index, "%s/trained_%s" % (exp_dir, suffix))
    print("adding")
    batch_size_add = 8192
    for i in range(0, big_npy.shape[0], batch_size_add):
        index.add(big_npy[i : i + batch_size_add])
    added = "%s/added_%s" % (exp_dir, suffix)
    faiss.write_index(index, added)
    print("Built index %s" % added)

    outside_index_root = os.getenv("outside_index_root", "assets/indices")
    os.makedirs(outside_index_root, exist_ok=True)
    target = "%s/%s_%s" % (outside_index_root, exp_name, suffix)
    try:
        if os.path.lexists(target):
            os.remove(target)
        link = os.link if platform.system() == "Windows" else os.symlink
        link(os.path.abspath(added), target)
    except OSError:
        shutil.copy(added, target)
    print("Linked index to %s" % target)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("filelist", help="write logs/<exp>/filelist.txt and config.json")
    p.add_argument("exp_name")
    p.add_argument("sr", choices=["32k", "40k", "48k"])
    p.add_argument("version", choices=["v1", "v2"])
    p.add_argument("--no-f0", action="store_true", help="model without pitch guidance")
    p.add_argument("--spk-id", type=int, default=0)

    p = sub.add_parser("index", help="train the faiss feature index")
    p.add_argument("exp_name")
    p.add_argument("version", choices=["v1", "v2"])

    args = parser.parse_args()
    if args.cmd == "filelist":
        write_filelist(args.exp_name, args.sr, args.version, not args.no_f0, args.spk_id)
    else:
        train_index(args.exp_name, args.version)


if __name__ == "__main__":
    main()
