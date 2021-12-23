import simpy
import Message
import Logger

SIMLOGGER = Logger.Logger()


class Simulation(object):

    def __init__(self, env, mix_network):
        self.env = env
        # self.param = simpy.Resource(env, param)
        self.mix_network = mix_network

    def __str__(self):
        return "({0})".format(self.mix_network)

    def perform_step(self):
        # method called every millisecond the simulation iterates
        while True:
            self.mix_network.check_network()
            yield self.env.timeout(1)
            # print('Simulation Step: ', self.env.now, '----------------------------------------------------------------')

    def setup_messages(self):  # CAN BE DELETED -> ONLY FOR TESTING PURPOSES
        # method called to initialize the messages that should be sent during the simulation and writes it into the
        # ingressProvider of the mix_network
        print('Simulation: setup_messages')

        m1 = Message.Message('U1', 'U2', 'MESSAGEPAYLOAD', '1', ['M1', 'M3'], [10, 10], 1, False)
        m2 = Message.Message('U2', 'U3', 'MESSAGEPAYLOAD', '2', ['M2', 'M3'], [10, 10], 3, False)
        m3 = Message.Message('U3', 'U1', 'MESSAGEPAYLOAD', '3', ['M2', 'M3'], [10, 10], 5, False)

        self.mix_network.ingress_provider.message_storage = [m1, m2, m3]

