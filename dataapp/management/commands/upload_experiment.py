from herbprofile.models import *
from datautils import *
import datautils.T2DConverter as T2dCon
import csv
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def upload_experiment(self):
        with open('experiments/experiments.csv', 'rb') as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			file_names, herb_name, usage_quantity =  row[0], row[1], row[2]
			if usage_quantity == '':
				usage_quantity = '0'
			self.upload(file_names, herb_name, int(usage_quantity))

    def handle(self, *args, **options):
        self.upload_experiment()

    def upload(self, file_names, herb_name, usage_quantity):
	    user = User.objects.get(username='admin')
	    herb = Herb.objects.filter(scientific_name=herb_name)[0]
	    inv = Inventory.objects.filter(herb=herb)[0]
	    exp_no = Experiment.objects.count() + 1

	    new_exp = Experiment(inventory=inv, experiment_no=exp_no, uploaded_by=user, operator=user, usage_quantity=usage_quantity)
	    new_exp.save()

	    # call the module by Liu Yong to convert t2d into csv and save into the same dir
	    # csv_path = get_csv_from_t2d(new_exp.t2d_file.url)
	    t2dfile_path = None
	    csv_path  =None
	    for file_name in file_names.split('*'):
			f = open('experiments/'+file_name, 'rb')
			herbprofile = HerbProfile(experiment = new_exp)
			herbprofile.file_object.save(f.name, File(f), save=True)

			t2dfile_path = herbprofile.file_object.path
			path, filename_ext = os.path.split(t2dfile_path)
			filename, extension = os.path.splitext(filename_ext)
			csv_path = herbprofile.file_object.url
			length = len(csv_path)-4
			csv_path = csv_path[:length]+".csv"

			herbprofile.csv_file = csv_path
			herbprofile.save()
			ma, csv_path = T2dCon.data_converter(path,filename ,extension, path)
			det_peaks = T2dCon.get_peaks(ma)

			# call the module by Liu Yong to get peaks from csv
			# peaks = get_peaks(new_exp.array_file)
			# save peaks into Peak table
			for peaks in det_peaks:
			    peak = Peak(experiment_id=new_exp.id, mz=peaks[0], intensity=peaks[1])
			    peak.save()
