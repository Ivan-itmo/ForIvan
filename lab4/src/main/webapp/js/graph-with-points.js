function drawAreaGraphWithPoints(lastR, allResults) {
    const canvas = document.getElementById('areaGraph');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const scale = 50;
    const tickLength = 8;

    ctx.clearRect(0, 0, width, height);
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.lineWidth = 0.5;

    for (let i = -8; i <= 8; i++) {
        const x = centerX + i * scale / 2;
        ctx.beginPath();
        ctx.moveTo(x, centerY - scale * 4);
        ctx.lineTo(x, centerY + scale * 4);
        ctx.stroke();
    }

    for (let i = -8; i <= 8; i++) {
        const y = centerY - i * scale / 2;
        ctx.beginPath();
        ctx.moveTo(centerX - scale * 4, y);
        ctx.lineTo(centerX + scale * 4, y);
        ctx.stroke();
        ctx.strokeStyle = '#000';
    }
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1.5;

    ctx.beginPath();
    ctx.moveTo(centerX - scale * 4, centerY);
    ctx.lineTo(centerX + scale * 4, centerY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY - scale * 4);
    ctx.lineTo(centerX, centerY + scale * 4);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(centerX + scale * 4 - 8, centerY - 5);
    ctx.lineTo(centerX + scale * 4, centerY);
    ctx.lineTo(centerX + scale * 4 - 8, centerY + 5);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(centerX - 5, centerY - scale * 4 + 8);
    ctx.lineTo(centerX, centerY - scale * 4);
    ctx.lineTo(centerX + 5, centerY - scale * 4 + 8);
    ctx.fill();

    ctx.font = '14px Arial';
    ctx.fillStyle = '#000';
    ctx.fillText('X', centerX + scale * 4 + 10, centerY - 10);
    ctx.fillText('Y', centerX + 10, centerY - scale * 4 - 10);

    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.font = '12px Arial';

    for (let i = -4; i <= 4; i++) {
        const x = centerX + i * scale;
        ctx.beginPath();
        ctx.moveTo(x, centerY - tickLength);
        ctx.lineTo(x, centerY + tickLength);
        ctx.stroke();

        if (i === -4) ctx.fillText('-R', x - 12, centerY + 20);
        if (i === -2) ctx.fillText('-R/2', x - 12, centerY + 20);
        if (i === 2)  ctx.fillText('R/2', x - 12, centerY + 20);
        if (i === 4)  ctx.fillText('R', x - 6, centerY + 20);
    }

    for (let i = -4; i <= 4; i++) {
        const y = centerY - i * scale;
        ctx.beginPath();
        ctx.moveTo(centerX - tickLength, y);
        ctx.lineTo(centerX + tickLength, y);
        ctx.stroke();

        if (i === -4) ctx.fillText('-R', centerX + 15, y + 4);
        if (i === -2) ctx.fillText('-R/2', centerX + 15, y + 4);
        if (i === 2)  ctx.fillText('R/2', centerX + 15, y + 4);
        if (i === 4)  ctx.fillText('R', centerX + 15, y + 4);
    }

    ctx.fillStyle = 'rgba(0, 123, 255, 0.3)';

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, scale * 4, Math.PI * 0.5, Math.PI);
    ctx.closePath();
    ctx.fill();

    ctx.fillRect(
        centerX,
        centerY - scale * 2,
        scale * 4,
        scale * 2
    );

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX - scale * 2, centerY);
    ctx.lineTo(centerX, centerY - scale * 4);
    ctx.closePath();
    ctx.fill();

    if (Array.isArray(allResults)) {
        allResults.forEach(point => {
            const normalizedX = point.x * (point.r / lastR);
            const normalizedY = point.y * (point.r / lastR);
            const px = centerX + normalizedX * scale * 4 / point.r;
            const py = centerY - normalizedY * scale * 4 / point.r;

            ctx.fillStyle = point.hit ? 'green' : 'red';
            ctx.beginPath();
            ctx.arc(px, py, 5, 0, 2 * Math.PI);
            ctx.fill();
        });
    }
}
