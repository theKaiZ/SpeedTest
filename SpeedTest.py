from time import time
import matplotlib.pyplot as plt
import numpy as np

class SpeedTest():
  functions = {}
  def __init__(self):
     pass
     
  def add_function(self,fun):
     new = {}
     new.update(num_calls=0)
     new.update(dts = [])
     self.functions[fun.__name__] = new
  def has_function(self,fun):
     if fun.__name__ in self.functions:
        return 1
     self.add_function(fun)
  def add_time(self,fun,t):
     self.has_function(fun)
     self.functions[fun.__name__]['dts'].append(t)
  def stats(self):
     fig = plt.figure()
     ax = fig.add_subplot(111)
     for n,key in enumerate(self.functions.keys()):
        print(key)
        print(*self.functions[key]['dts'])
        ax.bar(n,np.sum(self.functions[key]['dts']))
     ax.set_xticks(range(len(self.functions.keys())))
     ax.set_xticklabels(self.functions.keys(),rotation=90)
     fig.tight_layout()
     plt.show()


def time_runtime(function,min=0.0):
    def wrapper(*args, **kwargs):
        if function.__name__ == 'main':
           print("Start der Main function")
        else:
           print(function.__name__)
        start = time()
        result = function(*args, **kwargs)
        end = time()
        diff = end-start
        if diff > min:
          print("Time to run in seconds: {}".format(end-start))
        
        SpeedTest().add_time(function,diff)  
        if function.__name__ == 'main':
           print("Ende der Main function")  
           SpeedTest().stats()
        return result
    return wrapper
