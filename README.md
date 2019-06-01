# infnet-faltas
Script para calcular as faltas contabilizadas no moodle da faculdade Infnet. <br>
Ajudando a otimizar aquele 75% de presença :)

![Test Run](https://github.com/guiquintelas/infnet-faltas/blob/master/static/print.png)

**Instalação**
 
```
git clone https://github.com/guiquintelas/infnet-faltas.git
cd infnet-faltas
pip install beautifulsoup4
pip install PyInquirer
pip install requests
python main.py
```


**Funções da versão 2.0**:
- guardar dados de autenticação para futuras consultas
- Sistema de templates, podendo guardar suas escolhas para futuras execuções<br>
![Test Run](https://github.com/guiquintelas/infnet-faltas/blob/master/static/print_template.png)
- possivel selecionar dentre essas categorias:
  - escola
  - curso
  - classe
  - bloco
  - materia
- listando essas informações por materia
  - nome da materia
  - dias da semana
  - aulas dadas / total de aulas
  - frequencia atual
  - faltas
  - atrasos
  - dias nao lançados
  - faltas disponiveis
  - atrasos disponiveis
  
 
