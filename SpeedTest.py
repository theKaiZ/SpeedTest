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
     print(fun.__name__)
  def add_time(self,fun,t):
     self.has_function(fun)
     self.functions[fun.__name__]['dts'].append(t)
  def stats(self):
     fig = plt.figure()
     ax = fig.add_subplot(111)
     #num_keys = len(self.functions.keys())
     for n,key in enumerate(self.functions.keys()):
        print(key)
        t = time()
        dts = np.array(self.functions[key]['dts'])
        print(time()-t,"um das in ein array umzuwandeln")
        #TODO the thing with the plotting seems to be unpractical. Better check if the fist run is way longer than the
        #TODO other runs, but this will just indicate the use of jit
        #if len(dts)> num_keys:
          #if dts.max() > 2* dts.min():
             #if len(dts)>100:
               #plt.figure().add_subplot().bar(np.arange(100),dts[:100])

        #print(*self.functions[key]['dts'])
        ax.bar(n,np.sum(dts))
     ax.set_xticks(range(len(self.functions.keys())))
     ax.set_xticklabels(self.functions.keys(),rotation=90)
     fig.tight_layout()
     plt.show()


def time_runtime(function):
    def wrapper(*args, **kwargs):
        if function.__name__ == 'main':
           print("Start der Main function")
        start = time()
        result = function(*args, **kwargs)
        end = time()
        diff = end-start

        SpeedTest().add_time(function,diff)  
        if function.__name__ == 'main':
           print("Ende der Main function")  
           SpeedTest().stats()
        return result
    return wrapper
