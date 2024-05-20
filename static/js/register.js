const form =  document.getElementById('form');
const username =  document.getElementById('username');
const contact =  document.getElementById('contact');
const password =  document.getElementById('password');
const password2 =  document.getElementById('password2');

form.addEventListener('submit', (e) =>{
    e.preventDefault();

    checkInputs();
});

function checkInputs(){
    const usernamevalue = username.value.trim();
    const contactvalue = contact.value.trim();
    const passwordvalue = password.value.trim();
    const password2value = password2.value.trim();

    if(usernamevalue == ''){
        setErrorFor(username, 'This feild cannot be blank');
    } else {
        setSuccessFor(username);
    }

    if(contactvalue == ''){
        setErrorFor(contact, 'This feild cannot be blank')
    }else if (!isContact(contactvalue)){
        setErrorFor(contact,'It should contain only 10 digits')
    } else{
        setSuccessFor(contact);
    }


    if(passwordvalue == ''){
        setErrorFor(password, 'This feild cannot be blank')
    }else if (!isPassword(passwordvalue)){
        setErrorFor(password,'Password should contain atleast 8 char,1 uppercase,1 lowercase,1 digit,1 special char')
    } else{
        setSuccessFor(password);
    }

    if(password2value == ''){
        setErrorFor(password2, 'This feild cannot be blank')
    }else if (passwordvalue !== password2value){
        setErrorFor(password2,'Passwords does not match')
    } else{
        setSuccessFor(password2);
    }
}

function setErrorFor(input, message){
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    small.innerText=message;
    formControl.className = 'form-control error';
}

function setSuccessFor(input){
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}


function isPassword(password){
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=|{}[\]:;'"<>,.?/~]).{8,}$/.test(password);
}

function isContact(contact){
    return /^\d{10}$/.test(contact)
}