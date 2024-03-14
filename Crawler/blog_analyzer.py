'''
블로그글의 title + header에 포합되있는 주식 종목 추출
blog_id, 종목명
'''
from tqdm import tqdm
import pandas as pd

class BlogAnalyzer:
    def word_extractor(self, blog_df, li, w="company_name"):
        blog_df["content"] = blog_df["title"].str.cat(blog_df["header"], na_rep='', sep=' ')
        blog_df["content"].fillna('', inplace=True)
        print(blog_df.columns)
        if "blog_id" in blog_df.columns:
            blog_df.rename(columns={"blog_id": "blog_id"}, inplace=True)

        # company_name_li에 있는 회사 이름이 content에 포함되어 있는지 확인
        # 각 회사 이름에 대해 content 컬럼에서 검색하고, 결과를 저장
        result = pd.DataFrame(columns=['blog_id', w])
        for c in tqdm(li):
            mask = blog_df['content'].str.contains(c)
            filtered_df = blog_df.loc[mask, ['blog_id']]
            filtered_df[w] = c
            result = pd.concat([result, filtered_df])

        return result.reset_index(drop=True)


# class BlogAnalyzer:
#     def word_extractor(self,blog_df ,li,w = "company_name"):
#         blog_df["content"] = blog_df["title"] + blog_df["header"]
#         blog_df["content"] .fillna('', inplace=True)
#         tmp_li = []
#
#         if "blog_id" in blog_df.columns:
#             blog_df.rename(columns={"blog_id": "blog_id"},inplace=True)
#
#         # blog_df를 반복하면서 company_name_li에 있는 회사 이름이 content에 포함되어 있는지 확인
#         for index, row in tqdm(blog_df.iterrows(), total=len(blog_df)):
#             for c in li:
#                 if c in row['content']:
#                     # 결과 DataFrame에 추가
#                     tmp_li.append([ row['blog_id'],c])
#         result_df = pd.DataFrame(tmp_li,columns=['blog_id', w])
#         return result_df

