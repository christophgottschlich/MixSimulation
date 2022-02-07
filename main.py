# general imports
import simpy

# self defined classes
import Analytics
import ExgressProvider
import IngressProvider
import MixNetwork
import PoissonMix
import Simulation
import MessageGenerator
from Simulation import SIMLOGGER
from tkinter import *

root = Tk()

# Parameters for standard simulation run
st_DURATION_SIMULATION = 250000  # Milliseconds
st_NBR_USERS = 100
st_LAYER = [3, 3, 3]
st_PARAM_LAMDA = 35
st_PARAM_LAMDA_LOOP_COVER = 15
st_PARAM_LAMDA_DROP_COVER = 15
st_PARAM_LAMDA_MIX_COVER = 5
st_PARAM_MU = 5000
st_CRYPTO_DELAY = 500
st_USER_PROFILE = 5

# UI
# HEADER =======================================================================
label_titel = Label(root, text="Stop and Go Mix - Simulator")
label_titel.grid(row=0, column=1)
label_titel.config(font=("Arial", 25))
label_free_row = Label(root, text="  ")
label_free_row.grid(row=1, column=0)
label_standard_header = Label(root, text="Standard Values:")
label_standard_header.grid(row=2, column=2)


# Parameter Mu==================================================================
label_mu = Label(root, text="Parameter Mu")
e_mu = Entry(root, width=25)
label_mu.grid(row=3, column=0)
e_mu.grid(row=3, column=1)
label_mu_stand = Label(root, text=st_PARAM_MU)
label_mu_stand.grid(row=3, column=2)

# Parameter Parameter Lamda===================================================
label_lamda = Label(root, text="Parameter Lamda")
e_lamda = Entry(root, width=25)
label_lamda.grid(row=4, column=0)
e_lamda.grid(row=4, column=1)
label_lamda_stand = Label(root, text=st_PARAM_LAMDA)
label_lamda_stand.grid(row=4, column=2)

# Parameter number of Layers===================================================
label_layer_count = Label(root, text="Anzahl der Layers und Mixe (Format: [1, 2, 1])")
e_layer_count = Entry(root, width=25)
label_layer_count.grid(row=5, column=0)
e_layer_count.grid(row=5, column=1)
str_layers = str(st_LAYER)
label_layers_stand = Label(root, text=str_layers)
label_layers_stand.grid(row=5, column=2)

# Parameter Loop Cover===========================================
label_loop_cover = Label(root, text="Parameter Lamda Loop Cover")
e_loop_cover = Entry(root, width=25)
label_loop_cover.grid(row=6, column=0)
e_loop_cover.grid(row=6, column=1)
label_loop_cover_stand = Label(root, text=st_PARAM_LAMDA_LOOP_COVER)
label_loop_cover_stand.grid(row=6, column=2)

# Parameter Drop Cover===========================================
label_drop_cover = Label(root, text="Parameter Lamda Drop Cover")
e_drop_cover = Entry(root, width=25)
label_drop_cover.grid(row=7, column=0)
e_drop_cover.grid(row=7, column=1)
label_drop_cover_stand = Label(root, text=st_PARAM_LAMDA_DROP_COVER)
label_drop_cover_stand.grid(row=7, column=2)

# Parameter Mix Cover===========================================
label_mix_cover = Label(root, text="Parameter Lamda Mix Cover")
e_mix_cover = Entry(root, width=25)
label_mix_cover.grid(row=8, column=0)
e_mix_cover.grid(row=8, column=1)
label_mix_cover_stand = Label(root, text=st_PARAM_LAMDA_MIX_COVER)
label_mix_cover_stand.grid(row=8, column=2)

# Parameter Crypto Delay===========================================
label_crypto_delay = Label(root, text="Parameter Crypto Delay")
e_crypto_delay = Entry(root, width=25)
label_crypto_delay.grid(row=9, column=0)
e_crypto_delay.grid(row=9, column=1)
label_crypto_stand = Label(root, text=st_CRYPTO_DELAY)
label_crypto_stand.grid(row=9, column=2)

# Parameter Number of Users ==================================================
label_number_users = Label(root, text="Number Users")
e_number_users = Entry(root, width=25)
label_number_users.grid(row=10, column=0)
e_number_users.grid(row=10, column=1)
label_number_users_stand = Label(root, text=st_NBR_USERS)
label_number_users_stand.grid(row=10, column=2)

# Parameter User Profile =======================================================
label_user_profile = Label(root, text="User Profile")
e_user_profile = Entry(root, width=25)
label_user_profile.grid(row=11, column=0)
e_user_profile.grid(row=11, column=1)
label_user_profile_stand = Label(root, text=st_USER_PROFILE)
label_user_profile_stand.grid(row=11, column=2)

# Parameter Simulation duration================================================
label_dur_simulation = Label(root, text="Duration of Simulation (in ms)")
e_dur_simulation = Entry(root, width=25)
label_dur_simulation.grid(row=12, column=0)
e_dur_simulation.grid(row=12, column=1)
label_dur_simulation_stand = Label(root, text=st_DURATION_SIMULATION)
label_dur_simulation_stand.grid(row=12, column=2)

