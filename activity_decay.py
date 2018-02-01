####################################################
#
#
#ellis.mitrou.chum@ssss.gouv.qc.ca
#2017-12-28
#
##

import datetime, numpy

halflife = 73.83 #days



treatment_machine_qatrack = str(hdr_machine)

kerma_dicom = float(dicom_file_HDR['air_kermaDICOM'])
kerma_calibration_chum = float(dicom_file_HDR['air_kermaCHUM'][dicom_file_HDR['treatment_machine_array'].index(treatment_machine_qatrack)])


date_calibration_raw = dicom_file_HDR['calibration_dateCHUM'][dicom_file_HDR['treatment_machine_array'].index(treatment_machine_qatrack)]

date_dicom_raw = dicom_file_HDR['referecence_dateDICOM']


#python datetime objects:
date_today = datetime.date.today()
date_dicom = datetime.date(int(date_dicom_raw.split('-')[0]),int(date_dicom_raw.split('-')[1]),int(date_dicom_raw.split('-')[2]))
date_calibration = datetime.date(int(date_calibration_raw.split('-')[0]),int(date_calibration_raw.split('-')[1]),int(date_calibration_raw.split('-')[2]))


#total treatment time from dicom in seconds
treatment_time_tps = float(dicom_file_HDR['total_time_sec'])


days_since_calibration = (date_today - date_calibration).days

kerma_today_chum = kerma_calibration_chum*numpy.exp(-numpy.log(2)*days_since_calibration/halflife)

treatment_time_chum_today = kerma_dicom*treatment_time_tps/kerma_today_chum


#get user inputed time:
flexitron_minutes = int(time_flexitron.split(':')[0])
flexitron_seconds = int(time_flexitron.split(':')[1])

#total flexitron time in seconds
flexitron_time = flexitron_minutes*60 + flexitron_seconds





diff_time = int(treatment_time_chum_today) - flexitron_time