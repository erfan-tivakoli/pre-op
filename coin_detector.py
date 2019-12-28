import cv2
import numpy as np

coin_radius = 33

def find_coin(image_path):
    # Read image.
    # img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(img, (7, 7))
    rendered_image_path = 'rendered_image.png'

    best_pt = None

    # Apply Hough transform on the blurred image.
    for param2 in range(20, 100, 10):
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 20, param1=100,
                                            param2=param2, minRadius=20, maxRadius=500)

        # Draw circles that are detected.
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
            # colored = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            for pt in detected_circles[0, :]:
                # a, b, r = pt[0], pt[1], pt[2]

                # Draw the circumference of the circle.
                # cv2.circle(colored, (a, b), r, (0, 255, 0), 10)

                # Draw a small circle (of radius 1) to show the center.
                # cv2.circle(colored, (a, b), 1, (0, 0, 255), 3)
                # cv2.imshow("Detected Circle", img)
                # cv2.waitKey(0)
                best_pt = pt
                break

        else:
            break

    if best_pt is None:
        return None, None

    colored = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    a, b, r = best_pt[0], best_pt[1], best_pt[2]

    cv2.circle(colored, (a, b), r, (0, 255, 0), 10)

    cv2.imwrite(rendered_image_path, colored)
    return rendered_image_path, 33 / r
