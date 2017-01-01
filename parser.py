import dicom
import os
from os.path import isfile, join


class AnalyzeDicom:
    def __init__(self, dic_input_path, img_path, data_path, dic_output_path):
        self.image_path = img_path
        self.dicom_input_path = dic_input_path
        self.data_path = data_path
        self.dicom_output_path = dic_output_path

    def list_dicoms(self):
        all_dicoms = [f for f in os.listdir(self.dicom_input_path) if isfile(join(self.dicom_input_path, f))]

        counter = 1
        jpeg_files = []
        for dicom_file in all_dicoms:
            ds = dicom.read_file(self.dicom_input_path + dicom_file)
            if counter == 1:
                if not os.path.exists(self.data_path):
                    os.makedirs(self.data_path)
                file_name = ds.SOPInstanceUID + '.txt'
                with open(os.path.join(self.data_path, file_name), 'wb') as temp_file:
                    temp_file.write(str(ds))

            if not os.path.exists(self.image_path):
                os.makedirs(self.image_path)
            os.system('dcmj2pnm %s %s' % (self.dicom_input_path + '/' + dicom_file, self.image_path + '/' + ds.SOPInstanceUID + '.png'))
            counter += 1


    def convert_jpeg_to_dicoms(self):
        all_images = [f for f in os.listdir(self.image_path) if isfile(join(self.image_path, f))]

        for jpeg_images in all_images:
            base = os.path.basename(self.image_path + jpeg_images)
            get_file_name = os.path.splitext(base)[0]
            # print get_file_name
            os.system('img2dcm %s %s' % (self.image_path + '/' + jpeg_images, self.dicom_output_path + '/' + get_file_name + '.dcm'))
            print str(get_file_name) + '.dcm'


dicoms = AnalyzeDicom('orders/', 'images/', 'data/', 'outputs/')
dicoms.list_dicoms()
# dicoms.convert_jpeg_to_dicoms()
