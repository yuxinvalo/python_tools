#!/usr/bin/python3
# Project: performance tools
# Author: syx10
# Time 2021/1/30:12:05
import time
import os
import pickle


class TimerPerformance:
    def __init__(self):
        super(TimerPerformance).__init__()
        self.timer_perf = {}
        self.save_dir = os.getcwd() + '/performance/'

    def __set_tag(self, tag):
        if not self.timer_perf.get(tag):
            self.timer_perf[tag] = []

    def set_timer(self, tag, timer):
        if not self.timer_perf.get(tag):
            self.__set_tag(tag)
        self.timer_perf[tag].append(timer)

    def timer_wrapper(self, tag):
        def wrapper(func):
            def deco(*args, **kwargs):
                start = time.clock()
                res = func(*args, **kwargs)
                end = round(time.clock() - start, 6)
                self.set_timer(tag, end)
                return res
            return deco
        return wrapper


    def show_perf(self):
        import numpy as np
        max_mean = {}
        the_max_max = 0, ''
        the_max_mean = 0, ''
        for ele in self.timer_perf.keys():
            max_mean[ele] = [max(self.timer_perf[ele]), np.mean(self.timer_perf[ele])]
            print("Length of " + ele + " is " + str(len(self.timer_perf[ele])))
            print("Max " + ele + " timer: " + str(max_mean[ele][0]))
            print("Mean " + ele + " timer: " + str(max_mean[ele][1]))

        for ele in max_mean:
            if max_mean[ele][0] > the_max_max[0]:
                the_max_max = max_mean[ele][0], ele

            if max_mean[ele][1] > the_max_mean[0]:
                the_max_mean = max_mean[ele][1], ele
        print("The max time conso ====>" + str(the_max_max))
        print("The max mean time conso =====>" + str(the_max_mean))

    def set_save_dir(self, directory):
        if os.path.exists(directory):
            self.save_dir = directory
        else:
            return 'Directory: ' + str(directory) + ' not exist!'

    def save_perf(self):
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        if len(self.timer_perf) > 0:
            try:
                filename = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + '_perf.pkl'
                perf_file = open(self.save_dir + filename, 'wb')
                pickle.dump(self.timer_perf, perf_file)
                return perf_file.name
            except Exception as e:
                raise e
        else:
            return 'Performance object has no data to save!'


def performance_viewer(perf_obj=None, filepath=''):
    if perf_obj is None and filepath == '':
        raise ValueError + ' arguments exception.'
    if type(perf_obj) == TimerPerformance:
        if len(perf_obj.timer_perf) == 0:
            raise Exception('Performance object is empty')
        else:
            timer_perf = perf_obj.timer_perf
    elif os.path.exists(filepath):
        try:
            f = open(filepath, 'rb')
            timer_perf = pickle.load(f)
        except Exception as e:
            raise e
        finally:
            if f:
                f.close()
    else:
        raise ValueError + ' arguments exception.'

    import matplotlib.pyplot as plt
    for ele in timer_perf:
        plt.figure()
        plt.plot(timer_perf[ele])
        plt.title(ele + " timer")
        plt.show()