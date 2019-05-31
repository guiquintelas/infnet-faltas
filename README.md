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


**Funções da versão 1.3**:
- guardar dados de autenticação para futuras consultas
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
  
 
