import pandas as pd
import openpyxl
import re


def generate(file_in, file_comp):
    # Read Excel
    df_comp = pd.read_excel(file_comp,
                            header=2,
                            na_values=0)
    df_comp = pd.DataFrame({
        '대학': df_comp['대학이름'],
        '학과': df_comp['모집단위명'],
        '경쟁률': df_comp['2021학년도 최종경쟁률']
    })
    sheets = ['가군', '나군', '다군']
    temp = []
    for group in sheets:
        df_students = pd.read_excel(file_in,
                                    header=1,
                                    na_values='불합격',
                                    sheet_name=group + 'A')
        df_students['체크'] = df_students['체크'].fillna('불합격')
        df_students = pd.DataFrame({
            '계열': df_students[group + '계열'],
            '대학': df_students[group + '대학교'],
            '학과': + df_students[group + '전공'],
            '점수': df_students[group + '점수'],
            '정원': df_students[group + '정원'],
            '합불': df_students['체크']
        })
        temp.append(df_students)
    df_students = pd.concat(temp, axis=0)

    # Merge
    with open('subjects.txt', 'w') as f:
        f.write(str(df_students.학과.unique()))
        f.write(str(df_comp.학과.unique().tolist()))

    standard_subjects = df_students.학과.unique().tolist()
    subjects_subjects = df_comp.학과.unique().tolist()

    def replace_sub(i):
        for sta in standard_subjects:
            if i.startswith(sta):
                i = sta
        if i == '의학과':
            i = '의예'
        elif i == '약학과':
            i = '약학'
        elif i == '공학부-전자공학':
            i = '전자'
        elif i == '공학부-컴퓨터공학':
            i = '컴퓨터공'
        elif i == '공학부-화공생명공학':
            i = '화공'
        elif i == '자연과학부-화학':
            i = '화학'
        elif i == '국제인문학부-중국문화':
            i = '중국문화'
        elif i == '지리학과(자연)':
            i = '지리학자연'
        elif i == 'Hospitality경영학부':
            i = '호경'
        elif i == '바이오의공학부':
            i = '바의공'
        elif i == '산업경영공학부':
            i = '산업공'
        elif i == '의과대학':
            i = '의예'
        elif i == '자유전공학부(자연)':
            i = '자전자연'
        elif i == '자유전공학부(인문)':
            i = '자전인문'
        elif i == '컴퓨터학과(인문)':
            i = '컴퓨터인문'
        elif i == '컴퓨터학과(자연)':
            i = '컴퓨터자연'
        elif i == '자율전공학부':
            i = '자유전공'
        elif i == '기계공학부':
            i = '기계'
        elif i == '글로벌융합대학':
            i = '글로벌융합'

        return i

    def replace_sch(i):
        if i == '가톨릭대':
            i = '가톨릭'
        elif i == '동덕여대':
            i = '동덕여'
        elif i == '서울과학기술대':
            i = '서울과'
        elif i == '대구가톨릭대':
            i = '대가대'
        elif i == '덕성여대':
            i = '덕성여'
        elif i == '가톨릭관동대':
            i = '관동대'
        elif i == '한국교원대':
            i = '교원대'
        elif i == '금오공대':
            i = '금오공'
        elif i == '단국대(천안)':
            i = '단국천'
        elif i == '이화여대':
            i = '이화여자'
        elif i == '한양대(ERICA)':
            i = '한양에'
        elif i == '한국항공대':
            i = '항공대'
        elif i == '경상국립대':
            i = '경상대'

        return i

    df_comp.학과 = df_comp.학과.map(replace_sub)
    df_comp.대학 = df_comp.대학.map(replace_sch)

    df_comp['대학과'] = df_comp['대학']+df_comp['학과']
    df_comp = df_comp.drop(['대학', '학과'], axis=1)

    df_students['대학과'] = df_students['대학'] + df_students['학과']
    df_students = df_students.drop(['대학', '학과'], axis=1)

    df_result = pd.merge(df_students, df_comp, on='대학과', how='outer')

    return df_result.dropna(), df_result[df_result['경쟁률'].isnull()], df_result[df_result['합불'].isnull()]


df, err1, err2 = generate(file_in='raw_data.xlsx',
         file_comp='competition.xlsx',)

df.to_excel('subject_with_comp.xlsx', index=False)
print(df)
err1.to_excel('err1.xlsx', index=False)
err2.to_excel('err2.xlsx', index=False)

