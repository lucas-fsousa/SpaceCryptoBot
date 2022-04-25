from pyautogui import scroll, moveTo, center, screenshot, position, drag
from time import sleep, time


def __current_screen__():
    from App.Find import Find
    from App import Routines as routines
    from App.Objects.externalConfigs import ExternalConfigs
    find = Find()
    config = ExternalConfigs()
    screen = 0
    timeout = time().__add__(config.TransitionDelay * 2)
    routines.save_logs('validating screens')
    while timeout > time() and screen == 0:
        print('0')
        if find.search_for_image(find.ConnectWallet, to_click=False) is not None:
            routines.save_logs('login screen located')
            print('1')
            screen = 1
        elif find.search_for_image(find.StartBattleBtn, to_click=False) is not None:
            routines.save_logs('game home screen located')
            screen = 2
            print('2')
        elif find.search_for_image(find.ScreenBossFight, to_click=False) is not None:
            routines.save_logs('boss fight screen located')
            screen = 3
            print('3')
        else:
            routines.save_logs('no valid page was found')
            routines.reset_page()
            sleep(config.ConnectionScreen * 2)
    return screen


def __select_valid_ship__():
    from App import Routines as routines
    from App.Find import Find
    from App.Objects.externalConfigs import ExternalConfigs

    find = Find()
    config = ExternalConfigs()
    selected_ships = False
    box = find.search_for_image(find.EnergyBar, return_xy=False)
    if box is not None:
        find.calc_box_return_xy(box)
        result = find.locate_next(find.FightOnBtn)
        if result is not None:
            x, y = center(result)
            moveTo(x, y, config.MouseDelay)
            routines.click()
            routines.save_logs('a ship has been selected')
            selected_ships = True
        else:
            # page scrolling
            xy = find.search_for_image(find.StartBattleBtn, to_click=False)
            if xy is not None:
                x, y = xy
                x -= 300
                y -= 130
                routines.scroll_page(xy=(x, y), reverse=True)
                routines.click()
                moveTo(x, y, config.MouseDelay)
    else:
        # page scrolling
        xy = find.search_for_image(find.StartBattleBtn, to_click=False)
        if xy is not None:
            x, y = xy
            x -= 300
            y -= 130
            routines.scroll_page(xy=(x, y), reverse=True)
            routines.click()
            moveTo(x, y, config.MouseDelay)
    return selected_ships


