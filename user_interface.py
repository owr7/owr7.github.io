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
    # "recoverChanceCoeffA": 1,
    # "recoverChanceCoeffB": 1,
    "EnforcementLevel": 0.05,
    "Rmean": 7,
    "numberOfSim": 10,
    "duringOfSim": 10,
}


global_parameters = [[
    sg.Text("Global parameters", text_color='black', size=(500, 20))],
    [
        sg.Text("Number of agents:"),
        sg.In(size=(10, 1), enable_events=True, key="-numOfAgents-")],
    [
        sg.Text("Width:"),
        sg.In(size=(10, 1), enable_events=True, key="-width-")],
    [
        sg.Text("Height:"),
        sg.In(size=(10, 1), enable_events=True, key="-Height-")],
    [
        sg.Text("Disease import percentages:"),
        sg.In(size=(10, 1), enable_events=True, key="importDisease")],
    [
        sg.Text("Time units to take for calculate mean R coefficient:"),
        sg.In(size=(10, 1), enable_events=True, key="Rmean")],
    [
        sg.Text("Enforcement level (How much cops per one civilian agent:"),
        sg.In(size=(10, 1), enable_events=True, key="EnforcementLevel")],
]

probability_of_influence = [
    [sg.Text("Probability of influence", text_color='black', size=(500, 20))],
    [
        sg.Text("Chances of infection without masks:"),
        sg.In(size=(10, 1), enable_events=True, key="noMaskInfection")
    ],
    [
        sg.Text("Chances of infection with one mask:"),
        sg.In(size=(10, 1), enable_events=True, key="oneMaskInfectionI")
    ],
    [
        sg.Text("Chances of infection with one mask on both:"),
        sg.In(size=(10, 1), enable_events=True, key="bothMaskInfection")
    ]
]

probability_of_wearing_mask = [
    [sg.Text("Level of discipline", text_color='black')],
    [sg.Text("In the simple mode we use logistic distribution for transport from linear\ncombitaion of "
             "parameters to probability value [0,1]\n"
             "Write weights(Not necessarily normalized) for the following parameters:", size=(500, 100))],
    [
        sg.Text("Age:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskAgeW")
    ],
    [
        sg.Text("Health status:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskHealthW")
    ],
    [
        sg.Text("Socioeconomic:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskSocioecoW")
    ],
    [
        sg.Text("Government policy:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskPolicyW")
    ],
    [
        sg.Text("Presence of police:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskPoliceW")
    ],
    [
        sg.Text("Social influence:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskSocialInfW")
    ],
    [
        sg.Text("Crowding:"),
        sg.In(size=(10, 1), enable_events=True, key="wearMaskCrowdingW")
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
        sg.In(size=(10, 1), enable_events=True, key="numIllsW")
    ],
    [
        sg.Text("R coeff. as average of 7 times units"),
        sg.In(size=(10, 1), enable_events=True, key="RcoeffW")
    ],
    [
        sg.Text("Economic status:"),
        sg.In(size=(10, 1), enable_events=True, key="economicStatusW")
    ],

]
#
# dealing_with_the_disease = [
#     [sg.Text("Dealing with the disease", text_color='black', font='a')],
#     [sg.Text("After examining data from Israel and the United States,\n"
#              "we identified that there is an exponential dependence between the chances of recovery and age.\n"
#              "Therefore we assume P(Recovering)=a*exp(b*Age)\n"
#              "Please enter your coefficients\n"
#              "(The complement to 1 is the chance to not survived the illness)")],
#     [
#         sg.Text("a:"),
#         sg.In(size=(25, 1), enable_events=True, key="recoverChanceCoeffA")
#     ],
#     [
#         sg.Text("b:"),
#         sg.In(size=(25, 1), enable_events=True, key="recoverChanceCoeffB")
#     ],
# ]

which_data_to_show = [
    [sg.Text('Choose the online data you want to watch')],
    [
        sg.Checkbox("Number Of Ill", key='numOfIllsCB')],
    [sg.Checkbox("Number Of Teish", key='numOfTeishCB')],
    [sg.Checkbox("Number Of Recovery", key='numOfRecoveryCB')],
    [sg.Checkbox("R Coeff.", key='RmeanCB')],
    [sg.Checkbox("Ills come from abroad", key='numOfIllsAbroudCB')],
    [sg.Checkbox("Current Government policy", key='policyCB'),
     ],
]

send_button = [[sg.Button(button_text='Start Simulation', key='-SUBMIT-')]]

run_avg_simulation = [[sg.Text('No visual version', text_color='balck')],
                      [sg.Text(
                          'If you want to get result of average of some simulation,\nplease provide the next,'
                          '\nand press the button below', size=(200, 20))],
                      [sg.Text('Number of simulations:'),
                       sg.In(size=(10, 1), enable_events=True, key="numberOfSim")],
                      [sg.Text('During of each simulation:'),
                       sg.In(size=(10, 1), enable_events=True, key="duringOfSim")],
                      [sg.Button(button_text='Take Average on Simulations', key='-SUBMIT_AVG-')]]
# layout = [[sg.Column(global_parameters + probability_of_influence + probability_of_wearing_mask +
#                      government_policy + which_data_to_show + send_button)]]

layout = [[sg.Column(global_parameters + probability_of_influence + probability_of_wearing_mask),
           sg.Column(government_policy + which_data_to_show + send_button + run_avg_simulation)]]
# + dealing_with_the_disease
window = sg.Window("Corona Simulation", layout)


def input_check():
    for value in values:
        if values[value] == '':
            values[value] = default_dict[value]


while True:
    event, values = window.read()
    if event == '-SUBMIT-' or event == '-SUBMIT_AVG-':
        print('Hello World')
        input_check()

        infRate = [float(values['noMaskInfection']), float(values['oneMaskInfectionI']),
                   float(values['oneMaskInfectionI']), float(values['bothMaskInfection'])]

        mask_coeff = [float(values['wearMaskAgeW']), float(values['wearMaskHealthW']),
                      float(values['wearMaskSocioecoW']), float(values['wearMaskPolicyW']),
                      float(values['wearMaskPoliceW']), float(values['wearMaskSocialInfW']),
                      float(values['wearMaskCrowdingW'])]

        government_policy_coeff = [float(values['numIllsW']), float(values['RcoeffW']),
                                   float(values['economicStatusW'])]

        show_online_data = [float(values['numOfIllsCB']), float(values['numOfTeishCB']),
                            float(values['numOfRecoveryCB']), float(values['RmeanCB']),
                            float(values['numOfIllsAbroudCB']), float(values['policyCB'])]

        # deal_with_it = [float(values['recoverChanceCoeffA']), float(values['recoverChanceCoeffB'])]

        run_sim(int(values['-numOfAgents-']), int(values['-width-']), int(values['-Height-']), infRate=infRate,
                mask_coeff=mask_coeff, government_policy_coeff=government_policy_coeff, R_mean=int(values['Rmean']),
                enforcement_level=float(values['EnforcementLevel']), disease_importing=float(values['importDisease']),
                show_online_data=show_online_data, avg_sim=(event == '-SUBMIT_AVG-'), num_sim=int(values['numberOfSim']),
                during_sim=int(values['duringOfSim']))
        break
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
