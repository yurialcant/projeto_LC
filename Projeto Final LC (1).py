#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests as r


# In[3]:


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)


# In[4]:


resp.status_code


# In[5]:


raw_data = resp.json()


# In[6]:


raw_data[0]


# In[7]:


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])


# In[8]:


final_data.insert(0, ['Confirmados', 'Obitos', 'Recuperados', 'Ativos', 'Data'])
final_data


# In[9]:


CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4


# In[10]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]


# In[11]:


final_data


# In[12]:


import datetime as dt


# In[13]:


import csv


# In[14]:


with open('brasil-covid.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)


# In[15]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y-%m-%d')


# In[16]:


final_data


# In[17]:


def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return[
            {
                'label': labels[0],
                'data': y
            }
        ]


# In[18]:


def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return{
        'title': title,
        'display':display
    }


# In[19]:


def create_chart(x, y, labels, kind='bar', title=''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    chart = {
        'type': kind,
        'data':{
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }
    
    return chart


# In[20]:


def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content
    


# In[21]:


def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)


# In[22]:



import sys


# In[23]:


get_ipython().system('pip install Pillow')


# In[24]:


from PIL import Image


# In[25]:


from IPython.display import display


# In[26]:


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# In[27]:


y_data_1 = []
for obs in final_data[1::100]:
    y_data_1.append(obs[CONFIRMADOS])

y_data_2 = []
for obs in final_data[1::100]:
    y_data_2.append(obs[OBITOS])
    
labels = ['Confirmados', 'obitos']

x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))
    
chart = create_chart(x, [y_data_1, y_data_2], labels, title='Gráfico casos confirmados X obitos' )
chart_content = get_api_chart(chart)
save_image('meu-quartos-grafico.png', chart_content)
display_image('meu-quartos-grafico.png')


# In[41]:


from urllib.parse import quote
    


# In[42]:


def get_api_qrcode(link):
    text = quote(link)
    url_base = 'https://quickchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content


# In[44]:


url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png',get_api_qrcode(link))
display_image('qr-code.png')


# In[ ]:




