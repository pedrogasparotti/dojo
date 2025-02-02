alunos = [ 'Claudinho', 'Bochecha']

disciplinas = [ 'Suingue', 'Harmônia', 'Improviso', 'Chachado']

notas = (10, 9, 8, 10)

conteudo = []

for i in range(len(notas)):
    conteudo.append(f"A nota da {disciplinas[i]} foi {notas[i]}\n")

with open("boletim.txt", 'a') as arq:
    arq.writelines(conteudo)