# infnet-faltas
Script para calcular as faltas contabilizadas no moodle da faculdade Infnet. <br>
Ajudando a otimizar aquele 75% de presença :)

![Test Run](https://github.com/guiquintelas/infnet-faltas/blob/master/static/print.png)

**Funções da versão 1.0**:
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
  - frequencia atual
  - faltas
  - atrasos
  - dias nao lançados
  - faltas disponiveis
  - atrasos disponiveis
  
 **Utilização**
 
```
git clone https://github.com/guiquintelas/infnet-faltas.git
cd infnet-faltas
pip install selenium
pip install PyInquirer
python main.py
```
