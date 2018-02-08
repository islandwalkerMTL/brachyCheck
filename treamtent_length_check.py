#######################################################################
#
# This snippet compares the maximum allowable treatment length for a given applicator
# against the treatment length in the dicom plan. A negative value means there 
# might be a point activated beyond the allowable distance
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

channel_max_rel_pos_array = dicom_file_HDR['channel_max_rel_pos_array']

max_treatment_length = max(channel_max_rel_pos_array)/10 #in cm

#The margin between the max length permitted and the distance in the dicom
margin = hdr_max_length - max_treatment_length 

result = margin