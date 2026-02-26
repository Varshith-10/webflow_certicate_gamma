(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const utmParams = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];

  // Build UTM query string
  const utmString = utmParams
    .map(param => urlParams.has(param) ? `${param}=${encodeURIComponent(urlParams.get(param))}` : '')
    .filter(Boolean)
    .join('&');

  if (!utmString) return;

  // Append UTMs to every link
  document.querySelectorAll('a[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;

    const separator = href.includes('?') ? '&' : '?';
    link.setAttribute('href', `${href}${separator}${utmString}`);
  });
})();
