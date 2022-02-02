from Simulation import SIMLOGGER


class IngressProvider(object):
    def __init__(self, env, address):
        self.env = env
        self.address = address
        self.message_storage = []

    def __str__(self):
        return "({0},{1})".format(self.address, self.message_storage)

    def send_message(self, message):
        # method that sends the messages to the mix network at certain times
        print('IngressProvider: send_message message_id: ', message.message_id)
        SIMLOGGER.log('Step: ' + str(self.env.now)
                      + ' - IngressProvider: send_message with id: '
                      + str(message.message_id) + ' to address: ' + message.route[0])
        SIMLOGGER.action_to_csv(str(self.env.now), self.address, 'send', str(message.message_id), message.route[0])
        message.timestamp_msg_sent = self.env.now - 1  # needed to calculate time-window for accepting the message
        receiver = message.route[0]
        if len(message.route) > 0:
            message.route.pop(0)
        # self.message_storage.remove(message)
        return [message, receiver]

    def check_messages(self):
        # method that checks if messages should be sent into the network
        # print('IngressProvider: check_messages')
        messages_to_handle = []
        for message in self.message_storage:
            if message.ingress_provider_sending_time == self.env.now:
                messages_to_handle.append(self.send_message(message))
        return messages_to_handle

    def fill_message_storage(self, messages):
        # method that safes the initial messages for the simulation
        print('IngressProvider: fill_message_storage')
        self.message_storage = messages
