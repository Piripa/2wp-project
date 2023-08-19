from datetime import date
import re
a = [['Alessandro', '0123912', '08:10', 'Presente'], ['Vinicius', '123214912', '10:00', 'Presente']]
for i in a:
    nome = i[0]
    matricula = i[1]
    horario = i[2]
    estar_presente = i[3]
    print(nome,matricula,horario,estar_presente)


data_atual = date.today()
dataTexto = data_atual.strftime('%d_%m_%Y')
print(dataTexto)

    
