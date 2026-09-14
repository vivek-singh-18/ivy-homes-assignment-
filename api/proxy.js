export default async function handler(req, res) {
  // 1. CORS Validation
  const allowedOrigins = [
    'https://vivek-singh-18.github.io',
    'http://localhost:5173'
  ];
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  } else {
    // Default to the gh-pages domain if no matching origin is found
    res.setHeader('Access-Control-Allow-Origin', 'https://vivek-singh-18.github.io');
  }
  
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization, X-Target-Path');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // 2. Validate X-Target-Path to prevent open proxy abuse
  const targetPath = req.headers['x-target-path'] || '';
  if (!targetPath.startsWith('/auth/') && !targetPath.startsWith('/v1/')) {
    res.status(403).json({ error: "Forbidden: Invalid or missing target path" });
    return;
  }

  const fullTargetUrl = `https://solve.ivy.homes${targetPath}`;

  // 3. Construct headers securely
  const headers = new Headers();
  if (req.headers['authorization']) {
    headers.set('Authorization', req.headers['authorization']);
  }
  if (req.headers['content-type']) {
    headers.set('Content-Type', req.headers['content-type']);
  }
  
  // Inject the server-side API Key
  const apiKey = process.env.IVY_API_KEY;
  if (apiKey) {
    headers.set('X-API-Key', apiKey);
  } else {
    // Don't leak the key or missing key details to the client
    res.status(500).json({ error: "Server configuration error" });
    return;
  }

  try {
    const fetchOptions = {
      method: req.method,
      headers: headers,
    };

    if (req.method !== 'GET' && req.method !== 'HEAD' && req.body) {
      // Vercel parses JSON body automatically
      fetchOptions.body = typeof req.body === 'object' ? JSON.stringify(req.body) : req.body;
    }

    const response = await fetch(fullTargetUrl, fetchOptions);
    const data = await response.text();

    let parsedData = data;
    try {
      parsedData = JSON.parse(data);
    } catch(e) {
      // Return as text if not JSON
    }

    res.status(response.status).send(parsedData);
  } catch (error) {
    // DO NOT expose internal errors or stack traces that might leak secrets
    console.error("Proxy error:", error.message);
    res.status(500).json({ error: "Proxy upstream error" });
  }
}
