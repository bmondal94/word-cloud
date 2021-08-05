#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 13:07:13 2021

@author: bmondal
"""


import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image

np.set_printoptions(precision=3,suppress=True)

params = {'legend.fontsize': 18,
          'figure.figsize': (8, 6),
         'axes.labelsize': 24,
         'axes.titlesize': 24,
         'xtick.labelsize':24,
         'ytick.labelsize': 24,
         'errorbar.capsize':2}
plt.rcParams.update(params)

#%%
txt_path = '/home/bmondal/WORD_CLOUD/Title_Abstract.txt'
wordcloud_image = '/home/bmondal/WORD_CLOUD/janniclas2.eps'

STOPWORDS.update(['via','show','due','found','suggest','influence','two','C','three','value'\
                  'analysis','investigated'])
file_content=open (txt_path).read()

dove_mask = np.array(Image.open("/home/bmondal/WORD_CLOUD/index.png"))
dove_mask = np.fliplr(dove_mask) # Flip 180
wc =WordCloud(stopwords = STOPWORDS,
              #height=8,
              #width=10,
              repeat=True,
        collocations=False,
        include_numbers=True,
        background_color='white',
        mask=dove_mask,
        regexp=r"\S+",
        contour_color='darkgreen',
        contour_width=3,
        max_words=1000,
        max_font_size=70, 
        min_font_size=1,
        scale=6
).generate(file_content)
plt.imshow(wc)
plt.axis('off')
print('Written %s' %wordcloud_image)
plt.savefig(wordcloud_image, format='eps',dpi=600,papertype='a4',transparent=True,bbox_inches='tight',pad_inches=0.1)
#plt.savefig(wordcloud_image, bbox_inches='tight', transparent=True)
#plt.show()


