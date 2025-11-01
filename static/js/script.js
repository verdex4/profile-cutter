function calculate() {
    console.log("hello");
}

function show_text() {
    document.getElementById('result').textContent = "hello!!!!"
}  

document.getElementById('algorithm-form').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log("Form submitted!");
    
    const formData = new FormData(this);
    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});