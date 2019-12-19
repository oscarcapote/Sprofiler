from time import time
class profiler:

    functions_data = {}
    attrs = {}
    init_time = 0.0
    prof_name = ''
    def __init__(self,func):
        self.function = func
        print(self.functions_data)

    @classmethod
    def start_profiler(self,name):
        self.init_time = time()
        self.prof_name = name
        for f,d in self.functions_data.items():
            d['executed'] = 0

    @classmethod
    def time_elapsed(self):
        return time()-self.init_time

    def __call__(self, *args, **kwargs):
        #print(self.functions_data,self.function.__name__)
        self.functions_data[self.function.__name__] = self.functions_data.get(self.function.__name__,{'executed':0,'cum_time':0.0,'last_time':0.0,'times':[]})
        self.functions_data[self.function.__name__]['executed'] += 1
        #print(self.functions_data,self.function.__name__)
        #def crono(*args, **kwargs):
        tic = time()
        to_return = self.function(*args)
        tac = time()
        #print(func.__name__,'ha trigat en executarse',tac-tic)
        self.functions_data[self.function.__name__]['last_time']=tac-tic
        self.functions_data[self.function.__name__]['cum_time']+=tac-tic
        self.functions_data[self.function.__name__]['times'].append(tac-tic)

        #return to_return
        return to_return


    @classmethod
    def stop_profiler(self):
        self.finish_time = time()

    @classmethod
    def report(self):
        profile_time = self.time_elapsed()

        rep = '--------------------------------------------------------------------\n'
        rep += 'Profile analysis {}\n'.format(self.prof_name)
        for att,val in self.attrs.items():
            rep += '{}: {}\n'.format(att,val)
        rep += '\n\nFunctions:\n'
        for f,d in self.functions_data.items():
            rep += '\t-{}:\n'.format(f)
            rep += '\t\tExecuted {} times\n'.format(d['executed'])
            rep += '\t\tTotal execution time {} s\n'.format(d['cum_time'])
            rep += '\t\tMean execution time {} s\n'.format(100.0*float(d['cum_time'])/float(d['executed']))
            rep += '\t\tPercentage execution time about the analysis time {}% \n'.format(100.0*float(d['cum_time'])/profile_time)
        rep += '\n Total time {}'.format(profile_time)
        return rep

    @classmethod
    def write_rep(self,filename):
        s = self.report()
        f = open(filename,'w')
        f.write(s)

    @classmethod
    def show_rep(self):
        print(self.report())
