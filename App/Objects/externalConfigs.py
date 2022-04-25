import os
import yaml as ym
from pyautogui import alert
from App import Routines as routines


class ExternalConfigs:
    def __init__(self):
        try:
            stream = open(r"config.yaml", "r")
            configs = ym.safe_load(stream)
            conf = configs["configs"]
            game = configs["game_configs"]

            # ===================== SYSTEM CONFIGS =====================
            self.ConnectionScreen = float(conf["connection_screen"])
            self.TransitionDelay = float(conf["transition_delay"])
            self.DefaultDelay = float(conf["default_delay"])
            self.Confidence = float(conf["confidence"])
            self.Attempts = int(conf["attempts"])
            self.Timeout = float(conf["timeout"])
            self.MouseDelay = float(conf["mouse_delays"])
            self.InvertedMouse = bool(conf["inverted_mouse"])
            self.ResetLogsOnStart = bool(conf["reset_logs_on_start"])

            # ===================== GAME CONFIGS =======================
            self.MinShipsToStart = int(game["min_ships_to_start"])
            self.WaitBossFightScreen = int(game["wait_boss_fight_screen"])

        except Exception:
            alert('The application was terminated unexpectedly. If you didn\'t shut down, try deleting'
                  'the configuration files (config.yaml) and restarting the bot.')

    if not os.path.exists("config.yaml"):
        file = """
        # time in seconds
        configs:
            # default: 0.9 / trust the bot to click on the location. [Max: 1 / Min: 0.1]
            confidence: 0.9
        
            #default: False [False | True] / setting to use the mouse in reversed
            inverted_mouse: False
        
            # default 5.0 seconds / default system activity delay
            default_delay: 5.0
            
            # default 1.0 second / looping execution time delay
            looping_delay: 1.0
            
            # default 30.0 seconds / delay for error checking on initial connection screen
            connection_screen: 30.0
            
            # default 15.0 seconds / Used in screen transitions that may experience delays due to game server overload
            transition_delay: 15.0
            
            # recommended 0.2 speed move
            mouse_delays: 0.2
            
            # default: True [False | True] / reset application operation logs
            reset_logs_on_start: True
            
            # default: 2 / number of trying to read the user's screen
            attempts: 2
            
            # default: 30 / timeout in seconds for each execution attempt
            timeout: 30
        
        # game configuration settings
        game_configs:
            # default 10 / minimum value of the amount of ships in the fleet to start the battle
            min_ships_to_start: 10

            # default 300 seconds / time in seconds to wait on the boss fight screen
            wait_boss_fight_screen: 300
        """

        try:
            arq = open(r"config.yaml", "w")
            arq.write(file)
            arq.close()
        except Exception as ex:
            routines.save_logs(f'external configs open failed >> {ex}', 'external configs create')
