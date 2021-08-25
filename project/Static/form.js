document.addEventListener('load', adapt_labels);


function adapt_labels(){
    let weLabels = document.querySelectorAll('label');
    let weH2 = document.querySelectorAll('h2');
    weH2.innerText = 'arroz';
    weLabels.forEach((label) => {
        label.setAttribute('class', '')
        label.innerText += ':'
    });
}