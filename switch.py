import sys
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
    #   todo: create the simulation


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
