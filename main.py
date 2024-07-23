from PyQt5.QtWidgets import QWidget,QApplication, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout,QFileDialog
import os
from PIL import Image
from PIL.ImageFilter import SHARPEN
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy editor')
main_win.resize(650, 450)

#віджети
btn_folder = QPushButton("Папка")
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкізть")
btn_bw = QPushButton("Ч/Б")

lb_image = QLabel("Картинка")
list_files = QListWidget()

#лінії
col1 = QVBoxLayout()
col1.addWidget(btn_folder)
col1.addWidget(list_files)

row1 = QHBoxLayout()
row1.addWidget(btn_left)
row1.addWidget(btn_right)
row1.addWidget(btn_flip)
row1.addWidget(btn_sharp)
row1.addWidget(btn_bw)

col2 = QVBoxLayout()
col2.addWidget(lb_image)
col2.addLayout(row1)

main_row = QHBoxLayout()
main_row.addLayout(col1,20)
main_row.addLayout(col2,80)
main_win.setLayout(main_row)


workdir=''

def filter(filenames,extensions):
  result=[]
  for file in filenames:
    for ext in extensions:
      if file.endswith(ext):
        result.append(file)
  return result

def chooseWorkdir():
  global workdir
  workdir=QFileDialog.getExistingDirectory()


def showFilenamesList():
  extensions=['.png','.jpg','.gif','.jpeg']
  chooseWorkdir()
  filenames = filter(os.listdir(workdir),extensions) 
  list_files.clear()
  for file in filenames:
    list_files.addItem(file)


btn_folder.clicked.connect(showFilenamesList)



class ImageProcessor():
  def __init__(self):
    self.image = None
    self.dir = None
    self.filename = None
    self.save_dir ="Modified/"
  def loadImage(self, dir, filename):
    self.dir = dir
    self.filename=filename
    image_path = os.path.join(dir,filename)
    self.image = Image.open(image_path)
  def showImage(self, path):
    lb_image.hide()
    pixmapimage = QPixmap(path)
    w,h = lb_image.width(), lb_image.height()
    pixmapimage = pixmapimage.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
    lb_image.setPixmap(pixmapimage)
    lb_image.show()
  def saveImage(self):
    path = os.path.join(workdir, self.save_dir)
    if not(os.path.exists(path) or os.path.isdir(path)):
        os.mkdir(path)
    image_path = os.path.join(path, self.filename)
    self.image.save(image_path)
  def do_bw(self):
    self.image = self.image.convert("L")
    self.saveImage()
    image_path = os.path.join(workdir,self.save_dir,self.filename)
    self.showImage(image_path)
  def do_sharpen(self):
    self.image = self.image.filter(SHARPEN)
    self.saveImage()
    image_path = os.path.join(workdir,self.save_dir,self.filename)
    self.showImage(image_path)

  def do_left(self):
    self.image = self.image.transpose(Image.ROTATE_90)
    self.saveImage()
    image_path = os.path.join(workdir,self.save_dir,self.filename)
    self.showImage(image_path)
  def do_right(self):
    self.image = self.image.transpose(Image.ROTATE_270)
    self.saveImage()
    image_path = os.path.join(workdir,self.save_dir,self.filename)
    self.showImage(image_path)    
  def do_flip(self):
    self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
    self.saveImage()
    image_path = os.path.join(workdir,self.save_dir,self.filename)
    self.showImage(image_path)     
  

workimage = ImageProcessor()
 
def showChosenImage():
   if list_files.currentRow() >= 0:
       filename = list_files.currentItem().text()
       workimage.loadImage(workdir, filename)
       image_path = os.path.join(workimage.dir, workimage.filename)
       workimage.showImage(image_path)
 
list_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)


main_win.show()
app.exec()
