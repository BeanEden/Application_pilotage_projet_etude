import json
import os
from flask import Blueprint, render_template, request, jsonify

main = Blueprint('main', __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@main.route('/')
def index():
    return render_template('index.html', title="Dashboard NovaRetail")

@main.route('/cadrage/contexte')
def contexte():
    return render_template('context.html', title="Contexte & Objectifs")

@main.route('/cadrage/perimetre')
def perimetre():
    return render_template('scope.html', title="Périmètre & Livrables")

@main.route('/cadrage/parties-prenantes')
def parties_prenantes():
    WORKING_DAYS_2026 = 251
    stakeholders = load_json('collaborators.json')
    
    for s in stakeholders:
        s['tjm'] = round((s['salary'] * (1 + s['charge_rate'])) / WORKING_DAYS_2026, 2)
        
    return render_template('stakeholders.html', title="Parties Prenantes", stakeholders=stakeholders, working_days=WORKING_DAYS_2026)

@main.route('/cadrage/backlog')
def backlog():
    tasks = load_json('tasks.json')
    return render_template('backlog.html', title="Backlog Détaillé", tasks=tasks)

@main.route('/cadrage/gantt')
def gantt():
    weeks = ["12/05", "19/05", "26/05", "02/06", "09/06", "16/06", "23/06", "30/06", "07/07", "14/07"]
    tasks = load_json('tasks.json')
    return render_template('gantt.html', title="Planning Gantt", weeks=weeks, tasks=tasks)

@main.route('/cadrage/raci')
def raci():
    tasks = load_json('tasks.json')
    return render_template('raci.html', title="Matrice RACI", tasks=tasks)

@main.route('/cadrage/couts')
def couts():
    categories = ["Infrastructure", "Logiciel", "Matériel", "Déplacement", "Formation", "Autre"]
    buckets = ["Cadrage", "Architecture", "Modélisation", "Pipeline", "Power BI", "Rapport", "Soutenance"]
    collaborators = [s['name'] for s in load_json('collaborators.json')]
    costs = load_json('costs.json')
    
    return render_template('couts.html', title="Coûts Satellites", costs=costs, categories=categories, buckets=buckets, collaborators=collaborators)

@main.route('/cadrage/risques')
def risques():
    return render_template('risks.html', title="Risques & Hypothèses")

@main.route('/cadrage/budget')
def budget():
    tasks = load_json('tasks.json')
    collaborators = load_json('collaborators.json')
    satellite_costs = load_json('costs.json')
    
    return render_template('budget.html', 
                           title="Suivi Budgétaire", 
                           tasks=tasks, 
                           collaborators=collaborators, 
                           satellite_costs=satellite_costs)

@main.route('/cadrage/suivi')
def suivi():
    tasks = load_json('tasks.json')
    collaborators = load_json('collaborators.json')
    satellite_costs = load_json('costs.json')
    weeks = ["12/05", "19/05", "26/05", "02/06", "09/06", "16/06", "23/06", "30/06", "07/07", "14/07"]
    return render_template('suivi.html', title="Suivi d'Avancement", tasks=tasks, collaborators=collaborators, satellite_costs=satellite_costs, weeks=weeks)
