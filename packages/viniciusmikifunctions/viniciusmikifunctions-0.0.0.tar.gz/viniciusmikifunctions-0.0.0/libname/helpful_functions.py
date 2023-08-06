# hello world
def valide_entradas(lista_de_entradas, lista_de_tipos):
  if len(lista_de_entradas) != len(lista_de_tipos):
    raise IndexError("len(lista_de_entradas) must be equal len(lista_de_tipos)")
  else:
    for i in range(len(lista_de_entradas)):
      if isinstance(lista_de_entradas[i], lista_de_tipos[i]):
        pass
      else:
        raise ValueError(f"{lista_de_entradas[i]} must be an instance of {lista_de_tipos[i]}")