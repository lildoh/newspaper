import flet as ft
import requests
import os
import sqlite3
conn = sqlite3.connect("Newspaper.db", check_same_thread=False)
 
cursor = conn.cursor()
 
guardalnoticia = """
                    CREATE TABLE IF NOT EXISTS Noticias_guardadas(
                        idnoticia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        Titulo VARCHAR(50) NOT NULL  ,
                        usarioid INTEGER,
                        FOREIGN KEY(usarioid) REFERENCES Usarsario(idusuario)                  );
                    """
users= """ CREATE TABLE IF NOT EXISTS Usarsario( idusuario INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                                                 usarmame VARCHAR(40) NOT NULL,
                                                 password VARCHAR(40) NOT NULL);"""
article_select = "SELECT * FROM Noticias_guardadas"
cursor.execute(users)
cursor.execute(guardalnoticia)
 
results = cursor.fetchall()
 
#--------
def main(page: ft.Page):
    page.title = "jauncarlo"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = ft.ScrollMode.ALWAYS
 
   
 
 
    #light yagami
    def changetheme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if darklight.value else ft.ThemeMode.LIGHT
        )
        page.update()
 
    darklight = ft.Switch(label="🌞/🌙", value=False, on_change=changetheme)
   
    #login
    userbox= ft.TextField(label="user")
    passwordbox = ft.TextField(label="Password",password=True)
    def signupf(e):
       try:
           regitro= "INSERT INTO Usarsario(usarmame, password) VALUES (?,?)"
           pernambucano=(userbox.value, passwordbox.value)
           cursor.execute(regitro, pernambucano)
           show_app()
       except sqlite3.IntegrityError:
           userbox.label= "ta cojio"
           page.update()
    currentuser= None
    def loginf(e):
        global currentuser
        inisiasesion="SELECT idusuario FROM Usarsario WHERE usarmame=? AND password=?"
        perfamtutano=(userbox.value, passwordbox.value)   
        cursor.execute(inisiasesion, perfamtutano)
        result= cursor.fetchone()
        if result:
            currentuser= result[0]
            show_app()
        else:
            passwordbox.label="no"
            page.update()
    login = ft.ElevatedButton("Login", on_click=loginf)
    signup = ft.ElevatedButton("Create password", on_click=signupf)
 
    def show_app():
        logincontainer.visible = False
        appcontainer.visible = True
        button_back.visible = False
        page.update()
 
    def show_log(e):
        appcontainer.visible = False
        homecontainer.visible = False
        logincontainer.visible=True
        page.update()
   
    def show_app():
        logincontainer.visible = False
        appcontainer.visible = True
        button_back.visible = False
        allsaved_articles.visible = False
        page.update()
 
 
    #news
 
    def getNoticia(e):
 
        url=f"https://newsapi.org/v2/everything?q={noticia.value}&from=2026-04-1&sortBy=popularity&apiKey=ea55e105b5914e7f92a9dc6f162f456b"
        requests1=requests.get(url)
        data= requests1.json()
        articles = data["articles"]
 
        if len(articles) > 0:
 
            current_article = articles[0]
            author.value = current_article["author"]
            descr.value = current_article['description']
            title.value = current_article['title']
            butontourl.url = current_article['url']
            urltoimg.src = current_article['urlToImage']
            publishedAt.value = current_article['publishedAt']
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
        allsaved_articles.visible = False
        page.update()
 
 
    def saved_artcl(e):
        button_back.visible = True
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
        allsaved_articles.visible = True
        loadarticlef()
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
    allsaved_articles = ft.Dropdown(label= "SAVED ARTICLES",
                                    options=[
 
                                    ])
    noticia = ft.TextField(label="Que noticia deseas investigar?")
    jamon=ft.ElevatedButton("Buscar", on_click=getNoticia)
 
    logrequired = ft.ElevatedButton("Login/Sign in", on_click=show_log) #PUT INTO J2 CODE
 

 
    
    def loadarticlef(e):
     loadarticle="SELECT Titulo FROM Noticias_guardadas WHERE usarioid=?"
     membucano=(currentuser)
     cursor.execute(loadarticle, membucano)
     noticias= cursor.fetchall()
     allsaved_articles.options.clear()
     for i in noticias:
         allsaved_articles.options.append(ft.dropdown.Option(text=i[0]))
     page.update()
    def save(e):
     saveforuser="INSERT INTO Noticias_guardadas (Titulo, usarioid) VALUES (?, ?)"
     masambucano=(title.value, currentuser)
     cursor.execute(saveforuser, masambucano)
     conn.commit()
     loadarticlef()
    def deletef(e):
     if allsaved_articles.value:
         delete= "DELETE FROM Noticias_guardadas WHERE Titulo=? AND usarioid=?"
         german=(allsaved_articles.value, currentuser)
         cursor.execute(delete, german)
         conn.commit()
         loadarticlef()
     else:
         return
    button_save = ft.ElevatedButton(text="Save news", on_click=save)
    homecontainer = ft.Column([
        ft.Text(value="Welcome to", size = 20),
        ft.Text(value="NEWSNAMEIDK", weight=ft.FontWeight.BOLD,size = 50, italic= True ),
        logrequired
 
        ], visible=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    appcontainer = ft.Column([
        noticia,
        jamon,
        ft.Column([
            title,
            author,
            urltoimg,
            descr,
            content,
            publishedAt,
            button_save,
            saved_articles,
            button_back,
            allsaved_articles
        ])
    ], visible=False)
 
    #ui login
 
    if os.path.exists("password.txt"):
        signup.visible = False
    else:
        login.visible = False
        passwordbox.label = "Create password"
   
    logincontainer = ft.Column(
        [
            ft.Text("Login required", size=25),userbox,
            passwordbox,
            login,
            signup,
        ],  visible = False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
 
    page.add(
        ft.Row([darklight], alignment=ft.MainAxisAlignment.END),
        homecontainer,
        logincontainer,
        appcontainer
    )
 
ft.app(target=main)