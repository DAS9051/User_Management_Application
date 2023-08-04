function handleSubmit(event) {
    event.preventDefault(); 
 
    var System_Name = document.getElementById("System_Name").value;


    domain = "http://127.0.0.1:5000/delete-system";
    url = domain.concat("/", System_Name)  
    console.log(url)
    fetch(url, {
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.text())
    .then(text => console.log(text))
}

var form = document.querySelector("form");
form.addEventListener("submit", handleSubmit);
