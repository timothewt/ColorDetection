import argparse
import cv2


def get_image_from_arg():
    global image
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    image_path = vars(parser.parse_args())['image']
    return cv2.imread(image_path)


def get_colors_list():
    colors = []
    with open('colors.csv') as f:
        for row in f:
            row = row[:-1].replace('"', '').split(',')
            colors.append([row[1], [int(row[3]), int(row[4]), int(row[5])]])   # [name, hex, [R,G,B]]
    return colors


def find_color(rgb):
    result = []
    minimum_found = 1000
    for color in colors_list:
        diff = abs(rgb[0] - color[1][0]) + abs(rgb[2] - color[1][2]) + abs(rgb[2] - color[1][2])
        if diff < minimum_found:
            result = color
            minimum_found = diff
    return result


def on_image_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_rgb = image[y, x]
        color = find_color(pixel_rgb)
        color[1].reverse()  # reversed because cv2.rectangle() takes BGR as color parameter
        new_img = image
        cv2.rectangle(new_img, (10, 10), (990, 60), color[1], -1)
        font_color = (255, 255, 255) if sum(color[1]) < 500 else (0, 0, 0)
        cv2.putText(new_img, color[0] + ' (' + str(color[1][2]) + ', ' + str(color[1][1]) + ', ' + str(color[1][0]) + ')'
                    , (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 2)
        cv2.imshow('image', new_img)
        print('Clicked color:' + color[0] + ', RGB:', color[1])


image = get_image_from_arg()
colors_list = get_colors_list()
while True:
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', on_image_click)
    k = cv2.waitKey(1)
    if k == 27:
        cv2.destroyAllWindows()
        break
