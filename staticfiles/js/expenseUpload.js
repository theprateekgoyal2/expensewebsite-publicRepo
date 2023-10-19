// JavaScript to show/hide the CSV upload form
const uploadCsvButton = document.getElementById('upload-csv-button');
const csvUploadForm = document.getElementById('csv-upload-form');
const cancelCsvUpload = document.getElementById('cancel-csv-upload');

uploadCsvButton.addEventListener('click', () => {
  csvUploadForm.style.display = 'block';
  uploadCsvButton.style.display = 'none';
});

cancelCsvUpload.addEventListener('click', () => {
    csvUploadForm.style.display = 'none';
    uploadCsvButton.style.display = 'block';
});