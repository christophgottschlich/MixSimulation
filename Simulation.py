import Logger

SIMLOGGER = Logger.Logger()


class Simulation(object):

    def __init__(self, env, mix_network):
        self.env = env
        self.mix_network = mix_network

    def __str__(self):
        return "({0})".format(self.mix_network)

    def perform_step(self):
        # method called every millisecond the simulation iterates
        while True:
            self.mix_network.check_network()
            yield self.env.timeout(1)
