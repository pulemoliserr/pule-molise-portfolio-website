/* Contact form: send to Formspree in the background and show the result on the page. */
(function () {
  const form = document.getElementById('contact-form');
  if (!form || !window.fetch) return; // without fetch, the form posts normally to Formspree

  const status = form.querySelector('.form-status');
  const button = form.querySelector('button[type="submit"]');

  function show(message, ok) {
    status.textContent = message;
    status.className = 'form-status ' + (ok ? 'ok' : 'error');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const data = new FormData(form);
    // Formspree uses the "subject" field as the email subject: prefix it so
    // portfolio messages are easy to spot in the inbox
    data.set('subject', 'Portfolio: ' + (data.get('subject') || 'New message'));

    button.disabled = true;
    button.textContent = 'Sending...';
    status.textContent = '';

    fetch(form.action, {
      method: 'POST',
      body: data,
      headers: { Accept: 'application/json' },
    })
      .then(function (response) {
        if (response.ok) {
          form.reset();
          show('Thank you! Your message has been sent. I will get back to you soon.', true);
          return;
        }
        return response.json().then(function (body) {
          const detail = body && body.errors ? body.errors.map(function (e) { return e.message; }).join(', ') : '';
          show('Sorry, the message could not be sent' + (detail ? ' (' + detail + ').' : '.') + ' Please try again.', false);
        });
      })
      .catch(function () {
        show('Sorry, the message could not be sent. Please check your connection and try again.', false);
      })
      .finally(function () {
        button.disabled = false;
        button.textContent = 'Send Message';
      });
  });
})();
