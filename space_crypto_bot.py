
DEBUG = False
if not DEBUG:
    from App import Main as main
    main.start_app()
else:
    print('START DEBUG')
    from App import GameResources as res
    import cv2
    from App import Routines as routines
    from App.Objects.externalConfigs import ExternalConfigs
    from App.Find import Find
    from time import sleep
    from pyautogui import scroll, alert, moveTo, position, screenshot, drag
    sleep(5)
    find = Find()
    sc = screenshot()
    sc.save('first.jpg')
    print('foi')
    sleep(4)
    sc = screenshot()
    sc.save('second.jpg')

    im1 = cv2.imread('first.jpg')
    im2 = cv2.imread('second.jpg')

    prob = routines.compare_images(im1, im2)
    print(prob)

    res.__home_screen_activate__()

    alert('END DEBUG')
