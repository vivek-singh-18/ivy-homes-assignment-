export default async function handler(req, res) {
  // Add CORS headers so GitHub Pages can call this Vercel function
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // The actual endpoint on solve.ivy.homes to call. We'll pass it via a query param `path`
  // e.g., /api/proxy?path=/v1/listings
  const targetPath = req.query.path || '';
  
  // Reconstruct the full query string without the `path` param
  const queryParams = new URLSearchParams(req.query);
  queryParams.delete('path');
  const qs = queryParams.toString();
  const fullTargetUrl = `https://solve.ivy.homes${targetPath}${qs ? '?' + qs : ''}`;

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
    console.error("IVY_API_KEY environment variable is not set!");
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
    res.status(500).json({ error: error.message });
  }
}
