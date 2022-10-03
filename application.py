from flask import Flask, render_template, request
from ete3 import Tree
from CladogramGeneratorAlgorithm import generatePhlyogeneticTree

application = Flask('Cladogram Generator Algorithm')
application.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

@application.route('/', methods=['GET', 'POST'])
@application.route('/home', methods=['GET', 'POST'])
def homepage():
  return render_template('homepage.html')


@application.route('/generate', methods=['GET', 'POST'])
def generateCladogram():
  submitted = False
  newickString = None
  if request.method == "POST":
    #Cladogram Data Passed. Perform Data Preprocessing.
    dimensions = (int(request.form.get('rows')), int(request.form.get('columns')))
    print(dimensions)
    dcLabels = [None for i in range(dimensions[1])]
    speciesLabels = [None for i in range(dimensions[0])]
    inputData = [[None for j in range(dimensions[1])] for i in range(dimensions[0])]
    for data in request.form:
      print(data, type(data))
      if 'data' in data:
        coordinates = data.replace('data_', '').split('_')
        print(coordinates)
        coordinates = [int(i) for i in coordinates]
        inputData[coordinates[0]][coordinates[1]] = request.form.get(data)
      elif 'dc' in data:
        dcLabels[int(data.replace('dc_', ''))] = request.form.get(data)
      elif 'species' in data:
        speciesLabels[int(data.replace('species_', ''))] = request.form.get(data)
    print(dcLabels, speciesLabels, dimensions, inputData)
    newickString = generatePhlyogeneticTree(dcLabels, speciesLabels, dimensions, inputData)
    print(newickString)
    #Tree(newickString).render('mytree.png')
    Tree(newickString).render('static/mytree.png')
    submitted = True
  return render_template('cladogramAlgorithm.html', submitted=submitted, newickString=newickString)

application.run(host='0.0.0.0', port=8080, debug=True)