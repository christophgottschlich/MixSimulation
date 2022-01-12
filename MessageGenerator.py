import numpy
import random
import string
import Message


class MessageGenerator(object):
    def __init__(self, param_mu, param_lamda, param_lamda_cover_loop, param_lamda_cover_drop, param_lamda_cover_mix, sim_duration, mix_network, nbr_user, user_profile, crypto_delay):
        self.param_mu = param_mu
        self.param_lamda = param_lamda
        self.param_lamda_cover_loop = param_lamda_cover_loop
        self.param_lamda_cover_drop = param_lamda_cover_drop
        self.param_lamda_cover_mix = param_lamda_cover_mix
        self.sim_duration = sim_duration
        self.mix_network = mix_network
        self.nbr_user = nbr_user
        self.message_storage = []
        self.message_unique_id = 1
        self.user_profile = user_profile
        self.user_profile_array = self.def_user_profiles(nbr_user, user_profile)
        self.crypto_delay = crypto_delay

    def __str__(self):
        return "({0},{1},{2},{3},{4},{5},{6})".format(self.param_mu, self.param_lamda, self.sim_duration, self.param_lamda_cover_loop, self.param_lamda_cover_drop, self.param_lamda_cover_mix, self.nbr_user)

    def __getitem__(self, key):
        return self

    def def_user_profiles(self, nbr_user, profile):
        # method that creates an array of possible receivers for every user based on the given user_profile
        print('MessageGenerator: def_user_profiles')
        ret = []
        user_list = []
        for i in range(nbr_user):
            user_list.append(i + 1)

        for i in range(nbr_user):
            tmp_user_list = user_list.copy()
            tmp_user_list.remove(i + 1)
            tmp = random.sample(tmp_user_list, profile)
            ret.append(tmp)
        return ret


    def create_messages(self):
        # method that creates the whole message traffic for the simulation beforehand
        print('MessageGenerator: create_messages')
        # numpy.random.seed(42)
        pois_sending_message = numpy.random.poisson(self.param_lamda / 1, int(self.sim_duration / 60000))  # lamda and mu are given for every minute -> sim for milliseconds

        pois_loop_cover = numpy.random.poisson(self.param_lamda_cover_loop / 1, int(self.sim_duration / 60000))
        pois_drop_cover = numpy.random.poisson(self.param_lamda_cover_drop / 1, int(self.sim_duration / 60000))
        pois_mix_loop_cover = numpy.random.poisson(self.param_lamda_cover_mix / 1, int(self.sim_duration / 60000))

        print('LAMDA')
        print(pois_sending_message)
        print('LOOP COVER')
        print(pois_loop_cover)
        print('DROP COVER')
        print(pois_drop_cover)
        print('MIX COVER')
        print(pois_mix_loop_cover)

        possible_sender = []
        for i in range(self.nbr_user + 1):
            if i > 0:
                possible_sender.append(i)

        mixes = []
        for i in range(len(self.mix_network.mixes)):
            for q in range(len(self.mix_network.mixes[i])):
                mixes.append(self.mix_network.mixes[i][q].address)

        for i in range(len(pois_sending_message)):
            # normal messages to be sent
            messages_to_send = pois_sending_message[i]
            if messages_to_send != 0:
                for q in range(messages_to_send):
                    sender_ret = self.get_random_sender(possible_sender)
                    sender = sender_ret[0]
                    possible_sender = sender_ret[1]
                    if sender is not None:
                        self.init_message(i * 60000, 'U' + str(sender), 'U' + str(self.get_random_recipient(sender)), False)

            # loop cover messages to be sent
            loop_cover_to_send = pois_loop_cover[i]
            if loop_cover_to_send != 0:
                for q in range(loop_cover_to_send):
                    sender_ret = self.get_random_sender(possible_sender)
                    sender = sender_ret[0]
                    possible_sender = sender_ret[1]
                    if sender is not None:
                        self.init_message(i * 60000, 'U' + str(sender), 'U' + str(sender), True)

            # drop cover messages to be sent
            drop_cover_to_send = pois_drop_cover[i]
            if drop_cover_to_send != 0:
                for q in range(drop_cover_to_send):
                    sender_ret = self.get_random_sender(possible_sender)
                    sender = sender_ret[0]
                    possible_sender = sender_ret[1]
                    if sender is not None:
                        self.init_drop_cover(i * 60000, 'U' + str(sender))

            # mix loop cover messages to be sent
            mix_loop_cover_to_send = pois_mix_loop_cover[i]
            if mix_loop_cover_to_send != 0:
                for q in range(mix_loop_cover_to_send):
                    mix_sender_ret = self.get_random_sender(mixes)
                    mix_sender = mix_sender_ret[0]
                    possible_mixes = mix_sender_ret[1]
                    if mix_sender is not None:
                        self.init_mix_loop(i * 60000, mix_sender)

            possible_sender = []
            for q in range(self.nbr_user + 1):
                if q > 0:
                    possible_sender.append(q)

            mixes = []
            for p in range(len(self.mix_network.mixes)):
                for q in range(len(self.mix_network.mixes[p])):
                    mixes.append(self.mix_network.mixes[p][q].address)

        self.write_message_file(self.message_storage)
        return self.message_storage

    def get_random_route(self):
        # method that returns a random route array for the message to be created
        # print('MessageGenerator: get_random_route')
        route = []
        for layer in range(len(self.mix_network.mixes)):
            tmp = random.choice(self.mix_network.mixes[layer])
            route.append(tmp.address)
        return route

    def init_message(self, sim_timestamp, user_id, recipient, cover_bool):
        # method that creates a message for the simulation at a given timestamp
        # print('MessageGenerator: init_message')
        letters = string.ascii_lowercase
        payload = ''.join(random.choice(letters) for i in range(10))
        mu = [self.param_mu] * len(self.mix_network.mixes)
        m = Message.Message(user_id, recipient, payload, self.message_unique_id, self.get_random_route(), mu, sim_timestamp, cover_bool, self.crypto_delay)
        self.message_unique_id += 1
        self.message_storage.append(m)

    def init_message_w_route(self, sim_timestamp, user_id, recipient, cover_bool, route):
        # method that creates a message for the simulation at a given timestamp
        # print('MessageGenerator: init_message')
        letters = string.ascii_lowercase
        payload = ''.join(random.choice(letters) for i in range(10))
        mu = [self.param_mu] * len(self.mix_network.mixes)
        m = Message.Message(user_id, recipient, payload, self.message_unique_id, route, mu, sim_timestamp, cover_bool, self.crypto_delay)
        self.message_unique_id += 1
        self.message_storage.append(m)

    def get_random_recipient(self, user):
        # method that returns a random recipient for a given user
        # print('MessageGenerator: get_random_recipient')
        return random.choice(self.user_profile_array[user - 1])

    @staticmethod
    def get_random_sender(possible_senders):
        # method that returns a random sender and an array with the un-chosen senders
        # print('MessageGenerator: get_random_sender')
        tmp = possible_senders
        if len(tmp) > 0:
            choice = random.choice(tmp)
            tmp.remove(choice)
        else:
            choice = None
        return [choice, tmp]

    def init_drop_cover(self, sim_timestamp, user_id):
        # method that creates a drop cover message for a given user
        # print('MessageGenerator: init_drop_cover')
        random_route = self.get_random_route()
        random_layer = numpy.random.randint(1, len(random_route))
        drop_route = []
        for i in range(random_layer):
            drop_route.append(random_route[i])

        recipient = drop_route[len(drop_route) - 1]

        self.init_message_w_route(sim_timestamp, user_id, recipient, True, drop_route)

    def init_mix_loop(self, sim_timestamp, mix_addr):
        # method that creates mix loop cover message
        # print('MessageGenerator: init_mix_loop')
        nbr_layers = len(self.mix_network.mixes)
        layer = None
        for i in range(len(self.mix_network.mixes)):
            for mix in self.mix_network.mixes[i]:
                if mix.address == mix_addr:
                    layer = i # um das layer herauszufinden in dem sich der mix befindet

        # falls mix nicht gefunden wird ist layer=none -> muss abgefangen werden, da sonst fehler (aber die nachricht braucht ja eine route) -> evtl einfach dann garkeine anchricht senden
        if layer is not None:
            route = []
            itr = 1
            while len(route) != nbr_layers:  #solange bis ganze route gebaut wurde
                if (layer + itr) == nbr_layers:
                    itr -= nbr_layers
                if itr != 0:
                    route.append(random.choice(self.mix_network.mixes[layer + itr]).address) # fügt immer eine random adresse hinzu von der nächsten schicht
                else:
                    route.append(mix_addr) # wenn itr = 0 wird das eigentliche layer des mixes betrachtet (letzter schritt) -> muss adresse des mixes beinhalten

                itr += 1

            self.init_message_w_route(sim_timestamp, mix_addr, mix_addr, True, route)

    def write_message_file(self, messages):
        # method that wirtes every messages from the simulation run into a separate file
        print('MessageGenerator: write_message_file')
        f = open("messages/messages_sim.csv", "w")
        f.write('message_id,sender,recipient,payload,ingress_provider_sending_time,route,delays,valid_intervals,cover_bool' + '\n')
        for m in messages:
            f.write(str(m.message_id) + ',' + str(m.real_sender) + ',' + str(m.recipient) + ',' + str(m.payload) + ',' + str(m.ingress_provider_sending_time) + ',' + str(m.route).replace(',', ';') + ',' + str(m.delays).replace(',', ';') + ',' + str(m.valid_intervals).replace(',', ';') + ',' + str(m.cover_traffic) + '\n')
        f.close()

        f2 = open("messages/user_profiles.csv", "w")
        f2.write(
            'sender_id,recipients' + '\n')
        for i in range(len(self.user_profile_array)):
            f2.write(str(i + 1) + ',' + str(self.user_profile_array[i]).replace(',', ';') + '\n')
        f2.close()










