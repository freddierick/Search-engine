const fetch = require('node-fetch');
const { parse } = require('node-html-parser');

function getUrlFromHref(href){
    return href.split('https://')[1]?.split("\"")[0] || href.split('http://')[1]?.split("\"")[0]; //get URL for A tag
};

function getUrlsAndContent(pageTree){
    return new Promise((res,rej) => {
        let links = new Map();
        let content = [];
        findLinksOnAPage(pageTree);
        function findLinksOnAPage(s){
            s.forEach(e => {
                if ( e.rawTagName === 'a') {
                    p = getUrlFromHref(e.rawAttrs);
                    if (p) links.set(p);
                };
                if ( e.rawTagName === 'p' || e.rawTagName === 'h1' || e.rawTagName === 'h1') { 
                    if (e.childNodes[0]) content.push(e.childNodes[0]?.rawText);
                };
                findLinksOnAPage(e.childNodes);
            });
        };
        res({ links: [...links.keys()], content: content.join(' ') });
    });
};

async function crawl(URL){
    const f = await fetch(URL);
    const a = await f.text();
    parased = parse(a);
    q = await getUrlsAndContent(parased.childNodes);
    console.log(URL)
    q.links.map(async  (e) => {
        if (!e.startsWith('https://') && !e.startsWith('http://')) e = 'http://' + e;
        // console.log(`Crawling: ${e}`);
        if (e == URL) return;
        await crawl(e);
    });
};

crawl('https://en.wikipedia.org/wiki/Big_Bang');