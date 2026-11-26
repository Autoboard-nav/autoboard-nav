/* Worker de Cloudflare: reenvía los feeds oficiales de incidencias de tráfico (DATEX II) añadiendo CORS,
   para que la app pueda leerlos desde el navegador. Solo acepta las fuentes de la lista. Caché de 60 s.
   Uso: https://trafico.<tu-subdominio>.workers.dev/?src=gv  (Gobierno Vasco)  |  ?src=dgt  (DGT) */
const FUENTES = {
  gv:  'https://nap.dgt.es/datex2/dt-gv/SituationPublication/all/content.xml',
  dgt: 'https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v37.xml'
};
export default {
  async fetch(req) {
    const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET', 'Cache-Control': 'public, max-age=60' };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    const src = new URL(req.url).searchParams.get('src') || 'gv';
    if (!FUENTES[src]) return new Response('fuente desconocida', { status: 400, headers: cors });
    try {
      const r = await fetch(FUENTES[src], { cf: { cacheTtl: 60, cacheEverything: true }, headers: { 'User-Agent': 'autoboard-nav' } });
      return new Response(r.body, { status: r.status, headers: { ...cors, 'Content-Type': r.headers.get('content-type') || 'application/xml' } });
    } catch (e) {
      return new Response('error: ' + e.message, { status: 502, headers: cors });
    }
  }
};