# Hitting Set Analytics===============================================
label_space2 = Label(root, text="")
label_space2.grid(row=200, column=1)
label_hitting_set_analytics = Label(root, text="Hitting Set Analytics")
label_hitting_set_analytics.grid(row=201, column=0)
label_hitting_set_analytics.config(font=("Arial", 22))
label_number_messages = Label(root, text="Number of Messages")  # Calculate HS for this amount of messages
label_number_messages.grid(row=202, column=0)
e_number_messages = Entry(root, width=25)  # Calculate HS for this amount of messages
e_number_messages.grid(row=202, column=1)

label_window_start = Label(root, text="Time Window Start (in ms)")  # Calculate HS for this amount of messages
label_window_start.grid(row=203, column=0)
e_window_start = Entry(root, width=25)  # Calculate HS for this amount of messages
e_window_start.grid(row=203, column=1)

label_window_end = Label(root, text="Time Window End (in ms)")  # Calculate HS for this amount of messages
label_window_end.grid(row=204, column=0)
e_window_end = Entry(root, width=25)  # Calculate HS for this amount of messages
e_window_end.grid(row=204, column=1)


def simulate(simulation):
    while True:
        simulation.perform_step()


def get_analytics():
    # show message and mix analytics on UI
    anal = Analytics.Analytics("messages/messages_sim.csv", 
                               "activities/activity_log.csv", 
                               "activities/mix_status_log.csv", 
                               "messages/user_profiles.csv")
    
    message_analytics = anal.analyze_messages()
    action_analytics = anal.analyze_actions()
    mix_pool_analytics = anal.analyze_mix_status()

    label_analytics = Label(root, text="Analyse:")
    label_analytics.grid(row=100, column=1)
    label_analytics.config(font=("Arial", 18))
    label_message_analytics = Label(root, text=message_analytics)
    label_message_analytics.grid(row=101, column=1)
    label_action_analytics = Label(root, text=action_analytics)
    label_action_analytics.grid(row=102, column=1)
    label_mix_pool_analytics = Label(root, text=mix_pool_analytics)
    label_mix_pool_analytics.grid(row=103, column=1)

    print(anal.get_user_profile_data())


def calculate_hitting_set_click():
    # calculate and show hitting_set_analytics on UI
    anal = Analytics.Analytics("messages/messages_sim.csv", 
                               "activities/activity_log.csv",
                               "activities/mix_status_log.csv", 
                               "messages/user_profiles.csv")
    
    param_hs_start = int(e_window_start.get())
    param_hs_end = int(e_window_end.get())
    param_hs_number_msg = int(e_number_messages.get())

    hittingsets = anal.get_multiple_hitting_sets(param_hs_number_msg, param_hs_start, param_hs_end)


    # reset to not see any previous values that exceed the current values regarding horizontal space
    label_analytics_hittingset = Label(root, text="")
    label_analytics_hittingset.grid(row=210, column=1)
    label_analytics_hittingset = Label(root, text=hittingsets)
    label_analytics_hittingset.grid(row=210, column=1)


