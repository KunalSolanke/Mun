let chits = [];

const Messages = ()=>{
    fetch('/chits/api/messages',{
        method:'GET',
        mode:'cors',
        cache:'no-cache',
        headers:{
            'Content-Type': 'application/json'
        }
    })
    .then(response=>response.json())
    .then(messages=>chits=messages)
    .catch(error=>console.log(error))
    return chits
}

//setInterval(Messages, 60000)

