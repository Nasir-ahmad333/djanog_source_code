// toggle the navbar and animation 
let myButton = document.querySelector('.myButton')
let nav = document.querySelector('nav')
let navWrapper = document.querySelector('.nav-wrapper')
let ul = document.querySelector('nav ul')
let wrapperSpan = document.querySelectorAll('nav ul li span')
let searchBox = document.querySelector('#search-box')

Array.from(wrapperSpan).forEach(span => {
    span.addEventListener('click', e => {
        span.parentElement.classList.toggle('active')
        navWrapper.style.height = nav.clientHeight + 'px'
    })
})

myButton.addEventListener('click', e=> {
    navWrapper.classList.toggle('active')
    nav.classList.toggle('active')
    navWrapper.style.height = nav.clientHeight + 'px'
})

// for the animation of the navbar

window.addEventListener('scroll', e => {
    navWrapper.classList.toggle('sticky', window.scrollY > 0)
    if (window.scrollY > 0){
        navWrapper.classList.remove('sticky')
        navWrapper.style.height = "60px"
        nav.classList.remove('active')
        Array.from(wrapperSpan).forEach(span => {
            span.parentElement.classList.remove('active')
        })
    }
})

searchBox.addEventListener('click', e=> {
    searchBox.classList.toggle('active')
})