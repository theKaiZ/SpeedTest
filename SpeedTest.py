from time import time
import matplotlib.pyplot as plt
import numpy as np

class SpeedTest():
  functions = {}
  no_main = True
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
     self.functions[fun.__name__]['dts'].append(t)

  def stats(self):
     fig = plt.figure()
     ax = fig.add_subplot(111)
     units = ["s","ms","µs","ns"]
     num_keys = len(self.functions.keys())
     for n,key in enumerate(self.functions.keys()):
        dts = np.array(self.functions[key]['dts']).astype("float32")
        print("Function {}".format(key))
        if len(dts)>num_keys:
            #todo you can do this nicer! and shorter
            umax=umin=umean=0
            dtmin = dts.min()
            if dtmin > 0:
              while dtmin < 0.1:
                dtmin*=1000
                umin+=1
            dtmax = dts.max()
            if dtmax:
              while dtmax < 0.1:
                dtmax *= 1000
                umax+=1
            dtmean = dts.mean()
            if dts[0]>5*dtmean:
                print("Numba detected!")
            if dtmean:
              while dtmean < 0.1:
                dtmean *= 1000
                umean+=1
            print("Num runs: {}\n total time: {:.2f} s\n max: {:.2f} {}\n min: {:.2f} {}\n mean: {:.2f} {}\n\n".format(len(dts),dts.sum(),dtmax,units[umax],dtmin,units[umin],dtmean,units[umean]))
        else:
            print("Num runs: {}\n total time: {}\n".format(len(dts),dts.sum()))
        ax.bar(n,np.sum(dts))
     ax.set_xticks(range(len(self.functions.keys())))
     ax.set_xticklabels(self.functions.keys(),rotation=90)
     fig.tight_layout()
     fig.savefig("test.png")

def time_runtime(function):
    def wrapper(*args, **kwargs):
        if function.__name__ == 'main':
            print("Start of Main function")
            SpeedTest().no_main = False
        SpeedTest().has_function(function)
        start = time()
        result = function(*args, **kwargs)
        diff = time()-start
        SpeedTest().add_time(function,diff)
        if function.__name__ == 'main':
           print("End of Main function after {:.2f} seconds".format(diff))
           SpeedTest().stats()
        if SpeedTest().no_main:
            print(function.__name__,diff,"Sekunden")
        return result
    return wrapper
