function animateCSS(element, animationName, callback) {
  const node = document.querySelector(element)
  node.classList.add('animated', animationName)

  function handleAnimationEnd() {
      node.classList.remove('animated', animationName)
      node.removeEventListener('animationend', handleAnimationEnd)

      if (typeof callback === 'function') callback()
  }

  node.addEventListener('animationend', handleAnimationEnd)
}

function setNodesDisabledState(disabled) {
  var els = document.getElementsByClassName('node');
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
  if (nodeLiEl.classList.contains('disabled')) {
    event.preventDefault()
    return
  }
  var nodeId = el.getAttribute('node-id');
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
  })
  xhttp.send()
  return false
}

function hidePopupNodeForm() {
  document.getElementById('popup-node-form').style.display = 'none'
}

function updateNode() {
  var url = document.getElementById('form-node').action
  var node = {}
  node.id = document.getElementById('id').value
  node.title = document.getElementById('title').value
  node.codeOn = document.getElementById('codeOn').value
  node.codeOff = document.getElementById('codeOff').value
  node.iterations = document.getElementById('iterations').value
  var xhttp = new XMLHttpRequest()
  xhttp.open('POST', url)
  xhttp.setRequestHeader('Content-Type', 'application/json')
  xhttp.send(JSON.stringify(node))
  xhttp.addEventListener('load', function(event) {
    document.getElementById('popup-node-form').style.display = 'none'
    refreshNodes()
  })
}

var blurred = false

window.addEventListener('focus', function() {
  if (blurred) refreshNodes()
  blurred = false
})

window.addEventListener('blur', function() {
  blurred = true
})

animateCSS('#sloth', 'bounceInDown');
refreshNodes()
