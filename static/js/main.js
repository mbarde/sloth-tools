function animateCSSElement(element, animationName, callback) {
  element.classList.add('animated', animationName)
  function handleAnimationEnd() {
      element.classList.remove('animated', animationName)
      element.removeEventListener('animationend', handleAnimationEnd)
      if (typeof callback === 'function') callback()
  }
  element.addEventListener('animationend', handleAnimationEnd)
}

function animateCSS(elementSelector, animationName, callback) {
  var element = document.querySelector(elementSelector)
  animateCSSElement(element, animationName, callback)
}

function setNodesDisabledState(disabled) {
  var els = document.getElementsByClassName('node')
  for (var i = 0; i < els.length; i++) {
    if (disabled) {
      els[i].classList.add('disabled')
    } else {
      els[i].classList.remove('disabled')
    }
  }
}

function checkSwitch(el, event) {
  var nodeLiEl = el.parentElement.parentElement
  if (nodeLiEl.classList.contains('disabled') ||
      nodeLiEl.classList.contains('slided')) {
    event.preventDefault()
    return
  }
  unslideAll()
  var nodeId = el.getAttribute('node-id')
  if (el.checked) {
    switchState(nodeId, 'on')
  } else {
    switchState(nodeId, 'off')
  }
}

function switchState(nodeId, state) {
  animateCSS('#sloth', 'swing')
  setNodesDisabledState(true)
  var url = '/' + state + '?id=' + nodeId
  var xhttp = new XMLHttpRequest()
  xhttp.open('GET', url, true)
  xhttp.onreadystatechange = function() {
    setNodesDisabledState(false)
    if (this.readyState !== 4 && this.status !== 200) {
      console.error('Request failed:')
      console.error(this)
    }
  }
  xhttp.send()
}

function switchStateForAll(state) {
  animateCSS('#sloth', 'swing')
  setNodesDisabledState(true)
  var url = '/' + state
  var xhttp = new XMLHttpRequest()
  xhttp.open('GET', url, true)
  xhttp.onreadystatechange = function() {
    setNodesDisabledState(false)
    refreshNodes()
    if (this.readyState !== 4 && this.status !== 200) {
      console.error('Request failed:')
      console.error(this)
    }
  }
  xhttp.send()
}

function refreshNodes() {
  animateCSS('#sloth', 'bounce')
  setNodesDisabledState(true)
  var container = document.querySelector('div.container-nodes')
  var url = '/nodes'
  var xhttp = new XMLHttpRequest()
  xhttp.open('GET', url, true)
  xhttp.addEventListener('load', function(event) {
    container.innerHTML = ''
    container.insertAdjacentHTML('beforeend', xhttp.responseText)
  })
  xhttp.send()
}

function showPopupForm(type='node', clickEvent=false, objId=false, urlSuffix='') {
  if (clickEvent) clickEvent.preventDefault()
  var container = document.querySelector('div.popup .container')
  var url = `/${type}/create`
  if (urlSuffix.length > 0) url += urlSuffix
  if (objId !== false) url = `/${type}/update/` + objId
  var xhttp = new XMLHttpRequest()
  xhttp.open('GET', url)
  xhttp.addEventListener('load', function() {
    container.innerHTML = ''
    container.insertAdjacentHTML('beforeend', xhttp.responseText)
    document.getElementById('popup-form').style.display = 'block'
    if (type==='node') document.getElementById('title').focus()
  })
  xhttp.send()
  return false
}

function hidePopupForm() {
  document.getElementById('popup-form').style.display = 'none'
}

function submitForm(callback) {
  var form = document.getElementById('form-popup')
  var data = form2JSON(form)
  var url = form.action
  var xhttp = new XMLHttpRequest()
  xhttp.open(form.method, url)
  xhttp.setRequestHeader('Content-Type', 'application/json')
  xhttp.addEventListener('load', function(event) {
    hidePopupForm()
    callback()
  })
  xhttp.send(JSON.stringify(data))
}

function deleteNode(clickEvent, nodeId, nodeTitle) {
  if (!confirm(`Do you really want to delete node "${nodeTitle}"?`)) return
  if (clickEvent) clickEvent.preventDefault()
  var url = '/node/delete/' + nodeId
  var xhttp = new XMLHttpRequest()
  xhttp.open('DELETE', url)
  xhttp.addEventListener('load', function() {
    refreshNodes()
  })
  xhttp.send()
  return false
}

function deleteEvent(clickEvent, eventId, eventTitle, nodeId) {
  if (!confirm(`Do you really want to delete event "${eventTitle}"?`)) return
  if (clickEvent) clickEvent.preventDefault()
  var url = '/event/delete/' + eventId
  var xhttp = new XMLHttpRequest()
  xhttp.open('DELETE', url)
  xhttp.addEventListener('load', function() {
    showEventList(nodeId)
  })
  xhttp.send()
  return false
}


function showEventList(nodeId) {
  if (event) event.preventDefault()
  var container = document.querySelector('div.popup .container')
  var url = '/event/bynode/' + nodeId
  var xhttp = new XMLHttpRequest()
  xhttp.open('GET', url)
  xhttp.addEventListener('load', function(event) {
    container.innerHTML = ''
    container.insertAdjacentHTML('beforeend', xhttp.responseText)
    document.getElementById('popup-form').style.display = 'block'
  })
  xhttp.send()
  return false
}

function onToolClicked(element, event) {
  event.preventDefault()
  event.stopPropagation()
  unslideAll()
  element.style.display = 'none'
  var liElement = element.parentElement
  slideLi(liElement)
  return false
}

function slideLi(liElement) {
  var hiddenTools = liElement.getElementsByClassName('hidden-tools')[0]
  hiddenTools.style.display = 'inline-block'
  animateCSSElement(hiddenTools, 'slideInRight')
  liElement.classList.remove('unslided')
  liElement.classList.add('slided')
}

function unslideLi(liElement) {
  liElement.classList.remove('slided')
  liElement.classList.add('unslided')
  var tool = liElement.getElementsByClassName('tool')[0]
  tool.style.display = 'inline-block'
  var hiddenTools = liElement.getElementsByClassName('hidden-tools')[0]
  hiddenTools.style.marginRight = '-45px'
  animateCSSElement(hiddenTools, 'slideOutRight', function() {
    hiddenTools.style.display = 'none'
    hiddenTools.style.marginRight = '0'
  })
}

function unslideAll() {
  var slidedLis = document.getElementsByClassName('slided')
  for (var i = 0; i < slidedLis.length; i++) {
    unslideLi(slidedLis[i])
  }
}

function form2JSON(form) {
  var obj = {}
  var elements = form.querySelectorAll('input, select, textarea')
  for (var i = 0; i < elements.length; ++i) {
    var element = elements[i]
    var name = element.name
    var value = element.value

    if(name) {
      if (element.type === 'checkbox') {
        if (element.checked) obj[name] = value
      } else {
        obj[name] = value
      }
    }
  }
  return obj
}

var blurred = false

animateCSS('#sloth', 'bounceInDown')
refreshNodes()

window.addEventListener('click', unslideAll)

window.addEventListener('blur', function() {
  blurred = true
})

window.addEventListener('focus', function() {
  if (blurred) refreshNodes()
  blurred = false
})
