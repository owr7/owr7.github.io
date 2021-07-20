import PySimpleGUIWeb as sg
from ABM_viz import run_sim

default_dict = {
    "-numOfAgents-": 100,
    "-width-": 30,
    "-Height-": 30,
    "importDisease": 0.5,
    "noMaskInfection": 0.8,
    "oneMaskInfectionI": 0.25,
    "bothMaskInfection": 0.1,
    "wearMaskAgeW": 1,
    "wearMaskHealthW": 0,
    "wearMaskSocioecoW": 0,
    "wearMaskPolicyW": 0,
    "wearMaskPoliceW": 0,
    "wearMaskSocialInfW": 0,
    "wearMaskCrowdingW": 0,
    "numIllsW": 1,
    "RcoeffW": 0,
    "economicStatusW": 0,
    "EnforcementLevel": 0.05,
    "Rmean": 7,
    "numberOfSim": 10,
    "duringOfSim": 30,
    "immunity": 0.99,
}

global_parameters = [[
    sg.Text("Global parameters", text_color='black', size=(500, 20))],
    [
        sg.Text("Number of agents:"),
        sg.In(size=(10, 1), enable_events=True, key="-numOfAgents-", default_text=default_dict['-numOfAgents-'])],
    [
        sg.Text("Width:"),
        sg.In(size=(10, 1), enable_events=True, key="-width-", default_text=default_dict['-width-'])],
    [
        sg.Text("Height:"),
        sg.In(size=(10, 1), enable_events=True, key="-Height-", default_text=default_dict['-Height-'])],
    [
        sg.Text("Disease import percentages:"),
        sg.In(size=(10, 1), enable_events=True, key="importDisease", default_text=default_dict['importDisease'])],
    [
        sg.Text("Time units to take for calculate mean R coefficient:"),
        sg.In(size=(10, 1), enable_events=True, key="Rmean", default_text=default_dict['Rmean'])],
    [
        sg.Text("Enforcement level (How much cops per one civilian agent:"),
        sg.In(size=(10, 1), enable_events=True, key="EnforcementLevel", default_text=default_dict['EnforcementLevel'])],
]

probability_of_influence = [
    [sg.Text("Probability of influence", text_color='black', size=(500, 20))],
    [
        sg.Text("Chances of infection without masks:"),
        sg.In(size=(10, 1), enable_events=True, key="noMaskInfection", default_text=default_dict['noMaskInfection'])
    ],
    [
        sg.Text("Chances of infection with one mask:"),
        sg.In(size=(10, 1), enable_events=True, key="oneMaskInfectionI", default_text=default_dict['oneMaskInfectionI'])
    ],
    [
        sg.Text("Chances of infection with one mask on both:"),
        sg.In(size=(10, 1), enable_events=True, key="bothMaskInfection", default_text=default_dict['bothMaskInfection'])
    ],
    [
        sg.Text("Exponential reducing factor of immunity to disease of recovered agents:"),
        sg.In(size=(10, 1), enable_events=True, key="immunity", default_text=default_dict['immunity'])
    ]
]

probability_of_wearing_mask = [
    [sg.Text("Level of discipline", text_color='black')],
    [sg.Text("In the simple mode we use logistic distribution for transport from linear\ncombitaion of "
             "parameters to probability value [0,1]\n"
             "Write weights(Not necessarily normalized) for the following parameters:", size=(500, 100))],
    [
        sg.Text("Age:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskAgeW", default_text=default_dict['wearMaskAgeW'])
    ],
    [
        sg.Text("Health status:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskHealthW", default_text=default_dict['wearMaskHealthW'])
    ],
    [
        sg.Text("Socioeconomic:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskSocioecoW", default_text=default_dict['wearMaskSocioecoW'])
    ],
    [
        sg.Text("Government policy:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskPolicyW", default_text=default_dict['wearMaskPolicyW'])
    ],
    [
        sg.Text("Presence of police:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskPoliceW", default_text=default_dict['wearMaskPoliceW'])
    ],
    [
        sg.Text("Social influence:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskSocialInfW", default_text=default_dict['wearMaskSocialInfW'])
    ],
    [
        sg.Text("Crowding:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskCrowdingW", default_text=default_dict['wearMaskCrowdingW'])
    ]
]

