import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os, fnmatch
from threading import Thread
import subprocess as sub

#from PIL import ImageTk,Image 
import cv2
import numpy as np

import json
import h5py
from tkinter import messagebox

import sys
import ruamel.yaml

file_path1 = "cGOMSE_YpsoPod/"
file_path2 = "OGD_YpsoPod_noSkin/"

path_name = file_path1
lbl_folder = path_name + 'labels'
wgt_folder = path_name + 'weights'

#p = sub.Popen('./script',stdout=sub.PIPE,stderr=sub.PIPE)
#wrap = sub.Popen('./script',stdout=sub.PIPE,stderr=sub.PIPE)

class Contain_App(tk.Tk):
	def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
         
		self.geometry("820x550")
        # creating a container
		container = tk.Frame(self) 
		container.pack(side = "top", fill = "both", expand = True)
  
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
		self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
		for F in (StartPage, Page_cGOMSE, Results_cGOMSE, Page_OGD):
  
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky ="nsew")
  
		self.show_frame(StartPage)
  
    # to display the current frame passed as
    # parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
		frame.update()
		frame.event_generate("<<ShowFrame>>")



class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
				
		#Choose algorithm using Combobox
		tk.Label(self, text = "Select Algorithm :",
			font = ("Times New Roman", 10)).grid(column = 0,
			row = 1, padx = 10, pady = 25)
		# Combobox creation
		p = tk.StringVar()
		algorithmchosen = ttk.Combobox(self, width = 27, textvariable = p)
  
		# Adding combobox drop down list
		a_list = ['cGOMSE: Screen Matching',
		'OGD: Object Gaze Distance']
		algorithmchosen['values'] = a_list
		#algo_choice = algorithmchosen.get()
		algorithmchosen.current(1)
		algorithmchosen.grid(column = 1, row = 1)


		# Place the browsebutton onto the grid
		browse_button = tk.Button(self, text="Select File Path", padx=42, pady=15, command=lambda: self.select_filepath(algorithmchosen))
		browse_button.grid(row=6, column=1, pady=10)

		choose_config = tk.Button(self, text="Confirm Algorithm", padx=42, pady=15, command= lambda: self.next_frame(algorithmchosen,controller))
		choose_config.grid(row=7, column=1, pady=10)


	def next_frame(self,algorithmchosen,controller):
		algo_choice = algorithmchosen.get()

		if algo_choice == 'cGOMSE: Screen Matching':
			controller.show_frame(Page_cGOMSE)
	
		elif algo_choice == 'OGD: Object Gaze Distance':
			controller.show_frame(Page_OGD)


	def select_filepath(self,algorithmchosen):
		algo_choice = algorithmchosen.get()
		global path_name
		global path_label_chosen

		if algo_choice == 'cGOMSE: Screen Matching':
			init_dir = file_path1
		elif algo_choice == 'OGD: Object Gaze Distance':
			init_dir = file_path2

		self.filename = filedialog.askdirectory(initialdir=init_dir, title = "Select a Folder")
		path_name = self.filename
		path_label_chosen = tk.Label(self, anchor = 'w',wraplength = 450,text = "Chosen Directory: {0}".format(self.filename))
		path_label_chosen.grid(sticky = 'w',row = 6, column = 2)
		#change the directory
		os.chdir(path_name)

class cGOMSE_Execute(Thread):
	def __init__(self,a,b,c,d,name_UI,pgb):
		super().__init__()
		self.match = a
		self.warp = b
		self.ref = c
		self.image = d
		self.name_UI = name_UI
		self.bar = pgb

	def run(self):
	
		os.chdir('toolbox/')

		if	os.system('python make_gaze.py --showMatch '+ self.match + ' --showWarp ' + self.warp + ' --showReference ' + self.ref + ' --saveImages ' + self.image + ' --UI_class ' + self.name_UI) == 0 :
			messagebox.showerror(title="Done.",message="Success! 'make_gaze' executed")
		else:
			self.bar.stop()
			messagebox.showerror(title="Error",message="Error in executing file. 'labels' and 'weights' files may not match.")
		
		os.chdir('..')
		self.bar.destroy() #optional

	
			

