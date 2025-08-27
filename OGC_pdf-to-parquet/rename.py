import os
import re


def rename_parquet_files(output_dir: str, prefix: str = "train"):
    files = [f for f in os.listdir(output_dir) if f.endswith('.parquet')]
    files.sort()
    for i, f in enumerate(files, start=0):
        new_name = f"{prefix}_{i:05d}.parquet"
        if f != new_name:
            os.rename(os.path.join(output_dir, f), os.path.join(output_dir, new_name))
            print(f"Renommé: {f} -> {new_name}")


if __name__ == "__main__":
    out = os.environ.get("OUTPUT_FOLDER", "out_test")
    pref = os.environ.get("FILE_NAMES", "train")
    if not os.path.isdir(out):
        print(f"Dossier inexistant: {out}")
    else:
        rename_parquet_files(out, pref)
