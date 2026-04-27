document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('areaGraph');
    if (!canvas) return;

    canvas.addEventListener('click', function(e) {
        const rect = canvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const scale = 50;

        const textInputs = document.querySelectorAll('#mainForm input[type="text"]');
        let rNum;

        if (textInputs.length >= 3) {
            const existingR = parseFloat(textInputs[2].value.replace(',', '.'));
            if (!isNaN(existingR) && existingR >= 0.1 && existingR <= 3.0) {
                rNum = existingR;
            } else {
                const rValue = prompt("Введите R (0.1-3.0):", "1.0");
                if (!rValue) return;
                rNum = parseFloat(rValue.replace(',', '.'));
                if (isNaN(rNum) || rNum < 0.1 || rNum > 3.0) {
                    alert("R должен быть числом от 0.1 до 3.0");
                    return;
                }
            }
        } else {
            const rValue = prompt("Введите R (0.1-3.0):", "1.0");
            if (!rValue) return;
            rNum = parseFloat(rValue.replace(',', '.'));
            if (isNaN(rNum) || rNum < 0.1 || rNum > 3.0) {
                alert("R должен быть числом от 0.1 до 3.0");
                return;
            }
        }

        const x = ((clickX - centerX) / (scale * 4)) * rNum;
        const y = ((centerY - clickY) / (scale * 4)) * rNum;

        const xFormatted = Math.round(x);
        const yFormatted = parseFloat(y.toFixed(3));
        const rFormatted = parseFloat(rNum.toFixed(1));

        if (textInputs.length >= 3) {
            textInputs[0].value = xFormatted;
            textInputs[1].value = yFormatted;
            textInputs[2].value = rFormatted;
        }

        setTimeout(() => {
            const button = document.querySelector('#mainForm [type="submit"]');
            if (button) button.click();
        }, 150);
    });
});