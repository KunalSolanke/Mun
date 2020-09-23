var countries ,nav_toggle,main_div,sidebar,width,loadingWrapper=document.querySelector('.load'),afterLoad=document.querySelector('.after__load')  ;
window.addEventListener('load',()=>{
    
    SetMessages("initial")
    countries = document.querySelectorAll('.country')
    countries.forEach(country =>{
        country.addEventListener('click',()=>{
                inputField.value = country.querySelectorAll('div')[1].innerText ;
                countries.forEach(c=>{
                    c.classList.remove('added') ;
                    
                })
                country.classList.add("added")
                inputFieldDev.classList.add('clicked')
                inputField.classList.add('clicked')
                setTimeout(()=>{
                    inputFieldDev.classList.remove('clicked')
                    inputField.classList.remove('clicked')
                },1200)
        })
    })


    //nav_toggle
    nav_toggle = document.querySelector('.nav__toggle')
     main_div= document.querySelector('.main_div')
     sidebar = document.querySelector('.sidebar')
    nav_toggle.addEventListener('click',(e)=>{
         width = sidebar.clientWidth ;
       
        if(!nav_toggle.classList.contains('active')){
            nav_toggle.classList.add('active')
            main_div.style.transform =`translateX(${width}px)` ;
        }
        else{
            nav_toggle.classList.remove('active')
            main_div.style.transform =`translateX(0px)` ;
        }
    })
    setTimeout(()=>{
    
    afterLoad.classList.add('active')
    loadingWrapper.classList.add('inactive')},1000)
    

  
})


