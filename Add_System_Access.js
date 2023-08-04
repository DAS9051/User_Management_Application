function handleSubmit(event) {
    event.preventDefault(); 
 
    var userName = document.getElementById("user_name").value;
    var System_Name = document.getElementById("System_Name").value;
    var System_User_Name = document.getElementById("System_User_Name").value;

    domain = "http://127.0.0.1:5000/add-system-access";
    url = domain.concat("/",System_Name , "/", userName, "/", System_User_Name)  
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
