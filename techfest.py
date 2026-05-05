import flet as ft
import requests
import sqlite3
current_article = 0
articles = []
conn = sqlite3.connect("Newspaper.db", check_same_thread=False)
cursor = conn.cursor()
guardalnoticia = """
                    CREATE TABLE IF NOT EXISTS Noticias_guardadas(
                        idnoticia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                        Titulo VARCHAR(50) NOT NULL ,
                        usarioid INTEGER,
                        FOREIGN KEY(usarioid) REFERENCES Usarsario(idusuario),
                        UNIQUE(Titulo, usarioid));
                    """
users= """ CREATE TABLE IF NOT EXISTS Usarsario( idusuario INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                                 usarmame VARCHAR(40) NOT NULL UNIQUE,
                                                 password VARCHAR(40) NOT NULL);"""
article_select = "SELECT * FROM Noticias_guardadas"
cursor.execute(users)
cursor.execute(guardalnoticia)
results = cursor.fetchall()
#--------
def main(page: ft.Page):
    page.title = "Powerpuff News"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = ft.ScrollMode.ALWAYS
 
 
    #light yagami
    def changetheme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if darklight.value else ft.ThemeMode.DARK
        )
        page.update()
    darklight = ft.Switch(label="🌙/🌞", value=False, on_change=changetheme)
    #login
    userbox= ft.TextField(label="user")
    passwordbox = ft.TextField(label="Password",password=True)
    def signupf(e):
     if userbox.value and passwordbox.value:
       try:
           regitro= "INSERT INTO Usarsario(usarmame, password) VALUES (?,?)"
           pernambucano=(userbox.value, passwordbox.value)
           cursor.execute(regitro, pernambucano)
           conn.commit()
           getid="SELECT idusuario FROM Usarsario WHERE usarmame=? AND password=?"
           cursor.execute(getid, pernambucano)
           result=cursor.fetchone()
           if result:
              currentuser["id"]=result[0]
           show_app()
       except sqlite3.IntegrityError:
           openpassytaken()
           page.update()
     else:
        return
    currentuser= {"id":None}
    def loginf(e):
     if userbox.value and passwordbox.value:
        inisiasesion="SELECT idusuario FROM Usarsario WHERE usarmame=? AND password=?"
        perfamtutano=(userbox.value, passwordbox.value)  
        cursor.execute(inisiasesion, perfamtutano)
        result= cursor.fetchone()
        if result:
            currentuser["id"]= result[0]
            show_app()
        else:
            openpassy()
            page.update()
     else:
        return
    login = ft.ElevatedButton("Login", on_click=loginf)
    signup = ft.ElevatedButton("Sign up", on_click=signupf)
 
 
    def show_log(e):
        appcontainer.visible = False
        homecontainer.visible = False
        logincontainer.visible=True
 
        page.update()
    def show_app():
        logincontainer.visible = False
        appcontainer.visible = True
        button_back.visible = False
        allsaved_articles.visible = False #ALRIGHT, MAYBE ITS BECAUSE OPENING THE SAVEDS DOESNT WORK FOR LIL DOU BUT WHEN YOU CLICK SAVED ARTICLES THEN GO BACK, IT DELETES MANY THINGS, I ASSUME ITS BECAUSE OPENING SAVED ARTICLES HIDES SOME KEYS, WHICH IN TURN MAKES THE GOING BACK REAL MESSY, WE FIX
        butondelete.visible=False
        page.update()
    def go_backtolog(e):
        logincontainer.visible = True
        appcontainer.visible = False
        #separat:
 
        page.update()
    #POPUPS
    def openpassy():
        passy_text.value = "Wrong password!"
        passy.open = True
        page.update()
    def closepassy(e):
        passy.open = False
        page.update()
    def openpassytaken():
       passy_text.value = "Username taken!"
       passy.open = True
       page.update()
    ###
    #news
    def getNoticia(e):
        global current_article, articles
        try:
            url=f"https://newsapi.org/v2/everything?q={noticia.value}&from=2026-05-1&sortBy=popularity&apiKey=ea55e105b5914e7f92a9dc6f162f456b"
            requests1=requests.get(url)
            data= requests1.json()
        except:
            title.value="error"
            page.update()
            return
        articles = data["articles"]
 
        if len(articles) > 0:
            current_article = 0
            article = articles[current_article]
            author.value = article["author"]
            descr.value = article['description']
            title.value = article['title']
            butontourl.url = article['url']
            urltoimg.src = article['urlToImage']
            publishedAt.value = article['publishedAt']
            page.add(butontourl)
            page.update()
        else:
            descr.value =""
            title.value = "There is no article."
            author.value = ""
            urltoimg.src = ""
            publishedAt.value = ""
            page.update()
 
        page.update()
    def go_back(e):
        button_back.visible = False
        descr.visible = True
        title.visible = True
        author.visible = True
        butontourl.visible = True
        urltoimg.visible = True
        publishedAt.visible = True
        content.visible = True
        noticia.visible = True
        jamon.visible = True
        button_save.visible = True
        saved_articles.visible = True
        previous_noticia.visible = True
        next_noticia.visible = True
        allsaved_articles.visible = False
        butondelete.visible= False
        gobacklog.visible = True
        page.update()
    def opensav(e): #falta q te ponga la noticia entera no nama el titulo
       if allsaved_articles.value:
          sech="SELECT Titulo FROM Noticias_guardadas WHERE Titulo=? AND usarioid=?"
          framnambucano=(allsaved_articles.value,currentuser["id"])
          cursor.execute(sech, framnambucano)
          resultado= cursor.fetchone()
          if resultado:
             global current_article, articles
             try:
                url=f"https://newsapi.org/v2/everything?q={resultado[0]}&from=2026-05-1&sortBy=popularity&apiKey=ea55e105b5914e7f92a9dc6f162f456b"
                requests1=requests.get(url)
                data= requests1.json()
             except:
                title.value="error"
                page.update()
                return
             articles = data["articles"]
    
             if len(articles) > 0:
                current_article = 0
                article = articles[current_article]
                author.value = article["author"]
                descr.value = article['description']
                title.value = article['title']
                butontourl.url = article['url']
                urltoimg.src = article['urlToImage']
                publishedAt.value = article['publishedAt']
                page.add(butontourl)
                page.update()
             else:
                descr.value =""
                title.value = "There is no article."
                author.value = ""
                urltoimg.src = ""
                publishedAt.value = ""
                page.update()
    
             page.update()
             go_back(None)
       else:
           return
    def saved_artcl(e):
        descr.visible = False
        title.visible = False
        author.visible = False
        butontourl.visible = False
        urltoimg.visible = False
        publishedAt.visible = False
        content.visible = False
        noticia.visible = False
        jamon.visible = False
        button_save.visible = False
        saved_articles.visible = False
        previous_noticia.visible = False
        next_noticia.visible = False
        allsaved_articles.visible = True
        gobacklog.visible = False
        butondelete.visible= True
        button_back.visible = True
        loadarticlef()
        page.update()
   
    def going_back(e):
        global current_article, articles
       
        if articles != [0]:
            current_article -= 1
            article = articles[current_article]
 
            author.value = article["author"]
            descr.value = article['description']
            title.value = article['title']
            butontourl.url = article['url']
            urltoimg.src = article['urlToImage']
            publishedAt.value = article['publishedAt']
            page.update()
        else:
            descr.value =""
            title.value = "There is no article before this."
            author.value = ""
            urltoimg.src = ""
            publishedAt.value = ""
            page.update()
           
        page.update()
 
    def foward_noticia(e):
        global current_article, articles
       
        if articles != [-1]:
            current_article += 1
            article = articles[current_article]
 
            author.value = article["author"]
            descr.value = article['description']
            title.value = article['title']
            butontourl.url = article['url']
            urltoimg.src = article['urlToImage']
            publishedAt.value = article['publishedAt']
            page.update()
        else:
            descr.value =""
            title.value = "There is no article after this."
            author.value = ""
            urltoimg.src = ""
            publishedAt.value = ""
            page.update()
           
        page.update()
 
   
    descr = ft.Text(value="", size=30)
    title = ft.Text(value="", size=50, weight="bold")
    author = ft.Text(value="", size=20)
    butontourl= ft.ElevatedButton(text="go to page", url="wepa", url_target=ft.UrlTarget.BLANK)
    urltoimg = ft.Image(src = "bruh.png")
    publishedAt = ft.Text(value="", size=10, color="black")
    content = ft.Text(value="", size=20)
    button_back = ft.ElevatedButton(text="Go back", on_click=go_back)
    saved_articles = ft.ElevatedButton(text="Saved news", on_click=saved_artcl)
    allsaved_articles = ft.Dropdown(label= "SAVED ARTICLES",options=[ ], width = 200,on_change=opensav)
    noticia = ft.TextField(label="What news would you like to search for?")
    jamon=ft.ElevatedButton("Buscar", on_click=getNoticia)
    previous_noticia = ft.ElevatedButton("<- Prev", on_click=going_back)
    next_noticia = ft.ElevatedButton("Next ->", on_click=foward_noticia)
    gobacklog = ft.ElevatedButton("<- Login", on_click = go_backtolog)
   
    passy_text = ft.Text("")
    passy = ft.BottomSheet(
    content=ft.Container(
        content=ft.Column(
            width=200,
            height=200,
            controls=[
                passy_text,
                ft.ElevatedButton("Close", on_click=closepassy)
            ],
            alignment="center",
            horizontal_alignment="center"
        )
    )
)
    creds = ft.Text(value="by: Nathaniel Cortorreal, Do Lee, Juan Carlos, Alejandrox Pozo", size =10,italic= True)
    ppfimg = ft.Image(src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/ea5789c2-aacc-40ca-80ca-022e5730b9d4/dff400e-6748ce74-fbd0-47d5-8511-46043e148d34.png/v1/fill/w_732,h_1092,q_70,strp/the_powerpuff_girls__2016____season_4_poster_by_victorpinas_dff400e-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTI0MiIsInBhdGgiOiIvZi9lYTU3ODljMi1hYWNjLTQwY2EtODBjYS0wMjJlNTczMGI5ZDQvZGZmNDAwZS02NzQ4Y2U3NC1mYmQwLTQ3ZDUtODUxMS00NjA0M2UxNDhkMzQucG5nIiwid2lkdGgiOiI8PTgzMiJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.e4V4JY8JG_QegWIVkhJsCSMjkmwXkfKydeqxHSIQgdQ%22",
                      width=500,
                      height=500)
 
    def loadarticlef():
     if currentuser["id"]:
        loadarticle="SELECT Titulo FROM Noticias_guardadas WHERE usarioid=?"
        membucano=(currentuser["id"],)
        cursor.execute(loadarticle, membucano)
        noticias= cursor.fetchall()
        allsaved_articles.options.clear()
        for i in noticias:
            allsaved_articles.options.append(ft.dropdown.Option(key=i[0],text=i[0]))
        page.update()
     else:
        return
    def save(e):
     if currentuser["id"] is not None and title.value !="":
        print("GUARDANDO:", title.value, currentuser["id"]) #debug temporal se puede borra
        saveforuser="INSERT INTO Noticias_guardadas (Titulo, usarioid) VALUES (?, ?)"
        masambucano=(title.value, currentuser["id"])
        cursor.execute(saveforuser, masambucano)
        conn.commit()
        loadarticlef()
        print("USER:", currentuser["id"]) #debug temporal lo pueden borra
     else:
        return
    def deletef(e):
     if allsaved_articles.value:
         delete= "DELETE FROM Noticias_guardadas WHERE Titulo=? AND usarioid=?"
         german=(allsaved_articles.value, currentuser["id"])
         cursor.execute(delete, german)
         conn.commit()
         loadarticlef()
     else:
         return
    butondelete = ft.ElevatedButton(text="Delete", on_click=deletef)
    button_save = ft.ElevatedButton(text="Save news", on_click=save)
    homecontainer = ft.Container(
        content=ft.Column(
            [
                ft.Text("📰 PowerPuff News", size=42, weight="bold"),
                ft.Text("Stay updated with the latest news", size=16, color="grey"),
                ft.ElevatedButton(
                    "Login / Sign Up",
                    on_click=show_log,
                    style=ft.ButtonStyle(padding=20)
                ),
                ppfimg,
                creds
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
    padding=40,
    border_radius=20,
    bgcolor="#626262",
    )
    #apc
    appcontainer = ft.Container(
        content=ft.Column(
            [
                # search sect
                ft.Container(
                    content=ft.Row(
                        [noticia, jamon],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=15,
                    border_radius=15,
                    bgcolor="#626262"
                ),
                # articles sect
                ft.Container(
                    content=ft.Column(
                        [
                            title,
                            author,
                            urltoimg,
                            descr,
                            publishedAt,
                            ft.Row(
                                [button_save, butondelete],
                                spacing=10
                            ),
                            butontourl
                        ],
                        spacing=10
                    ),
                    padding=20,
                    border_radius=15,
                    bgcolor="#626262"
                ),
                # saveds sect
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Articles", weight="bold"),
       
                            ft.Row(
                               [previous_noticia, saved_articles, next_noticia],
                               spacing=5
                            ),
                            allsaved_articles,
                            button_back,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=15,
                    border_radius=15,
                    bgcolor="#626262",
                    width=250
 
                ),
                gobacklog
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        visible=False
    )
 
    #ui login
 
    logincontainer = ft.Container(
        content=ft.Column(
            [
                ft.Text("Login", size=30, weight="bold"),
                userbox,
                passwordbox,
                ft.Row(
                    [login, signup],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=30,
        width=350,
        border_radius=20,
        bgcolor="#626262",
        visible=False
    )
    page.overlay.append(passy)
    page.add(
        ft.Row([darklight], alignment=ft.MainAxisAlignment.END),
        homecontainer,
        logincontainer,
        appcontainer,
        passy
    )
ft.app(target=main)