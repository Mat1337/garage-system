import easyocr
import numpy
import torch
import cv2


def read_licence_plate(labels, cord, image, reader, region_threshold):
    detection_count = len(labels)
    x_shape, y_shape = image.shape[1], image.shape[0]

    print(f"[INFO] Total {detection_count} detections")
    print(f"[INFO] Searching for the licence plate")

    # used for finding the best possible licence plate on the image
    detection_threshold = 0.55
    detection_target = None

    # find the licence plate on the image
    for i in range(detection_count):
        detection = cord[i]
        if detection[4] >= detection_threshold:
            detection_threshold = detection[4]
            detection_target = detection

    # if the plate was found read the text from the plate
    if detection_target is not None:
        # extract the coordinates from the bounding box
        x1, y1, x2, y2 = int(detection_target[0] * x_shape), int(detection_target[1] * y_shape), int(detection_target[2] * x_shape), int(detection_target[3] * y_shape)
        coords = [x1, y1, x2, y2]

        # read the text from the licence plate
        return read_text(img=image, coords=coords, reader=reader, region_threshold=region_threshold)

    # if the plate was not found return nothing
    return None


def read_text(img, coords, reader, region_threshold):
    # separate coordinates from box
    xmin, ymin, xmax, ymax = coords
    number_plate = img[int(ymin):int(ymax), int(xmin):int(xmax)]

    # read the text from the licence plate image
    ocr_result = reader.readtext(number_plate)
    text = filter_text(region=number_plate, ocr_result=ocr_result, region_threshold=region_threshold)
    if len(text) == 1:
        text = text[0].upper()
    return text


def filter_text(region, ocr_result, region_threshold):
    rectangle_size = region.shape[0] * region.shape[1]

    plate = []
    for result in ocr_result:
        length = numpy.sum(numpy.subtract(result[0][1], result[0][0]))
        height = numpy.sum(numpy.subtract(result[0][2], result[0][1]))

        if length * height / rectangle_size > region_threshold:
            plate.append(result[1])
    return plate


if __name__ == '__main__':
    # load the easy ocr text reader
    easy_ocr = easyocr.Reader(['en'])
    easy_ocr_threshold = 0.2

    # load the licence plate recognition model
    print(f"[INFO] Loading model... ")
    model = torch.hub.load('yolov5', 'custom', source='local', path='model/licence/weights/best.pt', force_reload=True)

    # read the image into the memory
    image = cv2.imread("C:/Users/mat/Desktop/car.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect licence plates on the image
    print(f"[INFO] Detecting licence plates")
    results = model(image)

    # read the text from the licence plate
    licence_plate = read_licence_plate(results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1], image, easy_ocr, easy_ocr_threshold)
    print(f"[INFO] Licence plate '{licence_plate}'")

