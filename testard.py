import csv
from matplotlib import pyplot
import numpy as np
import os
from scipy.interpolate import *


def generate_dist():
    x = []
    t = []
    t1 = []
    with open('SensorDataStore.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            x.append(float(row[1]))
            t1.append(float(row[0]))
    x.sort(reverse=True)
    x[0] = (x[0] + x[1])/2
    for i in range(len(t1)):
        t.append(t1[i] - min(t1))
    f2 = interp1d(t, x, kind='quadratic', assume_sorted=True, bounds_error=True)


    spl = UnivariateSpline(t, f2(t))
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.set_xticks(np.arange(0, 1.5 * max(t), max(t) / 5))
    ax.set_yticks(np.arange(0, 2 * max(x), 2 * max(x) / 10))

    pyplot.plot(t, f2(t), '-', t, spl(t), 'b', lw=2.5)  #!!!! 'b' - цвет   lw - жирность
    # pyplot.plot(t, spl(t), 'b', lw=2.5)

    pyplot.xlim([0, max(t) + 0.2])
    pyplot.ylim([0, 2 * max(x)])
    pyplot.grid(True)
    pyplot.legend(['raw data', 'interpolation'], loc='best')
    pyplot.ylabel('Coordinate')
    pyplot.xlabel('Time')
    pyplot.title("S(t)")
    os.remove('graph.png')
    pyplot.savefig('graph.png')

def generate_speed():
    x = []
    t = []
    t1 = []
    v = []
    with open('SensorDataStore.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            x.append(float(row[1]))
            t1.append(float(row[0]))
        x.sort(reverse = True)
        for i in range(len(t1)):
            t.append(t1[i] - min(t1))

        accel = 2*(x[len(x)-1]-x[0])/(t[len(t)-1])/(t[len(t)-1])
        for time in t:
            v.append(-accel*time)
        v = np.array(v, float)

    spl = UnivariateSpline(t, v)
    spl.set_smoothing_factor(1)

    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.set_xticks(np.arange(0, 1.5 * max(t), max(t) / 5))
    ax.set_yticks(np.arange(0, 2 * max(v), 2 * max(v) / 10))

    pyplot.plot(t, spl(t), 'b', lw=2.5)

    pyplot.xlim([0, max(t) + 0.2])
    pyplot.ylim([0, 2 * max(v)])
    pyplot.grid(True)
    pyplot.ylabel('Speed')
    pyplot.xlabel('Time')
    pyplot.title("V(t)")
    os.remove('graph1.png')
    pyplot.savefig('graph1.png')

def generate_accel():
    x = []
    t = []
    t1 = []
    a = []
    with open('SensorDataStore.csv', 'r') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            x.append(float(row[1]))
            t1.append(float(row[0]))
            count += 1
        x.sort(reverse=True)
        for i in range(len(t1)):
            t.append(t1[i] - min(t1))

        accel = 2*(x[len(x)-1]-x[0])/(t[len(t)-1])/(t[len(t)-1])
        for i in range(count):
            a.append(accel)
        a = np.array(a, float)
    fig = pyplot.figure()
    ax = fig.add_subplot(111)

    ax.set_xticks(np.arange(0, 1.5 * max(t), max(t) / 5))
    ax.set_yticks(np.arange(0, 2 * max(a), round(max(a) / 4, 4)))
    pyplot.plot(t, a, 'b', lw=2.5)

    pyplot.xlim([0, max(t) + 0.2])
    pyplot.ylim([0, 2 * max(a)])
    print(x)
    print(t)
    print(a)
    pyplot.grid(True)
    pyplot.ylabel('Acceleration')
    pyplot.xlabel('Time')
    pyplot.title("a(t)")
    os.remove('graph2.png')
    pyplot.savefig('graph2.png')

def generate_all():
    print("generating plots")
    generate_dist()
    generate_speed()
    generate_accel()

# generate_all()