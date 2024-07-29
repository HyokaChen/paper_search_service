import aiohttp
from ninja import Router
from lxml.etree import HTML
from easydict import EasyDict
from datetime import datetime
from api.constants import API_CROSSREF, PUBMEB_BASE_URL, ARXIV_BASE_URL, MAPPINGS
from api.models import QuerySchema, ResultSchema
from django.core.handlers.asgi import ASGIRequest

router = Router()


@router.get("/")
def index(request: ASGIRequest):
    return {
        'hello': 'world'
    }


@router.post("/doi", response=ResultSchema)
async def doi(request: ASGIRequest, body: QuerySchema):
    url = f"{API_CROSSREF}{body.query}"
    conn = aiohttp.TCPConnector(force_close=True, limit=10, limit_per_host=2)
    timeout = aiohttp.ClientTimeout(total=300)
    async with aiohttp.ClientSession(timeout=timeout, connector=conn, headers={
        "Content-Type": "application/json; charset=utf-8",
    }) as session:
        async with session.get(url, ssl=False, allow_redirects=False) as resp:
            data = await resp.json()
            info = EasyDict(data)
            author_info = info.message.author
            organization_list = [x.name for x in author_info if x.get('name')]
            author_list = [x for x in author_info if x.get('given')]
            result = ResultSchema(
                doi=body.query,
                origin_url=info.message.URL,
                title=info.message.title[0],
                author=[f"{x.given} {x.family}" for x in author_list],
                organization=organization_list,
                magazine=info.message['container-title'],
                publisher=info.message.publisher,
                publication_year=int(info.message.indexed['date-parts'][0][0]),
                category=info.message.subject
            )
            return result


@router.post("/pubmed", response=ResultSchema)
async def pubmed(request: ASGIRequest, body: QuerySchema):
    url = f"{PUBMEB_BASE_URL}{body.query}/"
    conn = aiohttp.TCPConnector(force_close=True, limit=10, limit_per_host=2)
    timeout = aiohttp.ClientTimeout(total=300)
    async with aiohttp.ClientSession(timeout=timeout, connector=conn, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }) as session:
        async with session.get(url, ssl=False, allow_redirects=False) as resp:
            data = await resp.read()
            html = HTML(data.decode())
            doi = html.xpath('//span[@class="identifier doi"]/a/text()')
            if doi:
                self_resp = await session.post('http://localhost:8000/api/doi', json={
                    'query': doi[0].strip()
                })
                data = await self_resp.json()
                result = ResultSchema(**data.get('result'))
            else:
                result = ResultSchema(
                    pmid=body.query,
                    origin_url=url,
                    title=html.xpath('//h1[@class="heading-title"]/text()')[0].strip(),
                    author=html.xpath('//div[@class="authors-list"]/span/a/text()'),
                    magazine=html.xpath('//button[@id="full-view-journal-trigger"]/@title'),
                )
            return result


@router.post("/arxiv", response=ResultSchema)
async def arxiv(request: ASGIRequest, body: QuerySchema):
    url = f"{ARXIV_BASE_URL}{body.query}"
    conn = aiohttp.TCPConnector(force_close=True, limit=10, limit_per_host=2)
    timeout = aiohttp.ClientTimeout(total=300)
    async with aiohttp.ClientSession(timeout=timeout, connector=conn, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }) as session:
        async with session.get(url, ssl=False, allow_redirects=False) as resp:
            data = await resp.read()
            html = HTML(data)
            doi = html.xpath('//feed/entry/doi/text()')
            if doi:
                self_resp = await session.post('http://localhost:8000/api/doi', json={
                    'query': doi[0].strip()
                })
                data = await self_resp.json()
                result = ResultSchema(**data.get('result'))
            else:
                result = ResultSchema(
                    arxiv=body.query,
                    origin_url=html.xpath("//feed/entry/id/text()")[0],
                    title=html.xpath("//feed/entry/title/text()")[0],
                    author=html.xpath("//feed/entry/author/name/text()"),
                    magazine=['arXiv', ],
                    publisher='arXiv',
                    publication_year=datetime.strptime(html.xpath("//feed/entry/published/text()")[0],
                                                       "%Y-%m-%dT%H:%M:%SZ").year,
                    category=list(map(lambda x: MAPPINGS.get(x, x).strip(), html.xpath("//feed/entry/category/@term"))),
                    summary="".join(html.xpath("//feed/entry/summary/text()")).strip()
                )
            return result
