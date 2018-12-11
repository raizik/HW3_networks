import sys
import queue
import random
import numpy
#   time class for measuring returned finish time of the simulation


class Context:
    def __init__(self):
        self.time = 0
        self.lastTimeLogged = 0

    def get_time(self):
        return self.time

    def tick(self):
        self.time += 1

    def inc_by(self, val):
        self.time += val


#   the actual simulation
#   should print the output line
def switch(t, n, m, p_matrix, lambda_list, q_list, mu_list):
    #   create a context for time measure
    context = Context()

    #   initializing a 2D array of frame queues for each output port
    output_ports_queues = []
    for i in range(m):
        port_queue = queue.Queue(maxsize=q_list[i])
        output_ports_queues.append(port_queue)

    #   a counter array for deleted frames in each output port
    deleted_output_port = [m]

    #   a counter of the deleted frames (X)
    deleted_frames_counter = 0

    #   a counter array for finished frames in each output port
    frames_done_output_port = [m]

    #   a counter of the finished frames (Y)
    frames_done_counter = 0

    #   array of arrival times of frames
    arrivals = [0] * (sum(lambda_list) * t)

    #   array of times of insertion of a frame to a queue
    queue_insertion_times = [0] * (sum(lambda_list) * t)

    #   array of finishing times of frames
    finish_times = [0] * (sum(lambda_list) * t)

    #   frames left to be handled
    frames_left_counter = 0;

    #   simulation starts here
    while context.get_time() < t:
        context.tick()

        #   handle lambda[i] frames arriving at input port i
        for i in range(n):
            for frame in range(0, lambda_list[i]):
                #   insert arrival  time of current frame
                arrivals[frame] = context.get_time()
                #   pick an output port according to the port's probabilities
                output_port = numpy.random.choice(range(0, m-1), p_matrix[i])

                #   try to enqueue the frame to the chosen output port's queue
                try:
                    output_ports_queues[output_port].put(frame)
                except queue.Full:
                    deleted_output_port[output_port] += 1
                    deleted_frames_counter += 1
                    frames_left_counter -= 1
                #   update counter of frames left in queues
                frames_left_counter += 1
                #   update queue insertion time of current frame
                queue_insertion_times[frame] = context.get_time()
        #   empty output ports' queues
        context.tick()
        for j in range(m):
            #   handle mu_list[output_port] frames in the output port queue
            frames_done_output_port[j] += mu_list[j]
            frames_done_counter += mu_list[j]

            #   dequeue all the handled frames from output ports' queue
            for frame_d in range(mu_list[j]):
                index = output_ports_queues[j].get()
                finish_times[index] = context.get_time()
                frames_left_counter -= 1

    #   a loop for emptying the remaining frames in the queues
    #   handles remaining frames in output ports queues
    while frames_left_counter > 0:
        context.tick()
        output_port = numpy.random.choice(range(0, m - 1), p_matrix[i])
        #   handle mu_list[output_port] frames in the output port queue
        frames_done_output_port[output_port] += mu_list[output_port]
        frames_done_counter += mu_list[output_port]

        #   dequeue all the handled frames from output ports' queue
        for frame_d in range(mu_list[output_port]):
            index = output_ports_queues[output_port].get()
            finish_times[index] = context.get_time()
            frames_left_counter -= 1

    #   the output values:
    t_final = context.get_time()
    y = frames_done_counter
    x = deleted_frames_counter
    #   todo:  T_w and T_s: iterate over the times arrays to calculate these values


def main():
    t = sys.argv[1]
    n = sys.argv[2]
    m = sys.argv[3]

    #   initializing probabilities matrix
    rows = n
    columns = m
    matrix_p = []
    index_argv = 4
    for i in range(rows):
        sub = []
        for j in range(columns):
            sub.append(sys.argv[index_argv])
            index_argv += 1
        matrix_p.append(sub)

    #   initialize lambdas array
    lambda_array = []
    index_argv = 3 + n*m + 1
    for i in range(n):
        lambda_array.append(sys.argv[index_argv])
        index_argv += 1

    #   init Qs array
    q_array = []
    index_argv = 3 + n*m + n + 1
    for i in range(m):
        q_array.append(sys.argv[index_argv])
        index_argv += 1

    #   init mu array
    mu_array = []
    index_argv = 3 + n*m + n + m + 1
    for i in range(m):
        mu_array.append(sys.argv[index_argv])
        index_argv += 1

    #   call switch with suitable parameters
    switch(t, n, m, matrix_p, lambda_array, q_array, mu_array)

    #   print out result to file
