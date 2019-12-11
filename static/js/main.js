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

function showPopupNodeForm(event=false, nodeId=false) {
  if (event) event.preventDefault()
  var container = document.querySelector('div.popup .container')
  var url = '/node/create'
  if (nodeId !== false) url = '/node/update/' + nodeId
  var xhttp = new XMLHttpRequest()
  xhttp.open('GET', url)
  xhttp.addEventListener('load', function(event) {
    container.innerHTML = ''
    container.insertAdjacentHTML('beforeend', xhttp.responseText)
    document.getElementById('popup-node-form').style.display = 'block'
    document.getElementById('title').focus()
  })
  xhttp.send()
  return false
}

function hidePopupNodeForm() {
  document.getElementById('popup-node-form').style.display = 'none'
}

function updateNode() {
  var form = document.getElementById('form-node')
  var url = form.action
  var node = {}
  node.id = document.getElementById('id').value
  node.title = document.getElementById('title').value
  node.codeOn = document.getElementById('codeOn').value
  node.codeOff = document.getElementById('codeOff').value
  node.iterations = document.getElementById('iterations').value
  var xhttp = new XMLHttpRequest()
  xhttp.open(form.method, url)
  xhttp.setRequestHeader('Content-Type', 'application/json')
  xhttp.addEventListener('load', function(event) {
    hidePopupNodeForm()
    refreshNodes()
  })
  xhttp.send(JSON.stringify(node))
}

function deleteNode(event, nodeId) {
  console.log('pe')
  if (event) event.preventDefault()
  var url = '/node/delete/' + nodeId
  var xhttp = new XMLHttpRequest()
  xhttp.open('DELETE', url)
  xhttp.addEventListener('load', function(event) {
    refreshNodes()
  })
  xhttp.send()
  return false
}

function onToolClicked(element, event) {
  event.preventDefault()
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
  liElement.classList.add('slided')
}

function unslideLi(liElement) {
  liElement.classList.remove('slided')
  var tool = liElement.getElementsByClassName('tool')[0]
  tool.style.display = 'block'
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

var blurred = false

animateCSS('#sloth', 'bounceInDown')
refreshNodes()


window.addEventListener('blur', function() {
  blurred = true
})

window.addEventListener('focus', function() {
  if (blurred) refreshNodes()
  blurred = false
})
