from Simulation import SIMLOGGER


class PoissonMix(object):
    def __init__(self, env, address):
        self.env = env
        self.address = address
        self.message_pool = []
        self.message_mean = [0, 1]
        self.cover_message_mean = [0, 1]
        self.empty_pool = [0, 1]

        SIMLOGGER.reset_files()

    def __str__(self):
        return "({0},{1})".format(self.address, self.message_pool)

    def receive_message(self, message):
        # method for receiving incoming messages
        print('PoissonMix ', str(self.address), ': Receiving Message message_id: ', message.message_id)
        SIMLOGGER.log('Step: ' + str(self.env.now)
                      + ' - PoissonMix ' + str(self.address)
                      + ': Receiving Message with id: ' + str(message.message_id))
        SIMLOGGER.action_to_csv(str(self.env.now), self.address, 'receive', str(message.message_id), 'None')
        if self.validate_message(message):
            self.message_pool.append(message)

    def send_message(self, message):
        # Method for sending messages
        print('PoissonMix ', str(self.address), ': Sending Message message_id: ', message.message_id)
        tmp_message = message
      
        for i in range(len(self.message_pool)):
            if self.message_pool[i].message_id == message.message_id:
                self.message_pool.pop(i)
                break

        if len(tmp_message.route) > 0:
            tmp_message.delays.pop(0)
            address = tmp_message.route[0]
            tmp_message.route.pop(0)
            tmp_message.valid_intervals.pop(0)
        else:
            if tmp_message.recipient.startswith('U'):
                address = 'EP'
            else:
                return None
        SIMLOGGER.log('Step: ' + str(self.env.now) + ' - PoissonMix '
                      + str(self.address) + ': Sending Message with id: '
                      + str(tmp_message.message_id) + ' to address: ' + address)
        SIMLOGGER.action_to_csv(str(self.env.now), self.address, 'send', str(tmp_message.message_id), address)
        return [tmp_message, address]

    def validate_message(self, message):
        # method for validating if the message is correct and returns a boolean value
        # print('PoissonMix ', str(self.address), ': Validating Message')

        current_ms = self.env.now  # - message.timestamp_msg_sent
        if current_ms < message.valid_intervals[0][0] or current_ms > message.valid_intervals[0][1]:
            print('PoissonMix ', str(self.address), ': Rejecting Message ID ', message.message_id)
            SIMLOGGER.log('Step: ' + str(self.env.now) + ' - PoissonMix ' + str(self.address)
                          + ': REJECTING Message with id: ' + str(message.message_id)
                          + '. Message arrived after ' + str(current_ms)
                          + 'MS and is not in the specified time window ' + str(message.valid_intervals[0]))
            SIMLOGGER.action_to_csv(str(self.env.now), self.address, 'reject', str(message.message_id), 'None')

            return False
        SIMLOGGER.log('Step: ' + str(self.env.now) + ' - PoissonMix ' + str(self.address)
                      + ': ACCEPTING Message with id: ' + str(message.message_id)
                      + '. Message arrived after ' + str(current_ms)
                      + 'MS and is in the specified time window ' + str(message.valid_intervals[0]))
        SIMLOGGER.action_to_csv(str(self.env.now), self.address, 'accept', str(message.message_id), 'None')

        message.timestamp_msg_sent = self.env.now
        return True

    def check_messages(self):
        # method to check if messages should be sent
        # print('PoissonMix ', str(self.address), ': Checking Messages')

        # Mix Messages Analytics
        if self.env.now > 60000:  # start analytics after the first minute has passed to avoid including the warmup
            self.message_mean[0] += len(self.message_pool)
            self.message_mean[1] += 1

            for m in self.message_pool:
                if m.cover_traffic:
                    self.cover_message_mean[0] += 1
            self.cover_message_mean[1] += 1

            if len(self.message_pool) == 0:
                self.empty_pool[0] += 1
            self.empty_pool[1] += 1

        messages_to_handle = []
        for m in self.message_pool:
            if len(m.route) == 0 and m.delays[0] == 0:
                tmp1 = self.send_message(m)
                if tmp1 is not None:
                    messages_to_handle.append(tmp1)
            elif m.delays[0] == 0:
                tmp2 = self.send_message(m)
                if tmp2 is not None:
                    messages_to_handle.append(tmp2)
            else:
                m.delays[0] -= 1
        return messages_to_handle
