const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

const html_files_directory_path = 'C:/Users/wjdrb/vscode_code/htmls';
const captured_images_directory = 'captured_images';

// 리스너의 최대 개수 조정
require('events').EventEmitter.defaultMaxListeners = 15;

// HTML 파일을 처리하는 함수
async function processHtmlFile(filePath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.setViewport({
    width: 1920,
    height: 1080,
    deviceScaleFactor: 2,
  });

  // 로컬 HTML 파일 경로로 이동
  await page.goto(`file://${filePath}`, {waitUntil: 'networkidle2'});

  // 'mjx-math' 요소가 가시적일 때까지 대기
  await page.waitForSelector('mjx-math', {visible: true});

  const elements = await page.$$('mjx-math');

  for (let i = 0; i < elements.length; i++) {
    try {
      const screenshotPath = path.join(__dirname, captured_images_directory, `equation_${path.basename(filePath, '.html')}_${i + 1}.png`);
      await elements[i].screenshot({path: screenshotPath});
    } catch (error) {
      console.error(`오류 발생: 파일 '${path.basename(filePath)}', 요소 인덱스 ${i + 1} - ${error.message}`);
      // 오류를 캐치했으나, 루프는 계속됩니다.
    }
  }

  await browser.close();
}

(async () => {
  try {
    const files = await fs.readdir(html_files_directory_path);
    const htmlFiles = files.filter(file => file.endsWith('.html'));

    await Promise.all(htmlFiles.map(file => {
      const filePath = path.join(html_files_directory_path, file);
      return processHtmlFile(filePath);
    }));

    console.log('모든 HTML 파일이 처리되었습니다.');
  } catch (error) {
    console.error('오류 발생:', error);
  }
})();
