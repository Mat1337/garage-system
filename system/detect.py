import easyocr
import torch
import cv2

# load the licence plate recognition model
model = torch.hub.load('yolov5', 'custom', source='local', path='model/licence/weights/best.pt', force_reload=True)

# load the easy ocr text reader
easy_ocr = easyocr.Reader(['en'])
easy_ocr_threshold = 0.2


def read_licence_plate_text(image_path):
    # read the image into the memory
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect licence plates on the image
    results = model(image)

    # read the text from the licence plate
    return read_licence_plate(results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1], image, easy_ocr, easy_ocr_threshold)


def read_licence_plate(labels, cord, image, reader, region_threshold):
    detection_count = len(labels)
    x_shape, y_shape = image.shape[1], image.shape[0]

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
    plate_text = filter_text(ocr_result, region_threshold)

    # check for the extra space at the beginning
    if len(plate_text) != 0:
        plate_text = plate_text[1:]

    # return the licence plate text
    return plate_text


def filter_text(ocr_result, region_threshold):
    plate = ""
    for result in ocr_result:
        if result[2] >= region_threshold:
            plate += " " + result[1]
    return plate
