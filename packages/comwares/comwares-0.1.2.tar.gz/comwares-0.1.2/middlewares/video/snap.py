import numpy as np
import cv2
import random
import os
import sys
import time
import ffmpeg


def read_frame_by_time(in_file, time):
    """
    指定时间节点读取任意帧
    """
    out, err = (
        ffmpeg.input(in_file, ss=time)
            .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
            .run(capture_stdout=True)
    )
    return out


def get_video_info(in_file):
    """
    获取视频基本信息
    """
    try:

        # cap = cv2.VideoCapture(in_file)
        # while (cap.isOpened()):
        #     ret, frame = cap.read()
        #     cv2.imshow('image', frame)
        #     k = cv2.waitKey(20)
        #     # q键退出
        #     if (k & 0xff == ord('q')):
        #         break
        #
        # cap.release()
        # cv2.destroyAllWindows()
        probe = ffmpeg.probe(in_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)
        return video_stream
    except ffmpeg.Error as err:
        print(str(err.stderr, encoding='gbk'))
        sys.exit(1)


if __name__ == '__main__':
    # video_to_image()
    filename = "../../tmp/下载.mp4"

    # 读取视频的时长
    video_info = get_video_info(filename)
    total_duration = video_info['duration']
    # 随机选择一个时间
    # random_time = random.uniform(0, float(total_duration))
    random_time = 0.0001

    # 提取图片
    out = read_frame_by_time(filename, random_time)
    image_array = np.asarray(bytearray(out), dtype="uint8")
    img_frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # 显示图片
    cv2.imwrite('../../tmp/result.jpg', img_frame)

