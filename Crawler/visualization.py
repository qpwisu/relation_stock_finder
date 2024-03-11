from mysql_connector import MySQLDataConnector
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import pandas as pd
# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class Visualization:

    def __init__(self):
        self.connector = MySQLDataConnector(user='root',
                                       password='1234',
                                       host='localhost',
                                       database='STOCK')
    '''
    #1
        기간동안 가장 많은 블로그글이 올라온 정치인 topN 
        input :  start_date, end_date, topN
    '''
    def visualization_politician_topN(self,start_date, end_date, topN):
        # 막대 그래프 그리기 가장 많은 블로그글이 올라온 정치인 topN
        dff = self.connector.default_query(
            f"SELECT name, COUNT(name) AS cnt FROM politician_blog_TB WHERE date >= '{start_date}' AND date <= '{end_date}' GROUP BY name ORDER BY cnt DESC LIMIT {topN};")
        dff.plot.bar(x='name', y='cnt', rot=0)

        # 위 topN의 날짜별 언급 plot 그래프
        name_li = dff["name"].to_list()
        names_for_sql = ", ".join(f"'{name}'" for name in name_li)
        df = self.connector.default_query(f"SELECT name,date, COUNT(*) AS cnt FROM politician_blog_TB WHERE name in ({names_for_sql}) and date >= '{start_date}' AND date <= '{end_date}' GROUP BY name, date ORDER BY name, date; ")
        df['date'] = pd.to_datetime(df['date'])

        # pivot을 사용하여 'name'을 컬럼으로, 'Date'를 인덱스로 재구성
        pivot_df = df.pivot(index='date', columns='name', values='cnt')

        # plot 그래프 그리기
        pivot_df.plot(kind='line', marker='o', figsize=(10, 6))
        plt.title('날짜별 정치인 언급 횟수')
        plt.xlabel('날짜')
        plt.ylabel('언급 횟수')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    '''
    #2  
        기간동안 가장 많은 블로그글이 올라온 주식 topN
        input :  start_date, end_date, topN
    '''
    def visualization_stock_topN(self,start_date, end_date, topN):
        dff= self.connector.default_query(f"SELECT bsa.companyName, count(*) as cnt FROM ( SELECT * FROM politician_blog_TB WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb INNER JOIN blog_stock_analysis_TB AS bsa ON pb.blogID = bsa.blogID group by bsa.companyName order by cnt desc limit {topN};")
        dff.plot.bar(x='companyName', y='cnt', rot=0)

        # 위 topN의 날짜별 언급  그래프
        companyNames_li = dff["companyName"].to_list()
        companyNames_for_sql = ", ".join(f"'{companyName}'" for companyName in companyNames_li)
        df = self.connector.default_query(f"select pb.date,bs.companyName, count(*) as cnt from blog_stock_analysis_TB as bs join politician_blog_TB as pb on  bs.blogid= pb.blogid where bs.companyName in ({companyNames_for_sql}) and pb.date >= '{start_date}' AND pb.date <= '{end_date}' group by pb.date,bs.companyName; ")
        df['date'] = pd.to_datetime(df['date'])

        # pivot을 사용하여 'name'을 컬럼으로, 'Date'를 인덱스로 재구성
        pivot_df = df.pivot(index='date', columns='companyName', values='cnt')
        # plot 그래프 그리기
        pivot_df.plot(kind='line', marker='o', figsize=(10, 6))
        plt.title('날짜별 정치인 언급 횟수')
        plt.xlabel('날짜')
        plt.ylabel('언급 횟수')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    '''
        기간동안 정치인과 가장 많이 언급된 종목 topn의 언급수 그래프로 시각화
        input :  start_date, end_date, politician, topN
    '''
    def visualization_topN(self,start_date, end_date, politician, topN):
        df = self.connector.default_query(f"SELECT  pb.name,  bsa.companyName, count(*) as cnt FROM ( SELECT * FROM politician_blog_TB WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb INNER JOIN blog_stock_analysis_TB AS bsa ON pb.blogID = bsa.blogID group by pb.name,bsa.companyName ;")
        df2 = df[df["name"] == politician].sort_values(by=["cnt"],ascending=False)[:topN]
        df2.plot.bar(x='companyName', y='cnt', rot=0 ,fontsize=6)

        companyName_li = df2["companyName"].to_list()
        companyNames_for_sql = ", ".join(f"'{companyName}'" for companyName in companyName_li)
        df = self.connector.default_query(f"select pb.date,bs.companyName, count(*) as cnt from blog_stock_analysis_TB as bs join politician_blog_TB as pb on  bs.blogid= pb.blogid where pb.name = '{politician}' and bs.companyName in ({companyNames_for_sql}) and pb.date >= '{start_date}' AND pb.date <= '{end_date}' group by pb.date,bs.companyName; ")
        df['date'] = pd.to_datetime(df['date'])
        # pivot을 사용하여 'name'을 컬럼으로, 'Date'를 인덱스로 재구성
        pivot_df = df.pivot(index='date', columns='companyName', values='cnt')
        # plot 그래프 그리기
        pivot_df.plot(kind='line', marker='o', figsize=(10, 6))
        plt.title('날짜별 종목 언급 횟수')
        plt.xlabel('날짜')
        plt.ylabel('언급 횟수')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


    '''
    
        기간동안 종목과 가장 많이 언급된 정치인 topn의 언급수 그래프로 시각화
        input :  start_date, end_date, companyName, topN
    '''
    def visualization_reverse_topN(self,start_date, end_date, companyName, topN):
        df = self.connector.default_query(f"SELECT pb.name, count(*) as cnt FROM ( SELECT * FROM politician_blog_TB WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb INNER JOIN blog_stock_analysis_TB AS bsa ON pb.blogID = bsa.blogID where companyName = '{companyName}'  group by pb.name ;")
        df2 = df.sort_values(by=["cnt"],ascending=False)[:topN]
        df2.plot.bar(x='name', y='cnt', rot=0 ,fontsize=6)
        plt.show()
vslz = Visualization()
# df = vslz.visualization_politician_topN("20240227","20240227",10)
# df = vslz.visualization_stock_topN("20240220","20240227",5)
df2 = vslz.visualization_topN("20231101","20240227","조국",5)
# df2 = vslz.visualization_reverse_topN("20231101","20240227","대상",5)


