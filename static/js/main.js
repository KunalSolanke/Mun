window.addEventListener('load',()=>{
    const countries = document.querySelectorAll('.country')
    const inputField = document.querySelector('#sendTo')
    countries.forEach(country =>{
        country.addEventListener('click',()=>{
                inputField.value = country.querySelectorAll('div')[1].innerText ;
                countries.forEach(c=>{
                    c.classList.remove('added') ;
                })
                country.classList.add("added")
        })
    })


    //nav_toggle
    var nav_toggle = document.querySelector('.nav__toggle')
    var main_div= document.querySelector('.main_div')
    var sidebar = document.querySelector('.sidebar')
    nav_toggle.addEventListener('click',(e)=>{
        var width = sidebar.clientWidth ;
       
        if(!nav_toggle.classList.contains('active')){
            nav_toggle.classList.add('active')
            main_div.style.transform =`translateX(${width}px)` ;
        }
        else{
            nav_toggle.classList.remove('active')
            main_div.style.transform =`translateX(0px)` ;
        }
    })
})


