import sys
import queue
import time as ttime
import numpy as np
#   time class for measuring returned finish time of the simulation


class Context:
    def __init__(self, unit):
        self.time = 0
        self.lastTimeLogged = 0
        self.unit_time = unit

    def get_time(self):
        return self.time

    def tick(self):
        #   self.lastTimeLogged = ttime.time_ns()
        self.time += self.unit_time

    def inc_by(self, val):
        self.time += val


#   the actual simulation
#   should print the output line
def switch(t, n, m, p_matrix, lambda_list, q_list, mu_list):
    #   create a context for time measure
    context = Context(0.9)

    #   initializing a 2D array of frame queues for each output port
    output_ports_queues = [int(m)]
    for i in range(int(m)):
        port_queue = queue.Queue(maxsize=int(q_list[i]))
        output_ports_queues.insert(i, port_queue)
    t_w = 0
    t_s = 0
    #   frames left to be handled
    frames_left_counter = 0
    #   initialize events queue
    events = queue.Queue()
    while context.get_time() < float(t):
        for i_port in range(int(n)):
            event = queue.Queue(maxsize=int(lambda_list[i_port]))
            for frame in range(int(lambda_list[i_port])):
                #   pick an output port according to the port's probabilities
                output_port_array = np.random.choice([o for o in range(int(m))], 1, False, p_matrix[i_port])
                output_port = output_port_array[0]
                t_w -= context.get_time()
                event.put_nowait(output_port)
                frames_left_counter += 1
            events.put_nowait(event)
            context.tick()
    #   a counter array for deleted frames in each output port
    deleted_output_port = [0] * int(m)

    #   a counter of the deleted frames (X)
    deleted_frames_counter = 0

    #   the average waiting time and service time
    t_w = 0
    t_s = 0
    #   a counter array for finished frames in each output port
    frames_done_output_port = [0] * int(m)

    #   a counter of the finished frames (Y)
    frames_done_counter = 0

    done = False
    #   context.tick()
    # a counter array of frames to be serviced
    frames_to_service = [0] * int(m)
    frames_to_service_counter = 0
    #   simulation starts here
    t_tag = 0
    context = Context(0.9)
    while not events.empty():
        output_ports_counter = [0] * int(m)
        curr_event = events.get_nowait()
        while not curr_event.empty():
            output_ports_counter[curr_event.get_nowait()] += 1
        for o_port in range(int(m)):
            min_num = min(int(q_list[o_port]), int(output_ports_counter[o_port]))
            frames_done_output_port[o_port] += min_num
            frames_done_counter += frames_done_output_port[o_port]
            frames_left_counter -= frames_done_counter
            if int(q_list[o_port]) < int(output_ports_counter[o_port]):
                temp_t = int(output_ports_counter[o_port]) - int(q_list[o_port])
                deleted_output_port[o_port] += temp_t
                deleted_frames_counter += deleted_output_port[o_port]
                frames_left_counter -= deleted_frames_counter
            t_start_service_total = frames_done_output_port[o_port] * context.get_time()
            t_end_service_total = frames_done_output_port[o_port] * float(1/int(mu_list[o_port]))
            t_w += t_start_service_total
            t_s -= t_start_service_total
            t_s += t_end_service_total
            t_tag += min_num * float(1/int(mu_list[o_port]))
        context.tick()

    y = frames_done_counter
    #   todo: return frames done for each output port
    x = deleted_frames_counter
    #   todo: return deleted frames for each output port
    #   t_w_avg = float(t_w/y)
    #   t_s_avg = float(t_s/y)
    print("T': ")
    print(t_tag)
    print("x: ")
    print(x)
    print("x1: ")
    print(deleted_output_port[0])
    print("x2: ")
    print(deleted_output_port[1])
    print("y: ")
    print(y)
    print("y1: ")
    print(frames_done_output_port[0])
    print("y2: ")
    print(frames_done_output_port[1])
    print("Tw: ")
    #   print(t_w_avg)
    print("Ts: ")
    #   print(t_s_avg)

def main():
    t = sys.argv[1]
    n = sys.argv[2]
    m = sys.argv[3]
    #   initializing probabilities matrix
    rows = n
    columns = m
    matrix_p = []
    index_argv = 4
    for i in range(int(n)):
        sub = []
        for j in range(int(m)):
            sub.insert(j, sys.argv[index_argv])
            index_argv += 1
        matrix_p.append(sub)

    #   initialize lambdas array
    lambda_array = []
    index_argv = 3 + ((int(n)) * (int(m))) + 1
    for i in range(int(n)):
        lambda_array.insert(i, sys.argv[index_argv])
        index_argv += 1

    #   init Qs array
    q_array = []
    index_argv = 3 + ((int(n)) * (int(m))) + int(n) + 1
    for i in range(int(m)):
        q_array.insert(i, sys.argv[index_argv])
        index_argv += 1

    #   init mu array
    mu_array = [int(m)]
    index_argv = 3 + ((int(n)) * (int(m))) + int(n) + int(m) + 1
    for index in range(int(m)):
        #   print(index)
        mu_array.insert(index, sys.argv[int(index_argv)])
        index_argv += 1

    #   call switch with suitable parameters
    switch(t, n, m, matrix_p, lambda_array, q_array, mu_array)

    #   print out result to file


if __name__ == '__main__':
    main()
