import flet as ft
import requests
def main(page: ft.Page):
    page.title = "jauncarlo"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = ft.ScrollMode.ALWAYS

    # def loginjuanpao(e):
        #la cosa del login
    def changetheme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if darklight.value else ft.ThemeMode.LIGHT
        )
        page.update()
 
    darklight = ft.Switch(label="🌞/🌙", value=False, on_change=changetheme)
    def getNoticia(e):
   
            url=f"https://newsapi.org/v2/everything?q=%7B{noticia.value}%7D&from=2026-03-22&sortBy=popularity&apiKey=ea55e105b5914e7f92a9dc6f162f456b"
            requests1=requests.get(url)
            data= requests1.json()
            articles = data["articles"]
            current_article = articles[0]
            if len(articles) > 0:
   
                current_article = articles[0]
                author.value = current_article["author"]
                descr.value = current_article['description']
                title.value = current_article['title']
                urltoimg.src = current_article['urlToImage']
                publishedAt.value = current_article['publishedAt']
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
    urltoimg = ft.Image(src = "bruh.png")
    publishedAt = ft.Text(value="", size=10, color="black") #optional creo
    content = ft.Text(value="", size=20) #optional
    noticia = ft.TextField(label="Que noticia deseas investigar?")
    jamon=ft.ElevatedButton("Buscar", on_click=getNoticia)
 
 
 
    page.add(
        noticia,
        jamon,
        ft.Column([
            title,
            author,
            urltoimg,
            descr,
            content,
            publishedAt,
            darklight
 
]    ))
ft.app(target=main)