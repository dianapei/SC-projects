"""
Inspired by SouravJohar and updated by Diana Pei-Rung Yu
This program will collect <num_samples> of images with a particular label,
and store them in its own directory.

"""

import cv2
import os



def main():
    label_name = input('Label name: ')
    num_samples = int(input('Number of samples: '))

    img_save_path = 'image_data'
    img_label_path = os.path.join(img_save_path, label_name)

    try:
        os.mkdir(img_save_path)
    except FileExistsError:
        pass

    try:
        os.mkdir(img_label_path)
    except:
        print("{} directory already exists.".format(img_save_path))
        print('All images will be save with existing items in this folder!')

    cap = cv2.VideoCapture(0)
    ret = cap.set(3, 1920)
    ret = cap.set(4, 1080)

    start = False
    count = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            print('Error! Please check your webcam.')

        if count == num_samples:
            break

        cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "Collecting {}".format(count),\
                    (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Collecting images", frame)

        if start:
            pic = frame[100:500, 100:500]
            save_path = os.path.join(img_label_path, '{}.jpg'.format(count + 1))
            cv2.imwrite(save_path, pic)
            count += 1

        # press a to collect and pause collecting, press q to quit
        control = cv2.waitKey(10)
        if control == ord('a'):
            start = not start
        if control == ord('q'):
            break
    print('\n{} image(s) saved to {}'.format(count, img_label_path))



if __name__ == '__main__':
    main()