def __home_screen_activate__():
    from App.Objects.externalConfigs import ExternalConfigs
    from App.Find import Find
    import cv2
    from App.Routines import save_logs, scroll_page, compare_images

    config = ExternalConfigs()
    find = Find()
    success = False
    timeout = time().__add__(600)
    while True:
        _next = False

        if timeout < time():
            success = False
            break

        if find.search_for_image(find.CloseBtn) is not None:
            sleep(config.TransitionDelay * 2)
            break

        if find.search_for_image(find.StartBattleBtn, to_click=False) is not None:
            save_logs('monitoring home screen')
            _next = True
        else:
            sleep(config.DefaultDelay)
            save_logs('unknown screen route, restarting screen recognition')
            break

        sleep(config.DefaultDelay)
        if _next:
            save_logs('removing all selected ships')
            __remove_all_ships__()

            timeout = time().__add__(config.Timeout * 15)
            count_ships_selected = 0
            no_more_ships = False
            i = 0
            attempts = 0
            count_scroll = 0

            sc = screenshot()
            sc.save('first.jpg')
            sc.save('second.jpg')

            save_logs('locating ships to include in the fleet')
            while timeout > time() and count_ships_selected < 15 and not no_more_ships:
                if __select_valid_ship__():
                    count_ships_selected += 1
                    sleep(config.DefaultDelay / 2)
                else:
                    # verification scheme to identify if the list of ships is already at the end
                    count_scroll += 1
                    x, y = position()
                    w, h = screenshot().size
                    if i == 0:
                        sc = screenshot(region=(250, y - 250, w / 3, 350))
                        sc.save('first.jpg')
                        i += 1
                        continue

                    elif i == 1:
                        sc = screenshot(region=(250, y - 250, w / 3, 350))
                        sc.save('second.jpg')
                        i += 1
                        continue

                    im1 = cv2.imread('first.jpg')
                    im2 = cv2.imread('second.jpg')
                    probability = compare_images(im1, im2)
                    if probability == 1:
                        save_logs('the list of ships has come to an end, checking battle status')
                        no_more_ships = True
                    else:
                        sc.save('second.jpg')
                        sc = screenshot(region=(250, y - 250, w / 3, 350))
                        sc.save('first.jpg')

            # checks if it is possible to start a battle, otherwise it will wait a few seconds and restart the
            # fleet assembly process
            if count_ships_selected < config.MinShipsToStart:
                save_logs(f'Unable to start battle. > minimum ships required {config.MinShipsToStart} > '
                          f'selected {count_ships_selected}')
                xy = find.search_for_image(find.StartBattleBtn, to_click=False)
                if xy is not None:
                    for count in range(0, count_scroll, 1):
                        x, y = xy
                        x -= 250
                        y -= 220
                        scroll_page(xy=(x, y))
                        sleep(0.5)
                sleep(config.TransitionDelay * 2)
                attempts += 1
                continue

            save_logs(f'{count_ships_selected} ships selected for battle')
            no_have_btn = 0
            timeout = time().__add__(config.Timeout)
            while no_have_btn < 2 and timeout > time():
                no_have_btn = 0
                if find.search_for_image(find.StartBattleBtn) is None:
                    no_have_btn += 1
                if find.search_for_image(find.Confirmation) is None:
                    no_have_btn += 1
                sleep(config.DefaultDelay)

            sleep(config.TransitionDelay * 1.2)

            # checks if the start battle button persists on the screen
            if find.search_for_image(find.ScreenBossFight, to_click=False) is not None:
                success = True
        if success:
            break
    sleep(config.TransitionDelay)
    return success


def __connect_wallet__():
    from App.Objects.externalConfigs import ExternalConfigs
    from App.Find import Find
    from App.Routines import save_logs

    find = Find()
    config = ExternalConfigs()
    success = False
    try:
        timeout = time().__add__(config.ConnectionScreen * 2)
        count_click = 0
        while timeout > time() and count_click < 3:
            if find.search_for_image(find.ConnectWallet) is not None:
                count_click += 1
                sleep(config.DefaultDelay)

        if count_click == 2 or count_click == 3:
            save_logs('successful wallet connection')
            sleep(config.ConnectionScreen)
            success = True
    except Exception as ex:
        save_logs(f'failed trying to connect to metamask > {ex}', 'connect_wallet')
    finally:
        return success


def __boss_fight_screen__():
    from App.Objects.externalConfigs import ExternalConfigs
    from App.Find import Find
    from App.Routines import save_logs

    config = ExternalConfigs()
    find = Find()
    success = False
    try:
        save_logs('monitoring boss fight')
        timeout = time().__add__(config.WaitBossFightScreen)
        while timeout > time():
            find.search_for_image(find.Confirmation)
            sleep(2)

        timeout = time().__add__(config.Timeout)
        while timeout > time() and not success:
            while find.search_for_image(find.ChangeShips) is not None and timeout > time():
                success = True
        sleep(config.TransitionDelay)
        save_logs('upgrading ship resources')
    except Exception as ex:
        save_logs(f'error while monitoring the boss fight > {ex}', 'boss_fight_screen')
    finally:
        return success


def __remove_all_ships__():
    from App.Find import Find
    from App.Routines import save_logs, scroll_page

    find = Find()
    try:
        while find.search_for_image(find.RemoveShip) is not None:
            pass

        # # page scrolling
        # xy = find.search_for_image(find.StartBattleBtn, to_click=False)
        # save_logs('')
        # if xy is not None:
        #     x, y = xy
        #     scroll_page(xy=(x - 300, y - 220))

    except Exception as ex:
        save_logs(f'fails when trying to remove ships > {ex}', 'remove_all_ships')
