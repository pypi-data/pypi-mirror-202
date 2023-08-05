import cv2
import numpy as np
from matplotlib import pyplot as plt


def imshow(image):
    plt.imshow(image)
    plt.show()


def grid_image(image, size):
    out_image = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    if type(image) is list:
        if len(image) > 0:
            rows = int(np.ceil(np.sqrt(len(image))))
            colms = int(np.ceil(len(image) / rows))
            if len(image[0].shape) == 3:
                h, w, _ = image[0].shape
                newimages = [image[0]]
            else:
                h, w = image[0].shape
                newimages = [GRAY3Channels(image[0])]

            for i in image[1:]:
                if len(i.shape) == 3:
                    newimages.append(cv2.resize(i, (w, h)))
                else:
                    newimages.append(cv2.resize(GRAY3Channels(i), (w, h)))

            v_stacks = []
            for i in range(colms):
                h_stacks = []
                for j in range(rows):
                    if len(newimages) > (j + i * rows):
                        h_stacks.append(newimages[j + i * rows])
                    else:
                        blank_im = np.zeros_like(h_stacks[-1])
                        h, w = blank_im.shape[:2]

                        for j in range(3):
                            cv2.rectangle(
                                blank_im,
                                (int(w * 0.2 * j), int(h * 0.2 * j)),
                                (int(w * (1 - 0.2 * j)), int(h * (1 - 0.2 * j))),
                                (255, 255, 255),
                                max(int(min(h, w) * 0.05), 1),
                            )
                        h_stacks.append(blank_im)
                v_stacks.append(np.hstack(h_stacks))

            out_image = np.vstack(v_stacks)

    out_image = cv2.resize(out_image.copy(), size)
    return out_image


def GRAY3Channels(image, values=[1, 1, 1]):
    assert type(image) is np.ndarray
    if len(image.shape) == 2:
        newim = cv2.merge(
            [
                cv2.multiply(image, values[0], dtype=cv2.CV_8U),
                cv2.multiply(image, values[1], dtype=cv2.CV_8U),
                cv2.multiply(image, values[2], dtype=cv2.CV_8U),
            ]
        )
        newim = newim * 255 if np.max(newim) <= 1 else newim
        return newim
    else:
        return image


def ROIim(image, size=(1820, 980), coordinates=True):
    ratio = [1, 1]
    if size is not None:
        ratio = [image.shape[1] / size[0], image.shape[0] / size[1]]
        imageR = cv2.resize(image.copy(), size)
    x = cv2.selectROI(imageR)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    x2 = [
        int(x[0] * ratio[0]),
        int(x[1] * ratio[1]),
        int(x[2] * ratio[0]),
        int(x[3] * ratio[1]),
    ]
    if coordinates:
        return x2
    else:
        return image.copy()[x2[1] : x2[1] + x2[3], x2[0] : x2[0] + x2[2]]
