const randomColor = "#"+((1<<24)*Math.random()|0).toString(16); 

document.documentElement.style.setProperty('--animate-color', randomColor);