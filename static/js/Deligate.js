let textbox = document.getElementById("textbox")

let Success = ""

let errorMessage = ""

let form = document.getElementById("form")


const SetMessages = ()=>{
    textbox.innerHTML = ""
    const chits = Messages()
    chits.forEach(message=>{
        const wrapper = document.createElement('div')
        const header = document.createElement('div')
        const content = document.createElement('div')
        const replyButton = document.createElement('button') 

        content.textContent = message.chit
        header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from._id + ">"
        
        if(message.reply_to_country)
        {
            const replyHeader = document.createElement('div')
            replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country +"'s" + " message"
            wrapper.appendChild(replyHeader)
        }
        replyButton.textContent = "Reply"
        replyButton.addEventListener('click',()=>{
            fetch('/chits/deligate/reply',{
                method:'POST',
                body:JSON.stringify({
                    chit_to:message.chit_from.name,
                }),
                headers:{
                    'Content-Type':'application/json'
                }
            })
            .then(response=>response.json())
            .then(data=>Success=data.message)
            .catch(error=>errorMessage=error.message)
        })
        wrapper.appendChild(header)
        wrapper.appendChild(content)
        wrapper.appendChild(replyButton)
        textbox.appendChild(wrapper)
    })
}

form.addEventListener('submit',()=>{
    let formData = new FormData(form)
    fetch('/chits/deligate/',{
        method:'POST',
        body:JSON.stringify(formData),
        headers:{
            'Content-Type':'application/json'
        }
    })
    .then(response=>response.json())
    .then(data=>Success=data.message)
    .catch(error=>errorMessage=error.message)
})

setInterval(SetMessages, 60000)


