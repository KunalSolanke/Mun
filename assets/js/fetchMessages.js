let new_messages = [];
const Messages = async ()=>{
    const response =await fetch('/chits/api/messages/',{
        method:'GET',
        mode:'cors',
        cache:'no-cache',
        headers:{
            'Content-Type': 'application/json'
        }
    })
    const json = await response.json()
    new_messages = json 
    return new_messages
}


