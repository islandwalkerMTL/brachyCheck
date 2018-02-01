########
#code to calculate the difference between the expected channel length and the 
#dicom channel length for the given channel.
#
#EMITROU 2017-12-22
#
#ellis.mitrou.@ssss.gouv.qc.ca

#Interstitial applicator lengths:

import numpy as np


def calcIndDelta(indexer_lengths,expected_length):
	average_error = np.power(np.average(np.power(np.array(indexer_lengths)-expected_length,2)),0.5)
	
	return average_error


indLength_comfCath240mm = 1233
indLength_comfCath294mm = 1288
indLength_proGuide = 1288
indLength_freiburg = 0 # this value will change
indLength_rectum = 0 # this value will change





applicator_list_gyn = ['Vienna - sans aiguilles','Vienna - aiguilles', 'Mick', 'Colpostats', 'Cylindre']#

applicator_list_nonGYN =  ['Comfort Catheters-240mm', 'Comfort Catheters-294mm', 'Freiburg', 'Rectum']

#get the channel and length arrays from the dicom file import:
channels = dicom_file_HDR['channels']
lengths = dicom_file_HDR['lengths']



#Do the following for the gyn applicators:


if app_hdr in applicator_list_gyn:
	if 1 in channels:
		length1 = lengths[channels.index(1)]
	else:
		length1 = 0
	if 3 in channels:
		length3 = lengths[channels.index(3)]
	else:
		length3 = 0
	if 5 in channels:
		length5 = lengths[channels.index(5)]
	else:
		length5 = 0
		
	

if app_hdr == applicator_list_gyn[1]:
	lengths_without_gyn = lengths
	if 5 in channels:
		del lengths_without_gyn[channels.index(5)]
	#if 3 in channels:
	#	del lengths_without_gyn[channels.index(3)]
	if 1 in channels:
		del lengths_without_gyn[channels.index(1)]
		
	if lengths_without_gyn:
		delta_ch_interstitial = calcIndDelta(lengths_without_gyn,indLength_proGuide)

if app_hdr in applicator_list_nonGYN:
	#comfort cath 240 mm
	if app_hdr == applicator_list_nonGYN[0]:
		delta_ch_interstitial = calcIndDelta(lengths,indLength_comfCath240mm)
		
	#Comfort Catheters-294mm
	elif app_hdr == applicator_list_nonGYN[1]:
		delta_ch_interstitial = calcIndDelta(lengths,indLength_comfCath294mm)
	#Freiburg
	elif app_hdr == applicator_list_nonGYN[2]:
		delta_ch_interstitial = calcIndDelta(lengths,indLength_freiburg)
	#rectum
	elif app_hdr == applicator_list_nonGYN[3]:
		delta_ch_interstitial = calcIndDelta(lengths,indLength_rectum)

#uncomment the channel you want to check:		
#delta_ch1 = hdr_ch1 - length1
#delta_ch3 = hdr_ch3 - length3
#delta_ch5 = hdr_ch5 - length5

