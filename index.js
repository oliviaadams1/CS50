document.addEventListener('DOMContentLoaded', function () {

    let correct = document.querySelector('.correct');
    correct.addEventListener('click', function () {
        correct.style.backgroundColor = 'green';
        document.querySelector('#mc-feedback').innerHTML = "Correct!";
    });

    let incorrects = document.querySelectorAll('.incorrect');
    for (let i = 0; i < incorrects.length; i++) {
        incorrects[i].addEventListener('click', function () {
            incorrects[i].style.backgroundColor = 'red';
            document.querySelector('#mc-feedback').innerHTML = 'Incorrect';
        });
    }

    document.querySelector('#fr-btn').addEventListener('click', function () {
        let input = document.querySelector('input');
        if (input.value === 'Na') {
            input.style.backgroundColor = 'green'
            document.querySelector('#fr').innerHTML = 'Correct!';
        } else {
            input.style.backgroundColor = 'red'
            document.querySelector('#fr').innerHTML = 'Incorrect';
        }
    });
});