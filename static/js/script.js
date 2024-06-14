const board = document.getElementById('drawing-board');
const clearBtn = document.getElementById('clear-btn');
const predictBtn = document.getElementById('guess-btn');
const predictionText = document.getElementById('guess-result');

for (let i = 0; i < 28 * 28; i++) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.addEventListener('mousedown', () => cell.classList.add('active'));
    cell.addEventListener('mouseover', (e) => {
        if (e.buttons === 1) cell.classList.add('active');
    });
    board.appendChild(cell);
}

clearBtn.addEventListener('click', () => {
    document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('active'));
    typewriterInstance.deleteAll(1).typeString('Alright, lets start again. You can start drawing.').start();
});

predictBtn.addEventListener('click', async () => {
    const cells = document.querySelectorAll('.cell');
    const drawing = Array.from(cells).map(cell => cell.classList.contains('active') ? 1 : 0);

    if (drawing.every(cell => cell === 0)) {
        typewriterInstance.deleteAll(1).typeString('Ok, draw some animal, will ya?').start();
        return;
    }

    const response = await fetch('/guess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ drawing }),
    });

    const result = await response.json();
    typewriterInstance.deleteAll(1).typeString(result.label).start();
});

const typewriterInstance = new Typewriter(predictionText, {
    loop: false,
    delay: 1,
    deleteSpeed: 1,
    pauseFor: 500
});

typewriterInstance.typeString('Hello, lets draw dome animals!').start();

