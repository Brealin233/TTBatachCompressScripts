#type shebang here...

import argparse
from genericpath import isfile
import os
import subprocess

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='TT批量压缩图像、视频')

parser.add_argument('input_dir', help='输入目录')
parser.add_argument('output_dir', help='输出目录')
parser.add_argument('-q', '--quality', type=int, default=2, help='压缩质量参数，默认为2，数字越大压缩程度越大,图像建议1-10，视频建议0-51')
parser.add_argument('-ic', '--icodec', type=str, default="mjpeg", help='图像编码器参数，默认为mjpeg,可选为webp')
parser.add_argument('-mc', '--mcodec', type=str, default="libx264", help='视频编码器参数，默认为h.264,可选为h.265或libvpx-vp9(mp4)')

# 解析命令行参数
args = parser.parse_args()

# 获取输入目录和输出目录
input_dir = args.input_dir
output_dir = args.output_dir

# 检查输出目录是否存在，如果不存在则创建它
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if os.path.isfile(input_dir):
    basename, extension = os.path.splitext(input_dir)
    if output_dir == None:
        output_file = os.path.join(os.getcwd(), f"{basename}_compressed{extension}")
    else:
        output_file = os.path.join(output_dir, f"{basename}_compressed{extension}")

    # 图像
    if args.icodec == "webp":
            subprocess.run(["ffmpeg", "-i", input_dir, "-c:v", "libwebp", "-q:v", str(args.quality), output_file])
    else:
            subprocess.run(["ffmpeg", "-i", input_dir, "-c:v", "mjpeg", "-q:v", str(args.quality), output_file])
    print("压缩完成:", output_file)

    # 视频
    if input_dir.lower().endswith((".mp4", ".avi", ".mov")):
        if args.mcodec == "libx265":
            subprocess.run(["ffmpeg", "-i", input_dir, "-c:v", "libx265", "-q:v", str(args.quality), output_file])
        elif args.mcodec == "libvpx-vp9":
            subprocess.run(["ffmpeg", "-i", input_dir, "-c:v", "libvpx-vp9", "-q:v", str(args.quality), output_file])
        else:
            subprocess.run(["ffmpeg", "-i", input_dir, "-c:v","libx264","-crf", str(args.quality), output_file])

        print("压缩完成:", output_file)

else:
    # 遍历输入目录中的所有图像文件
    for filename in os.listdir(input_dir):
        # if filename.endswith(".jpg"):
        input_file = os.path.join(input_dir, filename)

        # 提取文件名和扩展名
        basename, extension = os.path.splitext(filename)

        # 构建输出文件路径
        output_file = os.path.join(output_dir, f"{basename}_compressed{extension}")

        if args.icodec == "webp":
            subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libwebp", "-q:v", str(args.quality), output_file])
        else:
            subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "mjpeg", "-q:v", str(args.quality), output_file])

        print("压缩完成:", output_file)

        if filename.lower().endswith((".mp4", ".avi", ".mov")):
            input_file = os.path.join(input_dir, filename)

            basename, extension = os.path.splitext(filename)

            output_file = os.path.join(output_dir, f"{basename}_compressed{extension}")

            if args.mcodec == "libx265":
                subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libx265", "-q:v", str(args.quality), output_file])
            elif args.mcodec == "libvpx-vp9":
                subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libvpx-vp9", "-q:v", str(args.quality), output_file])
            else:
                subprocess.run(["ffmpeg", "-i", input_file, "-c:v","libx264","-crf", str(args.quality), output_file])

            print("压缩完成:", output_file)
