import matplotlib.pyplot as plt
import sqlite3
import numpy as np

conn = sqlite3.connect('database_product.db')
c = conn.cursor()

trendSql = "SELECT product, date, avg(sentiment) FROM dataTable GROUP BY product, date ORDER BY date "
rows = c.execute(trendSql)
productTrends = {}
for row in rows:
    prod = row[0]
    date = row[1]
    average = row[2]
    if prod not in productTrends:
        productTrends[prod] = {}
        productTrends[prod]["dates"] = []
        productTrends[prod]["averages"] = []
    productTrends[prod]["dates"].append(date)
    productTrends[prod]["averages"].append(average)

numberProducts = len(productTrends)

fig, axs = plt.subplots(2, numberProducts)
#fig.autofmt_xdate(rotation=90)
fig.tight_layout(pad=3)

prodIdx = 0
for prod in productTrends:
    axs[0, prodIdx].plot(productTrends[prod]["dates"], productTrends[prod]["averages"])
    axs[0, prodIdx].set_title('Average Sentiment Value Product ' + prod)
    axs[0, prodIdx].set(xlabel='Date', ylabel='Average Sentiment')
    axs[0, prodIdx].set_xticks(productTrends[prod]["dates"])
    axs[0, prodIdx].set_xticklabels(productTrends[prod]["dates"], rotation=90, fontsize=4)
    axs[0, prodIdx].set_yticks([-2, -1, 0, 1, 2])
    #axs[0, prodIdx].set_yticklabels([-2, -1, 0, 1, 2], fontsize=8)
    prodIdx += 1

pieSql = "SELECT product, sentiment, count(*) FROM dataTable GROUP BY product, sentiment"
rows = c.execute(pieSql)
productSentiments = {}
for row in rows:
    prod = row[0]
    sentiment = row[1]
    count = row[2]

    if prod not in productSentiments:
        productSentiments[prod] = {}
    productSentiments[prod][sentiment] = count

print(productSentiments)

sentimentLabels = {
    -2: "StrongNegative",
    -1: "WeakNegative",
    0: "Neutral",
    1: "Weak Positive",
    2: "Strong Positive"
}
sentimentColors = {
    -2: "k",
    -1: "#FFF8DC",
    0: "#F0F8FF",
    1: "#6495ED",
    2: "b"
}
prodIdx = 0

from matplotlib.font_manager import FontProperties
fontProp = FontProperties()
fontProp.set_size('xx-small')
for prod in productSentiments:
    counts = []
    labels = []
    colors = []

    for sentiment in productSentiments[prod]:
        counts.append(productSentiments[prod][sentiment])
        labels.append(sentimentLabels[sentiment])
        colors.append(sentimentColors[sentiment])

    axs[1, prodIdx].set_title('Sentiments of Product ' + prod)
    axs[1, prodIdx].pie(counts, labels=labels, startangle=90, colors=colors)
    axs[1, prodIdx].legend(loc="lower center", bbox_to_anchor=(0.3, -0.4), prop=fontProp)

    prodIdx += 1

plt.show()
