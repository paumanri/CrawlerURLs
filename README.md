# CrawlerURLs
1. Instal·lem python. Quan el tinguem, creem un entorn virtual on estarà ubicat tot el projecte. Després, entrem dins de l'entorn virtual. L'entorn virtual no el pujo al repositori, podeu crear-lo amb la comanda de les captures <br/>
   ![image](https://github.com/user-attachments/assets/3fd2328d-c6ac-4478-b1d5-9a67bd58950b)

2. Instal·lem Selenium i Requests. <br/>
   ![image](https://github.com/user-attachments/assets/66c3ef92-1798-4a27-a63e-003c8c2d7feb)

3. Descarreguem el Chrome Driver i descomprimim el fitxer. Ara que ja tenim l'executable chrome.exe, ja podem començar el desenvolupament del projecte.
   
4. Creem el fitxer python crawler.py, separat en les tres fases per a poder anar comprovant el seu funcionament en porcions més petites. Quan les tres parts funcionen, ja tenim la lògica del crawler implementada.

5. Per a la vista HTML, instal·lem la llibreria de Python "Flask". <br/>
   ![image](https://github.com/user-attachments/assets/64da97a5-be30-47f5-9eae-6ae9aa490119)

6. Creem el fitxer app.py, que serà l'aplicació Flask amb la interfície web.

7. I seguidament creem la plantilla HTML per a la vista amb el formulari (templates/index.html).

8. En pic tenim tot muntat, i dins de l'entorn virtual, fem córrer l'aplicació flask en localhost. Entrem al navegador (en el meu cas, chrome) i provem si funciona omplint el formulari amb una URL. Se'ns obrirà directament el chromedriver i anirà carregant totes les URLs que trobi en la pàgina web determinada. <br/>
   ![image](https://github.com/user-attachments/assets/3b2a27a6-ce7c-4eab-a617-a9375a45a199)
   ![image](https://github.com/user-attachments/assets/33701ae9-ed24-4819-95db-fdb873d60111)
   
10. Quan hagi acabat de revisar totes les URLs, i en cas que trobi un enllaç que porti a un error 4XX, crearà un fitxer local de tipus CSV, on s'aguardaran les URLs que donen els errors 4XX (anomenat errors.csv, es crearà en la carpeta on tingueu el projecte).
