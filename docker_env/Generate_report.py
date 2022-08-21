#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version_info__ = ('1','9','2')

#############################################
# written by thomas.billaut@protonmail.com  #
# date 7/21/22                              #
# source on github                          #
#############################################

from fpdf import FPDF
from PIL import Image
import working_on_mitre_group
from sys import exit
from sys import platform
import os
import json
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.transforms import IdentityTransform
import yaml
import json
import pickle
import pandas as pd
from openhunt import visualizations as vis
from pandas.core.accessor import register_series_accessor
import argparse
from get_mitre_and_ossem_data import get_group
from get_mitre_and_ossem_data import get_ossem_data
import seaborn as sns
from making_kpi import draw_indicator
from clean_encoding import clean

plt.rcParams['figure.dpi'] = 150
matplotlib.rc('ytick', labelsize=7)


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        #self.image('logo.png', 160, 10, 33)
        #self.set_font('Arial', 'B', 15)
        self.set_font('Arial', 'B', 8)
        # Calculate width of title and position
        w = self.get_string_width(title) + 10
        self.set_x((200 - w) / 2)
        # Colors of frame, background and text
        #self.set_draw_color(0, 80, 180)
        #self.set_fill_color(230, 230, 0)
        #self.set_fill_color(200, 220, 255)
        #self.set_text_color(220, 50, 50)
        #self.set_text_color(82, 84, 93)
        # Thickness of frame (1 mm)
        #self.set_line_width(1)
        # Title
        self.set_text_color(128)
        #self.cell(w, 9, title, 0, 1, 'C', 1)
        self.cell(w, 9, title, 0, 0, 'C', 0)
        pdf.set_draw_color(213, 216, 220 )
        self.line(30,20,180,20)
        # Line break
        self.ln(12)

    def footer(self):
        # Position at 1.5 cm from bottom
        pdf.set_draw_color(213, 216, 220 )
        self.line(30,280,180,280)
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
        #self.cell(0, 10, author, 0, 0, 'L')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 13)
        # Background color
        #self.set_fill_color(200, 220, 255)
        #self.set_fill_color(40, 116, 166) 
        self.set_fill_color(93, 109, 126)
        # Title
        #self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        self.cell(0, 6, '%d.    %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_subtitle(self, numChapter, numSubchapter, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        #self.set_fill_color(200, 220, 255)
        #self.set_fill_color(93, 173, 226)
        self.set_fill_color(174, 182, 191 )
        # Title
        #self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        self.cell(0, 6, '       %d.%d    %s' % (numChapter, numSubchapter, label), 0, 1, 'L', 1)
        # Line break
        self.ln(2)

    def chapter_body(self, name):
        # Read text file
        with open(name, 'r') as fh:
            txt = (fh.read())
            #print(type(txt))
            #print(txt[38217:])
            if platform == 'linux' :
                txt.encode('cp1252', 'ignore')
            elif platform == 'win32' :
                txt.encode('latin-1', 'ignore')
            #print(type(txt))
            #print(txt)
            #txt = temp_txt.decode('latin-1', 'ignore')
            #txt = str(fh.read())
        # Times 12
        self.set_font('Arial', '', 9)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        #self.set_font('', 'I')
        #self.cell(0, 5, '\n')
        #self.ln()

    def chapter_body_annexe(self, name):
        # Read text file
        with open(name, 'r') as fh:
            txt = (fh.read())
            if platform == 'linux' :
                txt.encode('cp1252', 'ignore')
            elif platform == 'win32' :
                txt.encode('latin-1', 'ignore')
        self.set_font('Arial', '', 7)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()


    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)
    
    def print_subchapter(self, numChapter, numSubChapter, title, name):
        #self.add_page()
        self.chapter_subtitle(numChapter, numSubChapter, title)
        self.chapter_body(name)

    def print_subchapter_annexe(self, numChapter, numSubChapter, title, name):
        #self.add_page()
        self.chapter_subtitle(numChapter, numSubChapter, title)
        self.chapter_body_annexe(name)


def print_group_chapter(out_dir, pdf):
    file_list = os.listdir(out_dir)
    with open(out_dir + 'c1.txt','w') as f:
        f.write(chapter_1)
    f.close
    pdf.print_chapter(1, 'Threat Groups', out_dir +'c1.txt')
    sub_chapt = 1
    while True:
        sub_chapt_file = "c1_" + str(sub_chapt) +".txt"
        sub_chapt_file_modified = "c1_" + str(sub_chapt) +"_m.txt"
        if sub_chapt_file in file_list:
            with open(out_dir + sub_chapt_file,'r') as f:
                sub_chapt_name_lines = f.readlines()
                sub_chapt_name = sub_chapt_name_lines[0]
                with open(out_dir + sub_chapt_file_modified,'w') as g:
                    for line in sub_chapt_name_lines[1:]:
                        g.writelines(line)
                g.close()
            f.close()
            pdf.print_subchapter(1, sub_chapt, sub_chapt_name, out_dir + sub_chapt_file_modified)
            sub_chapt += 1
        else:
            break
    return 0


