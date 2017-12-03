from pytrends.request import TrendReq
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
import matplotlib.pyplot as plt

#This file requires all of the imports above in order to operate.
#This was built on a version of the pytrends package but the package was altered to better fit the needs of this program.
#created by scott huson. 



def fit_func(x, a, b, c):
    return a*x*x + b*x + c




search = input('What would you like to search for?\n')
time = "2012-12-14 2017-10-25"

#Sets up the google requestor for the trends API
pytrend = TrendReq()
pytrend.build_payload(kw_list=[search], cat=0, timeframe=time, geo='', gprop='') #creates the payload for the identifiers you want to test for 

print("loaded payload")
#Related Queries, returns a dictionary of dataframes
related_queries_dict = pytrend.related_queries()
#print(related_queries_dict)
lst = related_queries_dict[search]['top'].take(range(10))['query'].tolist()
lst_of_weights = related_queries_dict[search]['top'].take(range(10))['value'].tolist()
print("related terms for more data")
print(lst) 

lsta = []
lstb = []
lstc = []
lines = []
#This line takes the original search term and gets the equation of that graph
search_y_values = np.asarray(pytrend.interest_over_time()[search].tolist())
[aor, bor, cor] = curve_fit(fit_func, np.asarray(list(range(len(search_y_values)))), search_y_values)[0]

print(aor, bor, cor)

print("beginning loops")
for term in lst:
    pytrend.build_payload(kw_list=[term], cat=0, timeframe=time, geo='', gprop='')
    interest_over_time_df = pytrend.interest_over_time()
    lstOfPoints = interest_over_time_df[term].tolist()
    length = len(lstOfPoints)
    ypoints = list(range(length))
    ylst = np.asarray(lstOfPoints)
    xlst = np.asarray(ypoints)
    params = curve_fit(fit_func, xlst, ylst)
    [a, b, c] = params[0]
    #if abs(a - aor) < 0.4 and abs(b - bor) < 0.2 and abs(c - cor) < 25:
    lines.append(plt.plot(xlst, ylst))
    lsta.append(a)
    lstb.append(b)
    lstc.append(c)
    print(".")
    #else:
     #   print("nil " + term)
    
 
plt.title("Relative Popularity of " + search)
plt.xlabel("Time: " + time)
plt.ylabel("Relative Popularity")
#plt.legend(lines ,lst)
plt.draw()



print("Means")
meanx = 0
meany = 0
count = 0
for n in lsta:
    print(n, lst_of_weights[count], lst[count])
    meanx += n*lst_of_weights[count]
    meany += lstb[count]*lst_of_weights[count]/length
    count += 1
    

print("The first number is a good indication of the overall behavior of this search, the second term is a good indication of the initial value, or starting popularity of it. ")
print(meanx, meany)


#weighting equation




plt.show(block=True)
plt.close()




