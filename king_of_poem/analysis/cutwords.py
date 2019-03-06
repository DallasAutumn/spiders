import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


comments = []
with open('msg.txt', 'r', encoding='utf-8') as f:
    for row in f.readlines():
        comments.append(row)

comment_after_split = jieba.cut(str(comments), cut_all=False)
words = ' '.join(comment_after_split)

STOPWORDS = set(
    map(str.strip, open('stopwords.txt', encoding='utf-8').readlines()))
wc = WordCloud(width=2024, height=1400, background_color='white',
               stopwords=STOPWORDS, font_path='msyhbd.ttf', max_font_size=400, random_state=50)
wc.generate_from_text(words)
plt.imshow(wc)
plt.axis('off')
plt.show()
