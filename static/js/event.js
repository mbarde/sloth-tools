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

function showEventList(nodeId, clickEvent=false) {
  if (clickEvent) {
    clickEvent.preventDefault()
    clickEvent.stopPropagation()
  }
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

function changeEventTimeMode(el) {
  var fieldsets = document.getElementsByTagName('fieldset');
  for (var i = 0; i < fieldsets.length; i++) {
    var fieldset = fieldsets[i];
    if (fieldset.id.indexOf(el.value) > -1) {
      fieldset.style.display = 'block';
    } else {
      fieldset.style.display = 'none';
    }
  }
}
