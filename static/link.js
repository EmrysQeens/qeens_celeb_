window.onload = () =>{
     alert('Welcome \n Wish your families and friends with a nice page and a picture of your choice and a heart warming message... When generated a url shows below the create button you can view by clicking thw wish link.')
     const aud = document.querySelector('audio')
     document.onclick = () => aud.play()
}

document.addEventListener('DOMContentLoaded', e=>{
  const name = document.querySelector('#name')
  const image = document.querySelector('#image')
  const message = document.querySelector('#message')
  const btn = document.querySelector('#btn')
  let interval = undefined

  name.onfocus = e => e.target.value = ( e.target.value == "Full Name" ) ? "" : e.target.value  // placeholder
  name.oninput = () => btn.disabled = false

  const to_base64 = file => new Promise((resolve, reject)=>{
       const reader = new FileReader()
       if (file == undefined) return
       reader.readAsDataURL(file)
       reader.onload = () => resolve([reader.result, true])
       reader.onerror = (err) => reject([err, false])
   })

   const load = (e, bool) => {
        if (bool){
            const pt = ['•', '••', '•••']
            let counter = 0
            e.target.disabled = true
            interval = setInterval(()=>{
                e.target.innerText = pt[counter]
                counter = counter === 2 ? 0 : ++counter
            },1000)
            return
        }
        clearInterval(interval)
        e.target.innerText = 'Create'
        e.target.disabled = false
   }


  const generate = async (f) => {
    const nm = name.value
    if ( nm === ''){
        alert('Input valid name please..')
        return
    }
    if (image.files.length === 0){
        alert('Select your image....')
        return
    }
    if (message.innerText === '' ){
        alert('Write a message...')
        return
    }
    const b64_string = await to_base64 (image.files[0])
    if (!b64_string[1]) {
        alert('Reselect Image')
        return
    }
    load(f, true)
    const request = new XMLHttpRequest()
    request.timeout = 120000
    request.open('POST', '/', true)
    const infs = new FormData()
    const data = {'name' : nm, 'image': image.files.length === 0 ? 'NAN' : b64_string[0], 'msg': message.innerText}
    infs.append('data', JSON.stringify(data))
    request.send(infs)

    request.onload = e =>{
        if (request.status === 200){
            const ret_val = JSON.parse(request.responseText)
            if(ret_val['ret_val']){
                const pop = document.querySelector('#pop')
                const p = pop.querySelector('#url')
                const view = pop.querySelector('#view')
                p.innerText = 'URL   : ' + document.location['href'] + '-' + ret_val['lnk']
                view.href = document.location['href'] + ret_val['lnk']
                pop.style.display = 'block'
                alert('Click the View link to view your greetings')
            }
        }
        load(f, false)
    }

    const err = (e, msg) =>{
        alert(msg)
        load(e, false)
    }

    request.onerror = e => err(e, 'No connection!!!')
    request.ontimeout = e => err(e, 'Timeout to connect to server!!!')
  }

  btn.onclick = e => generate(e)

})
