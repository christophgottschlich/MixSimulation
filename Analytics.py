import csv
import numpy as np
from numpy import ndarray

from Simulation import SIMLOGGER


class Analytics:
    def __init__(self, message_file, actions_file, mix_status_file, user_profile_file):
        self.message_file = message_file,
        self.actions_file = actions_file,
        self.mix_status_file = mix_status_file,
        self.user_profile_file = user_profile_file,

    def analyze_messages(self):
        # method for analyzing the messages of the simulation run
        # print('Analytics: analyze_messages')
        message_data = self.get_message_data()

        real_messages = 0
        cover_messages = 0
        user_loop_cover = 0
        user_drop_cover = 0
        mix_loop_cover = 0
        for m in message_data:
            if m['cover_bool'] == 'False':
                real_messages += 1
            else:
                cover_messages += 1
                if m['sender'] == m['recipient']:
                    if m['sender'].startswith('U'):
                        user_loop_cover += 1
                    else:
                        mix_loop_cover += 1
                else:
                    user_drop_cover += 1

        mean_duration_messages = self.analyze_message_duration()

        re = 'Message Analytics \n'+'--TOTAL NBR MESSAGES: ' + str(len(message_data)) + '\n' \
            + '--real_messages: ' + str(real_messages) + '\n' \
                + '--mean_duration_valid_messages (Seconds): ' + str(mean_duration_messages / 1000) + '\n' \
                    + '--cover_messages: ' + str(cover_messages) + '\n' \
                        + '--user_loop_cover: ' + str(user_loop_cover) + '\n' \
                            + '--user_drop_cover: ' + str(user_drop_cover) + '\n' \
                                + '--mix_loop_cover: ' + str(mix_loop_cover)
        return re
    
    def analyze_users(self, max_users):
        message_data = self.get_message_data()
        sender_message_count = np.zeros((max_users+1,), dtype=int)
        for m in message_data:
            if m['sender'].startswith('U'):
                sender = int(m['sender'][1 : : ])
                sender_message_count[sender] += 1
        return sender_message_count

    def analyze_actions(self):
        # method for analyzing the actions performed during the simulation run
        # print('Analytics: analyze_actions')
        action_data = self.get_action_data()

        accepting = 0
        rejecting = 0
        for a in action_data:
            if a['action'] == 'accept':
                accepting += 1
            elif a['action'] == 'reject':
                rejecting += 1

        re = ''
        if accepting != 0:
            re = 'Action Analytics \n' + '--accepting_actions: ' + str(accepting) + '\n' \
                + '--rejecting_actions: ' + str(rejecting) + '\n' \
                    + '--rej/acc: ' + str(rejecting / accepting)
        
        return re

    def get_message_data(self):
        # method that returns an array of dictionaries based on the message file
        # print('Analytics: get_message_data')
        message_data = []

        with open(self.message_file[0], 'r') as file1:
            csv_file = csv.DictReader(file1)
            for row in csv_file:
                message_data.append(dict(row))
        file1.close()
        return message_data

    def get_mix_status_data(self):
        # method that returns an array of dictionaries based on the mix_status file
        # print('Analytics: get_mix_status_data')
        mix_status_data = []

        with open(self.mix_status_file[0], 'r') as file2:
            csv_file = csv.DictReader(file2)
            for row in csv_file:
                mix_status_data.append(dict(row))
        file2.close()
        return mix_status_data

    def get_user_profile_data(self):
        # method that returns an array of dictionaries based on the user_profiles file
        # print('Analytics: get_user_profile_data')
        user_profile_data = []

        with open(self.user_profile_file[0], 'r') as file3:
            csv_file = csv.DictReader(file3)
            for row in csv_file:
                user_profile_data.append(dict(row))
        file3.close()
        return user_profile_data

    def get_action_data(self):
        # method that returns an array of dictionaries based on the action file
        # print('Analytics: get_action_data')
        action_data = []
        print(self.actions_file)
        with open(self.actions_file[0], 'r') as file4:
            csv_file = csv.DictReader(file4)
            for row in csv_file:
                action_data.append(dict(row))
        file4.close()
        return action_data

    # returns path of a given message
    def get_path_of_message(self, message_id):
        data = self.get_action_data()
        specific_message_log = []
        for i in range(0, len(data)):
            if int(data[i]['message']) == int(message_id):
                specific_message_log.append(data[i])
        return specific_message_log

    # returns array with all messages involving given user
    def get_messages_from_user(self, user):
        data = self.get_action_data()
        user_log = []
        for i in range(0, len(data)):
            if str(data[i]['issuer']) == user:
                user_log.append(data[i])
        return user_log

    def get_messages_from_user_at_time(self, user, start_time, end_time):
        data = self.get_action_data()
        user_log = []
        for i in range(0, len(data)):
            if str(data[i]['issuer']) == user and start_time <= int(data[i]['timestamp']) <= end_time:
                user_log.append(data[i])
        return user_log

    # returns hitting_set of a given message with given time window
    def get_hitting_set_from_message_path(self, message_id, time_window_start, time_window_end): #betrachte alle Nachrichten, die 20 bis 40ms nach erhalt der Nachricht weitergeschickt wurden => time_window_start = 20, time_window_end = 40
        message_path = self.get_path_of_message(message_id)
        hs = []

        # delete received/accepted entries
        for i in range(0, len(message_path)):
            if message_path[i]['destination'] == 'None':
                message_path.pop(i)
        #print(message_path)

        x = [message_path[0]]
        while len(x) > 0:
            time = int(x[0]['timestamp'])
            issuer = x[0]['issuer']
            receiver = x[0]['destination']
            messages_receiver = self.get_messages_from_user_at_time(receiver, time + time_window_start,
                                                                    time + time_window_end)
            if len(messages_receiver) > 0:
                x.append(messages_receiver)
                x.pop(0)
            else:
                hs.append(issuer)
        return hs

    def analyze_mix_status(self):
        # method for analyzing the mean of messages stored in the mix nodes during simulation
        print('Analytics: analyze_mix_status')
        mix_message_data = self.get_mix_status_data()
        ret_separate = mix_message_data
        ret_mean = 0
        ret_mean_cover = 0
        ret_mean_empty_pool = 0
        for mix in mix_message_data:
            ret_mean += float(mix['mean_messages_in_pool'])
            ret_mean_cover += float(mix['mean_cover_messages_in_pool'])
            ret_mean_empty_pool += float(mix['empty_pool_mean'])
        ret_mean = ret_mean / len(mix_message_data)
        ret_mean_cover = ret_mean_cover / len(mix_message_data)
        ret_mean_empty_pool = ret_mean_empty_pool / len(mix_message_data)

        re = 'Action Analytics \n' + '--mean_messages_in_mix: ' + str(ret_mean) + '\n' + '--mean_cover_messages_in_mix: ' + str(ret_mean_cover) + '\n' + '--mean_empty_pool_mix (percentage of Simulation-time): ' + str(ret_mean_empty_pool * 100)

        return re

    def analyze_message_duration(self):
        # method that calculates the mean duration that valid messages need till arrival
        # print('Analytics: analyze_message_duration')

        message_data = self.get_message_data()
        valid_messages = []

        for m in message_data:
            if m['cover_bool'] == 'False':
                valid_messages.append(m)

        action_data = self.get_action_data()
        ep_receive_actions = []

        for a in action_data:
            if a['issuer'] == 'EP1' and a['action'] == 'receive':
                ep_receive_actions.append(a)

        tmp_count = 0
        tmp_duration = 0

        for m in valid_messages:
            for a in ep_receive_actions:
                if m['message_id'] == a['message']:
                    tmp_count += 1
                    tmp_duration += int(a['timestamp']) - int(m['ingress_provider_sending_time'])

        ret_mean = tmp_duration / tmp_count

        return ret_mean
