async function clear() {
	const response = await fetch("/api/clear", {method: "DELETE"});
	const data = await response.json()
	const resultDiv = document.getElementById('result');
	const resultP = document.createElement('p');
	resultP.textContent = `Кількість вилучених користувачів: ${data.amount}`;
	resultP.style.color = 'black';
	resultP.style.fontSize = '30px';
	resultP.style.fontFamily = 'Arial, sans-serif';
	resultDiv.appendChild(resultP)
}


document.getElementById("clear").addEventListener("click", clear);
