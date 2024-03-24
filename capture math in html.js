const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  

// 뷰포트를 1920x1080으로 설정하고 deviceScaleFactor를 2로 설정하여 해상도를 높임
    await page.setViewport({
    width: 1920,
    height: 1080,
    deviceScaleFactor: 2,
    });

  // HTML 파일의 로컬 경로 또는 웹 URL을 여기에 입력하세요.
  await page.goto('C:/Users/wjdrb/vscode_code/mathjax html.html', {waitUntil: 'networkidle2'});

  // MathJax가 렌더링한 수학식을 포함하는 요소를 찾음 (예: 모든 <p> 태그)
  const elements = await page.$$('mjx-math');

  // 각 요소의 스크린샷 캡처
  for (let i = 0; i < elements.length; i++) {
    await elements[i].screenshot({path: `captured_images/equation_${i + 1}.png`});
  }

  await browser.close();
})();
