"""
功能: 重命名文件级别后缀
用法: filelevel.exe -f FILES [FILES ...] -l level
特性:
 - 重命名格式为 '(PUB)'
"""

import argparse
import pathlib
import sys
import threading
import time
import typing


# 文件级别定义
class FileLevel(typing.NamedTuple):
    code: int
    names: typing.Tuple[str, ...]


FILE_LEVEL_DATA = (
    (0, ("",)),
    (1, ("公开", "PUB", "NOR")),
    (2, ("INT",)),
    (3, ("CON",)),
    (4, ("CLA",)),
)
FILE_LEVELS = [FileLevel(c, n) for c, n in FILE_LEVEL_DATA]
BRACKET_PAIRS = (" (（[【_-", " )）]】_-")


def remove_marks(filename: str, marks: typing.Tuple[str, ...]) -> str:
    for mark in marks:
        pos = filename.find(mark)
        if pos != -1:
            b, e = pos - 1, pos + len(mark)
            if b >= 0 and e <= len(filename) - 1:
                if (
                    filename[b] not in BRACKET_PAIRS[0]
                    or filename[e] not in BRACKET_PAIRS[1]
                ):
                    return filename[:e] + remove_marks(filename[e:], marks)
                filename = filename.replace(filename[b : e + 1], "")
                return remove_marks(filename, marks)
    return filename


def remove_level_and_digital_mark(filename: str) -> str:
    for file_level in FILE_LEVELS[1:]:
        filename = remove_marks(filename, file_level.names)
    filename = remove_marks(
        filename, tuple("".join([str(x) for x in range(1, 10)]))
    )
    return filename


def add_level_mark(
    filepath: pathlib.Path, filelevel: int, suffix: int
) -> pathlib.Path:
    cleared_stem = remove_level_and_digital_mark(filepath.stem)
    dst_stem = (
        f"{cleared_stem}({FILE_LEVELS[filelevel].names[0]})"
        if filelevel
        else cleared_stem
    )

    if dst_stem == filepath.stem:
        print(f"destination stem [{dst_stem}] equals to current.")
        return filepath
    dst_name = (
        f"{dst_stem}({suffix}){filepath.suffix}"
        if suffix
        else f"{dst_stem}{filepath.suffix}"
    )

    if filepath.with_name(dst_name).exists():
        return add_level_mark(filepath, filelevel, suffix + 1)
    print(f"rename [{filepath.name}] to [{dst_name}].")
    return filepath.with_name(dst_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", dest="level", type=int, default=0, help="target level, 0~4"
    )
    parser.add_argument(
        "-f",
        dest="files",
        type=str,
        nargs="+",
        required=True,
        help="source file or folder",
    )

    args = parser.parse_args()
    level = args.level
    targets = [pathlib.Path(f) for f in args.files if pathlib.Path(f).exists()]

    if not len(targets):
        print("no valid file or folder found.")
        sys.exit(-1)

    t0 = time.perf_counter()
    threads = []
    for target in targets:
        tt = "文件" if target.is_file() else "目录"
        print(f"start processing {tt:>6s} [{str(target)}]...")
        thread = threading.Thread(
            target=target.rename, args=(add_level_mark(target, level, 0),)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    print(
        f"[*] 目标数=[{len(targets)}]\n用时=[{time.perf_counter() - t0:.3f}]s."
    )


if __name__ == "__main__":
    main()
