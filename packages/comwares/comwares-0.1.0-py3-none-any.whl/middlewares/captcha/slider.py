from PIL import Image
import io
import cv2
import numpy as np
import base64
import matplotlib.pyplot as plt


# Take in base64 string and return cv image
def string_to_rgb(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return image


#  传入滑块背景图片本地路径和滑块本地路径，返回滑块到缺口的距离
def find_pic(img_bg_path, img_slider_path):
    """
    找出图像中最佳匹配位置
    :param img_bg_path: 滑块背景图本地路径
    :param img_slider_path: 滑块图片本地路径
    :return: 返回最差匹配、最佳匹配对应的x坐标
    """

    # 读取滑块背景图片，参数是图片路径，OpenCV默认使用BGR模式
    # cv.imread()是 image read的简写
    # img_bg 是一个numpy库ndarray数组对象
    img_bg = cv2.imread(img_bg_path)

    # 对滑块背景图片进行处理，由BGR模式转为gray模式（即灰度模式，也就是黑白图片）
    # 为什么要处理？ BGR模式（彩色图片）的数据比黑白图片的数据大，处理后可以加快算法的计算
    # BGR模式：常见的是RGB模式
    # R代表红，red; G代表绿，green;  B代表蓝，blue。
    # RGB模式就是，色彩数据模式，R在高位，G在中间，B在低位。BGR正好相反。
    # 如红色：RGB模式是(255,0,0)，BGR模式是(0,0,255)
    img_bg_gray = cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)

    # 读取滑块，参数1是图片路径，参数2是使用灰度模式
    img_slider_gray = cv2.imread(img_slider_path, 0)

    # 在滑块背景图中匹配滑块。参数cv.TM_CCOEFF_NORMED是opencv中的一种算法
    res = cv2.matchTemplate(img_bg_gray, img_slider_gray, cv2.TM_CCOEFF_NORMED)

    print('#' * 50)
    print(type(res))  # 打印：<class 'numpy.ndarray'>
    print(res)
    # 打印：一个二维的ndarray数组
    # [[0.05604218  0.05557462  0.06844381... - 0.1784117 - 0.1811338 - 0.18415523]
    #  [0.06151756  0.04408009  0.07010461... - 0.18493137 - 0.18440475 - 0.1843424]
    # [0.0643926    0.06221284  0.0719175... - 0.18742703 - 0.18535161 - 0.1823346]
    # ...
    # [-0.07755355 - 0.08177952 - 0.08642308... - 0.16476074 - 0.16210903 - 0.15467581]
    # [-0.06975575 - 0.07566144 - 0.07783117... - 0.1412715 - 0.15145643 - 0.14800543]
    # [-0.08476129 - 0.08415948 - 0.0949327... - 0.1371379 - 0.14271489 - 0.14166716]]

    print('#' * 50)

    # cv2.minMaxLoc() 从ndarray数组中找到最小值、最大值及他们的坐标
    value = cv2.minMaxLoc(res)
    # 得到的value，如：(-0.1653602570295334, 0.6102921366691589, (144, 1), (141, 56))

    print(value, "#" * 30)

    # 获取x坐标，如上面的144、141
    return value[2:][0][0], value[2:][1][0]


def findfic(target='background.png', template='slider.png'):
    """
    :param target: 滑块背景图
    :param template: 滑块图片路径
    :return: 模板匹配距离
    """
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)
    # 使用相关性系数匹配， 结果越接近1 表示越匹配
    # https://www.cnblogs.com/ssyfj/p/9271883.html
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    # opencv 的函数 minMaxLoc：在给定的矩阵中寻找最大和最小值，并给出它们的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # 因为滑块只需要 x 坐标的距离，放回坐标元组的 [0] 即可
    if abs(1 - min_val) <= abs(1 - max_val):
        distance = min_loc[0]
    else:
        distance = max_loc[0]
    return distance


class PuzleSolver:

    PIXELS_EXTENSION = 10

    def __init__(self, piece_path, background_path):
        self.piece_path = piece_path
        self.background_path = background_path

    def get_position(self):
        template, x_inf, y_sup, y_inf = self.__piece_preprocessing()
        background = self.__background_preprocessing(y_sup, y_inf)

        res = cv2.matchTemplate(background, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc

        origin = x_inf
        end = top_left[0] + self.PIXELS_EXTENSION

        return end - origin

    def __background_preprocessing(self, y_sup, y_inf):
        background = self.__sobel_operator(self.background_path)
        background = background[y_sup:y_inf, :]
        background = self.__extend_background_boundary(background)
        background = self.__img_to_grayscale(background)

        return background

    def __piece_preprocessing(self):
        img = self.__sobel_operator(self.piece_path)
        x, w, y, h = self.__crop_piece(img)
        template = img[y:h, x:w]

        template = self.__extend_template_boundary(template)
        template = self.__img_to_grayscale(template)

        return template, x, y, h

    def __crop_piece(self, img):
        white_rows = []
        white_columns = []
        r, c = img.shape

        for row in range(r):
            for x in img[row, :]:
                if x != 0:
                    white_rows.append(row)

        for column in range(c):
            for x in img[:, column]:
                if x != 0:
                    white_columns.append(column)

        x = white_columns[0]
        w = white_columns[-1]
        y = white_rows[0]
        h = white_rows[-1]

        return x, w, y, h

    def __extend_template_boundary(self, template):
        extra_border = np.zeros((template.shape[0], self.PIXELS_EXTENSION), dtype=int)
        template = np.hstack((extra_border, template, extra_border))

        extra_border = np.zeros((self.PIXELS_EXTENSION, template.shape[1]), dtype=int)
        template = np.vstack((extra_border, template, extra_border))

        return template

    def __extend_background_boundary(self, background):
        extra_border = np.zeros((self.PIXELS_EXTENSION, background.shape[1]), dtype=int)
        return np.vstack((extra_border, background, extra_border))

    def __sobel_operator(self, img_path):
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S

        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.GaussianBlur(img, (3, 3), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad

    def __img_to_grayscale(self, img):
        tmp_path = "/tmp/sobel.png"
        cv2.imwrite(tmp_path, img)
        return cv2.imread(tmp_path, 0)


def get_y_position(alpha):
    for row_id, row in enumerate(alpha):
        for col_id, col in enumerate(row):
            if col < 127:
                return row_id


def get_x_position(alpha):
    x = None
    for row_id, row in enumerate(alpha):
        for col_id, col in enumerate(row):
            if col < 127 and (x is None or col_id < x):
                x = col_id
    return x


if __name__ == '__main__':
    img_bg_path = 'example/background.jpg'
    img_slider_path = 'example/slider.jpg'
    # solver = PuzleSolver(img_slider_path, img_bg_path)
    # solution = solver.get_position()
    # print(solution)
    # distance = findfic(target=img_bg_path, template=img_slider_path)
    # print(distance)
    img = cv2.imread(img_bg_path, -1)
    r, g, b, a = cv2.split(img)
    image = Image.open(img_bg_path)
    plt.imshow(a)
    plt.show()

    print(get_y_position(a))
    print(get_x_position(a))
