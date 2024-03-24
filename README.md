# TeX2Image

## 0. Problem I met
* I want to obtain images of compiled LaTeX equations, but the range of syntax supported by each TeX compiler varies slightly, making the success of compilation inconsistent & incoherent.

* * *
## 1. Bring formulas from arxiv html files
1. Extract the IDs of the latest papers by category in arXiv's math category. The function allows specifying the category, the number of papers to extract, and the save directory as arguments. The format of the ID is like 2403.12345v1.

2. If an HTML file exists for a paper's ID, the HTML file is retrieved. (There are cases where no HTML file exists.) The HTML file contains equations in math alttext tags. These equations are extracted using BeautifulSoup. All these equations are successfully compiled in arXiv's HTML viewer.

3. For 32 math categories, equations are extracted for n papers per category. (Total 32*n papers). A csv file is created for each paper, and finally, all are combined into one csv file.

## 2. Bring TeX datas in HTML file with MathJax (Editing)
* MathJax can compile a wide range of expressions.
* Bring TeX datas in csv file from 1. in HTML file.

## 3. Capture the formula images in page (Editing)
* Using puppeteer and Node.js, we can capture the images.

## Finally, we can get TeX data and Images.
