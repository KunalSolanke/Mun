let textbox = document.getElementById("textbox")

let Success = ""

let errorMessage = ""

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
        const ApproveButton = document.createElement('button') 
        const DisapproveButton = document.createElement('button') 

        content.textContent = message.chit
        header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from._id + ">"
        
        if(message.reply_to_country)
        {
            const replyHeader = document.createElement('div')
            replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country +"'s" + " message"
            wrapper.appendChild(replyHeader)
        }
        ApproveButton.textContent = "Approve"
        DisapproveButton.textContent = "Disapprove"
        ApproveButton.addEventListener('click',()=>{
            fetch('/chits/moderator',{
                method:'POST',
                body:JSON.stringify({
                    chit_id:message.id,
                }),
                headers:{
                    'Content-Type':'application/json'
                }
            })
            .then(response=>response.json())
            .then(data=>Success=data.message)
            .catch(error=>errorMessage=error.message)
        })
        DisapproveButton.addEventListener('click',()=>{
            fetch('/chits/moderator/disapprove',{
                method:'POST',
                body:JSON.stringify({
                    chit_id:message.id,
                }),
                headers:{
                    'Content-Type':'application/json'
                }
            })
            .then(response=>response.json())
            .then(data=>Success=data.message)
            .catch(error=>errorMessage=error.message)
        })

        button_wrapper.appendChild(ApproveButton)
        button_wrapper.appendChild(DisapproveButton)
        wrapper.appendChild(header)
        wrapper.appendChild(content)
        wrapper.appendChild(button_wrapper)
        textbox.appendChild(wrapper)
    })
}

setInterval(SetMessages, 10000)


