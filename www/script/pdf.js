const container = document.querySelector('.feinpdf-container');
const url = container.getAttribute('data-url'); // HTMLコードで指定したPDFファイルのURLを取得
const pdfjsLib = window['pdfjs-dist/build/pdf'];
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.6.347/pdf.worker.min.js';

let pdfDoc = null,
 pageNum = 1,
 pageRendering = false,
 pageNumPending = null,
 feincanvas = document.createElement('canvas'),
 ctx = feincanvas.getContext('2d');

document.getElementById('feinpdf-viewer').appendChild(feincanvas);

function renderPage(num) {
 pageRendering = true;
 pdfDoc.getPage(num).then(page => {
  const containerWidth = document.getElementById('feinpdf-viewer').clientWidth;
  const scale = 3;
  const viewport = page.getViewport({ scale: scale });

  feincanvas.height = viewport.height;
  feincanvas.width = viewport.width;

  const renderContext = {
   canvasContext: ctx,
   viewport: viewport
  };
  const renderTask = page.render(renderContext);

  renderTask.promise.then(() => {
   feincanvas.style.width = `${containerWidth}px`;
   feincanvas.style.height = "auto";

   pageRendering = false;
   if (pageNumPending !== null) {
    renderPage(pageNumPending);
    pageNumPending = null;
   }
  });
 });

 document.getElementById('page-num').textContent = num;
}

function queueRenderPage(num) {
 if (pageRendering) {
  pageNumPending = num;
 } else {
  renderPage(num);
 }
}

// PDFを部分的にロード
pdfjsLib.getDocument({ url: url, rangeChunkSize: 65536 }).promise.then(pdfDoc_ => {
 pdfDoc = pdfDoc_;
 document.getElementById('page-count').textContent = pdfDoc.numPages;
 renderPage(pageNum);
});

document.getElementById('prev-page').addEventListener('click', () => {
 if (pageNum <= 1) {
  return;
 }
 pageNum--;
 queueRenderPage(pageNum);
});

document.getElementById('next-page').addEventListener('click', () => {
 if (pageNum >= pdfDoc.numPages) {
  return;
 }
 pageNum++;
 queueRenderPage(pageNum);
});
