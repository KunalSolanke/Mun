let textbox = document.querySelector(".chits_box"),
Success = "",
errorMessage = "",
form = document.querySelector("form"),
old_messages=[],
result =[] ,text;


var reply_to_id, type ="send",
url ,

inputField = document.querySelector('#sendTo'),
sendButton = document.querySelector('.chit_send_button'),
inputFieldDev = document.querySelector(".input_country") ;
text = document.querySelector(".message textarea")


const SetMessages = async ()=>{
    
    new_messages= await  Messages()
    result= new_messages.filter((message)=>!old_messages.some((message2)=>message.id===message2.id))
    result.forEach(message=>{
        const wrapper = document.createElement('div')
        wrapper.classList.add("single_chit")
        const header = document.createElement('div')
        header.classList.add("from")
        const content = document.createElement('div')
        content.classList.add("content")
        const button_wrapper = document.createElement('div')
        button_wrapper.classList.add('reply_button')
        const replyButton = document.createElement('button') 
        const replyHeader = document.createElement('div')
        replyHeader.classList.add('reply')
        content.textContent = message.chit
        header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from.country_id + ">"
        
        if(message.reply_to_country)
        {
            replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country +"'s " + " message"
            wrapper.appendChild(replyHeader)
        }
        replyButton.textContent = "Reply"
        replyButton.addEventListener('click',()=>{
            replyButton.classList.add('clicked')
            inputFieldDev.classList.add('clicked')
            inputField.classList.add('clicked')
            inputField.value = message.chit_from.country_id 
            type = "reply"
           reply_to_id=message.id
           setTimeout(()=>{
           replyButton.classList.remove('clicked')
           inputFieldDev.classList.remove('clicked')
           inputField.classList.remove('clicked')
           },500)
              
        })
        button_wrapper.appendChild(replyButton)
        wrapper.appendChild(header)
        wrapper.appendChild(content)
        wrapper.setAttribute("id",`${message.id}`)
        wrapper.appendChild(button_wrapper)
        textbox.appendChild(wrapper)
    })
     old_messages=new_messages ;
}





form.addEventListener('submit',(e)=>{
   
    e.preventDefault() ;
    sendButton.disabled=true 
    
    
    let formData = new FormData(form) 
    sendButton.classList.add('clicked')
   
    
    if(type=="send"){
        url ='/chits/deligate'
        send_data =JSON.stringify({
            "chit_to":formData.getAll("country_name")[0],
            "content" : formData.getAll("chit")[0]
         })
        

    }else{
        url ='/chits/deligate/reply'
        send_data =JSON.stringify({
            "chit_to":formData.getAll("country_name")[0],
            "content" : formData.getAll("chit")[0],
            "reply_to":reply_to_id
        })
    }
    fetch(url,{
        method:'POST',
        body:send_data,
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':formData.getAll('csrfmiddlewaretoken')
        }
    })
    .then(response=>response.json())
    .then(data=>{
        Success=data.message
        type ="send"
        
    })
    .catch(error=>errorMessage=error.message)
    setTimeout(()=>{
        sendButton.disabled=false
        text.disabled= false
        sendButton.classList.remove('clicked')
        console.log(text) 
        text.value =""
        
      
    },1000)
})

setInterval(SetMessages, 5000)


