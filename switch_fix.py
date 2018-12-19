import sys
import queue
import numpy as np
#   time class for measuring returned finish time of the simulation


class Context:
    def __init__(self):
        self.time = 0
        self.lastTimeLogged = 0
        #   self.unit_time = unit_t

    def get_time(self):
        return self.time

    def tick(self, unit_t):
        #   self.lastTimeLogged = ttime.time_ns()
        self.time += unit_t

    def inc_by(self, val):
        self.time += val


#   the actual simulation
#   should print the output line
def switch(t1, n1, m1, p_matrix1, lambda_list1, q_list1, mu_list1, file_temp):

    #   create a context for time measure
    #   context = Context()

    t_w = 0
    t_s = 0
    #   frames left to be handled
    frames_left_counter = 0
    #   initialize events queue
    events = []
    time_t = 0
    while float(time_t) < float(t1):
        for i_port in range(int(n1)):
            #   pick an output port according to the port's probabilities
            outport_array = [o for o in range(int(m1))]
            output_port_array = np.random.choice(outport_array, 1, False, p_matrix1[i_port])
            output_port = output_port_array[0]
            lambda_var1 = float(lambda_list1[i_port])
            val_exp = np.random.exponential(1.0/lambda_var1)
            time_t += (val_exp)
            #   context.tick(float(val_exp))
            entry = [float(time_t), [output_port, True, False]]
            queue.heappush(events, entry)
            frames_left_counter += 1
            #   t_w -= context.get_time()
    #   a counter array for deleted frames in each output port
    deleted_output_port = []
    for i1 in range(int(m1)):
        deleted_output_port.append(0)

    #   a counter of the deleted frames (X)
    deleted_frames_counter = 0

    #   a counter array for finished frames in each output port
    frames_done_output_port = []
    for i2 in range(int(m1)):
        frames_done_output_port.append(0)

    #   a counter of the finished frames (Y)
    frames_done_counter = 0

    #   simulation starts here
    t_tag = 0
    #   todo: check what should be the unit
    output_ports_counter = [0] * int(m1)
    free_port = [True] * (int(m1))
    ports_service_time = [0] * (int(m1))
    print(free_port[0])
    print(free_port[1])
    while not len(events) == 0:
        curr_event = queue.heappop(events)
        o_port = int(curr_event[1][0])
        is_new_frame = bool(curr_event[1][1])
        queued = bool(curr_event[1][2])
        time_stamp = float(curr_event[0])
        is_full = (int(output_ports_counter[o_port]) == int(q_list1[o_port]))
        is_port_free = free_port[o_port]
        #   print(o_port, is_new_frame, time_stamp, is_full, sep=",")
        if is_new_frame:
            if is_port_free:

            else:

        else:
            #   END SERVICE
            #   increment by start of service time
            t_w += time_stamp
            output_ports_counter[o_port] -= 1
            frames_done_counter += 1
            frames_done_output_port[o_port] += 1
            exp_out = np.random.exponential(1/int(mu_list1[o_port]))
            t_s += exp_out
            t_tag = time_stamp + exp_out
            free_port[o_port] = True

    y = frames_done_counter
    x = deleted_frames_counter
    t_w_avg = float(t_w/y)
    t_s_avg = float(t_s/y)
    #   print("x:")
    #   print(deleted_frames_counter)
    #   print("x1:")
    #   print(deleted_output_port[0])
    #   print("x2:")
    #   print(deleted_output_port[1])
    #   print("y:")
    #   print(frames_done_counter)
    #   print("y1:")
    #   print(frames_done_output_port[0])
    #   print("y2:")
    #   print(frames_done_output_port[1])

    file_temp.write("T': %.2f, x: %d, x1: %d, x2: %d, y: %d, y1: %d, y2: %d, Tw: %.2f, Ts: %.2f %%\n"
                    % (t_tag, deleted_frames_counter, deleted_output_port[0],
                       deleted_output_port[1], frames_done_counter, frames_done_output_port[0],
                        frames_done_output_port[1], t_w_avg, t_s_avg))


def main():
    file_temp = open("output.csv", "w+")

    t = sys.argv[1]
    n = sys.argv[2]
    m = sys.argv[3]
    #   initializing probabilities matrix
    rows = n
    columns = m
    matrix_p = []
    index_argv = 4
    print("matrix prob:")
    for i in range(int(n)):
        sub = []
        for j in range(int(m)):
            sub.append(float(sys.argv[index_argv]))
            print(index_argv)
            index_argv += 1
        matrix_p.append(sub)
    for i in range(int(n)):
        for j in range(int(m)):
            print(i, j, matrix_p[i][j], sep=",")

    #   initialize lambdas array
    lambda_array = []
    print("lambda array:")
    index_argv = 3 + ((int(n)) * (int(m))) + 1
    for i in range(int(n)):
        lambda_array.append(sys.argv[index_argv])
        print(i, index_argv, lambda_array[i], sep=",")
        index_argv += 1

    #   init Qs array
    q_array = []
    print("q list sizes array:")
    index_argv = 3 + ((int(n)) * (int(m))) + int(n) + 1
    for i in range(int(m)):
        q_array.append(sys.argv[index_argv])
        print(i, index_argv,q_array[i], sep=",")
        index_argv += 1

    #   init mu array
    mu_array = []
    print("mu array:")
    index_argv = 3 + ((int(n)) * (int(m))) + int(n) + int(m) + 1
    for index in range(int(m)):
        mu_array.append(sys.argv[int(index_argv)])
        print(index, index_argv, mu_array[index], sep=",")
        index_argv += 1

    #   call switch with suitable parameters
    for i in range(2):
        switch(t, n, m, matrix_p, lambda_array, q_array, mu_array, file_temp)
    file_temp.close()

    #   print out result to file


if __name__ == '__main__':
    main()
