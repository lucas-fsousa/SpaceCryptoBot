def start_app():
    from time import sleep
    from App.Routines import save_logs, reset_page
    from App import GameResources as resources
    from App.Objects.externalConfigs import ExternalConfigs

    config = ExternalConfigs()
    screen = 0
    save_logs('starting application')
    while True:
        isvalid = True
        if isvalid:
            while True:
                try:
                    if screen == 0:  # no screen selected
                        screen = resources.__current_screen__()
                    elif screen == 1:  # start game - connect wallet screen
                        screen = 0  # reset screen
                        if resources.__connect_wallet__():
                            screen = 2
                    elif screen == 2:  # home screen - ships activation
                        screen = 0  # reset screen
                        if resources.__home_screen_activate__():
                            screen = 3
                    elif screen == 3:  # boss fight screen
                        screen = 0  # reset screen
                        if resources.__boss_fight_screen__():
                            screen = 2
                    else:
                        screen = 0

                    if screen == 0:
                        reset_page()
                        sleep(config.TransitionDelay)
                    sleep(config.TransitionDelay)
                except Exception as ex:
                    print(ex)
        else:
            save_logs('try again.')
        sleep(config.DefaultDelay)
