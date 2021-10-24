import math
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

# para poder carregar uma malha .obj:
loadPrcFileData("", "load-file-type p3assimp")

# deativar caching (para que o panda3D não use dados "velhos"):
cache = BamCache.get_global_ptr()
cache.set_active(False)

class MeuApp(ShowBase):
  def __init__(self):
    '''Abre a janela, cria um gráfo de cena e prepara tudo que é preciso
    para renderizar essa cena na janela. Define a luz da cena, chama um
    método que carrega malhas em formato .obj e mapea texturas nelas. Chama
    também um método que define a câmera e o movimento/setting dela.'''
    ShowBase.__init__(self)
    self.carregarModelos()

    # definir luz e sombra:
    alight = AmbientLight("Ambient")
    alight.setColor((0.8, 0.8, 0.8, 1))
    alnp = self.render.attachNewNode(alight)
    self.render.setLight(alnp)

    plight = PointLight("plight")
    plight.setColor((0.6, 0.6, 0.6, 1))
    plight.setShadowCaster(True, 2048, 2048)
    self.render.setShaderAuto()
    plnp = self.render.attachNewNode(plight)
    plnp.setPos(2, 6, 3)
    self.render.setLight(plnp)
  
    # desativar trackball controle de camera:
    base.disableMouse()
    # chamar o método duckZoomTask cada frame:
    self.taskMgr.add(self.duckZoomTask, "DuckZoomTask")

  ##========== Método que carrega as malhas ==========
  def carregarModelos(self):
    '''Carrega malhas em formato .obj e mapea texturas nelas. Especifica
    a posição, escalonamento e a orientação dos modelos. Coloca os modelos
    no grafo de cena usando o método reparentTo.'''
    self.fundo = self.loader.loadModel("esquina_tex.obj")
    tex = loader.loadTexture("fundo.png")
    self.fundo.setTexture(tex,1)
    self.fundo.reparentTo(self.render) # fazendo a malha visível

    self.bob = self.loader.loadModel("bob190k_tex.obj")
    tex = loader.loadTexture("bob_clean.png")
    self.bob.setTexture(tex,1)
    self.bob.setScale(0.25, 0.25, 0.25) # escalonamento X, Y, Z
    self.bob.setHpr(60,0,0) # rotacao em volta de Z, X, Y
    self.bob.setPos(0.75, -3.725, 1.5) # posicao (X,Y,Z)
    self.bob.reparentTo(self.render)
 
    self.spot1 = self.loader.loadModel("spot190k_tex.obj")
    tex = loader.loadTexture("spot_white.png")
    self.spot1.setTexture(tex,1)
    self.spot1.setHpr(-78,0,0) # rotacao em volta de Z, X, Y
    self.spot1.setPos(-1, -4, 0)
    self.spot1.reparentTo(self.render)

    self.spot2 = self.loader.loadModel("spot190k_tex.obj")
    tex = loader.loadTexture("spot_brown.png")
    self.spot2.setTexture(tex,1)
    self.spot2.setHpr(78,0,0) # rotacao em volta de Z, X, Y
    self.spot2.setPos(1, -4, 0)
    self.spot2.reparentTo(self.render)

    self.background_spot1 = self.loader.loadModel("spot190k_tex.obj")
    tex = loader.loadTexture("spot_white.png")
    self.background_spot1.setTexture(tex,1)
    self.background_spot1.setScale(0.5, 0.5, 0.5) # escalonamento X, Y, Z
    self.background_spot1.setHpr(-127,0,0) # rotacao em volta de Z, X, Y
    self.background_spot1.setPos(5, -11, 0)
    self.background_spot1.reparentTo(self.render)

    self.background_spot2 = self.loader.loadModel("spot190k_tex.obj")
    tex = loader.loadTexture("spot_white.png")
    self.background_spot2.setTexture(tex,1)
    self.background_spot2.setScale(0.5, 0.5, 0.5) # escalonamento X, Y, Z
    self.background_spot2.setHpr(127,0,0) # rotacao em volta de Z, X, Y
    self.background_spot2.setPos(6, -11, 0)
    self.background_spot2.reparentTo(self.render)

    self.background_spot3 = self.loader.loadModel("spot190k_tex.obj")
    tex = loader.loadTexture("spot_brown.png")
    self.background_spot3.setTexture(tex,1)
    self.background_spot3.setScale(0.5, 0.5, 0.5) # escalonamento X, Y, Z
    self.background_spot3.setPos(5.5, -11.75, 0)
    self.background_spot3.reparentTo(self.render)

    self.background_spot3 = self.loader.loadModel("spot190k_tex.obj")
    tex = loader.loadTexture("spot_brown.png")
    self.background_spot3.setTexture(tex,1)
    self.background_spot3.setScale(0.5, 0.5, 0.5) # escalonamento X, Y, Z
    self.background_spot2.setHpr(60,0,0) # rotacao em volta de Z, X, Y
    self.background_spot3.setPos(-3, -11.75, 0)
    self.background_spot3.reparentTo(self.render)

  ##========== Método que define o movimento de camera ========== 
  def duckZoomTask(self, tarefa):
    '''
    Função que define o seguinte movimento de câmera, em loop, entre duas "visões":
    - Uma visão ampla de ambas as vaquinhas, encarando-se, em um campo verde;
    - Uma visão aproximada, com foco no patinho Bob em cima da vaquinha marrom.
    Além disso, essa função também define a dança do patinho Bob; ele gira em
    cima da cabeça da vaquinha marrom.
    '''
    # Referência da posição atual no ciclo [0, 1]
    t = (1+math.cos(math.pi*tarefa.time/6))/2

    # Câmera
    ## Posição
    self.camera.lookAt(0.75, -3.8, 1.5)
    self.camera.setPos(-1.25*t+0.5, 0.75, 2+3*t)
    ## FOV
    base.camLens.setFov(10 + 45*(1-t))

    # Bob
    self.bob.setHpr(45*(math.cos(math.pi*tarefa.time)), 0, 0) # rotacao em volta de Z, X, Y

    return tarefa.cont

aula4 = MeuApp()
# última linha: metódo run renderiza a janela e trata as background tarefas:
aula4.run()
