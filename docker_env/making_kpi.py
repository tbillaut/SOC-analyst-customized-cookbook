import plotly.graph_objects as go

def draw_indicator(nb_of_mitre_actors, nb_of_mitre_techniques, nb_of_actors, nb_of_techniques, nb_most_used_tech, image_file):
    fig = go.Figure()
    # draw gauge 0,0 -> nb of group
    fig.add_trace(go.Indicator(
        value = nb_of_actors,
        mode = "gauge+number",
        gauge = {'axis': {'range': [None, nb_of_mitre_actors],'visible': True}, 
                'steps' : [
                 {'range': [0, nb_of_mitre_actors/2], 'color': "lightgray"},
                 {'range': [nb_of_mitre_actors/2, nb_of_mitre_actors*3/4], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': nb_of_mitre_actors-1}},
        title= {'text': "Nb of threat actors"},
        domain = {'row': 0, 'column': 0}))
    # draw gauge 0,1 number of tech 
    fig.add_trace(go.Indicator(
        value = nb_of_techniques,
        mode = "gauge+number",
        gauge = {'axis': {'range': [None, nb_of_mitre_techniques],'visible': True}, 
                'steps' : [
                 {'range': [0, nb_of_mitre_techniques/2], 'color': "lightgray"},
                 {'range': [nb_of_mitre_techniques/2, nb_of_mitre_techniques*3/4], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': nb_of_mitre_techniques-1}},
        title= {'text': "Nb of used techniques"},
        domain = {'row': 0, 'column': 1}))
    # number of most used tech 
    fig.add_trace(go.Indicator(
        value = nb_most_used_tech,
        mode = "number+delta",
        title= {'text': "Most used techniques<br><span style='font-size:0.8em;color:gray'>Used by more than 30% of actors</span>"},
        gauge = {'shape': "bullet",'axis' : {'range': [None, nb_of_techniques],'visible': False}},
        delta = {'reference': nb_of_techniques, 'relative': True},
        #domain = {'row': 1, 'column': 1}))
        domain = {'x': [0.55, 1], 'y': [0, 0.3]}))

    # number of tech used once
    '''fig.add_trace(go.Indicator(
        value = 30,
        delta = {'reference': 150},
        gauge = {
            'shape': "bullet",
            'axis' : {'visible': False}},
        domain = {'x': [0.6, 1], 'y': [0.15, 0.35]}))'''
    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"})
    fig.write_image(image_file)
    #fig.show()

if __name__ == '__main__':
    image_file = 'key_indicators.png' 
    nb_of_mitre_actors = 125
    nb_of_mitre_techniques = 450
    nb_of_actors = 15
    nb_of_techniques = 120
    nb_most_used_tech = 30
    draw_indicator(nb_of_mitre_actors, nb_of_mitre_techniques, nb_of_actors, nb_of_techniques, nb_most_used_tech, image_file)