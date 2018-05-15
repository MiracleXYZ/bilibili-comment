from old_main import wordcloud_workflow
from os.path import join
from PIL import Image

PATH = './images/AprilFool'

# WIDTH = 1280
# HEIGHT = 720

def crop_image(img):
    im = Image.open(join(PATH, img))
    size = im.size
    print(size)
    left_half = im.crop((0, 0, size[0] // 2, size[1]))
    left_half.save(join(PATH, '{}_left.jpg'.format(img[:-4])))

    right_half = im.crop((size[0] // 2, 0, size[0], size[1]))
    right_half.save(join(PATH, '{}_right.jpg'.format(img[:-4])))

def merge_image(left, right, output):
    leftImg = Image.open(join(PATH, left))
    rightImg = Image.open(join(PATH, right))
    assert leftImg.size == rightImg.size
    WIDTH, HEIGHT = leftImg.size
    WIDTH *= 2

    target = Image.new('RGB', (WIDTH, HEIGHT))
    target.paste(leftImg, (0, 0, WIDTH//2, HEIGHT))
    target.paste(rightImg, (WIDTH//2, 0, WIDTH, HEIGHT))
    target.save(join(PATH, output))

crop_image('AprilFoolAi.jpg')
crop_image('AprilFoolLuna.jpg')
merge_image('AprilFoolAi_right.jpg', 'AprilFoolLuna_left.jpg', 'AprilFool.jpg')

wordcloud_workflow(21499426, join(PATH, 'AprilFoolAi_right.jpg'), join(PATH, 'WCLeft.png'))
wordcloud_workflow(21499446, join(PATH, 'AprilFoolLuna_left.jpg'), join(PATH, 'WCRight.png'))
merge_image('WCLeft.png', 'WCRight.png', 'WCAprilFool.png')