def resize_png(out_dir):
    """ Resize all png for pdf printing.

    :param out_dir: output directory where images are generated
    :type out_dir: string
    """
    file_list = os.listdir(out_dir)
    for im in file_list:
        if im.split(".")[1] == 'png':
            if not (im.split(".")[0].rfind("resize") > 0) :
                if (im.split(".")[0].rfind("data_source") > -1) :
                    image = Image.open(out_dir + im)
                    imageBox = image.getbbox()
                    cropped = image.crop(imageBox)
                    #image_size = image.size
                    image_size = cropped.size
                    new_image_size = (int(image_size[0]/3), int(image_size[1]/3) )
                    #resized_image = image.resize(new_image_size)
                    resized_image = cropped.resize(new_image_size)
                    resized_image.save(out_dir + im.split(".")[0] +'_resize.png')
                    image.close()
                elif (im.split(".")[0].rfind("indicators") > -1) :
                    image = Image.open(out_dir + im)
                    imageBox = image.getbbox()
                    cropped = image.crop(imageBox)
                    #image_size = image.size
                    image_size = cropped.size
                    new_image_size = (int(image_size[0]/1.5), int(image_size[1]/1.5) )
                    #resized_image = image.resize(new_image_size)
                    resized_image = cropped.resize(new_image_size)
                    resized_image.save(out_dir + im.split(".")[0] +'_resize.png')
                    image.close()
                elif im.split(".")[0].rfind("attack") > -1:
                    image = Image.open(out_dir + im)
                    w, h = image.size
                    cropped = image.crop((200,0,w-50,h))
                    #image_size = image.size
                    image_size = cropped.size
                    #print(image_size)
                    new_image_size = (int(image_size[0]/3), int(image_size[1]/3) )
                    #print(new_image_size)
                    #resized_image = image.resize(new_image_size)
                    resized_image = cropped.resize(new_image_size)
                    resized_image.save(out_dir + im.split(".")[0] +'_resize.png')
                    image.close()
                elif im.split(".")[0].rfind("tactic") > -1:
                    image = Image.open(out_dir + im)
                    imageBox = image.getbbox()
                    cropped = image.crop(imageBox)
                    #image_size = image.size
                    image_size = cropped.size
                    #print(image_size)
                    new_image_size = (int(image_size[0]/2), int(image_size[1]/2) )
                    #print(new_image_size)
                    #resized_image = image.resize(new_image_size)
                    resized_image = image.resize(new_image_size)
                    resized_image.save(out_dir + im.split(".")[0] +'_resize.png')
                    image.close()
                else :
                    image = Image.open(out_dir + im)
                    imageBox = image.getbbox()
                    cropped = image.crop(imageBox)
                    #image_size = image.size
                    image_size = cropped.size
                    new_image_size = (int(image_size[0]/3), int(image_size[1]/3) )
                    #resized_image = image.resize(new_image_size)
                    resized_image = cropped.resize(new_image_size)
                    resized_image.save(out_dir + im.split(".")[0] +'_resize.png')
                    image.close()
    return 0


def size_image_in_mm(im):
    image = Image.open(im)
    image_size = image.size
    len_x = int(image_size[0] * 24.5 /72 )
    len_y = int(image_size[1] * 24.5 /72 )
    image.close()
    return (len_x,len_y)


