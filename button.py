# Button
from machine import Pin, Timer
from time import ticks_ms


class button():
    def __init__(self, sw_id, pin_id):
        self.pin_id = pin_id
        self.sw_id = sw_id
        self.sw_name = "SW"+str(sw_id)
        self.signal = None
        self.pressed = 0
        self.pre_count = 0
        self.con_flag = 0
        self.sw = None
        self.button_init()
        self.last_check_tick = ticks_ms()
        self.debounce_cycle = 1
        self.threshold_1 = 12    # threshold between short press and long press
        self.threshold_2 = 60    # threshold between long press and continuous press

    def __SWx_Process(self):

        self.pressed = 1

    def button_init(self):
        self.sw = Pin(self.pin_id, Pin.IN, Pin.PULL_DOWN)
        self.sw.irq(lambda pin : self.__SWx_Process(), Pin.IRQ_RISING)

    def update(self):
        if self.pressed:
            # state check
            if self.sw.value() == 1:
                # Period calculation
                self.pre_count = self.pre_count+1
                # 
                if self.con_flag == 0 and self.pre_count >= self.threshold_2:
                    self.con_flag = 1
                    self.signal = self.sw_name+"_C_ON"
            else:
                # Recognize key mode
                # three different mode: short press, long_press, continuous_press
                if self.pre_count <= self.threshold_1:
                    self.signal = self.sw_name+"_S"
                elif self.threshold_1 < self.pre_count and self.pre_count < self.threshold_2:
                    self.signal = self.sw_name+"_L"
                elif self.pre_count >= self.threshold_2:
                    self.signal = self.sw_name+"_C_OFF"
                else:
                    print("Unexcept ERROR!")
                
                # reset register
                self.pressed = 0
                self.pre_count = 0
                self.con_flag = 0
                    
    
    def get_signal(self):
        self.update()
        mes = self.signal
        self.signal = None
        return mes
    
class button_sys:
    def __init__(self):
        self.buttons = {}
        self.signal_list = set()
        self.timer = None
        self.init()

    def init(self):
        self.timer = Timer(period=40, mode=Timer.ONE_SHOT, callback=lambda t:print("start Timer!"))
        self.timer.init(period=20, mode=Timer.PERIODIC, callback=lambda t:self.__get_signal_T())

    def add(self, button_id, pin_id):
        self.buttons[str(button_id)] = button(button_id, pin_id)

    def show_list(self):
        if len(self.buttons) != 0:
            for b in self.buttons.values():
                print(f"Key_id = {b.sw_id}, Pin_id = {b.pin_id}")

    def show_signals(self):
        print(self.signal_list)

    def get_signals(self):
        for b in self.buttons.values():
            signal_stream = b.get_signal()
            if signal_stream is not None:
                self.signal_list.add(signal_stream)
        signal_set = self.signal_list.copy()
        self.signal_list.clear()
        return signal_set
    
    def __get_signal_T(self):
        for b in self.buttons.values():
            signal_stream = b.get_signal()
            if signal_stream is not None:
                self.signal_list.add(signal_stream)
                
    def get_signal_T(self):
        signal_set = self.signal_list.copy()
        self.signal_list.clear()
        return signal_set
        
            




    

        

            




    

        
