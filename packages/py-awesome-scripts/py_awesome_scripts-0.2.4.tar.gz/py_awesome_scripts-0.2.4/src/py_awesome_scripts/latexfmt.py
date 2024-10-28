"""
功能: 格式化处理 latex 文件
命令: latexfmt.exe [FILES ...]
特性:
 - 移除拷贝之后的多余【-#*】字符
"""
import argparse
import concurrent.futures
import logging
import os
import pathlib
import re
import time

MATCH_EXPRESSIONS = (r"### ", r"[\*]+", r"-[ ]")
MATCH_REGS = list(re.compile(_) for _ in MATCH_EXPRESSIONS)

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(message)s')


def clear_copy_symbols(content: str) -> str:
    for reg in MATCH_REGS:
        content = re.sub(reg, "", content)
    return content


def format_tex_file(filepath: pathlib.Path) -> bool:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            clean_content = clear_copy_symbols(content)

            with open(filepath, "w", encoding="utf-8") as fw:
                fw.write(clean_content)
    except IOError as e:
        logging.error(e)
        return False
    else:
        return True


def format_tex_in_dir(dir_path: pathlib.Path) -> bool:
    tex_files = list(dir_path.glob("*.tex"))

    logging.info(f"开始处理目录{dir_path.name}下tex文件: {list(_.name for _ in tex_files)}")
    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ret = list(
            executor.submit(format_tex_file, pathlib.Path(f))
            for f in tex_files
        )
        for _ in concurrent.futures.as_completed(ret):
            pass
    logging.info(f"处理结束, 总共用时: {time.perf_counter() - t0:.3f}s")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        dest="directory",
        type=str,
        default=str(pathlib.Path.cwd()),
        help="tex文件目录",
    )

    args = parser.parse_args()
    directory = args.directory

    if not pathlib.Path(directory).exists():
        logging.info(f"输入参数不正确，路径[{directory}]不存在")
        parser.print_help()
        return

    format_tex_in_dir(pathlib.Path(directory))


if __name__ == "__main__":
    main()
