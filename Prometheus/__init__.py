##这是主策略包，本包主要利用同一币种之间期货与现货的价差获利
##outlier detection in difference of futures and spot prices
from numpy import arange,array,ones
from scipy import stats


xi = arange(0,9)
A = array([ xi, ones(9)])

# (Almost) linear sequence
y = [19, 20, 20.5, 21.5, 22, 23, 23, 25.5, 24]

# Generated linear fit
slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
line = slope*xi+intercept

print(line)
print(std_err)
print(r_value)
print(p_value)

