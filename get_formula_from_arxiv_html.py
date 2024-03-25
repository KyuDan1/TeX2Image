import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


# Given category of arXiv, get arxiv paper id and output list.
def get_arxiv_papers_link(category, max_papers=500, year="24", month="03" ):
    html_link = []
    base_url = "https://arxiv.org"
    category_url = f"{base_url}/list/{category}/{year}{month}?show=1000"
    print(category_url)
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
    # HTML  URL
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

def main():
    # 32 math categories
    math_categories = ['cs.HC',
  'cs.IR',
  'cs.IT',
  'cs.LG',
  'cs.LO',
  'cs.MA',
  'cs.MM',
  'cs.MS',
  'cs.NA',
  'cs.NE',
  'cs.NI',
  'cs.OH',
  'cs.OS',
  'cs.PF',
  'cs.PL',
  'cs.RO',
  'cs.SC',
  'cs.SD',
  'cs.SE',
  'cs.SI',
  'cs.SY']
    #start year, month
    year = 24
    month = 3

    #end year, month
    end_year = 20
    end_month = 3

   
    if not os.path.exists('csv_files_cs_2'):
        os.makedirs('csv_files_cs_2')

    # ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=24) as executor:
        # Future
        futures = [executor.submit(process_category, category, year, month, end_year, end_month) for category in math_categories]

       
        for future in as_completed(futures):
            print(future.result())  

def process_category(category, year, month, end_year, end_month):
    count = 0
    while True:
        for id in get_arxiv_papers_link(category=category, max_papers=500, year=f"{year:02d}", month=f"{month:02d}"):
            try:
                get_math_expressions(id, file_name=f"csv_files_cs_2/{id}_tex.csv")
                count = count + 1
                print(count)
            except Exception as e:
                count = count + 1
                print(count)
                continue
        
        if year == end_year and month == end_month:
            break
        
        month -= 1
        
        if month < 1:
            year -= 1
            month = 12

    print("complete")
            

if __name__ == "__main__":
    main()



# combine in one csv file.
folder_path = 'csv_files_cs_2'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

tex_data = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, usecols=['TeX'])  
    tex_data.append(df)

combined_df = pd.concat(tex_data).drop_duplicates().reset_index(drop=True)
output_path = os.path.join(folder_path, 'combined_tex.csv')
combined_df.to_csv(output_path, index=False)
print(f'combined csv file : {output_path}')
