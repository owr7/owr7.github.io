import io
import time
from matplotlib.backends.backend_agg import FigureCanvasAgg
from Clean_Corona import *
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUIWeb as sg
import matplotlib

matplotlib.use('TkAgg')

results_names = {
    1: "Ills Graph (per day)",
    2: "Teish Graph (cumulative)",
    3: "Recovery Graph (cumulative)",
    4: "Ills from abroad",
    5: "R coeff",
    6: "Policy (0: Open, 1: Mask & Distance, 2: Partial closure 3: Closure)",
}


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}
    if type(agent) == PoliceAgent:
        portrayal['Color'] = '#0000FF'
        portrayal['Layer'] = 0
    elif not agent.active:
        portrayal['Color'] = '#FFFFFF'
        portrayal['Layer'] = 1
    elif agent.health == HealthStatus.HEALTHY:
        portrayal['Color'] = '#00FF00'
        portrayal['Layer'] = 0
    elif agent.health == HealthStatus.ILL:
        portrayal['Color'] = '#FF0000'
        portrayal['Layer'] = 2
    elif agent.health == HealthStatus.TEISH:
        portrayal['Color'] = '#000000'
        portrayal['Layer'] = 3
    elif agent.health == HealthStatus.RECOVERING:
        portrayal['Color'] = '#ABCDEF'
        portrayal['Layer'] = 4

    return portrayal


def run_avg_sim(model: CoronaModel, num_of_simulations: int, during_of_simulation: int, data_avg):
    ills_per_day = data_avg[0]
    teish_per_day = data_avg[1]
    recovery_per_day = data_avg[2]
    abroud_ills_per_day = data_avg[3]
    R_per_day = data_avg[4]
    policy_per_day = data_avg[5]
    start_hour = time.time()
    finish_at = time.localtime(start_hour + num_of_simulations * during_of_simulation)

    avg_time_for_step = 0
    for i in range(during_of_simulation):
        start = time.time()
        model.step()
        ills_per_day[i] += count_ills(model) / num_of_simulations
        teish_per_day[i] += count_teish(model) / num_of_simulations
        recovery_per_day[i] += count_recovering(model) / num_of_simulations
        abroud_ills_per_day[i] += count_from_outside_ills(model) / num_of_simulations
        R_per_day[i] += model.get_current_R() / num_of_simulations
        policy_per_day[i] += model.get_current_policy() / num_of_simulations
        avg_time_for_step = avg_time_for_step * i / (i + 1) + (time.time() - start) * 1 / (i + 1)
        finish_at = time.localtime(start_hour + num_of_simulations * during_of_simulation * avg_time_for_step)
        sg.Window("Corona Simulation", [[sg.Text('Finish Time:' + str(finish_at.tm_hour)
                                                 + ':' + str(finish_at.tm_min) + ':' +
                                                 str(finish_at.tm_sec))]]).show()


def draw_figure(canvas, figure):
    plt.close('all')  # erases previously drawn plots
    canv = FigureCanvasAgg(figure)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is None:
        return None
    buf.seek(0)
    canvas.update(data=buf.read())
    return canv
    

def show_avg_graphs(figs):
    layout = [[sg.Text('Results of average simulation', text_color='black')],
              [sg.Column([[sg.Text(figs[0][0])],
                          [sg.Image(key='CANVAS_1')],
                          [sg.Text(figs[1][0])],
                          [sg.Image(key='CANVAS_2')],
                          [sg.Text(figs[2][0])],
                          [sg.Image(key='CANVAS_3')], ])],
              [sg.Column([[sg.Text(figs[3][0])],
                          [sg.Image(key='CANVAS_4')],
                          [sg.Text(figs[4][0])],
                          [sg.Image(key='CANVAS_5')],
                          [sg.Text(figs[5][0])],
                          [sg.Image(key='CANVAS_6')], ])],
              [sg.Button('OK')]]

    # create the form and show it without the plot
    window = sg.Window('Results of average simulation', layout, finalize=True,
                       element_justification='center', font='Helvetica 18', )

    # add the plot to the window
    for i, fig in enumerate(figs):
        fig_canvas_agg = draw_figure(window['CANVAS_' + str(i + 1)], fig[1])
    event, values = window.read()

    window.close()


def run_sim(num_of_agents: int, width: int, height: int, infRate=None, mask_coeff=None, government_policy_coeff=None,
            R_mean=7, enforcement_level=0.01, disease_importing=0.5, show_online_data=None, avg_sim=False,
            num_sim=1, during_sim=30, immunity=0.99, economic_status=None, rateTurnover=0.005):
    if economic_status is None:
        economic_status = [1.1, 1, 0.9, 0.95]
    if avg_sim:
        data_avg = [np.zeros(during_sim) for i in range(6)]
        for i in range(num_sim):
            model = CoronaModel(N=num_of_agents, width=width, height=height, infRate=infRate, mask_coeff=mask_coeff,
                                government_policy_coeff=government_policy_coeff, R_mean=R_mean,
                                enforcement_level=enforcement_level, disease_importing=disease_importing,
                                immunity=immunity, economic_status=economic_status, agent_turnover_rate=rateTurnover)
            run_avg_sim(model, num_sim, during_sim, data_avg)
        figs = []
        for j, k in enumerate(data_avg):
            fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
            fig.add_subplot(111).plot(list(range(during_sim)), k)
            figs.append((results_names[j + 1], fig))
        show_avg_graphs(figs)
        return

    grid = CanvasGrid(agent_portrayal, height, width, 400, 400)

    charts = [ChartModule([{"Label": "Ills",
                            "Color": "red"}],
                          data_collector_name='datacollector_1'),

              ChartModule([{"Label": "Teish",
                            "Color": "Balck"}],
                          data_collector_name='datacollector_2'),

              ChartModule([{"Label": "RECOVERING",
                            "Color": "Blue"}],
                          data_collector_name='datacollector_3'),

              ChartModule([{"Label": "R",
                            "Color": "green"}],
                          data_collector_name='datacollector_5'),

              ChartModule([{"Label": "Ills_from_outside",
                            "Color": "yellow"}],
                          data_collector_name='datacollector_4'),

              ChartModule([{"Label": "Policy",
                            "Color": "orange"}],
                          data_collector_name='datacollector_6'),

              ChartModule([{"Label": "Economic_status",
                            "Color": "purple"}],
                          data_collector_name='datacollector_7')
              ]

    chart_list = [grid] + [chart for chart, cbox in zip(charts, show_online_data) if cbox == 1]

    server = ModularServer(CoronaModel,
                           chart_list,
                           "Corona Model",
                           {"N": num_of_agents, "width": width, "height": height,
                            'infRate': infRate, 'mask_coeff': mask_coeff,
                            'government_policy_coeff': government_policy_coeff,
                            'R_mean': R_mean,
                            'enforcement_level': enforcement_level,
                            'disease_importing': disease_importing, 'immunity': immunity,
                            'economic_status': economic_status, 'agent_turnover_rate': rateTurnover})

    server.port = 8521  # The default
    server.launch()
