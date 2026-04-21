import flet as ft
import requests
import os
 
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
    passwordbox = ft.TextField(label="Password",password=True)
    def signupf(e):
        with open("password.txt", "w", encoding="utf-8") as file:
            file.write(passwordbox.value)
        show_app()
 
    def loginf(e):
        with open("password.txt", "r", encoding="utf-8") as file:
            saved = file.read()
 
        if passwordbox.value == saved:
            show_app()
        else:
            passwordbox.label = "Incorrect password"
            page.update()
    login = ft.ElevatedButton("Login", on_click=loginf)
    signup = ft.ElevatedButton("Create password", on_click=signupf)
 
    def show_log(e):
        appcontainer.visible = False
        homecontainer.visible = False
        logincontainer.visible=True
        page.update()
   
    def show_app():
        logincontainer.visible = False
        appcontainer.visible = True
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
 
    descr = ft.Text(value="", size=30)
    title = ft.Text(value="", size=50, weight="bold")
    author = ft.Text(value="", size=20)
    butontourl= ft.ElevatedButton(text="go to page", url="wepa", url_target=ft.UrlTarget.BLANK)
    urltoimg = ft.Image(src = "bruh.png")
    publishedAt = ft.Text(value="", size=10, color="black")
    content = ft.Text(value="", size=20)
 
    noticia = ft.TextField(label="Que noticia deseas investigar?")
    jamon=ft.ElevatedButton("Buscar", on_click=getNoticia)
 
    logrequired = ft.ElevatedButton("Login/Sign in", on_click=show_log)
   
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
            publishedAt
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
            ft.Text("Login required", size=25),
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
 