from Simulation import SIMLOGGER


class ExgressProvider(object):
    def __init__(self, env, address):
        self.env = env
        self.address = address
        self.message_storage = []

    def __str__(self):
        return "({0},{1})".format(self.address, self.message_storage)

    def receive_message(self, message):
        # method to handle the reception of messages coming out of the MixNetwork
        print('ExgressProvider: receive_message message_id: ', message.message_id)
        SIMLOGGER.log('Step: ' + str(self.env.now) + ' - ExgressProvider: receive_message with id: ' + str(message.message_id))
        SIMLOGGER.action_to_csv(str(self.env.now), self.address, 'receive', str(message.message_id), 'None')
        self.message_storage.append(message)