def print_chapter_2(out_dir,pdf):
    with open(out_dir + 'c2.txt','w') as f:
        f.write(chapter_2)
    f.close
    with open(out_dir + 'c2_1.txt','w') as f:
        f.write(chapter_2_1)
    f.close
    with open(out_dir + 'c2_2.txt','w') as f:
        f.write(chapter_2_2)
    f.close
    with open(out_dir + 'c2_3.txt','w') as f:
        f.write(chapter_2_3)
    f.close
    with open(out_dir + 'c2_4.txt','w') as f:
        f.write(chapter_2_4)
    f.close
    with open(out_dir + 'c2_5.txt','w') as f:
        f.write(chapter_2_5)
    f.close
    with open(out_dir + 'c2_6.txt','w') as f:
        f.write(chapter_2_5)
    f.close
    with open(out_dir + 'c2_7.txt','w') as f:
        f.write(chapter_2_7)
    f.close
    pdf.print_chapter(2, 'What TTPs to prioritize for detection ?', out_dir + 'c2.txt')
    pdf.image( out_dir + "key_indicators_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    #print(pdf.get_x(),pdf.get_y())
    pdf.print_subchapter(2, 1, "Tactics distribution", out_dir + "c2_1.txt")
    pdf.image( out_dir + "mitre_group_" + targeted_sector.lower() + "_repart_techid_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(2, 2, "Technique distribution", out_dir + "c2_2.txt")
    pdf.image( out_dir + "mitre_group_" + targeted_sector.lower() + "_tactic_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(2, 3, "Top 30 most used techniques", out_dir + "c2_3.txt")
    pdf.image( out_dir + "mitre_group_" + targeted_sector.lower() + "_most_used_techid_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(2, 4, "The Must be covered techniques", out_dir + "c2_4.txt")
    pdf.image( out_dir + "mitre_group_" + targeted_sector.lower() + "_top_tech_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(2, 5, "Top data source to collect for detections", out_dir + "c2_5.txt")
    #pdf.image( out_dir + "source_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.image( out_dir + "percentage_source_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(2, 6, "Top data component to collect for detections", out_dir + "c2_6.txt")
    #pdf.image( out_dir + "data_component_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.image( out_dir + "percentage_data_component_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(2, 7, "Top event to collect for detections", out_dir + "c2_7.txt")
    pdf.image( out_dir + "data_source_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.image( out_dir + "percentage_data_source_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    return 0


def print_annexe(out_dir,pdf):
    pdf.print_chapter(4, 'Annexes', out_dir + 'c0.txt')
    pdf.print_subchapter_annexe(4, 1, "List of all techniques used", out_dir + "annexe_1.txt")
    pdf.print_subchapter(4, 2, "Data sources reference for covering all mitre technique", out_dir + "c0.txt")
    pdf.image( out_dir + "reference_data_source_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.image( out_dir + "reference_percentage_data_source_to_prioritize_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(4, 3, "Data component reference for covering all mitre technique", out_dir + "c0.txt")
    pdf.image( out_dir + 'reference_data_component_to_prioritize_resize.png' , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.image( out_dir + 'reference_percentage_data_component_to_prioritize_resize.png' , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.print_subchapter(4, 4, "Event reference for covering all mitre technique", out_dir + "c0.txt")
    pdf.image( out_dir + 'reference_data_source_event_to_prioritize_resize.png' , x = None, y = None, w = 0, h = 0, type = '', link = '')
    pdf.image( out_dir + 'reference_percentage_data_source_event_to_prioritize_resize.png' , x = None, y = None, w = 0, h = 0, type = '', link = '')
    return 0


def print_chapter_3(out_dir, pdf):
    file_list = os.listdir(out_dir)
    with open(out_dir + 'c3.txt','w') as f:
        f.write(chapter_3)
    f.close
    pdf.print_chapter(3, 'How to detect most used techniques ?', out_dir +'c3.txt')
    sub_chapt = 1
    while True:
        sub_chapt_file = "c3_" + str(sub_chapt) +".txt"
        sub_chapt_file_modified = "c3_" + str(sub_chapt) +"_m.txt"
        if sub_chapt_file in file_list:
            with open(out_dir + sub_chapt_file,'r') as f:
                sub_chapt_name_lines = f.readlines()
                sub_chapt_name = sub_chapt_name_lines[0]
                with open(out_dir + sub_chapt_file_modified,'w') as g:
                    for line in sub_chapt_name_lines[1:]:
                        g.writelines(line)
                g.close()
            f.close()
            try: 
                pdf.print_subchapter(3, sub_chapt, sub_chapt_name, out_dir + sub_chapt_file_modified)
            except Exception as e:
                pdf.print_subchapter(3, sub_chapt, sub_chapt_name,out_dir + "c0.txt")
                print(e)
            tech_id_reformatted = (sub_chapt_name.split('\n')[0]).replace(".","_")
            try:
                pdf.image( out_dir + "attack_net_graph_"+ tech_id_reformatted +"_resize.png" , x = None, y = None, w = 0, h = 0, type = '', link = '')
            except Exception as e:
                print(e)
            sub_chapt += 1
        else:
            break
    return 0


def text_to_png(filename, number, title, size):
    fig = plt.figure(figsize=[2.5,2])
    # One can also directly draw texts to a figure with positioning
    # in pixel coordinates by using `.Figure.text` together with
    # `.transforms.IdentityTransform`.
    fig.text(50, 15, title, color="slategrey", fontsize=10,
            transform=IdentityTransform())
    fig.text(10, 35, number, color="grey", fontsize=size,
            transform=IdentityTransform())
    plt.savefig(filename)
    #plt.show()
    plt.close()
    return 0

def from_list_to_string(l):
    '''convert list of string as 1 unique string'''
    result = ""
    if len(l) > 0:
	    for item in l:
		    result = result + str(item) +", "
	    result = result[:-2]
    #print(result)
    return result


def save_list_todisk(filename, listname):
    '''save list to file on disk'''
    with open(filename,"wb") as f:
        pickle.dump(listname, f)
    f.close()
    return 0
    

def load_list_fromdisk(filename):
    '''dump file on disk to list'''
    with open(filename, "rb") as f:
        listname = pickle.load(f)
    f.close()
    return listname


def draw_top_technique_to_prioritize(df):
	ar_all_tech_id = df['technique_id'].reset_index(drop = True).value_counts()
	all_tech_list = ar_all_tech_id.index.to_list()
	r = '{:<15}'.format('technique_id') + '{:<50}'.format('tactic') + '{:<40}'.format('technique') + 'group' + '\n'
	for tech in all_tech_list:
		temp_df = df[df['technique_id'] == tech][['technique_id','tactic','technique','group']]
		#nb_of_group = temp_df['group'].count()
		list_of_group = from_list_to_string(temp_df['group'].to_list())
		r += '{:<15}'.format(str(tech)) + '{:<50}'.format(from_list_to_string(temp_df['tactic'].iloc[0])) + '{:<40}'.format(str(temp_df['technique'].iloc[0])) + list_of_group + '\n'
	with open(out_dir + "annexe_1.txt",'w') as f:
		f.write(r)
	f.close()
	df_tech_id = df['technique_id'].reset_index(drop = True).value_counts().nlargest(30).to_frame().reset_index()
	list_of_top_tech = df_tech_id['index'].tolist()
	save_list_todisk("top_tech_id_list.lst", list_of_top_tech)
	i = 1
	for item in list_of_top_tech:
		filename = "c3_" + str(i) + ".txt"
		result = str(item) +'\n'
		temp_group = from_list_to_string(df[df['technique_id'] == item]['group'].value_counts().index.to_list())
		result += "Used by group : " + temp_group +'\n\n'
		temp_tactic = from_list_to_string(df[df['technique_id'] == item]['tactic'].value_counts().index.to_list()[0])
		result += "Tactic : " + temp_tactic +'\n\n'
		temp_technique = from_list_to_string(df[df['technique_id'] == item]['technique'].value_counts().index.to_list())
		result += "Technique : " + temp_technique +'\n\n'
		temp_technique_desc = from_list_to_string(df[df['technique_id'] == item]['technique_description'].value_counts().index.to_list())
		result += temp_technique_desc +'\n'
		with open(out_dir + filename,"w") as f:
			f.write(result)
		f.close()
		i +=1 
	vis.barh_chart(df_tech_id,'technique_id','index','Technique to prioritize for detection')
	vis.plt.xlim(0,Number_of_group)
	vis.plt.ylabel('Technique ID')
	vis.plt.xlabel('Number of threat actors using the techniques')
	vis.plt.savefig(out_dir + output_graph)
	#vis.plt.show()
	vis.plt.close()
	return 0


def draw_technique_used_by_half_or_more_group(df):
    df_tech_id = df['technique_id'].reset_index(drop = True).value_counts()
    threashold = Number_of_group * 0.3
    df_top_tech_id = df_tech_id[df_tech_id > threashold] * 100 / Number_of_group
    df_top_result = df_top_tech_id.to_frame().reset_index()
    total_top_tech = df_top_result.shape[0]
    #text_to_png(out_dir +  "nb_of_top_tech.png", str(total_top_tech), r"Most used techniques",130)
    try :
        vis.barh_chart(df_top_result,'technique_id','index','Top Tech : techniques used by more than 30% of threat actors')
        vis.plt.xlim(0,100)
        vis.plt.ylabel('Technique ID')
        vis.plt.xlabel('Percentage of Groups using the techniques')
        vis.plt.savefig(out_dir + output_graph_top_tech)
        vis.plt.close()
    except :
        image = Image.open('default.png')
        image.save(out_dir + output_graph_top_tech)
        image.close()
    return total_top_tech


def draw_repartition_technique(df):
    '''Draw repartitions of techniques to most to least used'''
    total_sum_tech = df['technique_id'].value_counts().shape[0]
    df_list_of_tech = df['technique_id'].value_counts().to_frame().reset_index()
    list_of_tech = df_list_of_tech['index'].tolist()
    save_list_todisk("tech_id_list.lst", list_of_tech)
    total_used_tech = df['technique_id'].value_counts().sum()
    #text_to_png(out_dir +  "nb_of_tech.png", str(total_sum_tech), r"   Techniques used",85)
    eigthy_percent_sum_tech = df['technique_id'].value_counts().shape[0]*0.8
    twenty_percent_sum_tech = df['technique_id'].value_counts().shape[0]*0.2
    dict_repartition = {}
    for item in range(1,total_sum_tech):
        dict_repartition[item] = df['technique_id'].value_counts().nlargest(item).sum()/total_used_tech*100
    s = pd.Series(dict_repartition, name = 'Percentage of coverage').to_frame()
    s['Most to least used number of techniques'] = s.index
	#print(s)
	#print(s.to_frame().reset_index())
    g = sns.relplot(x="Most to least used number of techniques", y="Percentage of coverage", kind="line", data=s)
    g.ax.axvline(x = twenty_percent_sum_tech, color='r')
    g.ax.axvline(x = eigthy_percent_sum_tech, color='g')
    g.axes[0,0].set_xlim(0,total_sum_tech)
    g.axes[0,0].set_ylim(0,100)
    g.savefig(out_dir + output_graph_tactic)
    return total_sum_tech


def draw_tactical_repartition(df):
    '''Draw chart for representing enterprise tactics repartition '''
    ordered_enterprise_tactics = ['reconnaissance','resource-development','initial-access','execution','persistence','privilege-escalation','defense-evasion','credential-access','discovery','lateral-movement','collection','command-and-control','exfiltration','impact']
    df_tactic = df['tactic'].explode().reset_index(drop = True).value_counts().reindex(index = ordered_enterprise_tactics)
    df_tactic.fillna(0,inplace=True)
    df_tactic = df_tactic.to_frame().reset_index()
    df_tactic['percent'] = (df_tactic['tactic'] / df_tactic['tactic'].sum()) * 100
    try:
        vis.barh_chart(df_tactic,'percent','index','Tactic distribution accross all used techniques')
        vis.plt.xlabel('Tactic distribution percentage')
        vis.plt.savefig(out_dir + output_graph_repartition)
    except Exception as e:
        image = Image.open('default.png')
        image.save(out_dir + output_graph_repartition)
        image.close()
    return 0


def draw_technique_netwok_graph(dfo,tech_id_ref):
    filename = 'attack_net_graph_' + (str(tech_id_ref)).replace(".","_") + '.png'
    vis.attack_network_graph(dfo[(dfo['technique_id']==tech_id_ref)])
    #vis.plt.show()
    vis.plt.savefig(out_dir + filename)
    vis.plt.close()
    return 0


def draw_reference_data_source_to_prioritize(dfo):
    filename = 'reference_data_source_to_prioritize.png'
    df_data_source = dfo[['technique_id','data_source','data_component']].drop_duplicates()
    event_id = df_data_source['data_source'].value_counts().nlargest(40).to_frame().reset_index()
    title = 'Most Relevant data source to prioritize for all techniques and subtechniques detection'
    vis.barh_chart(event_id,'data_source','index',title, xlabel = 'Count of techniques and sub techniques covered by each data source')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_reference_percentage_data_source_to_prioritize(dfo):
    filename = 'reference_percentage_data_source_to_prioritize.png'
    df_data_source = dfo[['technique_id','data_source','data_component']].drop_duplicates()
    nb_tech_and_subtech = df_data_source['technique_id'].drop_duplicates().reset_index().shape[0]
    event_id = df_data_source['data_source'].value_counts().nlargest(40).to_frame().reset_index()
    event_id['percentage']=event_id['data_source']/nb_tech_and_subtech*100
    title = 'Most Relevant data source to prioritize for all techniques and subtechniques detection'
    vis.barh_chart(event_id,'percentage', 'index', title, xlabel = 'Percentage of techniques and sub techniques covered by each data source')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_reference_data_component_to_prioritize(dfo):
    filename = 'reference_data_component_to_prioritize.png'
    df_data_source = dfo[['technique_id','data_source','data_component']].drop_duplicates()
    event_id = df_data_source['data_component'].value_counts().nlargest(40).to_frame().reset_index()
    title = 'Most Relevant data component to prioritize for all techniques and subtechniques detection'
    vis.barh_chart(event_id,'data_component','index',title, xlabel = 'Count of techniques and sub techniques covered by each data component')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_reference_percentage_data_component_to_prioritize(dfo):
    filename = 'reference_percentage_data_component_to_prioritize.png'
    df_data_source = dfo[['technique_id','data_source','data_component']].drop_duplicates()
    nb_tech_and_subtech = df_data_source['technique_id'].drop_duplicates().reset_index().shape[0]
    event_id = df_data_source['data_component'].value_counts().nlargest(40).to_frame().reset_index()
    event_id['percentage']=event_id['data_component']/nb_tech_and_subtech*100
    title = 'Most Relevant data component to prioritize for all techniques and subtechniques detection'
    vis.barh_chart(event_id,'percentage', 'index', title, xlabel = 'Percentage of techniques and sub techniques covered by each data component')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_reference_eventid_to_prioritize(dfo):
    filename = 'reference_data_source_event_to_prioritize.png'
    df_data_source = dfo[['technique_id','data_source','data_component','event_id']].drop_duplicates()
    event_id = df_data_source['event_id'].value_counts().nlargest(40).to_frame().reset_index()
    title = 'Most Relevant Event (Top 40)\n to prioritize for all techniques and subtechniques detection'
    vis.barh_chart(event_id,'event_id','index',title, xlabel = 'Count of techniques and sub techniques covered by each event')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_reference_percentage_eventid_to_prioritize(dfo):
    filename = 'reference_percentage_data_source_event_to_prioritize.png'
    df_data_source = dfo[['technique_id','data_source','data_component','event_id']].drop_duplicates()
    nb_tech_and_subtech = df_data_source['technique_id'].drop_duplicates().reset_index().shape[0]
    event_id = df_data_source['event_id'].value_counts().nlargest(40).to_frame().reset_index()
    event_id['percentage']=event_id['event_id']/nb_tech_and_subtech*100
    title = 'Most Relevant Event (Top 40)\n to prioritize for all techniques and subtechniques detection'
    vis.barh_chart(event_id,'percentage', 'index' ,title, xlabel = 'Percentange of techniques and sub techniques covered by each event')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_data_source_to_prioritize(dfo, all_tech):
    filename = 'data_source_to_prioritize.png'
    df_temp = dfo[dfo['technique_id'].isin(all_tech)]
    #print(df_temp.shape, dfo.shape )
    df_data_source = df_temp[['technique_id','data_source','data_component','event_id']].drop_duplicates()
    event_id = df_data_source['event_id'].value_counts().nlargest(40).to_frame().reset_index()
    title = 'Most Relevant Event (Top 40)\n to prioritize for techniques and subtechniques detection'
    vis.barh_chart(event_id,'event_id','index',title, xlabel = 'Count of techniques and sub techniques covered by each event')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_percentage_data_source_to_prioritize(dfo, all_tech):
    filename = 'percentage_data_source_to_prioritize.png'
    df_temp = dfo[dfo['technique_id'].isin(all_tech)]
    #print(df_temp.shape, dfo.shape )
    df_data_source = df_temp[['technique_id','data_source','data_component','event_id']].drop_duplicates()
    nb_tech_and_subtech = df_data_source['technique_id'].drop_duplicates().reset_index().shape[0]
    event_id = df_data_source['event_id'].value_counts().nlargest(40).to_frame().reset_index()
    event_id['percentage']=event_id['event_id']/nb_tech_and_subtech*100
    title = 'Most Relevant Event (Top 40)\n to prioritize for techniques and subtechniques detection'
    vis.barh_chart(event_id,'percentage', 'index', title, xlabel = 'Percentage of techniques and sub techniques covered by each event')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_source_to_prioritize(dfo, all_tech):
    filename = 'source_to_prioritize.png'
    df_temp = dfo[dfo['technique_id'].isin(all_tech)]
    #print(df_temp.shape, dfo.shape )
    df_data_source = df_temp[['technique_id','data_source','data_component']].drop_duplicates()
    event_id = df_data_source['data_source'].value_counts().nlargest(40).to_frame().reset_index()
    title = 'Most Relevant data source (Top 40)\n to prioritize for techniques and subtechniques detection'
    vis.barh_chart(event_id,'data_source','index',title, xlabel = 'Count of techniques and sub techniques covered by each data source')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_percentage_source_to_prioritize(dfo, all_tech):
    filename = 'percentage_source_to_prioritize.png'
    df_temp = dfo[dfo['technique_id'].isin(all_tech)]
    #print(df_temp.shape, dfo.shape )
    df_data_source = df_temp[['technique_id','data_source','data_component']].drop_duplicates()
    nb_tech_and_subtech = df_data_source['technique_id'].drop_duplicates().reset_index().shape[0]
    event_id = df_data_source['data_source'].value_counts().nlargest(40).to_frame().reset_index()
    event_id['percentage']=event_id['data_source']/nb_tech_and_subtech*100
    title = 'Most Relevant data source (Top 40)\n to prioritize for techniques and subtechniques detection'
    vis.barh_chart(event_id,'percentage','index', title, xlabel = 'Percentage of techniques and sub techniques covered by each data source')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_component_to_prioritize(dfo, all_tech):
    filename = 'data_component_to_prioritize.png'
    df_temp = dfo[dfo['technique_id'].isin(all_tech)]
    #print(df_temp.shape, dfo.shape )
    df_data_source = df_temp[['technique_id','data_source','data_component']].drop_duplicates()
    event_id = df_data_source['data_component'].value_counts().nlargest(40).to_frame().reset_index()
    title = 'Most Relevant data component (Top 40)\n to prioritize for techniques detection'
    vis.barh_chart(event_id,'data_component','index',title, xlabel = 'Count of techniques and sub techniques covered by each data component')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


def draw_percentage_component_to_prioritize(dfo, all_tech):
    filename = 'percentage_data_component_to_prioritize.png'
    df_temp = dfo[dfo['technique_id'].isin(all_tech)]
    #print(df_temp.shape, dfo.shape )
    df_data_source = df_temp[['technique_id','data_source','data_component']].drop_duplicates()
    nb_tech_and_subtech = df_data_source['technique_id'].drop_duplicates().reset_index().shape[0]
    event_id = df_data_source['data_component'].value_counts().nlargest(40).to_frame().reset_index()
    event_id['percentage']=event_id['data_component']/nb_tech_and_subtech*100
    title = 'Most Relevant data component (Top 40)\n to prioritize for techniques detection'
    vis.barh_chart(event_id,'percentage','index',title, xlabel = 'Percentage of techniques and sub techniques covered by each data component')
    vis.plt.savefig(out_dir + filename)
    #vis.plt.show()
    vis.plt.close()
    return 0


if __name__ == '__main__':
    __version__ = '.'.join(__version_info__)
    parser = argparse.ArgumentParser(description='Beta version tool for generating a threat report based on mitre and ossem source')
    parser.add_argument("-ts", "--targeted_sector", action = "store", dest = "targeted_sector", type=str, help="Give the targeted sector\n")
    parser.add_argument("-go", "--generate_only", action = 'store_true' , default = False, dest = "generate_only", help="Generation of the report only for debug\n")
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args()

    if not args.targeted_sector :
        print("[-] - Please enter a targeted sector in order the report to be generated\n")
        exit(0)
    else:
        targeted_sector = args.targeted_sector
        generate_only = args.generate_only

    
    #targeted_sector = "Healthcare"
    title = 'Must Have SOC Analysts customized cookbook'
    subtitle = 'Leverage automation and threat intel data analysis for prioritizing detection'
    sector = "Report customized for " + str(targeted_sector) + " sector"
    intro = """This report aims at providing  statical analysis of TTPs (Tactics, Techniques and Procedures) used by threat actors targetting """ + targeted_sector + """ sector in order to help SOC in operationalizing their mission.\n
While contextualising, gathering and analysing available data for a given sector, the overall objective is to introduce a different threat perspective for SOC teams - a perspective based on all known (and shared) threat actor behaviours. The main idea is to provide to SOC team a dedicated baseline to operationalize their efficiency in their daily job from collections to remediations.\n
The 1st chapter enumerates the threat actors based on MITRE data sources.\nThe 2nd chapter gives statistics about TTPs and data sources to collect in order to maximise detection capability (beware of bias).\nThe 3rd and last chapter gives detailed information on how to detect the most used techniques.\nThis report is AUTOMATICALLY generated based on MITRE ATT&CK and OSSEM data.\n
MITRE ATT&CK (https://attack.mitre.org) is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base is used as a foundation for the development of specific threat models and methodologies in the private sector, in government, and in the cybersecurity product and service community.
With the creation of ATT&CK, MITRE is fulfilling its mission to solve problems for a safer world - by bringing communities together to develop more effective cybersecurity. ATT&CK is open and available to any person or organization for use at no charge.\n
The OSSEM (Open Source Security Events Metadata / https://github.com/OTRF/OSSEM) is a community-led project that focuses primarily on the documentation and standardization of security event logs from diverse data sources and operating systems. Security events are documented in a dictionary format and can be used as a reference while mapping data sources to data analytics used to validate the detection of adversarial techniques. In addition, the project provides a common data model (CDM) that can be used for data engineers during data normalization procedures to allow security analysts to query and analyze data across diverse data sources. Finally, the project also provides documentation about the structure and relationships identified in specific data sources to facilitate the development of data analytics.\n
This is a beta version (work still in progress).
Good enough for now.
May this work be of help for you. \n\n
Feedbacks, contributions and enrichments are welcome :)
Thomas Billaut <thomas.billaut@protonmail.com>
https://github.com/tbillaut\n""" 
    chapter_1 = "This chapter aims at giving the list of threat groups targetting the " + targeted_sector + " sector.\nData are extracted from MITRE ATT&CK.\nInformation and citation links can be retrieved from MITRE ATTACK website (https://attack.mitre.org/groups).\n"
    chapter_2 = "This chapter aims at providing some statistics about tactics and techniques used by the previous threat actors. While understanding most used and share techniques, SOC analysts should be able to focus on most used tactics and techniques. And possibly adopt a new perspective of the priority."
    chapter_2_1 = "The following chart gives the tactics distribution of all used techniques used by the threat actors.\nThis representation may offer a new perpective for SOC teams concerning detection capabilities."
    chapter_2_2 = "The following graph gives the techniques distribution accross all of those threat actors.\nIt aims at understanding how many techniques need to be covered in order to have the suitable level of detection.\nThe profile can be compared to the pareto model where covering 20% of the most used techniques would covered 80% of the total of techniques used.\nThe red line gives the number of techniques corresponding to 20% of total techniques used.\nThe green line gives the number of techniques corresponding to 80% of total techniques used."
    chapter_2_3 = "The following graph gives the top 30 techniques that are most used by all of those threat actors.\nFor each most used technique, the number of group using this technique is given."
    chapter_2_4 = "The following graph is just a focus of the previous one by giving the techniques that are used by almsot 30% of the threat actors.\nFor each technique, the percentage of threat actors using this technique is given."
    chapter_2_7 = "The following graph gives the top 40 event to collect in order to be able to detect the techniques used by threat actors.\nPlease see annexes for reference."
    chapter_2_5 = "The following graph gives the top 40 data source to collect in order to be able to detect the techniques used by threat actors.\nPlease see annexes for reference."
    chapter_2_6 = "The following graph gives the top 40 data component to collect in order to be able to detect the techniques used by threat actors.\nPlease see annexes for reference."
    chapter_3 = "This chapter aims at reviewing the most used techniques from most used to least used while providing more detailed information on the technique, the collection data required for detection and how to detect the technique."
    default_chapter = "< To be corrected or added in future releases >"
    author = 'Thomas Billaut <thomas.billaut@protonmail.com>'
    if platform == 'linux' :
        out_dir = './out/'
    elif platform == 'win32' :
        out_dir = ".\\out\\"
    WIDTH = 210
    HEIGHT = 297

    print("[+] - starting script")
    report_name = "SOC_cookbook_for_" + targeted_sector.lower() +".pdf"

    # debug mode for not generating the report from here to -->

    if  not generate_only :

        if not os.path.isdir("out"):
            os.mkdir("out")


        print("[+] - retrieving mitre group and ossem data")

        get_group()
        get_ossem_data()

        ### Generate and retrieve data from mitre att&ck
        with open(out_dir + 'c0.txt','w') as f:
                f.write(default_chapter)
        f.close
        print("[+] - generating threat actor paragraph")
        f = "mitre_group.json"
        with open(f,"r") as file:
            group = json.loads(file.read())
        file.close()
        nb_of_mitre_actors = len(group)
        working_on_mitre_group.write_group_as_paragraph(group, targeted_sector.lower())
        
        ### retrieve sector threat actors from mitre att&ck
        print("[+] - retrieving threat actors")
        working_on_mitre_group.retrieve_group_tech(group, targeted_sector.lower() )
        
        ### Analyse mitre data
        print("[+] - analysing threat actors ttps")
        f_target = "mitre_group_" + targeted_sector.lower() + ".json"
        output_graph = f_target.split('.')[0] + '_most_used_techid.png'
        output_graph_repartition = f_target.split('.')[0] + '_repart_techid.png'
        output_graph_top_tech = f_target.split('.')[0] + '_top_tech.png'
        output_graph_tactic  = f_target.split('.')[0] + '_tactic.png'
        with open(f_target,"r") as file:
            dict_group = json.loads(file.read())
        file.close()
        # create a list of dataframe for each group
        result=[]
        for group in dict_group:
            temp_df = pd.json_normalize(dict_group[group])
            temp_df['group'] = group
            result.append(temp_df)
        # create a consolidated dataframe object
        df = result[0]
        for datafme in result[1:]:
            df = df.append(datafme, ignore_index=True, sort=False)
        # Filter out revoked technique id
        try:
            df = df.loc[df['revoked']!=True]
        except Exception as e:
            pass
        Number_of_group = df['group'].value_counts().shape[0]
        nb_of_actors = Number_of_group
        # text_to_png(out_dir + "nb_of_group.png", str(Number_of_group), r"     Threat actors", 130)
        nb_of_techniques = draw_repartition_technique(df)
        draw_top_technique_to_prioritize(df)
        nb_most_used_tech = draw_technique_used_by_half_or_more_group(df)
        draw_tactical_repartition(df)
        print("[+] - finished analysing threat actors ttps")

        f_ossem="techniques_to_events_mapping.yaml"
        with open(f_ossem,"r") as f:
            c=f.read()
        f.close()
        # OLD, json object now
        # ym=yaml.safe_load(c)
        ym=json.loads(c)
        dfo = pd.json_normalize(ym)
        nb_of_mitre_techniques = dfo[['technique_id']].drop_duplicates().shape[0]
        print("[+] - starting visualize data")
        top_tech = load_list_fromdisk("top_tech_id_list.lst")
        all_tech = load_list_fromdisk("tech_id_list.lst")
        for tech in top_tech:
            try :
                print(('[+] - draw tech %s')%(tech))
                draw_technique_netwok_graph(dfo, tech)
            except Exception as e:
                print(e)
        draw_data_source_to_prioritize(dfo,all_tech)
        draw_percentage_data_source_to_prioritize(dfo, all_tech)
        draw_component_to_prioritize(dfo, all_tech)
        draw_percentage_component_to_prioritize(dfo, all_tech)
        draw_source_to_prioritize(dfo, all_tech)
        draw_percentage_source_to_prioritize(dfo, all_tech)
        draw_reference_data_source_to_prioritize(dfo)
        draw_reference_percentage_data_source_to_prioritize(dfo)
        draw_reference_eventid_to_prioritize(dfo)
        draw_reference_percentage_eventid_to_prioritize(dfo)
        draw_reference_data_component_to_prioritize(dfo)
        draw_reference_percentage_data_component_to_prioritize(dfo)
        print("[+] - finished visualize data")

        ### draw kpi 
        image_file = out_dir + "key_indicators.png"
        draw_indicator(nb_of_mitre_actors, nb_of_mitre_techniques, nb_of_actors, nb_of_techniques, nb_most_used_tech, image_file)

        # resize images
        resize_png(out_dir)
        print("[+] - images resized")

    ## --> to there / to be scratched for testing onny the report generation

    # clean the text file for latin-1 encoding required by FPDF
    print("[+] - cleaning the report for latin-1 encoding")
    clean(out_dir)

    # generate the report
    print("[+] - generate report")
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(30, 80, title)
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 100, subtitle)
    pdf.image("triangulated-image_map.png" , x = 0, y = 110, w = 0, h = 0, type = '', link = '')
    pdf.set_xy(70,240)
    pdf.set_font('Arial','I', 10)
    pdf.cell(0, 10, sector)
    pdf.add_page()
    pdf.set_font('Arial','', 8)
    pdf.set_xy(35,60)
    pdf.multi_cell(140, 5, intro, 0, 'L')
    print_group_chapter(out_dir, pdf)
    print_chapter_2(out_dir,pdf)
    print_chapter_3(out_dir,pdf)
    print_annexe(out_dir,pdf)
    pdf.output(report_name, 'F')
    print("[+] - Finished")
    if platform == 'linux' :
        os.popen('cp '+ report_name + " " + out_dir + report_name)
    elif platform == 'win32':
        os.popen('copy '+ report_name + " " + out_dir + report_name)
    print("[+] - Enjoyed : )")