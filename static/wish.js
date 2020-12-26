window.onload = () =>{
    const aud = document.querySelector('audio')
    document.onclick = () => aud.play()
}


document.addEventListener('DOMContentLoaded', e=>{
    const wish = document.querySelector('#wish')
    const p = document.querySelector('#wisher')
    const wisher = wish.innerText
    console.log(wisher)
    wish.remove()

    let counter = 0;
    let writer = setInterval(()=>{
        p.innerText = wisher.substr(0,counter++)
        if ( p.innerText === wisher) clearInterval(writer)
    }, 500)
})