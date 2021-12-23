from datetime import datetime


class Logger:
    def __init__(self):
        self.timestamp = datetime.now().timestamp()
        self.mix_status = []
        with open("activities/activity_log.csv", "w") as file1:
            file1.write('timestamp,issuer,action,message,destination' + "\n")
        file1.close()

        with open("activities/mix_status_log.csv", "w") as file2:
            file2.write('mix,mean_messages_in_pool' + "\n")
        file2.close()

    def log(self, txt):
        # method that writes a log file
        with open("logs/simulation_run_" + str(self.timestamp) + ".txt", "a") as file3:
            file3.write(txt + "\n")
        file3.close()

    @staticmethod
    def action_to_csv(timestamp, issuer, action, message, destination):
        # method that writes a log file
        with open("activities/activity_log.csv", "a") as file4:
            file4.write(timestamp + ',' + issuer + ',' + action + ',' + message + ',' + destination + "\n")
        file4.close()

    @staticmethod
    def mix_status_to_csv(network):
        with open("activities/mix_status_log.csv", "a") as file5:
            for layer in range(len(network.mixes)):
                for mix in network.mixes[layer]:
                    mean = mix.message_mean[0] / mix.message_mean[1]
                    file5.write(mix.address + ',' + str(mean) + "\n")
        file5.close()
