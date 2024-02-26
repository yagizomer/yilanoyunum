# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 22:15:37 2024

@author: Asus
"""

# Imports
import turtle
import time
import random


# Score ve delay
score = 0
high_score = 0
delay = 0.1    # Yılanın hareket hızını kontrol eden gecikme süresi.


# Ekran ayarları
wn = turtle.Screen()
wn.title('YILAN OYUNU')
wn.bgcolor("green")
wn.setup(width=700, height=700)
wn.tracer(0)  # Ekran güncellemelerini kapatır, manuel güncelleme yapılacak.

# Oyun alanının ana hatlarını oluşturalım
pencil = turtle.Turtle()
pencil.speed(0)
pencil.shape('circle')
pencil.color('black')
pencil.penup()
pencil.hideturtle()  # Turtle nesnesini gizler, sadece çizim yapmak için kullanılır.
pencil.goto(310,310)
pencil.pendown()
pencil.goto(-310,310)
pencil.goto(-310,-310)
pencil.goto(310,-310)
pencil.goto(310,310)
pencil.penup()



# Yılanın Kafasını oluşturalım
head = turtle.Turtle()
head.speed(0) # Animasyon hızını en hızlıya ayarlar.
head.shape("circle")
head.color('black')
head.penup()
head.goto(0,0)
head.direction = 'stop' # Yılanın başlangıçta hareket etmemesi için yön 'stop'.


# Yılan yemi oluşturalım
food = turtle.Turtle()
food.speed(0) # Animasyon hızını en hızlıya ayarlar.
food.shape("square")
food.color('red')
food.penup()
food.goto(0,100)

# yılanın vücudunu dinamik bir şekilde yönetmek ve oyunun ilerleyişi sırasında
#yılanın büyümesini sağlamak için kullanılır. Başlangıçta boş bir listedir. Daha sonrasında yem
#yedikçe aratacak ve her bi element segment listesine eklenecek.
segments = []

# # Skor tablosu için bir turtle nesnesi oluşturalım.
pen = turtle.Turtle()
pen.speed(0)
pen.shape('circle')
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 310)
pen.write('Score: 0 High Score: 0', align = 'center', font = ('Courier', 24, 'normal'))

### Fonksiyonlar
# Skor tablosunu güncellemek
def update_score():
    pen.clear()
    pen.write('Score: {} High Score: {}'.format(score, high_score), align='center', font = ('Courier', 24, 'normal'))

# Yılanın yönünü klavye hareketine göre değiştiren fonksiyonlar.
def go_up():
    if head.direction != 'down':  #aşağı doğru değilse
        head.direction = 'up'     #yukarı doğru çevir
def go_down():
    if head.direction != 'up':    
        head.direction = 'down'
def go_left():
    if head.direction != 'right':
        head.direction = 'left'
def go_right():
    if head.direction != 'left':
        head.direction = 'right'

# Yılanın her bir segmentinin ve başının konumunu günceller. 
def move():
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)
    # Segment 0'ı başa taşı
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)
    # Yılanın aynı yönde hareket etmesini sağlayın
    if head.direction == 'up':
        head.sety(head.ycor() + 10)
    if head.direction == 'down':
        head.sety(head.ycor() - 10)
    if head.direction == 'left':
        head.setx(head.xcor() - 10)
    if head.direction == 'right':
        head.setx(head.xcor() + 10)

# Çarpışma meydana geldiğinde oyuna ne yapacağını söyleyen işlevi yazalım
def collision():
    global score, delay # Global değişkenleri fonksiyon içinde kullanmak için bildirme
    time.sleep(0.5)
    head.goto(0,0)
    head.direction = 'stop'

    for segment in segments:
        segment.goto(1000, 1000) # segmentleri ekrandan kaldır
        segment.hideturtle()
    
    segments.clear()
    score = 0 # Skoru sıfırla
    update_score() # Skoru güncelle
    delay = 0.1 # Gecikmeyi sıfırla


### Oyun klavyeden bastığımız tuşları dinlesin
wn.listen()
wn.onkeypress(go_up, 'Up')
wn.onkeypress(go_down, 'Down')
wn.onkeypress(go_left, 'Left')
wn.onkeypress(go_right, 'Right')

#Oyun ekranının güncellenmesini yapalım
while True:
    # Pencereyi tekrar tekrar günceller
    wn.update()

    # Sınır ile çarpışma olup olmadığını kontrol edin
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        collision()

    # Yılanın yiyeceği yiyip yemediğini kontrol edin
    if head.distance(food) < 20:
        # Rastgele yeni bir yem
        food.goto(random.randint(-290,290),random.randint(-290,290))
        # Ve yılan yemi yedikçe gövdesine eklenen her bir element segmentse eklensin
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape('circle')
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)
        # Yılan her yiyecek yediğinde, oyunun hızı artsın
        delay -= 0.001
        # Skor güncellensin
        score += 10
        if score > high_score:
            high_score = score
        update_score()

    # Yılanın hareketi için gerekli
    move()

    # Kendi vücuduyla çarpışma kontrolü
    for segment in segments:
        if segment.distance(head) < 10:
            collision()
    # Bu, yılanın hareketlerini görsel olarak takip edebilmemizi sağlar.
    time.sleep(delay)

# oyun sürekli olarak kullanıcı girdilerini alabilir ve yılanın hareketlerini güncelleyebilir.
wn.mainloop()