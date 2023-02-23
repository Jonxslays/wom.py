const paths = window.location.pathname.split("/").filter((p) => !!p);
const defaultVersion = "stable";

try {
  const req = new XMLHttpRequest();
  req.open("GET", "/versions.json");
  req.onload = handle404Redirect;
  req.send();
} catch {
  // Go to the default version if there was any error
  navTo404(defaultVersion);
}

function navTo404(path) {
  // Navigate to the 404 page for the given path
  window.location.replace(`/${path}/404.html`);
}

function handle404Redirect(e) {
  if (e.target.status !== 200) {
    // Go to default version if we couldn't fetch the versions
    return navTo404(defaultVersion);
  }

  // Current available site versions
  const versions = JSON.parse(e.target.response);
  const version = versions.filter(
    (v) => v.title.toLowerCase() === paths[0].toLowerCase()
  );

  if (version.length) {
    navTo404(version[0].title);
  } else {
    // Go to the default version if no versions matched
    navTo404(defaultVersion);
  }
}
