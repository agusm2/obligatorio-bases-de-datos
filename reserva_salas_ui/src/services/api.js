const API_BASE_URL = import.meta.env.VIE_API_BASE_URL;

async function request(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;

  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  const config = {
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
    method: options.method || "GET",
    body: options.body ? JSON.stringify(options.body) : undefined,
  };

  const res = await fetch(url, config);

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(errorText || `Error ${res.status}`);
  }

  if (res.status === 204) return null;

  return res.json();
}

export { request }