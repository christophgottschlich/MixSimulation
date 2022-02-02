class MixNetwork(object):
    def __init__(self, env, layer, mixes, ingress_provider, exgress_provider):
        self.env = env
        self.layer = layer
        self.mixes = mixes
        self.ingress_provider = ingress_provider
        self.exgress_provider = exgress_provider

    def __str__(self):
        return "({0},{1},{2},{3})".format(self.layer, self.mixes, self.ingress_provider, self.exgress_provider)

    def get_mix_by_address(self, addr):
        # method that returns the mix with the given address
        # print('MixNetwork: get_mix_by_address')
        for i in range(len(self.mixes)):
            for mix in self.mixes[i]:
                if mix.address == addr:
                    return mix

    def get_layer(self, index_of_layer):
        # method that returns the array of mixes from a given layer
        # print('MixNetwork: get_layer')
        return self.mixes[index_of_layer]

    def set_layer(self, index_of_layer, mixes):
        # method that initializes a layer with an array of mixes
        # print('MixNetwork: set_layer')
        self.mixes[index_of_layer] = mixes

    def mix_in_last_layer(self, mix):
        # method that returns boolean value with true when the mix is in the last layer of the network
        # print('MixNetwork: mix_in_last_layer')
        for last_layer_mix in self.mixes[len(self.mixes) - 1]:
            if last_layer_mix.address == mix.address:
                return True
        return False

    def handle_messages(self, messages_to_handle):
        # method that sends messages to the dedicated mix nodes
        # print('MixNetwork: handle_messages')

        for message in messages_to_handle:
            if message[1] != 'EP':  # if the message should be handed to another mix
                destination_mix = self.get_mix_by_address(message[1])
                destination_mix.receive_message(message[0])
            else:
                self.exgress_provider.receive_message(message[0])

    def check_network(self):
        # method that checks the whole network and performs sending, receiving etc
        # print('MixNetwork: check_network')

        # check ingressProvider to inject messages into the network
        incoming_messages = self.ingress_provider.check_messages()
        if len(incoming_messages) > 0:
            if len(incoming_messages[0]) > 0:
                self.handle_messages(incoming_messages)

        # check the whole mix_network if any mixes have to send messages
        messages_to_handle = []
        for layer in range(len(self.mixes)):
            for mix in self.mixes[layer]:
                inc = mix.check_messages()
                if len(inc) > 0:
                    messages_to_handle += inc

        if len(messages_to_handle) > 0:
            if len(messages_to_handle[0]) > 0:
                self.handle_messages(messages_to_handle)