government_policy = [
    [sg.Text("Government Policy", text_color='black')],
    [sg.Text("In the simple mode we use logistic distribution for transport from linear combitaion of\n "
             "parameters to probability value [0,1]\n"
             "Empty parameter will not consider\n"
             "Write weights(Not necessarily normalized) for the following parameters:", size=(500, 100))],
    [
        sg.Text("Number of ills:"),
        sg.In(size=(10, 1), enable_events=True, key="numIllsW", default_text=default_dict['numIllsW'])
    ],
    [
        sg.Text("R coeff."),
        sg.In(size=(10, 1), enable_events=True, key="RcoeffW", default_text=default_dict['RcoeffW'])
    ],
    [
        sg.Text("Economic status:"),
        sg.In(size=(10, 1), enable_events=True, key="economicStatusW", default_text=default_dict['economicStatusW'])
    ],

]

which_data_to_show = [
    [sg.Text('Choose the online data you want to watch')],
    [
        sg.Checkbox("Number Of Ill", key='numOfIllsCB', default=True)],
    [sg.Checkbox("Number Of Teish", key='numOfTeishCB', default=True)],
    [sg.Checkbox("Number Of Recovery", key='numOfRecoveryCB', default=True)],
    [sg.Checkbox("R Coeff.", key='RmeanCB', default=True)],
    [sg.Checkbox("Ills come from abroad", key='numOfIllsAbroudCB', default=True)],
    [sg.Checkbox("Current Government policy", key='policyCB', default=True),
     ],
]

send_button = [[sg.Button(button_text='Start Simulation', key='-SUBMIT-')]]

run_avg_simulation = [[sg.Text('No visual version', text_color='balck')],
                      [sg.Text(
                          'If you want to get result of average of some simulation,\nplease provide the next,'
                          '\nand press the button below', size=(500, 50))],
                      [sg.Text('Number of simulations:'),
                       sg.In(size=(10, 1), enable_events=True, key="numberOfSim", default_text=default_dict['numberOfSim'])],
                      [sg.Text('During of each simulation:'),
                       sg.In(size=(10, 1), enable_events=True, key="duringOfSim", default_text=default_dict['duringOfSim'])],
                      [sg.Button(button_text='Take Average on Simulations', key='-SUBMIT_AVG-')]]

layout = [[sg.Column(global_parameters + probability_of_influence + probability_of_wearing_mask),
           sg.Column(government_policy + which_data_to_show + send_button + run_avg_simulation)]]

window = sg.Window("Corona Simulation", layout)


def input_check():
    for value in values:
        if values[value] == '':
            values[value] = default_dict[value]


while True:
    event, values = window.read()
    if event == '-SUBMIT-' or event == '-SUBMIT_AVG-':
        input_check()

        infRate = [float(values['bothMaskInfection']), float(values['oneMaskInfectionI']),
                   float(values['oneMaskInfectionI']), float(values['noMaskInfection'])]

        mask_coeff = [float(values['wearMaskAgeW']), float(values['wearMaskHealthW']),
                      float(values['wearMaskSocioecoW']), float(values['wearMaskPolicyW']),
                      float(values['wearMaskPoliceW']), float(values['wearMaskSocialInfW']),
                      float(values['wearMaskCrowdingW'])]

        government_policy_coeff = [float(values['numIllsW']), float(values['RcoeffW']),
                                   float(values['economicStatusW'])]

        show_online_data = [float(values['numOfIllsCB']), float(values['numOfTeishCB']),
                            float(values['numOfRecoveryCB']), float(values['RmeanCB']),
                            float(values['numOfIllsAbroudCB']), float(values['policyCB'])]

        run_sim(int(values['-numOfAgents-']), int(values['-width-']), int(values['-Height-']), infRate=infRate,
                mask_coeff=mask_coeff, government_policy_coeff=government_policy_coeff, R_mean=int(values['Rmean']),
                enforcement_level=float(values['EnforcementLevel']), disease_importing=float(values['importDisease']),
                show_online_data=show_online_data, avg_sim=(event == '-SUBMIT_AVG-'),
                num_sim=int(values['numberOfSim']),
                during_sim=int(values['duringOfSim']), immunity=values['immunity'])
        break
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
