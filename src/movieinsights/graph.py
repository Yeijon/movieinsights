"""
* 从数据库中取出需要的数据，然后用来分析和绘图
"""

import pandas as pd
import plotly.express as px
import sqlite3
import sys

def fetch_data(db_name):
    conn = sqlite3.connect(db_name)
    query = '''
    SELECT year, country, category, rating FROM movie
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = fetch_data('../../share/Demo.sqlite')

# 拆分国别列和类型列
df['country'] = df['country'].str.split(' ')
df = df.explode('country')
df['category'] = df['category'].str.split(' ')
df = df.explode('category')

# 添加 num 列，计算同年份同国家的电影数量
df['num'] = df.groupby(['year', 'country'])['rating'].transform('count')
print(df)

# 按年份和国别计算平均评分
result = df.groupby(['year', 'country'])['rating'].mean().reset_index()

pivot_df = result.pivot(index='year', columns='country', values='rating')

# figure1
fig = px.line(pivot_df, color='country', labels={'value': '综合评分', 'year': '时间'}, title='不同国家电影评分随时间的变化')
fig.show()

# figure2
fig = px.scatter(result, x='year', y='rating', color='country',
                 labels={'rating': '综合评分', 'year': '时间'},
                 title='不同国家电影评分随时间的变化')

fig.show()

# figure3
fig = px.scatter(df,
                 x='year',
                 y='rating',
                 size='num',
                 color='category',
                 labels={'rating': '评分', 'year': '时间'},
                 title='不同类别电影评分随时间的变化')

# 显示图表
fig.show()