#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:05:57 2021

@author: bmondal
"""
import string
import re
import glob
import numpy as np
import pandas as pd
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import wordcloud
import matplotlib.pyplot as plt
from PIL import Image
import nltk
from nltk.corpus import stopwords
import PyPDF2
from calendar import month_name

#%%
ENGLISH_STOP = set(stopwords.words('english'))

class research_paper_wordcloud():

    def __init__(self, paper_path):
        '''
        find all pdf under paper_path
        '''
        self.paper_path = paper_path
        self.PDFs = glob.glob(paper_path + '/*pdf') #any PDF can be found?
        self.texts = ''  # store all texts
        self.tokens = None
        self.words = None
        self.paper_stop = ['fig','figure','supplementary', 'author','press',
                            'PubMed', 'manuscript','nt','et','al', 'laboratory',
                            'article',
                            'additional', 'additionalfile','additiona file',
                            'SupportingInformation']
        months = [month_name[i].lower() for i in range(1,13)]
        self.paper_stop.extend(months)
        self.paper_stop.extend(list(map(lambda x: x.capitalize(), self.paper_stop)))
        self.paper_stop = set(self.paper_stop)
    
    def extract_text_from_pdf(self):
        for pdf in self.PDFs:
            with open(pdf, 'rb') as paper:
                pdf = PyPDF2.PdfFileReader(paper)
                for page_num in range(pdf.getNumPages()-1):
                    page = pdf.getPage(page_num)
                    self.texts += page.extractText()
    
    def remove_unnecessary_text(self):
        self.tokens = nltk.word_tokenize(self.texts)
        self.tokens =  nltk.pos_tag(self.tokens) #(tag the nature of each word, verb? noun?)

        self.words = []
        num_regex = re.compile('[0-9]+')
        for word, tag in self.tokens:
            IS_VERB = tag.startswith('V')
            IS_STOP = word in set(string.punctuation)
            IS_ENGLISH_STOP = word in set(ENGLISH_STOP)
            IS_WORDCLOUD_STOP = word in wordcloud.STOPWORDS
            IS_NUMBER = num_regex.search(word)
            IS_PAPER_STOP = word in self.paper_stop
            condition = [IS_VERB, IS_STOP, IS_ENGLISH_STOP,
                        IS_WORDCLOUD_STOP, IS_NUMBER, IS_PAPER_STOP]
            if not any(condition):
                if word == "coli":
                    self.words.append('X. ray') #break down of X. ray
                else:
                    self.words.append(word)

        self.words = ' '.join(self.words)

    def generate_wordcloud(self, figurename):
        dove_mask = np.array(Image.open("/home/bmondal/WORD_CLOUD/index.png"))
        wc = wordcloud.WordCloud(  
                collocations=False,
                background_color='white',
                mask=dove_mask,
                contour_color='darkgreen',
                contour_width=3,
                max_words=1000,
                max_font_size=40, 
                min_font_size=3,
                scale=3
        )
        try:
            wc.generate(self.words)
            plt.imshow(wc) #, interpolation="bilinear")
            plt.axis('off')
            plt.savefig(figurename, bbox_inches='tight', transparent=True)
        except ValueError:
            print(self.words)

#%%
PDF_path = '/home/bmondal/WORD_CLOUD'
wordcloud_image = '/home/bmondal/WORD_CLOUD/janniclas.jpg'

wc = research_paper_wordcloud(PDF_path)
wc.extract_text_from_pdf()
wc.remove_unnecessary_text()
wc.generate_wordcloud(wordcloud_image)
