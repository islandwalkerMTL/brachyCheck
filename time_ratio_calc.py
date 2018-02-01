####################################################
#This snippet calculates the ratio between the total 
#time in the tandem vs the total time in ring/ovoids
#for GYN bracytherapy. 
#
#ellis.mitrou.chum@ssss.gouv.qc.ca
#2017-12-27
#
##




applicator_list_gyn = ['Vienna - sans aiguilles','Vienna - aiguilles', 'Mick']


if app_hdr in applicator_list_gyn:
    ring_ovoid_time = 0
    channels = dicom_file_HDR['channels']
    ch_times = dicom_file_HDR['ch_times']
    if 1 in channels:
	    ring_ovoid_time = ch_times[channels.index(1)]

    if 3 in channels:
		ring_ovoid_time += ch_times[channels.index(3)]

    if 5 in channels:
		hdr_time_ratio = ch_times[channels.index(5)]/ring_ovoid_time

		
else:
    hdr_time_ratio = None


