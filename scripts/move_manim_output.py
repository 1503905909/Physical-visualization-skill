"""Move Manim MP4 output to a centralized project output directory."""

from pathlib import Path
import shutil
import argparse


def find_latest_video(media_dir: Path, scene_name: str = None):
    if not media_dir.exists():
        raise FileNotFoundError(f"指定的 media 目录不存在: {media_dir}")

    video_files = list(media_dir.rglob("*.mp4"))
    if scene_name:
        video_files = [p for p in video_files if scene_name in p.name]

    if not video_files:
        raise FileNotFoundError("未找到任何 MP4 视频文件，请先运行 Manim 渲染。")

    # 按修改时间排序，取最新生成的
    video_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return video_files[0]


def move_video(src: Path, dst_dir: Path):
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    return dst


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MEDIA_DIR = ROOT_DIR / "media" / "videos"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "output" / "videos" / "manim"


def main():
    parser = argparse.ArgumentParser(description="将 Manim 生成的 MP4 移动到 output/videos/manim/ 目录。")
    parser.add_argument(
        "--media-dir",
        type=Path,
        default=DEFAULT_MEDIA_DIR,
        help="Manim 生成视频的根目录，通常是 media/videos"
    )
    parser.add_argument(
        "--scene-name",
        type=str,
        default=None,
        help="可选的场景名称过滤，用于查找对应 MP4 文件"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="目标输出目录"
    )

    args = parser.parse_args()
    latest_video = find_latest_video(args.media_dir, args.scene_name)
    target_path = move_video(latest_video, args.output_dir)
    print(f"已复制视频到: {target_path}")


if __name__ == "__main__":
    main()
