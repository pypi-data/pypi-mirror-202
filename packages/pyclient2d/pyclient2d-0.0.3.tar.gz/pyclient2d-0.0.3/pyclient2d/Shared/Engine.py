import sys

from ..Math import Number, time_from, get_system_time, time_between


class Engine:

    def run(self):
        pass

    def __init__(self,
                 ms_per_tick: Number = 15,
                 should_render: bool = True):
        """
        Creates an instance of the main Engine used to power pyclient2d
        :param ms_per_tick: Number of ms per game-tick
        :param should_render: Should this instance of the engine actually render anything?
        """

        self.__ms_per_tick = ms_per_tick
        self.__tickrate = float(1e3) / ms_per_tick
        self.run = self.__mainloop_norender if not should_render else self.__mainloop

        self.__setup_globals()

    def __setup_globals(self):
        self.__tickbase = 0
        self.__frames_per_second = 0

        self.__running = True
        self.__init_time = get_system_time()

    def get_engine_time(self) -> float:
        return time_from(self.__init_time)

    def update(self):
        self.__tickbase += 1

    def render(self):
        pass

    def __mainloop(self):
        """"""
        lag = 0.0
        updates, frames = 0, 0
        prev_time = get_system_time()
        while self.__running:
            current_time = get_system_time()
            lag += time_between(prev_time, current_time)
            while lag >= self.__ms_per_tick:
                self.update()
                lag -= self.__ms_per_tick
                updates += 1
                if self.__tickbase % int(self.__tickrate) == 0:
                    print(f"Frames: {frames}")
                    print(f"Ticks: {updates}")
                    frames, updates = 0, 0
            self.render()
            frames += 1
            prev_time = current_time
        sys.exit(0)

    def __mainloop_norender(self):
        pass


