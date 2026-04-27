document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('checkForm');
    const xInput = document.getElementById('xInput');
    const yInput = document.getElementById('yInput');
    const rInput = document.getElementById('rInput');

    function showErrorMessage(message) {
        const errorMessageDiv = document.getElementById('errorMessage');
        errorMessageDiv.textContent = message;
        errorMessageDiv.style.display = 'block';
    }

    function hideErrorMessage() {
        const errorMessageDiv = document.getElementById('errorMessage');
        errorMessageDiv.style.display = 'none';
    }

    form.addEventListener('submit', function (e) {
        let isValid = true;
        let errorMessage = "";

        const x = xInput.value.trim();
        if (x === "") {
            errorMessage = "Поле X не должно быть пустым.\n";
            isValid = false;
        } else if (x.length > 8) {
            errorMessage += "X не должен содержать более 8 символов.\n";
            isValid = false;
        } else {
            const numberRegex = /^-?\d*\.?\d+$/;
            if (!numberRegex.test(x)) {
                errorMessage += "X должен быть числом.\n";
                isValid = false;
            } else {
                const xNum = parseFloat(x);
                if (xNum < -5 || xNum > 5) {
                    errorMessage += "X должен быть в диапазоне от -5 до 5.\n";
                    isValid = false;
                }
            }
        }

        const y = yInput.value.trim();
        if (y === "") {
            errorMessage = "Поле Y не должно быть пустым.\n";
            isValid = false;
        } else {
            const numberRegex = /^-?\d*\.?\d+$/;
            if (!numberRegex.test(y)) {
                errorMessage += "Y должен быть числом.\n";
                isValid = false;
            } else {
                const yNum = parseFloat(y);
                if (yNum < -3 || yNum > 5) {
                    errorMessage += "Y должен быть в диапазоне от -3 до 5.\n";
                    isValid = false;
                }
            }
        }

        const r = rInput.value.trim();
        if (r === "") {
            errorMessage = "Поле R не должно быть пустым.\n";
            isValid = false;
        } else {
            const numberRegex = /^-?\d*\.?\d+$/;
            if (!numberRegex.test(r)) {
                errorMessage += "R должен быть числом.\n";
                isValid = false;
            } else {
                const yNum = parseFloat(y);
                if (yNum < 0.1 || yNum > 3) {
                    errorMessage += "R должен быть в диапазоне от 0.1 до 3.\n";
                    isValid = false;
                }
            }
        }

        if (!isValid) {
            e.preventDefault();
            showErrorMessage(errorMessage.trim());
        } else {
            hideErrorMessage();
        }
    });

    xInput.addEventListener('input', hideErrorMessage);
    yInput.addEventListener('change', hideErrorMessage);
    rInput.addEventListener('input', hideErrorMessage);
});

