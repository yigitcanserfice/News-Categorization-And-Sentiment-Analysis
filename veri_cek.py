import requests
from bs4 import BeautifulSoup

# List of URLs to scrape
urls = ['https://www.haberler.com/spor/taraftar-cildirdi-fenerbahce-nin-futbolcusuna-16612547-haberi/',
        'https://www.haberler.com/haberler/fatma-sahin-odul-alirken-gaziantep-i-sular-16612639-haberi/',
        'https://www.haberler.com/haberler/akaryakita-pes-pese-indirimler-benzin-33-16611217-haberi/',
        'https://www.haberler.com/haberler/cok-guzel-hareketler-deki-ekrem-imamoglu-taklidi-16611843-haberi/',
        'https://www.haberler.com/politika/mhp-kocaeli-milletvekili-saffet-sancakli-16612690-haberi/',
        'https://www.haberler.com/haberler/ece-ronay-in-suc-dosyasi-kabarik-cikti-adam-16610862-haberi/',
        'https://www.haberler.com/ekonomi/dunyanin-en-zengin-aileleri-siralandi-zirvede-16611849-haberi/',
        'https://www.haberler.com/spor/derbiye-gitmeyen-ali-koc-hasan-arat-i-aradi-16612414-haberi/',
        'https://www.haberler.com/spor/fenerbahce-den-derbi-sonrasi-olay-paylasim-16612756-haberi/',
        'https://www.haberler.com/spor/besiktas-ta-deprem-aboubakar-ve-colley-ilk-11-de-16612102-haberi/',
        'https://www.haberler.com/guncel/sokak-kopeklerinin-saldirisina-ugrayan-cocugun-babasi-cocugumun-vucudunun-cogu-yerinde-et-kalmamis-y-16610580-haberi/',
        'https://www.haberler.com/3-sayfa/mersin-de-tartistigi-erkek-arkadasi-tarafindan-silahli-vurulan-genc-kiz-hayatini-kaybetti-16611259-haberi/',
        'https://www.haberler.com/guncel/sivas-ta-otomobil-kazasi-yardim-etmek-icin-duran-2-kisi-hayatini-kaybetti-16611315-haberi/',
        'https://www.haberler.com/guncel/israil-askerleri-hamas-in-tunelleri-karsisinda-saskina-dondu-16610963-haberi/',
        'https://www.haberler.com/haberler/husiler-in-gemileri-hedef-aliriz-tehdidinin-16612897-haberi/',
        'https://www.haberler.com/haberler/cok-guzel-hareketler-deki-ekrem-imamoglu-taklidi-16611843-haberi/',
        'https://www.haberler.com/haberler/husiler-in-gemileri-hedef-aliriz-tehdidinin-16612897-haberi/',
        'https://www.haberler.com/haberler/hak-ettiler-diyen-ismail-kartal-dan-16612882-haberi/',
        'https://www.haberler.com/spor/riza-calimbay-derbi-sonrasi-adeta-ates-puskurdu-16612923-haberi/',
        'https://www.haberler.com/haberler/ankara-daki-vahsete-sessiz-kalamadi-16612008-haberi/',
        'https://www.haberler.com/magazin/konserlerime-engel-oluyorlar-diyen-aleyna-tilki-16606865-haberi/',
        'https://www.haberler.com/magazin/oyuncu-filiz-tacbas-chp-den-izmir-foca-belediye-16605452-haberi/',
        'https://www.haberler.com/dunya/gta-6-grand-theft-auto-6-fragmani-yayinlandi-16596210-haberi/',
        'https://www.haberler.com/ekonomi/apple-turkiye-fiyatlarina-zam-yapti-en-pahali-16584678-haberi/',
        'https://www.haberler.com/teknoloji/fransa-devlet-calisanlarinin-whatsapp-i-16581447-haberi/',
        'https://www.haberler.com/haberler/marmara-daki-deprem-oncesi-telefonlara-gelen-16593257-haberi/',
        ]


with open("output.txt", "w", encoding="utf-8") as file:
    for url in urls:
        # Make a request to the URL
        response = requests.get(url)
        content = response.content

        # Parse the HTML content
        soup = BeautifulSoup(content, "html.parser")

        # Find titles
        titles = soup.find("main", {"class": "mtm-20 hbptContent haber_metni"})

        # Write titles to the file


        titles_text = titles.text.strip()
        print(titles_text)
        file.write(f'{titles_text},\n')
