from json_logic import jsonLogic


with open("data.json", "r") as alunos:
    data = alunos.read()

print(jsonLogic( { "if": [ { "missing": [ "formData.length", "formData.radius" ] }, 0, { "*": [ { "var": "formData.length" }, { "*": [ { "var": "formData.radius" }, { "var": "formData.radius" } ] }, { "var": 3.14 } ] } ] }, data))