const form =  document.getElementById('form');
const contact =  document.getElementById('contact');
const password =  document.getElementById('password');

form.addEventListener('submit', (e) =>{
    e.preventDefault();

    checkInputs();
});

function checkInputs(){
    const contactvalue = contact.value.trim();
    const passwordvalue = password.value.trim();

    if(contactvalue == ''){
        setErrorFor(contact, 'This feild cannot be blank')
    }else{
    }

    if(passwordvalue == ''){
        setErrorFor(password, 'This feild cannot be blank')
    }else{
    }
}

    function setErrorFor(input, message){
        const formControl = input.parentElement;
        const small = formControl.querySelector('small');
        small.innerText=message;
        formControl.className = 'form-control error';
    }
