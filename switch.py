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

    #   frames left to be handled
    frames_left_counter = 0
    done = False
    #   context.tick()
    # a counter array of frames to be serviced
    frames_to_service = [0] * int(m)
    frames_to_service_counter = 0
    #   simulation starts here
    while not done:

        context.tick()
        #   ARRIVAL TO INPUT PORTS
        if context.get_time() < float(t):
            for i in range(int(n)):
                for frame in range(int(lambda_list[i])):
                    #   print("here rach")
                    #   pick an output port according to the port's probabilities
                    output_port_array = np.random.choice([o for o in range(int(m))], 1, False, p_matrix[i])
                    output_port = output_port_array[0]
                    #   print(output_port)
                    #   if queue is empty - handle frame immediately
                    #   try to enqueue the frame to the chosen output port's queue
                    try:
                        output_ports_queues[output_port].put_nowait(int(frame))
                    except queue.Full:
                        frames_to_service[output_port] += 1
                        frames_to_service_counter += 1
                        #   deleted_output_port[output_port] += 1
                        #   deleted_frames_counter += 1
                        continue
                        #   update counter of frames left in queues
                    frames_left_counter += 1
                    #   subtracting insertion to queue time from T_w
                    t_w -= context.get_time()

        #   END SIMULATION?
        elif frames_left_counter <= 0:
            done = True
            continue
        #   HANDLE FRAMES IN OUTPUT PORTS
        #   context.tick()

        for j in range(int(m)):
            #   handle mu_list[output_port] frames in the output port queue
            #   dequeue mu[j] frames from jth queue
            for d_frame in range(int(mu_list[j])):
                    try:
                        output_ports_queues[j].get_nowait()
                    except queue.Empty:
                        while not output_ports_queues[j].full() and frames_to_service[j] > 0:
                            output_ports_queues[j].put_nowait(int(d_frame))
                            frames_to_service[j] -= 1
                            frames_to_service_counter -= 1
                            frames_left_counter += 1
                            #   subtracting insertion to queue time
                            t_w -= context.get_time()
                        d_frame -= 1
                        continue
                    #   print("here frame_d post try block")
                    #   finish_times.insert(index, context.get_time())
                    #   add/subtract start of service time to/from Tw/Ts
                    t_w += context.get_time()
                    #   t_s -= context.get_time()
                    frames_left_counter -= 1
                    frames_done_output_port[j] += 1
                    frames_done_counter += 1
                    #   adding end of service time to T_w
                    t_s += float(1 / int(mu_list[j]))
                    #   t_w += context.get_time()
                    #   exit_if = False
                    if frames_to_service[j] > 0:
                        try:
                            output_ports_queues[j].put_nowait(int(d_frame))
                        except queue.Full:
                            deleted_output_port[j] += 1
                            deleted_frames_counter += 1
                            frames_to_service_counter -= 1
                            frames_to_service[j] -= 1
                            #   exit_if = True
                            continue
                        frames_to_service[j] -= 1
                        frames_to_service_counter -= 1
                        frames_left_counter += 1
                        #   subtracting insertion to queue time from T_w
                        t_w -= context.get_time()
            #   handle frames left end of cycle
            while frames_to_service[j] > 0:
                try:
                    output_ports_queues[j].put_nowait(0)
                except queue.Full:
                    deleted_output_port[j] += 1
                    deleted_frames_counter += 1
                    frames_to_service_counter -= 1
                    frames_to_service[j] -= 1
                    continue
                frames_to_service[j] -= 1
                frames_to_service_counter -= 1
                frames_left_counter += 1
                #   subtracting insertion to queue time from T_w
                t_w -= context.get_time()

    t_final = context.get_time()
    y = frames_done_counter
    x = deleted_frames_counter
    t_w_avg = float(t_w/frames_done_counter)
    t_s_avg = float(t_s/frames_done_counter)
    print("T': ")
    print(t_final)
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
    print(t_w_avg)
    print("Ts: ")
    print(t_s_avg)


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