class Page_cGOMSE(tk.Frame):
	def __init__(self,parent,controller, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		yaml = ruamel.yaml.YAML()

		with open(path_name +'toolbox/default_configs/make_gaze.yaml') as fin:
			read_data = yaml.load(fin)
			default_dil = read_data["dilation"]
			default_wgt = read_data["weights_path"][11:]
			default_lbl = read_data["label_dir"][10:]

		#print(default_dil,default_wgt,default_lbl)

		wgt_file_button = tk.Button(self, text="Select 'weights' folder", padx=5, pady=5, command=lambda: self.select_folder("weight",weightchosen))
		wgt_file_button.grid(row=0, column=2, pady=5)

		#choosing weight file using Combobox
		tk.Label(self, text = "Select file in '\weight' path :").grid(row = 0,
			column = 3, padx = 5, pady = 5)
		# Combobox creation
		n = tk.StringVar()
		weightchosen = ttk.Combobox(self, width = 25, textvariable = n)

		w_list = fnmatch.filter(os.listdir(path_name + 'weights'), '*.h5') 
		# Adding combobox drop down list
		weightchosen['values'] = w_list
		weightchosen.set(default_wgt)
		weightchosen.grid(row = 0, column = 4)

		lbl_file_button = tk.Button(self, text="Select 'labels' folder", padx=5, pady=5, command=lambda: self.select_folder("label",labelchosen))
		lbl_file_button.grid(row=1, column=2, pady=5)

		#choosing label file using Combobox
		tk.Label(self, text = "Select file in '\label' path :").grid(row = 1,
			column = 3, padx = 5, pady = 5)
		# Combobox creation
		m = tk.StringVar()
		labelchosen = ttk.Combobox(self, width = 25, textvariable = m)


		l_list = fnmatch.filter(os.listdir(path_name + 'labels'), '*.json') 
		# Adding combobox drop down list
		labelchosen['values'] = l_list
		labelchosen.set(default_lbl)
		labelchosen.grid(row = 1, column = 4)

		lbl_go = tk.Button(self, text="Go", padx=5, pady=2, command=lambda: self.list_lbl(yaml,labelchosen,weightchosen,entry_dilations,entry_cl_weights))
		lbl_go.grid(row=1, column=6, pady=10, padx =5)

		#Number of dilations
		entry_dilations = tk.Entry(self, width = 20)
		lbl_dilations = tk.Label(self, text="Number of dilations:")
		entry_dilations.insert(0, default_dil) # default
		lbl_dilations.grid(row=2, column=2,padx = 5, pady = 5)
		entry_dilations.grid(row=2, column=3)
           
    
		#number of class weights
		entry_cl_weights = tk.Entry(self, width=20)
		lbl_cl_weights = tk.Label(self, text="Number of class weights:")

		lbl_cl_weights.grid(row=3, column=2,padx = 5, pady = 5)
		entry_cl_weights.grid(row=3, column=3)



		# Place the applybutton onto the grid
		apply_button = tk.Button(self, text="Apply", padx=30, pady=10, command= lambda: self.apply_config_cGOMSE(yaml,entry_dilations,entry_cl_weights,weightchosen,labelchosen))
		apply_button.grid(row=5, column=3, padx=50, pady=20)

		showmatch_check = tk.BooleanVar()
		showwarp_check = tk.BooleanVar()
		showref_check = tk.BooleanVar()
		saveimg_check = tk.BooleanVar()
		UIname_check = tk.BooleanVar()

		c1 = tk.Checkbutton(self, text='Show Matches', width=20, variable=showmatch_check, onvalue='True', offvalue='False', anchor="w")
		c1.grid(row=8, column=3)

		c2 = tk.Checkbutton(self, text='Show Warp', width=20, variable=showwarp_check, onvalue='True', offvalue='False', anchor="w")
		c2.grid(row=9, column=3)

		c3 = tk.Checkbutton(self, text='Show Reference', width=20, variable=showref_check, onvalue='True', offvalue='False', anchor="w")
		c3.grid(row=10, column=3)

		c4 = tk.Checkbutton(self, text='Save Images', width=20, variable=saveimg_check, onvalue='True', offvalue='False', anchor="w")
		c4.grid(row=11, column=3)

		c5 = tk.Checkbutton(self, text='Name of UI object: ', width=20, variable=UIname_check, onvalue='True', offvalue='False', anchor="w")
		c5.grid(row=12, column=3)

		frm_UI = tk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
		#lbl_UI = Label(frm_UI, text="Phone", width=15)

		entry_UI = tk.Entry(frm_UI, width = 15)
		entry_UI.delete(0, tk.END)
		entry_UI.insert(0, "Phone")
		entry_UI.grid(row=0, column=0,sticky="w")

		#lbl_UI.grid(row=0, column=0,sticky="w")
		frm_UI.grid(row=12, column=4,sticky="w")

		# Place the applybutton onto the grid
		next_button = tk.Button(self, text="Run Algorithm \N{RIGHTWARDS BLACK ARROW}", padx=30, pady=10, command= lambda: self.next_window(entry_UI,showmatch_check,showwarp_check,showref_check,saveimg_check))
		next_button.grid(row=13, column=3, padx=50, pady=20)

		back_button = tk.Button(self, text="Back", padx=20, pady=8, command= lambda: controller.show_frame(StartPage))
		back_button.grid(row=14, column=2, padx=20, pady=10)

		results_button = tk.Button(self, text="See Results", padx=20, pady=8, command= lambda: controller.show_frame(Results_cGOMSE))
		results_button.grid(row=14, column=5, padx=20, pady=10)


	def list_lbl(self,yaml,labelchosen,weightchosen,entry_dilations,entry_cl_weights):
		label_new = labelchosen.get()
		weight_new = weightchosen.get()
		keys = []

		with open(path_name +'/toolbox/default_configs/make_gaze.yaml') as fin:
			read_data = yaml.load(fin)

			dil_new = read_data["dilation"]

			entry_dilations.delete(0, tk.END)
			entry_dilations.insert(0, dil_new)



	def select_folder(self,fol_type,factorchosen):
		global lbl_folder
		global wgt_folder

		self.filename = filedialog.askdirectory(initialdir=path_name, title = "Select a Folder")
		
		if fol_type=='weight':
			wgt_folder = self.filename
			rw = 0
			w_list = fnmatch.filter(os.listdir(wgt_folder), '*.h5') 
			factorchosen['values'] = w_list

		elif fol_type=='label':
			lbl_folder = self.filename
			rw = 1
			l_list = fnmatch.filter(os.listdir(lbl_folder), '*.json') 
			factorchosen['values'] = l_list


		
	def apply_config_cGOMSE(self,yaml,entry_dilations,entry_cl_weights,weightchosen,labelchosen):
		dil_new = entry_dilations.get()
		cl_wgts_new = entry_cl_weights.get()
		wgt_new = weightchosen.get()
		label_new = labelchosen.get()

    
		lbl_confirm = tk.Label(self, text="Configurations set!")
		lbl_confirm.grid(row=7, column=3,padx = 3, pady = 5)
    
		with open(path_name + '/toolbox/default_configs/make_gaze.yaml') as fin:
			alter_data = yaml.load(fin)
			alter_data["dilation"] = int(dil_new)
			alter_data["weights_path"] = '../weights/'+ wgt_new
			alter_data["label_dir"] = '../labels/'+ label_new  

		#print(dil_new,wgt_new,label_new)
    
		#overwrites .yaml file. BEWARE before making changes: this opens file in write mode, i.e. wipes the file clean while opening
		with open(path_name + '/toolbox/default_configs/make_gaze.yaml','w') as fp:
			yaml.dump(alter_data, fp)

		#with open('../../02_Algorithms/cGOMSE_YpsoPod/toolbox/default_configs/make_gaze.yaml') as fp:
		 #   yaml.dump(alter_data, sys.stdout)

		with open(path_name + '/labels/'+label_new) as fjson:
			label_data = json.load(fjson)
			num_wgt = len(label_data)
			entry_cl_weights.delete(0, tk.END)
			entry_cl_weights.insert(0, num_wgt)


	def next_window(self,entry_UI,showmatch_check,showwarp_check,showref_check,saveimg_check):

		name_UI = entry_UI.get()
		#d = showmatch_check.get()
		#print(d,showwarp_check.get(),showref_check.get(),saveimg_check)
		a = str(showmatch_check.get())
		b = str(showwarp_check.get())
		c = str(showref_check.get())
		d = str(saveimg_check.get())

		pgb = ttk.Progressbar(self, orient = tk.HORIZONTAL, length = 200, mode = 'determinate' )
		pgb.grid(row=13, column=4, padx=50, pady=10)
		pgb.start(20)

		#abort_button  = tk.Button(self, text="Abort", padx=30, pady=10, command= lambda: self.abort())
		#abort_button.grid(row=14, column=5, padx=50, pady=10)

		exec_algo = cGOMSE_Execute(a,b,c,d,name_UI,pgb)
		exec_algo.start()


class Results_cGOMSE(tk.Frame):
	def __init__(self,parent,controller, *args, **kwargs):
		tk.Frame.__init__(self, parent)


		# Place the applybutton onto the grid
		att_metrics_button = tk.Button(self, text="Attention Metrics", padx=30, pady=10, command= lambda: self.att_metrics())
		att_metrics_button.grid(row=2, column=2, padx=50, pady=20)

		heat_maps_button = tk.Button(self, text="Heat Maps", padx=30, pady=10, command= lambda: self.heat_maps())
		heat_maps_button.grid(row=3, column=2, padx=50, pady=20)

	def att_metrics(self):
		lbl_metrics = tk.Label(self, text="something something about data")
		lbl_metrics.grid(row=2, column=3,padx = 5, pady = 5)

	def heat_maps(self):
		#heat_canvas = tk.Canvas(self,width = 500, height = 500
		img_path = path_name + '/outputs/heatmaps/'
		#img = ImageTk.PhotoImage(Image.open(img_path))
		#heat_canvas.create_image(10,10, image=img) 
		list_dir_img = fnmatch.filter(os.listdir(img_path), '*.jpgnewest.jpg')

		for study_name in list_dir_img:
			img = cv2.imread(img_path+study_name)
			cv2.imshow(study_name,img)
			cv2.waitKey(1)
		
		destroy_button = tk.Button(self, text="Destroy All Windows", padx=30, pady=10, command= lambda: self.destroy_windows(cv2))
		destroy_button.grid(row=3, column=4, padx=50, pady=20)

	def destroy_windows(self,cv2):
		cv2.destroyAllWindows()



class OGD_Execute(Thread):
	def __init__(self,cmmnd,pgb):
		super().__init__()
		self.cmmnd = cmmnd
		self.bar = pgb

	def run(self):
	
		#IMPORTANT NOTE: os.system uses 'exit code of the method' to indicate failure, which is why if any error occurs during execution of this python file, it will return != 0 and it will not be possible to distinguish which error occurred.
		#Therefore, please check whether 'labels' and 'weights' not matching is the actual cause. If it is, you will see error of type:
		#"ValueError: Layer #389 (named "mrcnn_bbox_fc"), weight <tf.Variable 'mrcnn_bbox_fc/kernel:0' shape=(1024, 24) dtype=float32_ref> has shape (1024, 24), but the saved weight has shape (1024, 36)" 

		if (self.cmmnd == 'gaze'):

			if	os.system('python toolbox/make_gaze_OGD.py') == 0 :
				messagebox.showerror(title="Done.",message="Success! 'make_gaze' executed")
			else:
				self.bar.stop()
				messagebox.showerror(title="Error",message="Error in executing file. 'labels' and 'weights' files may not match.")
		
			self.bar.destroy() #optional

		elif (self.cmmnd == 'video'):

			if	os.system('python toolbox/make_gaze_OGD.py') == 0 :
				messagebox.showerror(title="Done.",message="Success! 'make_video' executed")
			else:
				self.bar.stop()
				messagebox.showerror(title="Error",message="Error in executing file. 'labels' and 'weights' files may not match.")
		
			self.bar.destroy() #optional
		




class Page_OGD(tk.Frame):
	def __init__(self, parent,controller, *args, **kwargs):
		tk.Frame.__init__(self, parent)

		yaml = ruamel.yaml.YAML()

		with open(file_path2 +'/toolbox/default_configs/make_gaze.yaml') as fin:
			read_data = yaml.load(fin)
			default_dil = read_data["dilations"]
			default_cl_weights_pic = read_data["class_weights"]
			default_wgt = read_data["weights_path"][11:]
			default_lbl = read_data["label_dir"][10:]

		#print(default_dil,default_wgt,default_lbl)
		#default_dil = self.count_dil(default_dil_pic)
		default_cl_weights = self.count_dil(default_cl_weights_pic)


		wgt_file_button = tk.Button(self, text="Select 'weights' folder", padx=5, pady=5, command=lambda: self.select_folder("weight",weightchosen))
		wgt_file_button.grid(row=0, column=2, pady=5)


		#choosing weight file using Combobox
		tk.Label(self, text = "Select file in '\weight' path :").grid(row = 0,
			column = 3, padx = 5, pady = 5)
		# Combobox creation
		n = tk.StringVar()
		weightchosen = ttk.Combobox(self, width = 30, textvariable = n)

		w_list = fnmatch.filter(os.listdir(path_name + '/weights'), '*.h5') 
	
		weightchosen['values'] = w_list
		weightchosen.set(default_wgt)
		weightchosen.grid(row = 0, column = 4, padx = 40)

		lbl_file_button = tk.Button(self, text="Select 'labels' folder", padx=5, pady=5, command=lambda: self.select_folder("label",labelchosen))
		lbl_file_button.grid(row=1, column=2, pady=5)


		#choosing label file using Combobox
		tk.Label(self, text = "Select file in '\label' path :").grid(row = 1,
			column = 3, padx = 5, pady = 5)
		# Combobox creation
		m = tk.StringVar()
		labelchosen = ttk.Combobox(self, width = 30, textvariable = m)


		l_list = fnmatch.filter(os.listdir(path_name + '/labels'), '*.json') 
		# Adding combobox drop down list
		labelchosen['values'] = l_list
		labelchosen.set(default_lbl)
		labelchosen.grid(row = 1, column = 4, padx = 40)

		lbl_go = tk.Button(self, text="Go", padx=5, pady=2, command=lambda: self.list_lbl(labelchosen,weightchosen,entry_dilations,entry_cl_weights))
		lbl_go.grid(row=1, column=5, pady=5, padx =5)


		#Number of dilations
		entry_dilations = tk.Entry(self, width = 20)
		lbl_dilations = tk.Label(self, text="Dilations:")
		entry_dilations.insert(0, default_dil) # default
		lbl_dilations.grid(row=2, column=2,padx = 5, pady = 5)
		entry_dilations.grid(row=2, column=3)

		#number of class weights
		entry_cl_weights = tk.Entry(self, width=20)
		lbl_cl_weights = tk.Label(self, text="Number of class weights:")
		entry_cl_weights.insert(0, default_cl_weights) # default
		lbl_cl_weights.grid(row=3, column=2,padx = 5, pady = 5)
		entry_cl_weights.grid(row=3, column=3)


		# Place the applybutton onto the grid
		apply_button = tk.Button(self, text="Apply", padx=30, pady=10, command= lambda: self.apply_config_OGD(yaml,entry_dilations,entry_cl_weights,weightchosen,labelchosen))
		apply_button.grid(row=5, column=3, padx=50, pady=25)

		mask_button = tk.Button(self, text="Make Mask \N{RIGHTWARDS BLACK ARROW}", padx=30, pady=10, command= lambda: self.make_mask_exec())
		mask_button.grid(row=13, column=3, padx=50, pady=10)

		video_button = tk.Button(self, text="Make Gaze Video \N{RIGHTWARDS BLACK ARROW}", padx=30, pady=10, command= lambda: self.make_video_exec())
		video_button.grid(row=15, column=3, padx=50, pady=10)

		gaze_button = tk.Button(self, text="Make Gaze \N{RIGHTWARDS BLACK ARROW}", padx=30, pady=10, command= lambda: self.make_gaze_exec())
		gaze_button.grid(row=14, column=3, padx=50, pady=10)

		back_button = tk.Button(self, text="Back", padx=30, pady=8, command= lambda: controller.show_frame(StartPage))
		back_button.grid(row=16, column=2, padx=20, pady=10)

		self.bind("<<ShowFrame>>", self.update_options(weightchosen,labelchosen))
		#self.bind("<<ShowFrame>>", self.test_class())

	def update_options(self, weightchosen,labelchosen):
		w_list = fnmatch.filter(os.listdir(path_name + '/weights'), '*.h5') 
		weightchosen['values'] = w_list

		l_list = fnmatch.filter(os.listdir(path_name + '/labels'), '*.json') 
		labelchosen['values'] = l_list

	
	def test_class(self):
		print("testing testing 123")
		

	def list_lbl(self,labelchosen,weightchosen,entry_dilations,entry_cl_weights):
		label_new = labelchosen.get()
		weight_new = weightchosen.get()
		keys = []
		
		with open(lbl_folder+'/'+label_new) as fjson:
			label_data = json.load(fjson)
			num_wgt = len(label_data)

			lbl_dilations_list = tk.Label(self, wraplength = 300)
			lbl_dilations_list['text'] = ""
			lbl_dilations_list['text'] = label_data
			lbl_dilations_list.grid(row=3, column=4,padx = 5, pady = 5)

			cl_weights_new_pic = self.make_dil(num_wgt-1)

			entry_dilations.delete(0, tk.END)
			entry_dilations.insert(0, cl_weights_new_pic)

			entry_cl_weights.delete(0, tk.END)
			entry_cl_weights.insert(0, num_wgt-1)

		#with h5py.File(wgt_folder + '/' + weight_new,'r') as f: # open file
			#for layer, g in f.items():
				#print(" {} with Group: {}".format(layer, g))

		#if len(label_data) != 10 :
			#messagebox.showerror(title="Error",message=" 'labels' and 'weights' do not match")


	def select_folder(self,fol_type,factorchosen):
		global lbl_folder
		global wgt_folder

		self.filename = filedialog.askdirectory(initialdir=path_name, title = "Select a Folder")
		
		if fol_type=='weight':
			wgt_folder = self.filename
			rw = 0
			w_list = fnmatch.filter(os.listdir(wgt_folder), '*.h5') 
			factorchosen['values'] = w_list

		elif fol_type=='label':
			lbl_folder = self.filename
			rw = 1
			l_list = fnmatch.filter(os.listdir(lbl_folder), '*.json') 
			factorchosen['values'] = l_list


	def count_dil(self, def_pic):
		x = int(len(def_pic)/2 + 1)
		return x

	def make_dil(self,def_dil):
		def_cl_wgt = int(def_dil)
		x = "1"
		for i in range(def_cl_wgt-1):
			x = x + "_1"
		return x


	def apply_config_OGD(self,yaml,entry_dilations,entry_cl_weights,weightchosen,labelchosen):
		dil_new = entry_dilations.get()
		cl_weights_new = entry_cl_weights.get()
		wgt_new = weightchosen.get()
		label_new = labelchosen.get()

		#print(dil_new,wgt_new,label_new)
		#dil_new_pic = self.make_dil(dil_new)
		cl_weights_new_pic = self.make_dil(cl_weights_new)
    
		lbl_confirm = tk.Label(self, text="Configurations set!")
		lbl_confirm.grid(row=7, column=3,padx = 3, pady = 5)
    
		with open(path_name + '/toolbox/default_configs/make_gaze.yaml') as fin:
			alter_data = yaml.load(fin)
			alter_data["dilations"] = str(dil_new)
			alter_data["class_weights"] = str(cl_weights_new_pic)
			alter_data["weights_path"] = 'weights/'+ wgt_new
			alter_data["label_dir"] = 'labels/' + label_new

		#print(dil_new,wgt_new,label_new)
    
		#overwrites .yaml file. BEWARE before making changes: this opens file in write mode, i.e. wipes the file clean while opening
		with open(path_name + '/toolbox/default_configs/make_gaze.yaml','w') as fp:
			yaml.dump(alter_data, fp)

		#with open('../../02_Algorithms/cGOMSE_YpsoPod/toolbox/default_configs/make_gaze.yaml') as fp:
		 #   yaml.dump(alter_data, sys.stdout)

		with open(path_name + '/labels/'+label_new) as fjson:
			label_data = json.load(fjson)
			num_wgt = len(label_data)
			entry_cl_weights.delete(0, tk.END)
			entry_cl_weights.insert(0, num_wgt-1)

	def abort(self):
		print('trying to abort')

		#self.stop_threads.set()
        #self.thread1.join()
        #self.thread2.join()
        #self.thread1 = None
        #self.thread2 = None


	def make_mask_exec(self):
		print(os.getcwd())
		os.system('python toolbox/make_mask.py')

	def make_gaze_exec(self):
	
		pgb = ttk.Progressbar(self, orient = tk.HORIZONTAL, length = 200, mode = 'determinate' )
		pgb.grid(row=14, column=4, padx=50, pady=10)
		pgb.start(20)

		abort_button  = tk.Button(self, text="Abort", padx=30, pady=10, command= lambda: self.abort())
		abort_button.grid(row=14, column=5, padx=50, pady=10)

		exec_algo = OGD_Execute('gaze',pgb)
		exec_algo.start()

		#if	os.system('python toolbox/make_gaze_OGD.py') == 0 :
		#	print("Operation successful")
		#else:
		#	messagebox.showerror(title="Error",message="Error in executing algorithm. 'labels' and 'weights' files may not match.")


	def make_video_exec(self):
		pgb = ttk.Progressbar(self, orient = tk.HORIZONTAL, length = 200, mode = 'determinate' )
		pgb.grid(row=15, column=4, padx=50, pady=10)
		pgb.start(20)

		exec_algo = OGD_Execute('video',pgb)
		exec_algo.start()

		#os.system('python misc/make_mask_gaze_videoOGD.py')

	
		
root = Contain_App()
root.mainloop()