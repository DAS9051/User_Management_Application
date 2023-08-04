function handleSubmit(event) {
    event.preventDefault(); 
 
    var System_Name = document.getElementById("System_Name").value;
    var Description = document.getElementById("Description").value;
    var Company = document.getElementById("Company").value;
    var Software = document.getElementById("Software").value;

    domain = "http://127.0.0.1:5000/create-system";
    url = domain.concat("/", System_Name, "/", Description, "/", Company, "/", Software)  
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
