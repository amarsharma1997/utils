from os import walk,mkdir
from os.path import isfile,join,getmtime,exists
from PIL import Image
import datetime
from shutil import copyfile

"""
List all the files in the source path
Check if a file is an image then get its last modified date
If that is a folder then get all files inside that folder
maintain a map of date with the file object
Once all files are listed
create a folder with the date and copy all the files with the modified date on that date

"""

class CopyManager:
	def __init__(self):
		self.fileNameOccurances = {}

	def getFileNameToCopy(self,modifieddate,filename):
		key= modifieddate + filename
		if self.fileNameOccurances.get(key) == None:
			self.fileNameOccurances[key] = 0
			return filename
		self.fileNameOccurances[key] += 1
		return "fc(" + str(self.fileNameOccurances[key])+ ") " + filename



class PathConstansts:
	source_path = "D:\\Gallery\\Random Photos"
	destination_path= "D:\\Gallery\\Sorted Photos"


class FileWithPath:
	def __init__(self,parent_dir,filename):
		self.parent_dir = parent_dir
		self.filename = filename
		self.file_path = join(parent_dir,filename)


class FileWorker:
	def __init__(self):
		self.list_of_files =[]
		self.date_file_map = {}
		self.copyManager=CopyManager()

	def list_all_files(self,path):
		print("Listing all files")
		for (dirpath, dirnames, filenames) in walk(path):
			for filename in filenames:
				file_path = join(dirpath,filename)
				### write your files extensions here
				if filename.split(".")[-1]=="mp4":
					self.list_of_files.append(FileWithPath(dirpath,filename))
					continue
				try:
					Image.open(file_path)
					self.list_of_files.append(FileWithPath(dirpath,filename))
				except Exception as e:
					print(e)

	def show_all_files(self):
		print("Total Images found: ",len(self.list_of_files))

	def map_files_with_date(self):
		for current_file in self.list_of_files:
			last_modified_date = datetime.date.fromtimestamp(getmtime(current_file.file_path))
			last_modified_date_as_string = str(last_modified_date)
			if self.date_file_map.get(last_modified_date_as_string) == None:
				self.date_file_map[last_modified_date_as_string] = []
			self.date_file_map[last_modified_date_as_string].append(current_file)

	def copy_files_in_respective_datefolder(self):
		for lastmodifieddate, fileobjects in self.date_file_map.items():
			destination_path = join(PathConstansts.destination_path, lastmodifieddate)
			print(destination_path)
			mkdir(destination_path)
			for fileobject in fileobjects:
				try:
					copyfile(fileobject.file_path, join(destination_path,self.copyManager.getFileNameToCopy(lastmodifieddate,fileobject.filename)))
				except Exception as e:
					print(fileobject.file_path + e)

if __name__ == "__main__":
	fileWorker = FileWorker()
	fileWorker.list_all_files(PathConstansts.source_path)
	fileWorker.show_all_files()
	fileWorker.map_files_with_date()
	fileWorker.copy_files_in_respective_datefolder()
	fileWorker.showStats()

