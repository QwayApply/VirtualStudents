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

    def replace(i):
        for sta in standard_subjects:
            if i.startswith(sta):
                i = sta
        return i

    df_comp.학과 = df_comp.학과.map(replace)

    df_comp['대학과'] = df_comp['대학']+df_comp['학과']
    df_comp = df_comp.drop(['대학', '학과'], axis=1)

    df_students['대학과'] = df_students['대학'] + df_students['학과']
    df_students = df_students.drop(['대학', '학과'], axis=1)

    df_result = pd.merge(df_students, df_comp, on='대학과', how='outer')

    return df_result.dropna(), df_result[df_result['경쟁률'].isnull()]


df, err = generate(file_in='raw_data.xlsx',
         file_comp='competition.xlsx',)

df.to_excel('subject_with_comp.xlsx', index=False)
err.to_excel('err.xlsx', index=False)
