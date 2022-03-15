from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd

	
window = Tk()
window.title('数据处理')
window.geometry('360x350') 

str_plate384filerequirement ="首先当前目录需要一个化合物Compound.csv文件，compound文件须包含MOLENAME/Plate location/cas/MolWt四列，同时这个文件设置成UTF8格式的，然后要处理的文件包含Position384列,处理后的数据保存在Position384Output.csv"
str_plate96filerequirement = "首先当前目录需要一个化合物Compound.csv文件，compound文件须包含MOLENAME/Plate location/cas/MolWt四列，同时这个文件设置成UTF8格式的，然后要处理的文件包含Position96列，处理后的数据保存在Position96Output.csv"
str_datascreeningfilerequirement = "文件表格的第一行必须要包含有Sequence/RawData/Position384/OriginalSequence四列，且RawData这一列需要是数字，处理后的数据保存在DataScreeningOutput.csv"

########数据筛选处理#############
filename_list=[] 
def chosescreeningfile():
	filepath = filedialog.askopenfilenames(filetype=[("csv file","*.csv")])
	filename_list.clear()
	filename_list.append(filepath)
	str_list= filename_list[0][0].split('/')	
	lbfile.configure(text=str_list[-1])
def datascreening():
	
	Position384 = []
	Sequence = []
	RawData = []
	df = pd.read_csv(filename_list[0][0]) 
	for (index, row) in df.iterrows():
		if float( row.RawData) > float(threshold_entry.get()) : 
			Sequence.append(row.Sequence)
			RawData.append(row.RawData)
			Position384.append(df.Position384[df.OriginalSequence.tolist().index(row.Sequence)])

	outdf1 = pd.DataFrame({'Sequence':Sequence}) 
	outdf2 = pd.DataFrame({'RawData':RawData}) 
	outdf3 = pd.DataFrame({'Position384':Position384}) 
	outdf = pd.concat([outdf1,outdf2,outdf3],axis=1)
	outdf.index = outdf.index + 1
	outdf.to_csv("DataScreeningOutput.csv")
	messagebox.showinfo('提醒',"处理完成")
def datascreeningfilerequirement():
	messagebox.showinfo('文件要求',str_datascreeningfilerequirement)
	
ttk.Label(window,justify="left", text="384板数据筛选" ).grid(column=0, row=0)
ttk.Label(window, justify="left",text="文件名：").grid(column=0, row=1) 
lbfile =ttk.Label(window, text=" ")
lbfile.grid(column=1, row=1)
ttk.Button(window, text="文件说明", command=datascreeningfilerequirement).grid(column=0, row=2)
ttk.Button(window, text="选择文件", command=chosescreeningfile).grid(column=1, row=2)
ttk.Label(window,justify="left", text="阈值：" ).grid(column=2, row=2)
threshold_entry=ttk.Entry(window,width = 8 )
threshold_entry.grid(column=3, row=2) 
threshold_entry.insert(0,"30.0")
#threshold_entry.pack()
ttk.Button(window, text="处理文件", command=datascreening).grid(column=0, row=3)

###############384转96################################

def chose384file():
	filepath = filedialog.askopenfilenames(filetype=[("csv file","*.csv")])
	filename_list.clear()
	filename_list.append(filepath)
	
	str_list= filename_list[0][0].split('/')	
	lb384.configure(text=str_list[-1])
