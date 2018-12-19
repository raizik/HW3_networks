import sys
try:
    import queue as queue
except ImportError:
    import Queue as queue
import numpy as np


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
            if is_full:
                if not is_port_free:
                    deleted_output_port[o_port] += 1
                    deleted_frames_counter += 1
                    if queued:
                        output_ports_counter[o_port] -= 1
                        t_w += time_stamp
                elif is_port_free:
                    #   print("bad")
                    #   add/sub start of service time
                    t_w += time_stamp
                    if not queued:
                        output_ports_counter[o_port] += 1
                        t_w -= time_stamp
                    lambda_var = float(mu_list1[o_port])
                    exp_out1 = np.random.exponential(1.0/lambda_var)
                    time_entry = time_stamp + exp_out1
                    entry = [time_entry, [o_port, False, False]]
                    queue.heappush(events, entry)
                    free_port[o_port] = False
                    ports_service_time[o_port] = exp_out1
                #    continue
            if not is_full:
                if not is_port_free:
                    if not queued:
                        output_ports_counter[o_port] += 1
                        #   sub enter to queue time
                        t_w -= time_stamp
                    new_event = [time_stamp + ports_service_time[o_port], [o_port, True, True]]
                    queue.heappush(events, new_event)
                if is_port_free:
                    if not queued:
                        #   sub enter to queue time
                        t_w -= time_stamp
                        output_ports_counter[o_port] += 1
                        new_event = [time_stamp + ports_service_time[o_port], [o_port, True, True]]
                        queue.heappush(events, new_event)
                    else:
                            t_w += time_stamp
                            lambda_var = float(mu_list1[o_port])
                            exp_out2 = np.random.exponential(1.0/lambda_var)
                            time_entry = time_stamp + exp_out2 + ports_service_time[o_port]
                            entry = [time_entry, [o_port, False, False]]
                            queue.heappush(events, entry)
                            free_port[o_port] = False
                            ports_service_time[o_port] = exp_out2
        else:
            #   END SERVICE
            output_ports_counter[o_port] -= 1
            frames_done_counter += 1
            frames_done_output_port[o_port] += 1
            lambda_var = float(mu_list1[o_port])
            exp_out = np.random.exponential(1.0/lambda_var)
            t_tag = time_stamp + exp_out
            #   adding end of service time
            t_s += exp_out
            free_port[o_port] = True
            ports_service_time[o_port] = 0

    y = frames_done_counter
    x = deleted_frames_counter
    t_w_avg = float(t_w/y)
    t_s_avg = float(t_s/y)

    file_temp.write("T': %.8f, x: %d, x1: %d, x2: %d, y: %d, y1: %d, y2: %d, Tw: %.8f, Ts: %.8f %%\n"
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
    for i in range(int(n)):
        sub = []
        for j in range(int(m)):
            sub.append(float(sys.argv[index_argv]))
            index_argv += 1
        matrix_p.append(sub)

    #   initialize lambdas array
    lambda_array = []
    index_argv = 3 + ((int(n)) * (int(m))) + 1
    for i in range(int(n)):
        lambda_array.append(sys.argv[index_argv])
        index_argv += 1

    #   init Qs array
    q_array = []
    index_argv = 3 + ((int(n)) * (int(m))) + int(n) + 1
    for i in range(int(m)):
        q_array.append(sys.argv[index_argv])
        index_argv += 1

    #   init mu array
    mu_array = []
    index_argv = 3 + ((int(n)) * (int(m))) + int(n) + int(m) + 1
    for index in range(int(m)):
        mu_array.append(sys.argv[int(index_argv)])
        index_argv += 1

    #   call switch with suitable parameters
    for i in range(2):
        switch(t, n, m, matrix_p, lambda_array, q_array, mu_array, file_temp)
    file_temp.close()

    #   print out result to file


if __name__ == '__main__':
    main()
