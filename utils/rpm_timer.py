
import time


def calc_rpm(n, t1, t2):
    duration_min = float(t2 - t1)/60.0
    revs = n
    return revs/duration_min


def main():

    n = int(raw_input("N Revolutions to time? "))

    while True:
        raw_input("Hit a key to start")
        t1 = time.time()
        raw_input("Hit a key to stop")
        t2 = time.time()

        print "RPM: {0}".format(calc_rpm(n, t1, t2))
    

if __name__ == "__main__":
    main()
