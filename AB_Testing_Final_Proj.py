# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 09:38:18 2016

@author: dhey2
"""
import numpy as np

""" Evaluation Metrics:
•	Gross conversion: That is, number of user-ids to complete checkout and 
        enroll in the free trial divided by number of unique cookies to click 
        the "Start free trial" button. (dmin= 0.01)
•	Retention: That is, number of user-ids to remain enrolled past the 14-day 
        boundary (and thus make at least one payment) divided by number of 
        user-ids to complete checkout. (dmin=0.01)
•	Net conversion: That is, number of user-ids to remain enrolled past the 
        14-day boundary (and thus make at least one payment) divided by the 
        number of unique cookies to click the "Start free trial" button. 
        (dmin= 0.0075)
"""
"""
#Calculating Standard Deviation
probs = {'p_g_conversion' : 0.20625, 
         'p_retention' : 0.53, 
         'p_n_conversion' : 0.1093125}
n = 5000    #total cookies
n = n *.08  #total cookies that click "start free trial"
print n
sd = np.sqrt(probs['p_g_conversion'] * (1 - probs['p_g_conversion']) / n)
print 'p_g_conversion sd =', round(sd,4)

n = probs['p_g_conversion'] * n
print n
sd = np.sqrt(probs['p_retention'] * (1 - probs['p_retention']) / n)
print 'p_retention sd =', round(sd,4)

n = 5000 * .08
sd = np.sqrt(probs['p_n_conversion'] * (1 - probs['p_n_conversion']) / n)
print 'p_n_conversion sd =', round(sd,4)

#Calculating Number of Pageviews
a = .05
b = .2

n_g_conversion = 25835 / .08
n_retention = 0 #39115 /.08 / 0.20625 #Note this is 0 because using the retention metric was driving up the duration of the experiment
n_n_conversion = 27413 / .08
pageviews = max(n_g_conversion, n_retention, n_n_conversion) * 2
print pageviews
#Duration and exposure
pageviews = round(pageviews, 0)
traffic = 40000
diversion = .9
print
print pageviews / (traffic * diversion)

#Sanity Checks
""""""Invariants
1. cookies
2. clicks
3. click through prob = cookies that clicked "start free trial" / total cookies 
""""""
#experiment totals
pageviews_e = 344660
clicks_e = 28325
enrollments_e = 3423
payments_e = 1945
ct_prob_e = float(clicks_e) / pageviews_e 
#control totals
pageviews_c = 345543
clicks_c = 28378
enrollments_c = 3785
payments_c = 2033
ct_prob_c = float(clicks_c) / pageviews_c 
#cookies control limits
p = .5
z = 1.96
se = np.sqrt(p * (1-p) / (pageviews_e + pageviews_c))
upper = round(p + z * se, 4)
lower = round(p - z * se, 4)
print "cookie: ", lower, "\t", upper
phat = round(pageviews_c / float(pageviews_e + pageviews_c), 4)
print phat, phat < upper and phat > lower
#clicks control limits
p = .5
z = 1.96
se = np.sqrt(p * (1-p) / (clicks_e + clicks_c))
upper = round(p + z * se, 4)
lower = round(p - z * se, 4)
print "clicks: ", lower, "\t", upper
phat = round(clicks_c / float(clicks_e + clicks_c), 4)
print phat, phat < upper and phat > lower
#click through control limits
z = 1.96
p = ct_prob_c
print p
se = np.sqrt(p * (1-p) / float(pageviews_c))
upper = round(p + z * se, 4)
lower = round(p - z * se, 4)
print "click-through: ", lower, "\t", upper
phat = round(ct_prob_e, 4)
print phat, phat < upper and phat > lower
"""
#effect size tests
import csv
import pandas as pd
import numpy as np

c_df = pd.read_csv('Final Project Results - Control.csv')
e_df = pd.read_csv('Final Project Results - Experiment.csv')
#only use first 23 rows bc of missing enrollments and payments for the last rows
c_df = c_df.head(23)
e_df = e_df.head(23)
#retention confidence interval
x_vars = ["Enrollments", "Payments", "Payments"]
n_vars = ["Clicks", "Enrollments", "Clicks"]
d_mins = [.01, .01, .0075]
for i in range(3):
	var_x = x_vars[i]
	var_n = n_vars[i]
	phat_c = float(c_df[var_x].sum()) / c_df[var_n].sum()
	phat_e = float(e_df[var_x].sum()) / e_df[var_n].sum()
	dhat = phat_e - phat_c
	phat_pool = float(c_df[var_x].sum() + e_df[var_x].sum()) / (c_df[var_n].sum() + e_df[var_n].sum())
	se_pool = np.sqrt(phat_pool * (1 - phat_pool) * (1.0/c_df[var_n].sum() + 1.0/e_df[var_n].sum()))
	z = 2.24	#now using Bonfierri alpha = .05/2, previously was 1.96
	upper = round(dhat + z * se_pool, 4)
	lower = round(dhat - z * se_pool, 4)
	print var_x, "/", var_n 
	print "dhat =", dhat, "p-hat pool = ", phat_pool, "se pool =", se_pool
	print "lower =", lower, "upper =", upper
	print "Statistical Significance:", not(0.0 < upper and 0.0 > lower) 
	print "Practical Significance:", not(d_mins[i] < upper and d_mins[i] > lower) and not(-d_mins[i] < upper and -d_mins[i] > lower)
	print
	
#Sign Tests
c_df['retention'] = c_df['Payments'] / c_df['Enrollments']
c_df['net_conversion'] = c_df['Payments'] / c_df['Clicks']
c_df['gross_conversion'] = c_df['Enrollments'] / c_df['Clicks']
e_df['retention'] = e_df['Payments'] / e_df['Enrollments']
e_df['net_conversion'] = e_df['Payments'] / e_df['Clicks']
e_df['gross_conversion'] = e_df['Enrollments'] / e_df['Clicks']
metrics = {"retention" : 0, "net_conversion" : 0, "gross_conversion" : 0}
for i in range(23):
	for metric in metrics.iterkeys():
		if e_df[metric][i] > c_df[metric][i]:
			metrics[metric] += 1
print metrics


