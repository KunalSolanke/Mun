let textbox = document.querySelector(".chits_box"),
Success = "",
errorMessage = "",
form = document.querySelector("form"),
old_messages=[],
result =[] ;


var reply_to_id, type ="send",
url ,
inputField = document.querySelector('#sendTo'),
sendButton = document.querySelector('.chit_send_button'),
inputFieldDev = document.querySelector(".input_country"),
csrf = document.querySelector(".csrf"),
chit_div ;


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
        const ApproveButton = document.createElement('button') 
        const DisapproveButton = document.createElement('button') 

        content.textContent = message.chit
        header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from.country_id + ">"
        
        if(message.reply_to_country)
        {
            const replyHeader = document.createElement('div')
            replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country +"'s" + " message"
            wrapper.appendChild(replyHeader)
        }
        ApproveButton.textContent = "Approve"
        DisapproveButton.textContent = "Disapprove"
        ApproveButton.addEventListener('click',()=>{
            ApproveButton.disabled=true 
            ApproveButton.classList.add('clicked')
            fetch('/chits/moderator/',{
                
                method:'POST',
                body:JSON.stringify({
                    chit_id:message.id,
                }),
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrf.value
                }
            })
            .then(response=>response.json())
            .then(data=>{Success=data.message
                chit_div =document.getElementById(message.id)
                chit_div.remove()
               })
            .catch(error=>errorMessage=error.message)

            setTimeout(()=>{
                ApproveButton.disabled=false
                ApproveButton.classList.remove('clicked') 
              
            },2000)
        })
        DisapproveButton.addEventListener('click',()=>{
            DisapproveButton.disabled=true 
            DisapproveButton.classList.add('clicked')
            fetch('/chits/moderator/disapprove/',{
                method:'POST',
                body:JSON.stringify({
                    chit_id:message.id,
                }),
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken':csrf.value
                }
            })
            .then(response=>response.json())
            .then(data=>{
                Success=data.message
                chit_div =document.getElementById(message.id)
                chit_div.remove()
            })
            .catch(error=>errorMessage=error.message)
            setTimeout(()=>{
                DisapproveButton.disabled=false
                DisapproveButton.classList.remove('clicked') 
              
            },2000)
        })

        button_wrapper.appendChild(ApproveButton)
        button_wrapper.appendChild(DisapproveButton)
        wrapper.appendChild(header)
        wrapper.appendChild(content)
        wrapper.appendChild(button_wrapper)
        wrapper.setAttribute("id",`${message.id}`)
        textbox.appendChild(wrapper)
    })
    old_messages=new_messages ;
}

setInterval(SetMessages, 10000)


