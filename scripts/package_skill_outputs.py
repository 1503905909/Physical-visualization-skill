"""Package generated Manim videos and Streamlit simulation outputs into dedicated project folders."""

from pathlib import Path
import shutil
import argparse

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MEDIA_DIR = ROOT_DIR / "media" / "videos"
DEFAULT_MANIM_OUTPUT_DIR = ROOT_DIR / "output" / "videos" / "manim"
DEFAULT_SIM_OUTPUT_DIR = ROOT_DIR / "output" / "results" / "physics_interactive_sim_lab"
DEFAULT_SIM_WEB_DIR = ROOT_DIR / "output" / "www" / "physics_interactive_sim_lab"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_final_videos(media_dir: Path, scene_name: str = None):
    video_files = [p for p in media_dir.rglob("*.mp4") if "partial_movie_files" not in p.parts]
    if scene_name:
        video_files = [p for p in video_files if scene_name in p.name]
    return sorted(video_files, key=lambda p: p.stat().st_mtime, reverse=True)


def package_manim(scene_name: str = None, copy_all: bool = False):
    ensure_dir(DEFAULT_MANIM_OUTPUT_DIR)
    videos = find_final_videos(DEFAULT_MEDIA_DIR, scene_name)
    if not videos:
        raise FileNotFoundError("未找到任何 final MP4 视频文件，请先运行 Manim 渲染。")

    selected = videos if copy_all else videos[:1]
    copied = []
    for video in selected:
        dest = DEFAULT_MANIM_OUTPUT_DIR / video.name
        shutil.copy2(video, dest)
        copied.append(dest)
    return copied


def package_sim():
    ensure_dir(DEFAULT_SIM_OUTPUT_DIR)
    # Also copy any HTML examples to a web-ready directory for lightweight deployment
    ensure_dir(DEFAULT_SIM_WEB_DIR)
    examples_dir = ROOT_DIR / ".trae" / "skills" / "physics-interactive-sim-lab" / "examples"
    copied = []
    if examples_dir.exists():
        for html in examples_dir.glob("*.html"):
            dest = DEFAULT_SIM_WEB_DIR / html.name
            shutil.copy2(html, dest)
            copied.append(dest)
    return DEFAULT_SIM_OUTPUT_DIR, DEFAULT_SIM_WEB_DIR, copied


def main():
    parser = argparse.ArgumentParser(
        description="将 Manim 渲染视频和交互仿真输出归档到指定目录。"
    )
    parser.add_argument(
        "--scene-name",
        type=str,
        default=None,
        help="可选的 Manim 场景名称过滤，仅复制匹配文件。"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="复制 media/videos 下所有 final MP4 文件，而非仅最新一个。"
    )
    parser.add_argument(
        "--package-sim",
        action="store_true",
        help="创建物理仿真实验的输出目录（默认已存在）。"
    )
    args = parser.parse_args()

    copied = []
    if args.all or args.scene_name is not None:
        copied = package_manim(scene_name=args.scene_name, copy_all=args.all)
    else:
        copied = package_manim(copy_all=False)

    print("已归档 Manim 视频到:")
    for path in copied:
        print(f"  - {path}")

    if args.package_sim:
        sim_path, web_path, copied_html = package_sim()
        print(f"已确保仿真输出目录存在: {sim_path}")
        print(f"已确保轻量 Web 输出目录存在: {web_path}")
        if copied_html:
            print("已复制 HTML 示例到:")
            for p in copied_html:
                print(f"  - {p}")
        else:
            print("未找到 HTML 示例文件可复制。")


if __name__ == "__main__":
    main()
