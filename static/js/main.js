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

function onNodeClick(el, event) {
  jobQueue.addJob(() => {
    return  new Promise((resolve, reject) => {
      checkSwitch(el, event).then(resolve)
    })
  })
  displayJobs()
}

function checkSwitch(el, event) {
  return new Promise((resolve, reject) => {
    var nodeLiEl = el.parentElement.parentElement
    if (nodeLiEl.classList.contains('slided')) {
      event.preventDefault()
      event.stopPropagation()
      resolve()
      return
    }
    unslideAll()
    var nodeId = el.getAttribute('node-id')
    if (el.checked) {
      switchState(nodeId, 'on').then(resolve)
    } else {
      switchState(nodeId, 'off').then(resolve)
    }
  })
}

function switchState(nodeId, state) {
  return new Promise((resolve, reject) => {
    animateCSS('#sloth', 'swing')
    setNodesDisabledState(true)
    var url = '/' + state + '?id=' + nodeId
    var xhttp = new XMLHttpRequest()
    xhttp.open('GET', url, true)
    xhttp.onreadystatechange = function() {
      if (this.readyState !== 4 && this.status !== 200) {
        console.error('Request failed:')
        console.error(this)
      }
      resolve()
    }
    xhttp.send()
  })
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
  if (clickEvent) {
    clickEvent.preventDefault()
    clickEvent.stopPropagation()
  }
  document.getElementById('btn-add-node').style.display = 'none'
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
    if (type==='node') {
      const title = document.getElementById('title')
      if (title) title.focus()
    }
  })
  xhttp.send()
  return false
}

function toggleOptions() {
  var o = document.getElementById('optional');
  var r = document.getElementById('required');
  var b = document.getElementById('btn-options');
  if (r.style.display == 'block') {
    r.style.display = 'none'
    o.style.display = 'block'
    b.innerHTML = 'Show required values'
  }
  else {
    r.style.display = 'block'
    o.style.display = 'none'
    b.innerHTML = 'Show optional values'
  }
}

function hidePopupForm() {
  document.getElementById('popup-form').style.display = 'none'
  document.getElementById('btn-add-node').style.display = 'block'  
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
  if (clickEvent) {
    clickEvent.preventDefault()
    clickEvent.stopPropagation()
  }
  var url = '/node/delete/' + nodeId
  var xhttp = new XMLHttpRequest()
  xhttp.open('DELETE', url)
  xhttp.addEventListener('load', function() {
    refreshNodes()
  })
  xhttp.send()
  return false
}

function reorderNodes(posFrom, posTo) {
  var url = '/node/reorder/' + posFrom + '/' + posTo
  var xhttp = new XMLHttpRequest()
  xhttp.open('POST', url)
  xhttp.addEventListener('load', function() {
    refreshNodes()
  })
  xhttp.send()
}

function onToolClicked(element, event) {
  event.preventDefault()
  event.stopPropagation()
  unslideAll()
  var liElement = element.parentElement.parentElement
  slideLi(liElement)
  return false
}

function slideLi(liElement) {
  liElement.classList.remove('unslided')
  liElement.classList.add('slided')
}

function unslideLi(liElement) {
  liElement.classList.remove('slided')
  liElement.classList.add('unslided')
}

function unslideAll() {
  var slidedLis = document.getElementsByClassName('slided')
  for (var i = 0; i < slidedLis.length; i++) {
    unslideLi(slidedLis[i])
  }
}

function displayJobs() {
  let waitingJobs = jobQueue.getJobCount() - 1
  let container = document.getElementById('jobs-container')
  if (waitingJobs > 0) {
    let counter = document.getElementById('jobs-counter')
    var text = waitingJobs.toString() + ' request'
    if (waitingJobs > 1) text += 's'
    counter.innerHTML = text
    container.style.display = 'block'
  } else {
    container.style.display = 'none'
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
var jobQueue = new JobQueue(5)
jobQueue.onJobDone = displayJobs
jobQueue.onAllJobsDone = () => { setNodesDisabledState(false) }

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
