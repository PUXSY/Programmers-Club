import pynput.keyboard

class KeybordLisner:
    def __init__(self):
        self.current_key
        
    def run(self) -> None:
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
    