def start_simulation_click():
    # run personalized simulation
    duration_simulation = st_DURATION_SIMULATION  # Milliseconds
    nbr_users = st_NBR_USERS
    layer = st_LAYER  # LAYER.length = number of layers + LAYER[i] = mix nodes in particular layer
    param_lamda = st_PARAM_LAMDA  # arrival rate
    param_lamda_loop_cover = st_PARAM_LAMDA_LOOP_COVER
    param_lamda_drop_cover = st_PARAM_LAMDA_DROP_COVER
    param_lamda_mix_cover = st_PARAM_LAMDA_MIX_COVER
    param_mu = st_PARAM_MU  # serving time
    crypto_delay = st_CRYPTO_DELAY
    user_profile = st_USER_PROFILE
    
    #      /[ [1-9]* (,[1-9]*)? /]
    if e_mu.get() != "":
        param_mu = int(e_mu.get())
    if e_lamda.get() != "":
        param_lamda = int(e_lamda.get())
    if e_layer_count.get() != "":
        print(len(e_layer_count.get())-1)
        if e_layer_count.get()[0] == "[" and e_layer_count.get()[len(e_layer_count.get())-1] == "]":
            layer = e_layer_count.get()
    if e_loop_cover.get() != "":
        param_lamda_loop_cover = int(e_loop_cover.get())
    if e_drop_cover.get() != "":
        param_lamda_drop_cover = int(e_drop_cover.get())
    if e_mix_cover.get() != "":
        param_lamda_mix_cover = int(e_mix_cover.get())
    if e_crypto_delay.get() != "":
        crypto_delay = int(e_crypto_delay.get())
    if e_number_users.get() != "":
        nbr_users = int(e_number_users.get())
    if e_user_profile.get() != "":
        user_profile = int(e_user_profile.get())
    if e_dur_simulation.get() != "":
        duration_simulation = int(e_dur_simulation.get())

    print("Click",
          param_mu,
          param_lamda,
          layer,
          param_lamda_loop_cover,
          param_lamda_drop_cover,
          param_lamda_mix_cover,
          crypto_delay,
          nbr_users,
          user_profile,
          duration_simulation)
    
    print('\nSETUP ***************************************************************************************************')
    env = simpy.Environment()

    in_prov = IngressProvider.IngressProvider(env, 'IP1')
    ex_prov = ExgressProvider.ExgressProvider(env, 'EP1')

    iter_mixes = 1
    mixes = []
    # string operations to get the wanted data formatr
    if isinstance(layer, str):
        layer = layer.replace('[', '').replace(']', '').replace(' ', '')
        layer = layer.split(',')

    # create the needed mix network based on the inputs
    for i in range(len(layer)):
        tmp_layer = []
        for q in range(int(layer[i])):
            tmp_layer.append(PoissonMix.PoissonMix(env, 'M' + str(iter_mixes)))
            iter_mixes += 1
        mixes.append(tmp_layer)

    mix_network = MixNetwork.MixNetwork(env, 1, mixes, in_prov, ex_prov)

    mg = MessageGenerator.MessageGenerator(param_mu,
                                           param_lamda,
                                           param_lamda_loop_cover,
                                           param_lamda_drop_cover,
                                           param_lamda_mix_cover,
                                           duration_simulation,
                                           mix_network,
                                           nbr_users,
                                           user_profile,
                                           crypto_delay)

    mix_network.ingress_provider.fill_message_storage(mg.create_messages())
    simulation = Simulation.Simulation(env, mix_network)
    env.process(simulation.perform_step())

    print('\nSIMULATION **********************************************************************************************')
    env.run(until=duration_simulation)

    print(simulation.mix_network.exgress_provider)
    print('Simulation completed')
    SIMLOGGER.mix_status_to_csv(mix_network)
    get_analytics()


def start_standard_simulation_click():
    # run standard simulation
    duration_simulation = st_DURATION_SIMULATION  # Milliseconds
    nbr_users = st_NBR_USERS
    layer = st_LAYER  # LAYER.length = number of layers + LAYER[i] = mix nodes in particular layer
    param_lamda = st_PARAM_LAMDA  # arrival rate
    param_lamda_loop_cover = st_PARAM_LAMDA_LOOP_COVER
    param_lamda_drop_cover = st_PARAM_LAMDA_DROP_COVER
    param_lamda_mix_cover = st_PARAM_LAMDA_MIX_COVER
    param_mu = st_PARAM_MU  # serving time
    crypto_delay = st_CRYPTO_DELAY
    user_profile = st_USER_PROFILE

    print("Click",
          param_mu,
          param_lamda,
          layer,
          param_lamda_loop_cover,
          param_lamda_drop_cover,
          param_lamda_mix_cover,
          crypto_delay,
          nbr_users,
          duration_simulation)

    print('\nSETUP ***************************************************************************************************')
    env = simpy.Environment()
    in_prov = IngressProvider.IngressProvider(env, 'IP1')
    ex_prov = ExgressProvider.ExgressProvider(env, 'EP1')

    iter_mixes = 1
    mixes = []
    # create mix network based on the standard values
    for i in range(len(layer)):
        tmp_layer = []
        for q in range(int(layer[i])):
            tmp_layer.append(PoissonMix.PoissonMix(env, 'M' + str(iter_mixes)))
            iter_mixes += 1
        mixes.append(tmp_layer)

    mix_network = MixNetwork.MixNetwork(env, 1, mixes, in_prov, ex_prov)
    mg = MessageGenerator.MessageGenerator(param_mu,
                                           param_lamda,
                                           param_lamda_loop_cover,
                                           param_lamda_drop_cover,
                                           param_lamda_mix_cover,
                                           duration_simulation,
                                           mix_network,
                                           nbr_users,
                                           user_profile,
                                           crypto_delay)

    mix_network.ingress_provider.fill_message_storage(mg.create_messages())
    simulation = Simulation.Simulation(env, mix_network)
    env.process(simulation.perform_step())

    print('\nSIMULATION **********************************************************************************************')
    env.run(until=duration_simulation)

    print(simulation.mix_network.exgress_provider)
    print('Simulation completed')

    SIMLOGGER.mix_status_to_csv(mix_network)

    get_analytics()


# Start Simulation Buttons =============================================================================================
enter_button = Button(root, text="Start Simulation", command=start_simulation_click)
enter_button.grid(row=20, column=1)
standard_simulation_button = Button(root, text="Start Standard Simulation", command=start_standard_simulation_click)
standard_simulation_button.grid(row=20, column=2)

label_space = Label(root, text="")
label_space.grid(row=21, column=1)

# Hitting Set Analytics Button
standard_simulation_button = Button(root, text="Calculate Hitting Set", command=calculate_hitting_set_click)
standard_simulation_button.grid(row=205, column=1)

root.mainloop()
