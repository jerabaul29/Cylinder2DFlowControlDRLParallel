from threading import Thread
from tensorforce import TensorforceError
from tensorforce.environments import Environment
import socket
from echo_server import EchoServer
import time


class RemoteEnvironmentClient(Environment):
    """Used to communicate with a RemoteEnvironmentServer. The idea is that the pair
    (RemoteEnvironmentClient, RemoteEnvironmentServer) allows to transmit information
    through a socket seamlessly.

    The RemoteEnvironmentClient can be directly given to the Runner.

    The RemoteEnvironmentServer herits from a valid Environment add adds the socketing.
    """

    def __init__(self,
                 example_environment,
                 port=12230,
                 host=None,
                 verbose=1,
                 buffer_size=262144,
                 timing_print=False,
                 ):
        """(port, host) is the necessary info for connecting to the Server socket.
        """

        # templated tensorforce stuff
        self.observation = None
        self.thread = None

        self.buffer_size = buffer_size

        self.timing_print = timing_print

        # make arguments available to the class
        # socket
        self.port = port
        self.host = host
        # misc
        self.verbose = verbose
        # states and actions
        self.example_environment = example_environment

        # start the socket
        self.valid_socket = False
        self.socket = socket.socket()
        # if necessary, use the local host
        if self.host is None:
            self.host = socket.gethostname()
        # connect to the socket
        self.socket.connect((self.host, self.port))
        if self.verbose > 0:
            print('Connected to {}:{}'.format(self.host, self.port))
        # now the socket is ok
        self.valid_socket = True

        self.episode = 0
        self.step = 0

        self.time_start = 0
        self.crrt_time = 0
        self.armed_time_measurement = False
        self.start_function = 0
        self.end_function = 0
        self.crrt_time_function = 0
        self.total_function_time = 0
        self.proportion_env_time = 0

    def states(self):
        return self.example_environment.states()

    def actions(self):
        return self.example_environment.actions()

    def max_episode_timesteps(self):
        return self.example_environment.max_episode_timesteps()

    def close(self):
        # TODO: think about sending a killing message to the server? Maybe not necessary - can reuse the
        # server maybe - but may be needed if want to clean after us.
        if self.valid_socket:
            self.socket.close()

    def reset(self):
        self.update_time_function_start()

        # perform the reset
        _ = self.communicate_socket("RESET", 1)

        # get the state
        _, init_state = self.communicate_socket("STATE", 1)

        # Updating episode and step numbers
        self.episode += 1
        self.step = 0

        if self.verbose > 1:
            print("reset done; init_state:")
            print(init_state)

        self.update_time_function_end()

        self.print_time_information()

        return(init_state)

    def update_time_function_start(self):
        if self.armed_time_measurement:
            self.start_function = time.time()

    def update_time_function_end(self):
        if self.armed_time_measurement:
            self.end_function = time.time()
            self.crrt_time_function = self.end_function - self.start_function
            self.start_function = None
            self.total_function_time += self.crrt_time_function

    def arm_time_measurements(self):
        if not self.armed_time_measurement:
            self.armed_time_measurement = True
            if self.timing_print:
                print("arming time measurements...")
            self.time_start = time.time()

    def print_time_information(self):
        if self.timing_print and self.armed_time_measurement:
            print("summary timing measurements...")
            self.total_time_since_arming = time.time() - self.time_start
            print("total time since arming: {}".format(self.total_time_since_arming))
            print("total time in env functions: {}".format(self.total_function_time))
            print("proportion in env functions: {}".format(float(self.total_function_time) / float(self.total_time_since_arming)))

    def execute(self, actions):
        # arm the time measurements the first time execute is hit
        self.arm_time_measurements()

        self.update_time_function_start()

        # send the control message
        self.communicate_socket("CONTROL", actions)

        # ask to evolve
        self.communicate_socket("EVOLVE", 1)

        # obtain the next state
        _, next_state = self.communicate_socket("STATE", 1)

        # check if terminal
        _, terminal = self.communicate_socket("TERMINAL", 1)

        # get the reward
        _, reward = self.communicate_socket("REWARD", 1)

        # now we have done one more step
        self.step += 1

        if self.verbose > 1:
            print("execute performed; state, terminal, reward:")
            print(next_state)
            print(terminal)
            print(reward)

        self.update_time_function_end()

        return (next_state, terminal, reward)

    def communicate_socket(self, request, data):
        """Send a request through the socket, and wait for the answer message.
        """

        to_send = EchoServer.encode_message(request, data, verbose=self.verbose)
        self.socket.send(to_send)

        # TODO: the recv argument gives the max size of the buffer, can be a source of missouts if
        # a message is larger than this; add some checks to verify that no overflow
        received_msg = self.socket.recv(self.buffer_size)

        request, data = EchoServer.decode_message(received_msg, verbose=self.verbose)

        return(request, data)
