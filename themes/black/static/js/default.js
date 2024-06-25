function getRandomColor() {
    let color;
    do {
        color = Math.floor(Math.random() * 16777215).toString(16);
        while (color.length < 6) {
            color = "0" + color;
        }
        color = "#" + color;
    } while (isTooDark(color));
    return color;
}

function isTooDark(color) {
    const r = parseInt(color.slice(1, 3), 16);
    const g = parseInt(color.slice(3, 5), 16);
    const b = parseInt(color.slice(5, 7), 16);

    const brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    return brightness < 0.4; 
}

const randomColor = getRandomColor();
document.documentElement.style.setProperty('--animate-color', randomColor);