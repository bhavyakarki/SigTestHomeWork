import numpy as np
from numpy import genfromtxt
from scipy.stats import ttest_ind
from scipy.stats import ks_2samp
from scipy.stats import wilcoxon
from scipy import stats
import csv
import math

class SignificanceTesting(object):
	def __init__(self, filePath):
		self.filePath = filePath
		self.dataset = self.loadData()

	def loadData(self):
		self.models_scores = ['Baseline_R2', 'Baseline+Fusion_R2', 'Baseline+Ordering_R2',\
							  'Baseline+Ordering+Fusion_R2', 'Baseline_RSU4',	'Baseline+Fusion_RSU4', \
							  'Baseline+Ordering_RSU4', 'Baseline+Ordering+Fusion_RSU4']
		self.data = genfromtxt(self.filePath, delimiter=',')[1:].T
		self.data = np.asfarray(self.data)
		self.stat_distr(self.models_scores, self.data)

	
	def stat_distr(self, header, data):
		rouges = dict()
		print(len(header))
		for i,topic in enumerate(header):
			rouges[topic] = []
			mean = np.mean(data[i],dtype=np.float64) 	
			rouges[topic].append(mean)
			median = np.median(data[i])
			rouges[topic].append(median)
			mode = stats.mode(data[i])
			rouges[topic].append(mode)
			min_x = min(data[i], key=float)
			rouges[topic].append(min_x)
			max_x = max(data[i], key=float)
			rouges[topic].append(max_x)
	
		print rouges
		

	def ksTest(self, listA, listB):
		value, pvalue = ks_2samp(listA, listB) 
		return pvalue

	def tTest(self, listA, listB):
		value, pvalue = ttest_ind(listA, listB)
		return pvalue

	def wilcoxonTest(self, listA, listB):
		T, pvalue = wilcoxon(listA, listB)
		return pvalue

	def consolidateTests(self, data, a, b):
		results = []
		mean1 = np.mean(data[a],dtype=np.float64)
		mean2 = np.mean(data[b],dtype=np.float64)
		mean_diff = math.fabs(mean1-mean2)
		results.append(mean_diff)
		results.append(self.ksTest(data[a],data[b]))
		results.append(self.tTest(data[a],data[b]))
		results.append(self.wilcoxonTest(data[a],data[b]))
		return results

	def writeOutput(self, filepath, cols, row, resultsDatai, data):
		resultsFile = open(filepath, 'w')
		#resultsData[0] = ['metric','model', 'mean diff', 'P(T test)', 'P(wilcoxon test)' ,'P(ks test)']
		for row in xrange(1,7):
			resultsData[row][0]= 'ROUGE-2'
		for row in xrange(7,14):
			resultsData[row][0]= 'ROUGE-SU4'
		resultsData[1][1] = 'Baseline & Fusion'
		resultsData[2][1] = 'Baseline & Ordering'
		resultsData[3][1] = 'Fusion & Ordering'
		resultsData[4][1] = 'Baseline & Ordering+Fusion'
		resultsData[5][1] = 'Ordering & Ordering+Fusion'
		resultsData[6][1] = 'Fusion & Ordering+Fusion'
		resultsData[7][1] = 'Baseline & Fusion'
		resultsData[8][1] = 'Baseline & Ordering'
		resultsData[9][1] = 'Fusion & Ordering'
		resultsData[10][1] = 'Baseline & Ordering+Fusion'
		resultsData[11][1] = 'Ordering & Ordering+Fusion'
		resultsData[12][1] = 'Fusion & Ordering+Fusion'
	
		
		resultsData[1][2:] = self.consolidateTests(data, 0, 1)
		resultsData[2][2:] = self.consolidateTests(data, 0, 2)
		resultsData[3][2:] = self.consolidateTests(data, 1, 2)
		resultsData[4][2:] = self.consolidateTests(data, 0, 3)
		resultsData[5][2:] = self.consolidateTests(data, 2, 3)
		resultsData[6][2:] = self.consolidateTests(data, 1, 3)
		resultsData[7][2:] = self.consolidateTests(data, 4, 5)
		resultsData[8][2:] = self.consolidateTests(data, 4, 6)
		resultsData[9][2:] = self.consolidateTests(data, 5, 6)
		resultsData[10][2:] = self.consolidateTests(data, 4, 7)
		resultsData[11][2:] = self.consolidateTests(data, 6, 7)
		resultsData[12][2:] = self.consolidateTests(data, 5, 7)

		with resultsFile:
			writer = csv.writer(resultsFile)
			writer.writerows(resultsData)
		resultsFile.close()


	def boxingPlot(self):
		plt.figure()
		plt.boxplot(self.data.T)
		plt.show()
		


if __name__ == '__main__':
	filePath = "ROUGE_SCORES.csv"
	sigInstance = SignificanceTesting(filePath)
	#print "iiiiiiii",sigInstance.data
	resultsData = [[0 for x in range(6)] for y in range(14)]
	resultsData[0] = ['metric','model', 'mean diff', 'P(T test)', 'P(wilcoxon test)' ,'P(ks test)']
	pl = sigInstance.writeOutput("SigTestResults.csv", 6, 14, resultsData, sigInstance.data)


