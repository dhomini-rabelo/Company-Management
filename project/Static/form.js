document.addEventListener('DOMContentLoaded', adapt_labels)

function adapt_labels(){
    let weTextArea = document.querySelector('textarea')
    let weLabels = document.querySelectorAll('label')
    let weInputs = document.querySelectorAll('input')

    weTextArea.setAttribute('rows', '2')
    weTextArea.setAttribute('required', '')

    weLabels.forEach((label) => {
        if ('span' === label.innerHTML.slice(label.innerHTML.length - 6, label.innerHTML.length - 2)){
            label.innerHTML = label.innerHTML.slice(0, label.innerHTML.length - 35)
            label.innerHTML += ':'
        }else{
            label.innerHTML = `${label.innerHTML.slice(0, label.innerHTML.length - 13)}:`
        }
    })

    weInputs.forEach((input) => {
        let type = input.getAttribute('type')
        let name = input.getAttribute('name')
        let nameExceptions = {'nome_user':1, 'email_user':3, 'bio':2}
        if ((type !== 'file' && type !== 'submit' && type !== 'hidden')&&(!(name in nameExceptions))){
            input.setAttribute('required', '')
            input.setAttribute('value', '')
        }
        if (type === 'text' && input.getAttribute('name').slice(0, 4) == 'data'){
            input.setAttribute('type', 'date')
            input.setAttribute('value', '2021-01-01')
        }
    })

}