import json
import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify

main = Blueprint('main', __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static', 'uploads', 'architecture')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_collaborators():
    WORKING_DAYS_2026 = 251
    collabs = load_json('collaborators.json')
    for c in collabs:
        c['tjm'] = round((c['salary'] * (1 + c['charge_rate'])) / WORKING_DAYS_2026, 2)
    return collabs

def get_dynamic_timeline(tasks):
    dates = []
    for t in tasks:
        if t.get('start_date'): dates.append(datetime.strptime(t['start_date'], '%Y-%m-%d'))
        if t.get('end_date'): dates.append(datetime.strptime(t['end_date'], '%Y-%m-%d'))
    
    if not dates:
        default_weeks = ["12/05", "19/05", "26/05", "02/06", "09/06", "16/06", "23/06", "30/06", "07/07", "14/07"]
        default_months = ["Mai 2026", "Juin 2026", "Juil 2026"]
        return default_weeks, default_months, "2026-05-12", 70
    
    min_date = min(dates)
    max_date = max(dates)
    start_project_date = min_date.strftime('%Y-%m-%d')
    
    # Generate weeks
    weeks = []
    curr = min_date
    while curr <= max_date + timedelta(days=6):
        weeks.append(curr.strftime('%d/%m'))
        curr += timedelta(days=7)
        
    if not weeks:
        weeks.append(min_date.strftime('%d/%m'))
        
    # Generate months
    months = []
    curr_month = min_date.replace(day=1)
    while curr_month <= max_date:
        months.append(curr_month.strftime('%b %Y'))
        # Add 32 days and replace day to 1 to advance by 1 month safely
        next_month = (curr_month + timedelta(days=32)).replace(day=1)
        curr_month = next_month
        
    if not months:
        months.append(min_date.strftime('%b %Y'))
        
    total_days = (max_date - min_date).days
    if total_days <= 0: total_days = 7

    return weeks, months, start_project_date, total_days

def get_project_total():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    costs = load_json('costs.json')
    
    total_rh = 0
    for t in tasks:
        days = 10 if '2 sem' in t.get('duration', '') else 5
        for name in t.get('assignees', []):
            co = next((c for c in collaborators if c['name'] == name), None)
            if co: total_rh += co.get('tjm_applied', 0) * days
    
    total_sat = 0
    for c in costs:
        try: total_sat += float(c.get('amount', 0))
        except: pass

    return total_rh + total_sat

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@main.route('/api/save-roi', methods=['POST'])
def save_roi():
    data = request.json
    save_json('roi.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-costs', methods=['POST'])
def save_costs():
    data = request.json
    save_json('costs.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-collaborators', methods=['POST'])
def save_collaborators():
    data = request.json
    # Optionally strip the dynamically calculated 'tjm' before saving
    for c in data:
        if 'tjm' in c:
            del c['tjm']
    save_json('collaborators.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-tasks', methods=['POST'])
def save_tasks():
    data = request.json
    save_json('tasks.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-architecture', methods=['POST'])
def save_architecture():
    data = request.json
    save_json('architecture.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-events', methods=['POST'])
def save_events():
    data = request.json
    save_json('events.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-operating-costs', methods=['POST'])
def save_operating_costs():
    data = request.json
    save_json('operating_costs.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-export-configs', methods=['POST'])
def save_export_configs():
    data = request.json
    save_json('export_configs.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-project-info', methods=['POST'])
def save_project_info():
    data = request.json
    save_json('project_info.json', data)
    return jsonify({"status": "success"})

@main.route('/api/save-user-stories', methods=['POST'])
def save_user_stories():
    data = request.json
    save_json('user_stories.json', data)
    return jsonify({"status": "success"})

@main.route('/api/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    if file:
        # Simple filename cleaning
        filename = file.filename.replace(" ", "_")
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        url = f"/static/uploads/architecture/{filename}"
        return jsonify({"status": "success", "url": url})

@main.route('/')
def index():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    events = load_json('events.json')
    costs = load_json('costs.json')
    project_total = get_project_total()
    weeks, months, start_project, total_days = get_dynamic_timeline(tasks)
    return render_template('index.html', title="Dashboard Vocalis", 
                           tasks=tasks, collaborators=collaborators, 
                           events=events, costs=costs, 
                           project_total=project_total, weeks=weeks)

@main.route('/cadrage/contexte')
def contexte():
    info = load_json('project_info.json')
    if not info: info = {}
    return render_template('context.html', title="Contexte & Objectifs", info=info)

@main.route('/cadrage/perimetre')
def perimetre():
    info = load_json('project_info.json')
    if not info: info = {}
    return render_template('scope.html', title="Périmètre & Livrables", info=info)

@main.route('/cadrage/parties-prenantes')
def parties_prenantes():
    WORKING_DAYS_2026 = 251
    stakeholders = get_collaborators()
    tasks = load_json('tasks.json')
    costs = load_json('costs.json')
    info = load_json('project_info.json')
    if not info: info = {}
    return render_template('stakeholders.html', title="Parties Prenantes", stakeholders=stakeholders, working_days=WORKING_DAYS_2026, tasks=tasks, costs=costs, info=info)

@main.route('/cadrage/user-stories')
def user_stories():
    data = load_json('user_stories.json')
    if not data:
        data = []
    return render_template('user_stories.html', title="Epics & User Stories", user_stories=data)

@main.route('/cadrage/backlog')
def backlog():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    return render_template('backlog.html', title="Backlog Détaillé", tasks=tasks, collaborators=collaborators)

@main.route('/cadrage/gantt')
def gantt():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    weeks, months, start_project_date, total_days = get_dynamic_timeline(tasks)
    return render_template('gantt.html', title="Planning Gantt", 
                           weeks=weeks, months=months, 
                           start_project_date=start_project_date, total_days=total_days, 
                           tasks=tasks, collaborators=collaborators)

@main.route('/cadrage/raci')
def raci():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    return render_template('raci.html', title="Matrice RACI", tasks=tasks, collaborators=collaborators)

@main.route('/cadrage/couts')
def couts():
    categories = ["Infrastructure", "Logiciel", "Matériel", "Déplacement", "Formation", "Autre"]
    buckets = ["Cadrage & analyse", "Architecture & setup", "Développement des 4 infrastructures", "Tests & évaluation", "Documentation & soutenance"]
    collaborators = [s['name'] for s in load_json('collaborators.json')]
    costs = load_json('costs.json')
    
    return render_template('couts.html', title="Coûts Satellites", costs=costs, categories=categories, buckets=buckets, collaborators=collaborators)

@main.route('/cadrage/roi')
def roi():
    roi_data = load_json('roi.json')
    if not roi_data: roi_data = {"revenues": [], "savings": []}
    
    project_total = get_project_total()
    op_costs = load_json('operating_costs.json')
    return render_template('roi.html', title="Calcul ROI", roi_data=roi_data, project_total=project_total, op_costs=op_costs)

@main.route('/api/save-risks', methods=['POST'])
def save_risks():
    data = request.json
    save_json('risks.json', data)
    return jsonify({"status": "success"})

@main.route('/cadrage/risques')
def risques():
    risks = load_json('risks.json')
    if not risks:
        risks = []
    project_total = get_project_total()
    return render_template('risks.html', title="Risques & Hypothèses", risks=risks, project_total=project_total)

@main.route('/cadrage/architecture')
def architecture():
    import itertools
    architectures = load_json('architecture.json')
    for arch in architectures:
        steps = arch.get('steps', [])
        if not steps:
            arch['phases'] = []
            continue
            
        adj = {s['id']: [] for s in steps}
        in_degree = {s['id']: 0 for s in steps}
        step_map = {s['id']: s for s in steps}
        
        for s in steps:
            prev = s.get('previous_step_id')
            if prev and prev in adj:
                adj[prev].append(s['id'])
                in_degree[s['id']] += 1
                
        queue = [sid for sid in in_degree if in_degree[sid] == 0]
        sorted_steps = []
        
        while queue:
            if sorted_steps:
                last_cat = sorted_steps[-1].get('category', '')
                candidates = [q for q in queue if step_map[q].get('category', '') == last_cat]
                if candidates:
                    candidates.sort(key=lambda x: step_map[x].get('subcategory', ''))
                    curr = candidates[0]
                else:
                    queue.sort(key=lambda x: (step_map[x].get('category', ''), step_map[x].get('subcategory', '')))
                    curr = queue[0]
            else:
                queue.sort(key=lambda x: (step_map[x].get('category', ''), step_map[x].get('subcategory', '')))
                curr = queue[0]
                
            queue.remove(curr)
            sorted_steps.append(step_map[curr])
            
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)
                    
        for s in steps:
            if s not in sorted_steps:
                sorted_steps.append(s)
                
        arch['steps'] = sorted_steps
        
        phases = []
        for cat, cat_group in itertools.groupby(sorted_steps, key=lambda x: x.get('category', '')):
            cat_steps = list(cat_group)
            sub_phases = []
            for sub, sub_group in itertools.groupby(cat_steps, key=lambda x: x.get('subcategory', '')):
                sub_phases.append({'name': sub, 'steps': list(sub_group)})
            phases.append({'name': cat, 'subcategories': sub_phases})
            
        arch['phases'] = phases

    return render_template('architecture.html', title="Architecture du Projet", steps=architectures)

@main.route('/api/save-modelisation', methods=['POST'])
def save_modelisation():
    data = request.json
    save_json('modelisation.json', data)
    return jsonify({"status": "success"})

@main.route('/cadrage/modelisation')
def modelisation():
    modelisations = load_json('modelisation.json')
    if not modelisations:
        modelisations = []
    return render_template('modelisation.html', title="Modélisation des Tables", modelisations=modelisations)

@main.route('/cadrage/budget')
def budget():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    satellite_costs = load_json('costs.json')
    categories = ["Infrastructure", "Logiciel", "Matériel", "Déplacement", "Formation", "Autre"]
    weeks, months, start_project_date, total_days = get_dynamic_timeline(tasks)
    return render_template('budget.html', title="Suivi Budgétaire", tasks=tasks, 
                           collaborators=collaborators, satellite_costs=satellite_costs, 
                           categories=categories, weeks=weeks, months=months, 
                           start_project_date=start_project_date, total_days=total_days)

@main.route('/cadrage/rentabilite')
def rentabilite():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    satellite_costs = load_json('costs.json')
    categories = ["Infrastructure", "Logiciel", "Matériel", "Déplacement", "Formation", "Autre"]
    return render_template('rentabilite.html', title="Rentabilité du Projet", tasks=tasks, collaborators=collaborators, satellite_costs=satellite_costs, categories=categories)

@main.route('/cadrage/devis')
def devis():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    satellite_costs = load_json('costs.json')
    return render_template('devis.html', title="Devis Client", tasks=tasks, collaborators=collaborators, satellite_costs=satellite_costs)

@main.route('/cadrage/suivi')
def suivi():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    satellite_costs = load_json('costs.json')
    events = load_json('events.json')
    weeks, months, _, _ = get_dynamic_timeline(tasks)
    return render_template('suivi.html', title="Suivi d'Avancement", tasks=tasks, collaborators=collaborators, satellite_costs=satellite_costs, events=events, weeks=weeks)

@main.route('/cadrage/evenements')
def evenements():
    events = load_json('events.json')
    total_costs = sum(float(e.get('cost', 0)) for e in events)
    total_savings = sum(float(e.get('saving', 0)) for e in events)
    differential = total_savings - total_costs
    
    event_types = [
        "Tâche supplémentaire", 
        "Temps supplémentaire", 
        "Coût satellite", 
        "RH - Congés", 
        "RH - Départ", 
        "RH - Recrutement", 
        "Retard", 
        "Autre"
    ]
    
    return render_template('events.html', 
                         title="Journal des Évènements", 
                         events=events, 
                         total_costs=total_costs, 
                         total_savings=total_savings, 
                         differential=differential,
                         event_types=event_types)

@main.route('/cadrage/exploitation')
def exploitation():
    costs = load_json('operating_costs.json')
    categories = ["Cloud / Infra", "Licences", "Maintenance", "Support", "Formation", "Autre"]
    return render_template('operating_costs.html', title="Coûts d'Exploitation", costs=costs, categories=categories)

@main.route('/cadrage/kanban')
def kanban():
    tasks = load_json('tasks.json')
    collaborators = get_collaborators()
    return render_template('kanban.html', title="Kanban du Projet", tasks=tasks, collaborators=collaborators)

@main.route('/cadrage/export')
def export_page():
    configs = load_json('export_configs.json')
    pages = [
        {"id": "contexte", "title": "Contexte & Objectifs", "url": "/cadrage/contexte"},
        {"id": "perimetre", "title": "Périmètre & Livrables", "url": "/cadrage/perimetre"},
        {"id": "parties-prenantes", "title": "Équipe & RH", "url": "/cadrage/parties-prenantes"},
        {"id": "risques", "title": "Risques & Hypothèses", "url": "/cadrage/risques"},
        {"id": "architecture", "title": "Architecture du Projet", "url": "/cadrage/architecture"},
        {"id": "modelisation", "title": "Modélisation des Tables", "url": "/cadrage/modelisation"},
        {"id": "user-stories", "title": "Epics & User Stories", "url": "/cadrage/user-stories"},
        {"id": "backlog", "title": "Backlog Détaillé", "url": "/cadrage/backlog"},
        {"id": "gantt", "title": "Planning Gantt", "url": "/cadrage/gantt"},
        {"id": "raci", "title": "Matrice RACI", "url": "/cadrage/raci"},
        {"id": "suivi", "title": "Suivi d'Avancement", "url": "/cadrage/suivi"},
        {"id": "evenements", "title": "Journal des Évènements", "url": "/cadrage/evenements"},
        {"id": "couts", "title": "Coûts Satellites", "url": "/cadrage/couts"},
        {"id": "exploitation", "title": "Coûts d'Exploitation", "url": "/cadrage/exploitation"},
        {"id": "budget", "title": "Suivi Budgétaire", "url": "/cadrage/budget"},
        {"id": "rentabilite", "title": "Rentabilité du Projet", "url": "/cadrage/rentabilite"},
        {"id": "roi", "title": "Calcul ROI", "url": "/cadrage/roi"}
    ]
    return render_template('export.html', title="Centre d'Exportation", configs=configs, pages=pages)