def plate384to96():
	Alphabet_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
	plate96_list = []
	df = pd.read_csv(filename_list[0][0]) 

	compound_df = pd.read_csv('Compound.csv')

	MOLENAME_list = []
	MolWt_list = []
	cas_list =[]
	for (index, row) in df.iterrows():
		str_list=row.Position384.split()
		PlateNo = int(str_list[1])
		RowNo = Alphabet_list.index(str_list[2][0])
		ColumnNo = int(str_list[2][1:])
		
		plate96=(PlateNo-1)*4+1+(RowNo%2 *2 +(ColumnNo+1)%2)
		str_96= str(plate96)+"-"+Alphabet_list[int(RowNo/2)]+str(int((ColumnNo+1)/2))
		plate96_list.append(str_96)

		# look for compound 
		flag = False
		for (j, r) in compound_df.iterrows() : 
			if str_96 == (r['Plate location']) : 
				MOLENAME_list.append(r.MOLENAME)
				MolWt_list.append(r.MolWt)
				cas_list.append('#'+r.cas)
				flag=True
		
		if flag == False :
			MOLENAME_list.append("n/a")
			MolWt_list.append("n/a")
			cas_list.append("n/a")
			
	outdf = pd.DataFrame({'Position96':plate96_list}) 
	MOLENAMEdf = pd.DataFrame({'MOLENAME':MOLENAME_list}) 
	MolWtdf = pd.DataFrame({'MolWt':MolWt_list}) 
	casdf = pd.DataFrame({'cas':cas_list}) 

	outdf['Position384']=df['Position384']
	outdf['MOLENAME']=MOLENAMEdf['MOLENAME']
	outdf['MolWt']=MolWtdf['MolWt']
	outdf['cas']=casdf['cas']

	outdf.index = outdf.index + 1
	outdf.to_csv("Position384Output.csv")
	
	messagebox.showinfo('提醒',"处理完成") 
def plate384filerequirement() :
	messagebox.showinfo('提醒',str_plate384filerequirement)
	
ttk.Label(window, text="384板转96板" ).grid(column=0, row=6) 
ttk.Label(window, text="文件名：").grid(column=0, row=8) 
lb384 =ttk.Label(window, text=" ")
lb384.grid(column=1, row=8)

ttk.Button(window, text="文件说明", command=plate384filerequirement).grid(column=0, row=9)
ttk.Button(window, text="选择文件", command=chose384file).grid(column=1, row=9)
ttk.Button(window, text="处理文件", command=plate384to96).grid(column=0, row=10)

###################96板处理#####################
def chose96file():
	filepath = filedialog.askopenfilenames(filetype=[("csv file","*.csv")])
	filename_list.clear()
	filename_list.append(filepath) 
	
	str_list= filename_list[0][0].split('/')	
	lb96.configure(text=str_list[-1])
def plate96process():

	df = pd.read_csv(filename_list[0][0]) 

	compound_df = pd.read_csv('Compound.csv')
	MOLENAME_list = []
	MolWt_list = []
	cas_list =[]
	for (index, row) in df.iterrows():
		for (j, r) in compound_df.iterrows() : 
			if row.Position96 == (r['Plate location']) : 
				MOLENAME_list.append(r.MOLENAME)
				MolWt_list.append(r.MolWt)
				cas_list.append('#'+r.cas)
	
	outdf = pd.DataFrame( ) 
	MOLENAMEdf = pd.DataFrame({'MOLENAME':MOLENAME_list}) 
	MolWtdf = pd.DataFrame({'MolWt':MolWt_list}) 
	casdf = pd.DataFrame({'cas':cas_list}) 

	outdf['Position96']=df['Position96']
	outdf['MOLENAME']=MOLENAMEdf['MOLENAME']
	outdf['MolWt']=MolWtdf['MolWt']
	outdf['cas']=casdf['cas']

	outdf.index = outdf.index + 1
	outdf.to_csv("Position96Output.csv")
	messagebox.showinfo('提醒',"处理完成")
str_plate96filerequirement
def plate96filerequirement() :
	messagebox.showinfo('提醒',str_plate96filerequirement)
	
ttk.Label(window, text="96板处理" ).grid(column=0, row=11) 
ttk.Label(window, text="文件名：").grid(column=0, row=12) 
lb96 =ttk.Label(window, text=" ")
lb96.grid(column=1, row=12)
ttk.Button(window, text="文件说明", command=plate96filerequirement).grid(column=0, row=13)
ttk.Button(window, text="选择文件", command=chose96file).grid(column=1, row=13)
ttk.Button(window, text="处理文件", command=plate96process).grid(column=0, row=14)


window.mainloop() 