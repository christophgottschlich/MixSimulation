from datetime import datetime


class Logger:
    def __init__(self):
        self.timestamp = datetime.now().timestamp()
        self.mix_status = []

        # in the beginning the files are deleted
        self.reset_files()

    def log(self, txt):
        # method that writes a log file
        with open("logs/simulation_run_" + str(self.timestamp) + ".txt", "a") as file3:
            file3.write(txt + "\n")
        file3.close()

    @staticmethod
    def action_to_csv(timestamp, issuer, action, message, destination):
        # method that writes a log file for all actions performed in the simulation
        with open("activities/activity_log.csv", "a") as file4:
            file4.write(timestamp + ',' + issuer + ',' + action + ',' + message + ',' + destination + "\n")
        file4.close()

    @staticmethod
    def mix_status_to_csv(network):
        # method that writes a file with the status data of the mixes
        with open("activities/mix_status_log.csv", "a") as file5:
            for layer in range(len(network.mixes)):
                for mix in network.mixes[layer]:
                    mean = mix.message_mean[0] / mix.message_mean[1]
                    mean_not_empty = mix.message_mean[0] / (mix.message_mean[1] - mix.empty_pool[0])
                    cover_mean = mix.cover_message_mean[0] / mix.cover_message_mean[1]
                    empty_pool = mix.empty_pool[0] / mix.empty_pool[1]
                    file5.write(mix.address + ',' + str(mean)
                                + ',' + str(cover_mean)
                                + ',' + str(empty_pool)
                                + ',' + str(mean_not_empty)
                                + "\n")
        file5.close()

    @staticmethod
    def reset_files():
        # method that deletes the log files for a new simulation run
        with open("activities/activity_log.csv", "w") as file1:
            file1.write('timestamp,issuer,action,message,destination' + "\n")
        file1.close()

        with open("activities/mix_status_log.csv", "w") as file2:
            file2.write('mix,mean_messages_in_pool,mean_cover_messages_in_pool,empty_pool_mean,mean_pool_not_empty' + "\n")
        file2.close()
