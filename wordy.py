import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv("futbol-femenino-chat.csv")
print(df.head())

# chat = " ".join(cat.split()[1] for cat in df.message_selector)
chat = " ".join(df['message_selector'].astype(str))

word_cloud = WordCloud(collocations = False, background_color = 'white').generate(chat)
# Display the generated Word Cloud
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()