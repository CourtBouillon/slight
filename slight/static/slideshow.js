Reveal.initialize({
  controls: true,
  progress: true,
  history: true,
  center: true,
  slideNumber: true,
  plugins: [ RevealHighlight, RevealNotes ],
});

document.querySelector('#edit a').addEventListener('click', event => {
  event.preventDefault();
  var editable = !document.querySelector('#edition').classList.toggle('hidden');
  document.querySelector('#tags').classList.toggle('hidden');
  document.querySelectorAll('section').forEach(section => {
    section.setAttribute('contenteditable', editable);
  });
});

document.querySelectorAll('[data-format] a').forEach(anchor => {
  anchor.addEventListener('click', event => {
    event.preventDefault();
    document.execCommand('formatBlock', false, anchor.parentNode.id);
  });
});
document.querySelectorAll('[data-command] a').forEach(anchor => {
  anchor.addEventListener('click', event => {
    event.preventDefault();
    document.execCommand(anchor.parentNode.id, false, null);
  });
});

document.querySelector('#add a').addEventListener('click', event => {
  var section = document.createElement('section');
  section.setAttribute('contenteditable', 'true');
  section.innerHTML = '<h2>Title</h2><p>Content</p>';
  event.target = document.querySelector('div.slides').insertBefore(
    section, document.querySelector('section.present').nextSibling);
  Reveal.next();
  event.preventDefault();
  return false;
});

document.querySelector('#remove a').addEventListener('click', event => {
  if (Reveal.isLastSlide() && Reveal.isFirstSlide()) { return false }
  index = Reveal.getIndices().h - Reveal.isLastSlide();
  event.target = document.querySelector('section.present').remove();
  Reveal.slide(index, 0, 0);
  event.preventDefault();
  return false;
});

document.querySelector('#save a').addEventListener('click', event => {
  var sections = Array.from(document.querySelectorAll('section')).map(
    section => '<section>' + section.innerHTML + '</section>\n').join('');
  event.target.parentNode.classList.remove('saved');
  event.target.parentNode.classList.remove('error');
  event.target.parentNode.classList.add('saving');
  var request = new XMLHttpRequest();
  request.addEventListener('readystatechange', () => {
    if (request.readyState === 4) {
      event.target.parentNode.classList.replace('saving', request.status === 200 ? 'saved' : 'error');
    }
  });
  request.open('POST', 'save', true);
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  request.send('sections=' + encodeURIComponent(sections));
  event.preventDefault();
  return false;
});
