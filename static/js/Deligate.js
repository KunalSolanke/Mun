
var reply_to_id
let textbox = document.querySelector(".chits_box")
let Success = ""
let errorMessage = ""
let form = document.querySelector("form")
var type ="send"
var url ;
var inputField = document.querySelector('#sendTo')
var sendButton = document.querySelector('.chit_send_button')
const SetMessages = ()=>{
    textbox.innerHTML = ""
    const chits = Messages()
    
    chits.forEach(message=>{
        const wrapper = document.createElement('div')
        wrapper.classList.add("single_chit")
        const header = document.createElement('div')
        header.classList.add("from")
        const content = document.createElement('div')
        content.classList.add("content")
        const button_wrapper = document.createElement('div')
        button_wrapper.classList.add('reply_button')
        const replyButton = document.createElement('button') 
        
        content.textContent = message.chit
        header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from.country_id + ">"
        
        if(message.reply_to_country)
        {
            const replyHeader = document.createElement('div')
            replyHeader.classList.add('reply')
            replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country +"'s " + " message"
            wrapper.appendChild(replyHeader)
        }
        replyButton.textContent = "Reply"
        replyButton.addEventListener('click',()=>{
            inputField.value = message.chit_from.country_id 
            type = "reply"
           reply_to_id=message.id
           console.log(message)
           
            
        })
        button_wrapper.appendChild(replyButton)
        wrapper.appendChild(header)
        wrapper.appendChild(content)
        wrapper.appendChild(button_wrapper)
        textbox.appendChild(wrapper)
    })

  // textbox.scrollTop = textbox.scrollHeight - textbox.clientHeight;
}





form.addEventListener('submit',(e)=>{
   
    e.preventDefault() ;
    sendButton.disabled=true 
    
    let formData = new FormData(form) 
    var send_data 
    
    if(type=="send"){
        url ='/chits/deligate/'
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
    },3000)
})

setInterval(SetMessages, 5000)


