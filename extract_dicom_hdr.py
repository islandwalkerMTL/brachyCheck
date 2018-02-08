#######################################################################
#
# This script will be used to extract data from the dicom file
# that the physicist uploads. It will later be compared to the
# qatrack entry pre-treatment.
#
#
# Copyright (c) [2018] [Ellis Mitrou]
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject 
# to the following conditions: 

# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####################################################################

import dicom, sys, os.path, numpy

HDR_results = dict() #Define an empty dictionary to put all the results in


#This function gets the channel number and the indexer Length
#for each of those channels.
def getChannels(dicom_info):
    #dicom_info = pydicom.read_file(str(dicom_file))
    setupsequence = dicom_info.ApplicationSetupSequence
    channelseq = setupsequence[0].ChannelSequence
    ch_num=[]
    cath_num = []
    ind_length=[]
    ch_total_time = []
    for i in range(0,len(channelseq)):
        #this is the channel number that the catheter was mapped to.
        ch_num.append(int(channelseq[i].TransferTubeNumber))
        ind_length.append(int(channelseq[i].ChannelLength))
        ch_total_time.append(float(channelseq[i].ChannelTotalTime))
        #this is the catheter number. nucletron calls it a channel though
        cath_num.append(int(channelseq[i].ChannelNumber)) 
    return ch_num, ind_length, ch_total_time, cath_num
	
#Returns the total reference air kerma at 1 m.
def getTRAK(dicom_info):
    #dicom_info = pydicom.read_file(dicom_file)
    TRAK_1cm = float(dicom_info.ApplicationSetupSequence[0] \
        .TotalReferenceAirKerma)
    TRAK_1m = TRAK_1cm*0.0001*dicom_info.FractionGroupSequence[0] \
        .ReferencedBrachyApplicationSetupSequence[0] \
            .BrachyApplicationSetupDose
    return TRAK_1m

#Returns the prescription in cGy
def getPrescription(dicom_info):
    #dicom_info = pydicom.read_file(str(dicom_file))
    prescription = 100*float(dicom_info.FractionGroupSequence[0] \
        .ReferencedBrachyApplicationSetupSequence[0] \
            .BrachyApplicationSetupDose)
    return prescription

#Returns the patient INFO
def getPatientINFO(dicom_info):
    #dicom_info = pydicom.read_file(dicom_file)
	patient_ID = int(dicom_info.PatientID)
	patient_LASTNAME = dicom_info.PatientName.split('^')[0]
	patient_FIRSTNAME = dicom_info.PatientName.split('^')[1]
	
	
	return patient_ID, patient_LASTNAME, patient_FIRSTNAME

#Returns information about the brachy plan from the dicom
def getPlanINFO(dicom_info):
	PlanName = dicom_info.RTPlanLabel
	ApprovalStatus = dicom_info.ApprovalStatus
	return PlanName, ApprovalStatus

#Returns the total time in seconds and in minutes
def getTotalTime(dicom_info):
	channelTimes = getChannels(dicom_info)[2]
	TotalTimeSec = numpy.sum(channelTimes) # total time in seconds
	[min, sec] = (divmod(TotalTimeSec,60))
	TotalTimeMin = str(int(min)) + ':' + str(int(sec))
	
	return TotalTimeSec, TotalTimeMin


def getHDRcalibration(dicom_info):
    #This section looks inside a text file and gets 
	#the last calibration for the machine name found in the dicom
    treatment_machine_name = dicom_info.TreatmentMachineSequence[0] \
        .TreatmentMachineName
    filename = '/chum/dsp/Radio-oncologie/commun/Physique' + ' ' + \
        'radio-onco/Utilisateurs/Ellis/Projets/BrachyCheck/' + \
            'qatrack/Ir192-Activity-CHUM.txt'
    calibdate_array=[]
    treatment_machine_array = []
    air_kerma_array = []
    
    with open(filename,"r") as f:
        calib_data = f.read().splitlines()
	
	for i in range(1,len(calib_data)):
		calibdate_array.append(calib_data[i].split(',')[0].strip())
		treatment_machine_array.append(calib_data[i].split(',')[1].strip())
		air_kerma_array.append(float(calib_data[i].split(',')[2].strip()))
		

	
	
	calibration_dateCHUM = calibdate_array
	air_kermaCHUMarray = air_kerma_array
	
	
	#This part gets the dicom air kerma strength and reference date.
	
	x = dicom_info.SourceSequence[0].SourceStrengthReferenceDate
	reference_dateDICOM = x[:4] + '-' + x[4:6] + '-'+ x[6:]
	air_kermaDICOM = dicom_info.SourceSequence[0].ReferenceAirKermaRate
	
	
	
	
	return air_kermaCHUMarray, calibration_dateCHUM,  air_kermaDICOM, \
        reference_dateDICOM, treatment_machine_array

def getTreatmentLength(dicom_info):
    channel_max_rel_pos = []
    for cath in range(0,len(dicom_info.ApplicationSetupSequence[0] \
        .ChannelSequence)):
        channel_max_rel_pos.append(float((dicom_info.ApplicationSetupSequence[0] \
            .ChannelSequence[cath].BrachyControlPointSequence[-1] \
                .ControlPointRelativePosition)))
    return channel_max_rel_pos

#From Danis Blais' catphan analysis program


mode_command = False
if 'FILE' in vars() or 'FILE' in globals():
    # on recupere le nom du fichier a partir de l'objet FILE 
    # qui nous est passe et on ferme le fichier pour ne pas avoir de conflit
    filename = FILE.name
    FILE.close()
else:
    # le programme a ete lance en dehors de QATrack+
    if len(sys.argv) < 2:
        print 'SVP specifiez en argument le nom du fichier'
        quit()
    else:
        filename = str(sys.argv[1])
        if not os.path.isfile(filename):
            print "Le fichier specifie n'existe pas"
            quit()
        mode_command = True


dicom_info = dicom.read_file(filename)

HDR_results['nom_plan_HDR'] = getPlanINFO(dicom_info)[0]
HDR_results['Prescription'] = getPrescription(dicom_info)
HDR_results['patient_LASTNAME'] = getPatientINFO(dicom_info)[1]
HDR_results['patient_ID'] = getPatientINFO(dicom_info)[0]
HDR_results['patient_FIRSTNAME'] = getPatientINFO(dicom_info)[2]
HDR_results['TRAK'] = getTRAK(dicom_info)#
HDR_results['channels'] = getChannels(dicom_info)[0]
HDR_results['lengths'] = getChannels(dicom_info)[1]
HDR_results['ch_times'] = getChannels(dicom_info)[2]
HDR_results['total_time_sec'] = getTotalTime(dicom_info)[0]
HDR_results['total_time_min'] = getTotalTime(dicom_info)[1]

#source information
HDR_results['air_kermaCHUM'] = getHDRcalibration(dicom_info)[0]
HDR_results['calibration_dateCHUM'] = getHDRcalibration(dicom_info)[1]
HDR_results['air_kermaDICOM']= float(getHDRcalibration(dicom_info)[2])
HDR_results['referecence_dateDICOM']= getHDRcalibration(dicom_info)[3]
HDR_results['treatment_machine_array']= getHDRcalibration(dicom_info)[4]
HDR_results['channel_max_rel_pos_array'] = getTreatmentLength(dicom_info)

result = HDR_results

print HDR_results


