import queue
import sys
import numpy as np


def main():
    events = []
    t_temp = 1
    while t_temp < 5:
        for i_port in range(5):
            #   event is a queue of arrays of the form: [output_port, arrival_time, is_being_serviced]
            #   event = queue.Queue(maxsize=int(lambda_list[i_port]))
            for frame in range(3):
                #   pick an output port according to the port's probabilities
                entry = [1/t_temp, [1, False, False]]
                queue.heappush(events, entry)
            #   events.put_nowait(event)
            t_temp += 1
    new_entry = [0.31, [2, True, True]]
    queue.heappush(events, new_entry)
    while not len(events) == 0:
        curr_event = queue.heappop(events)
        print("len",len(events), sep=":")
        print(curr_event[0], curr_event[1][0], curr_event[1][1], curr_event[1][2], sep=",")
    print(np.random.choice([o for o in range(2)], 1, False, [0.1, 0.9])[0])
    print(np.random.exponential(1.0/20.0))


if __name__ == '__main__':
    main()