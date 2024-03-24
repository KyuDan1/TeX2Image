import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

# 32 math categories
math_categories = [
    "math.AG",
    "math.AT",
    "math.AP",
    "math.CT",
    "math.CA",
    "math.CO",
    "math.AC",
    "math.CV",
    "math.DG",
    "math.DS",
    "math.FA",
    "math.GM",
    "math.GN",
    "math.GT",
    "math.GR",
    "math.HO",
    "math.IT",
    "math.KT",
    "math.LO",
    "math.MP",
    "math.MG",
    "math.NT",
    "math.NA",
    "math.OA",
    "math.OC",
    "math.PR",
    "math.QA",
    "math.RT",
    "math.RA",
    "math.SP",
    "math.ST",
    "math.SG",
]

# Given category of arXiv, get arxiv paper id and output list.
def get_arxiv_papers_link(category="math.AG", max_papers=5, save_dir="./arxiv_papers"):
    html_link = []
    base_url = "https://arxiv.org"
    category_url = f"{base_url}/list/{category}/current"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        response = requests.get(category_url)
        if response.status_code != 200:
            print("Failed to retrieve the webpage")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        paper_links = soup.find_all("a", title="Abstract", limit=max_papers)
        

        for link in paper_links:
            abstract_page = base_url + link["href"]
            extracted_content = abstract_page.rsplit('/', 1)[-1] +"v1"
            html_link.append(extracted_content)
        #print(html_link)
        return html_link
            

    except Exception as e:
        print(f"An error occurred: {e}")


# If we get id of paper, get mathematics formula from html file
def get_math_expressions(arxiv_id, file_name='math_expressions.csv'):
    # HTML 파일의 URL
    url = f'https://arxiv.org/html/{arxiv_id}'


    response = requests.get(url)
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        # <math alttext=""> tag
        math_tags = soup.find_all('math', alttext=True)
        unique_expressions = set() #uniqueness
                
        for tag in math_tags:
            alttext = tag['alttext'].strip()
            unique_expressions.add(alttext)
        
        # save in csv 
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['TeX'])
            for expression in unique_expressions:
                writer.writerow([expression])
                
        print(f'formula saved: {file_name}')
    else:
        return -1

# get formula in csv.
    # 32 * 30 = 960 papers
count = 0
error_count = 0
for categ in math_categories:
    for id in get_arxiv_papers_link(category=categ, max_papers=30, save_dir="./arxiv_papers"):
        try:
            get_math_expressions(id, file_name=f"csv_files/{id}_tex.csv")
            count = count + 1
            print(count, "/ 960")
        except Exception as e:
            count = count + 1
            error_count = error_count +1
            print(count, "/ 960")
            continue
print(f"complete, error:{error_count}  complete:{960-error_count}")
            





# combine in one csv file.
folder_path = 'csv_files'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

tex_data = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, usecols=['TeX'])  # 'TeX' 열만 읽어옵니다.
    tex_data.append(df)

combined_df = pd.concat(tex_data).drop_duplicates().reset_index(drop=True)
output_path = os.path.join(folder_path, 'combined_tex.csv')
combined_df.to_csv(output_path, index=False)
print(f'combined csv file : {output_path}')

