import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

df = pd.read_csv("../illojuan_documental-chat/2023-11-23  -- 15 44 27 - 15 45 28 = 800.csv")
print(df.head())

# chat = " ".join(cat.split()[1] for cat in df.message_selector)
chat = " ".join(df['message_selector'].astype(str))

# Define custom stopwords
custom_stopwords = set(["https", "www", "que", "to", "el","de","a","el","la","lo","e","y","con","se"]) | set(STOPWORDS)
# custom_stopwords = set(STOPWORDS)

word_cloud = WordCloud(width=1000, height=600, stopwords=custom_stopwords, collocations = False, background_color = 'white').generate(chat)
# Display the generated Word Cloud
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()