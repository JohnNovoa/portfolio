(function () {
  // Lightbox for project images
  var dlg = document.querySelector('.lightbox');
  if (dlg && typeof dlg.showModal === 'function') {
    var big = dlg.querySelector('img');
    var cap = dlg.querySelector('.lb-cap');
    document.querySelectorAll('.zoom').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var im = btn.querySelector('img');
        big.src = im.currentSrc || im.src;
        big.alt = im.alt;
        cap.textContent = im.alt;
        dlg.showModal();
      });
    });
    dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  }

  // Copy email button (status is announced to screen readers)
  var status = document.createElement('span');
  status.className = 'sr';
  status.setAttribute('role', 'status');
  document.body.appendChild(status);
  document.querySelectorAll('.copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () {
        var label = btn.textContent;
        btn.textContent = 'Email copied';
        btn.classList.add('done');
        status.textContent = 'Email address copied';
        setTimeout(function () { btn.textContent = label; btn.classList.remove('done'); status.textContent = ''; }, 2200);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { window.location.href = 'mailto:' + text; });
      } else {
        window.location.href = 'mailto:' + text;
      }
    });
  });
})();
