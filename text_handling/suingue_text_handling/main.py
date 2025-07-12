import ast

with open("alunos.txt", "r") as alunos:
    file = alunos.read().strip()
    aluno_list = ast.literal_eval(file)
    for aluno in aluno_list:
        print(aluno)