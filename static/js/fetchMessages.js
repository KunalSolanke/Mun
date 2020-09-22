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
    
    if(json.detail && json.detail == "Authentication credentials were not provided."){
       
        window.location="/accounts/login" 
        
    }else{
      new_messages = json }
    return new_messages
}


