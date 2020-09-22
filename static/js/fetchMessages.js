let new_messages = [];
const Messages = async (url)=>{
    const response =await fetch(`/chits/api/messages/${url}`,{
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


