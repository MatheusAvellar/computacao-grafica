import numpy as np

def lerMalha(nome):
  """Recebe uma string com o nome do arquivo .obj a ser lido. Retorna um
  np.ndarray com as x,y,z coordenadas dos pontos (uma coluna é um ponto) da
  malha e uma lista de strings, onde cada elemento da lista define uma face."""
  vertices = []
  faces = []
  arquivo = open(nome, "r")
  for line in arquivo:
    if line[0] == "v":
      partes = line.split(" ")
      vertices.append([float(partes[1]), float(partes[2]), float(partes[3])])
    if line[0] == "f":
      faces.append(line)
  arquivo.close()
  pontos = np.transpose(np.array(vertices))
  return pontos, faces

def escreverMalha(pts, faces, nome):
  """Recebe uma nd.array com x,y,z coordenadas de todos os pontos da malha,
  uma lista com os strings representando as faces da malha e
  um nome do arquivo no qual a malha deve ser escrita (em formato .obj)."""
  novo = np.transpose(pontos)
  arquivo = open(nome, "w")
  for ponto in novo:
    arquivo.write("v ")
    for eixo in ponto:
      arquivo.write(str(eixo) + " ")
    arquivo.write("\n")

  for face in faces:
    arquivo.write(face)
  arquivo.close()
  
#=================================================================
# # # # # # # # # # # # # # # #
#  Matheus Avellar de Barros  #
#      DRE 117038497          #
# # # # # # # # # # # # # # # #
#    Bob & seus amigos        #
#     _       _      _        #
#   >(.)__  <(.)__ =(.)__     #
#    (___/   (___/  (___/     #
#                             #
#             Ilustração por  #
#      Hayley Jane Wakenshaw  #
# # # # # # # # # # # # # # # #

def transformacaoAfim(pts):
  """Recebe um np.ndarray com x,y,z coordenadas de pontos. A função adiciona
  a 4a coordenada para representar os pontos em coordenadas homogêneas
  e aplica uma transformação afim. O valor de retorno é um np.ndarray
  com x,y,z coordenadas dos pontos transformados."""

  ###################################
  # - "Sentado no plano XY, eixo Z passa pelo toro"
  min_z = min(pts[1])
  # Rotaciona a base de Bob para alinhá-la com o eixo XY;
  # translada para encostar Bob no eixo XY
  Mtrs_rot = np.transpose(np.array([
    [ 1,  0,  0,    0   ],
    [ 0,  0, -1,    0   ],
    [ 0,  1,  0, -min_z ],
    [ 0,  0,  0,    1   ]
  ]))
  #   Matriz de rotação   +   M.transl.
  #      (θ = 90°)          (Tz = min{z})
  # | 1   0      0    0 |   | 0 0 0  0 |
  # | 0  cosθ  -senθ  0 | + | 0 0 0  0 |
  # | 0  senθ   cosθ  0 |   | 0 0 0 Tz |
  # | 0   0      0    1 |   | 0 0 0  1 |

  ###################################
  # - "Altura igual a 1"
  # Pega altura de Bob
  h = max(pts[1]) - min(pts[1])
  # Fator de escala é inverso da altura (queremos altura_final = 1)
  s = 1/h
  # Matriz de escalonamento com fator de altura
  Mscale = np.transpose(np.array([
    [ s, 0, 0, 0 ],
    [ 0, s, 0, 0 ],
    [ 0, 0, s, 0 ],
    [ 0, 0, 0, 1 ]
  ]))

  ###################################
  # - "Virado para o eixo Y positivo"
  # Rotaciona a base de Bob para alinhá-la com o eixo XY
  # Translada para o encostar Bob no eixo XY
  Mrotate = np.transpose(np.array([
    [ 0,  1,  0,  0 ],
    [-1,  0,  0,  0 ],
    [ 0,  0,  1,  0 ],
    [ 0,  0,  0,  1 ]
  ]))
  #   Matriz de rotação
  #      (θ = −90°)
  # | cosθ  -senθ  0  0 |
  # | senθ   cosθ  0  0 |
  # |  0      0    1  0 |
  # |  0      0    0  1 |

  ###################################
  Mfinal = Mtrs_rot @ Mscale @ Mrotate
  print("Matriz de transformação final:")
  print(np.transpose(Mfinal))
  # Deve ser a seguinte:
  # |  0.          0.         -2.25600696  0.         |
  # | -2.25600696  0.          0.          0.         |
  # |  0.          2.25600696  0.         -2.04760571 |
  # |  0.          0.          0.          1.         |

  # Aplica a transformação em todos os pontos de Bob
  pts_new = []
  for pt in np.transpose(pts):
    # Adiciona 4ª dimensão ao vetor do ponto
    pt_w = np.append(pt, 1)
    # Aplica todas as transformações
    res = pt_w @ Mfinal
    # Remove 4ª dimensão, e adiciona à lista de pontos
    pts_new.append(res[:-1])

  return np.transpose(np.array(pts_new))

#=================================================================

pontos, faces = lerMalha("bob.obj")
pontos = transformacaoAfim(pontos)
escreverMalha(pontos, faces, "bob_novo.obj")
