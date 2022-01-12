import numpy


class Message(object):
    def __init__(self, real_sender, recipient, payload, message_id, route, para_mu,  ingress_provider_sending_time, cover_traffic, crypto_delay):
        self.real_sender = real_sender
        self.recipient = recipient
        self.payload = payload
        self.message_id = message_id
        self.route = route
        self.para_mu = para_mu   # Array with average delay for mixes in milliseconds
        self.valid_intervals = []
        self.ingress_provider_sending_time = ingress_provider_sending_time
        self.delays = []  # Array with actual delay for mixes in milliseconds -> calculated with para_mu + exponential distribution
        self.timestamp_msg_sent = 0
        self.cover_traffic = cover_traffic
        self.crypto_delay = crypto_delay

        for i in range(len(para_mu)):
            self.delays.append(int(numpy.random.exponential(para_mu[i], 1).item(0)) + self.crypto_delay)

        tmp = ingress_provider_sending_time
        for i in range(len(self.delays)):
            tmp += self.delays[i]
            delay_tmp = self.delays[i]
            if delay_tmp < 5:  # vermeidet bei zu geringen delays (relativ gesehen) die direkte ablehnung durch ein zu geringes zeitintervall
                delay_tmp = 5

            border_left = round(tmp - 2*delay_tmp)
            if border_left < 0:
                border_left = 0
            border_right = round(tmp + 2*delay_tmp)
            self.valid_intervals.append([border_left, border_right])
            # tmp = 0

    def __str__(self):
        return "({0},{1},{2},{3},{4},{5},{6},{7},{8},{9})".format(self.message_id, self.real_sender, self.recipient, self.payload, self.message_id, self.route, self.delays, self.valid_intervals, self.ingress_provider_sending_time, self.cover_traffic)

    def __getitem__(self, key):
        return self
