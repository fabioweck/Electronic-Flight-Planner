import PySimpleGUI as sg
from file_handler import FileHandler
from weather import Weather
from global_variables import Variables
from weight_and_balance import EnvelopeChart, WeightAndBalance
import ctypes
import platform

#####################################
########### - Classes - #############
#************************************

class Environment:

    def __init__(self) -> None:  
        sg.LOOK_AND_FEEL_TABLE['MyTheme'] = {'BACKGROUND': '#023246',
                                                'TEXT': '#ffffff',
                                                'INPUT': '#d4d4ce',
                                                'TEXT_INPUT': '#023246',
                                                'SCROLL': '#d4d4ce',
                                                'BUTTON': ('#ffffff', '#023246'),
                                                'PROGRESS': ('#D1826B', '#CC8019'),
                                                'BORDER': 2, 'SLIDER_DEPTH': 1, 
                                                'PROGRESS_DEPTH': 5, }
        sg.theme('MyTheme')
        self.make_dpi_aware()

    #Function to increase visual looking clearness/sharpness
    def make_dpi_aware(self):
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)


class Layouts:

    def __init__(self) -> None:
        self.favorites_file = FileHandler()

    def weather_tab(self):

        tab1_list_column = [
            [sg.Text('Favorites', size=(10,1))],
            [sg.Listbox(self.favorites_file.get_favorites(), size=(10, 10), key='favorites', right_click_menu=['', ['Delete']], enable_events=True)],
            [sg.In(key='add-favorite', size=(5,1)), sg.Button('ADD'), sg.Push()]
        ]

        tab1_display_column = [
            [sg.Push(), sg.Button('Search'), sg.In(key='search_metar', size=(6,1)), sg.Push()],
            [sg.Frame('Metar/TAF',[[sg.Multiline(size=(100,20), key='display-weather')], 
            [sg.Push(), sg.Button('Clear')]])]
        ]

        tab1_layout = [
            [sg.Column(tab1_list_column), sg.Column(tab1_display_column)], 
                    ]
        return tab1_layout
    
    
    def weight_and_balance_tab(self):

        tab2_calc1 = [
            [sg.Push(), sg.Text('AIRCRAFT LOADING'), sg.Push()],
            [sg.Text('Item', size=(4,0)), sg.Text('Arm'), sg.Text('Weight'), sg.Text('Moment')],
            [sg.Text('Pilot'),                         sg.In(size=(5,0), default_text=131.0, key='arm1'),  sg.In(size=(5,0), key='column1',  default_text=180),sg.In(size=(7,0), key='column21')],
            [sg.Text('Co-Pilot'),                      sg.In(size=(5,0), default_text=131.0, key='arm2'),  sg.In(size=(5,0), key='column2',  default_text=180),sg.In(size=(7,0), key='column22')],
            [sg.Text('Seat 10'),                       sg.In(size=(5,0), default_text=174.2, key='arm3'),  sg.In(size=(5,0), key='column3',  default_text=0),  sg.In(size=(7,0), key='column23')],
            [sg.Text('Seat 3'),                        sg.In(size=(5,0), default_text=202.5, key='arm4'),  sg.In(size=(5,0), key='column4',  default_text=0),  sg.In(size=(7,0), key='column24')],
            [sg.Text('Seat 4'),                        sg.In(size=(5,0), default_text=202.5, key='arm5'),  sg.In(size=(5,0), key='column5',  default_text=0),  sg.In(size=(7,0), key='column25')],
            [sg.Text('Seat 5'),                        sg.In(size=(5,0), default_text=260.5, key='arm6'),  sg.In(size=(5,0), key='column6',  default_text=0),  sg.In(size=(7,0), key='column26')],
            [sg.Text('Seat 6'),                        sg.In(size=(5,0), default_text=260.5, key='arm7'),  sg.In(size=(5,0), key='column7',  default_text=0),  sg.In(size=(7,0), key='column27')],
            [sg.Text('Seat 7'),                        sg.In(size=(5,0), default_text=295.5, key='arm8'),  sg.In(size=(5,0), key='column8',  default_text=0),  sg.In(size=(7,0), key='column28')],
            [sg.Text('Seat 8'),                        sg.In(size=(5,0), default_text=295.5, key='arm9'),  sg.In(size=(5,0), key='column9',  default_text=0),  sg.In(size=(7,0), key='column29')],
            [sg.Text('Seat 9 LH Belted Toilet'),       sg.In(size=(5,0), default_text=322.5, key='arm10'), sg.In(size=(5,0), key='column10', default_text=0),  sg.In(size=(7,0), key='column210')],
            [sg.Text('Nose baggage'),                  sg.In(size=(5,0), default_text=74.0, key='arm11'),  sg.In(size=(5,0), key='column11', default_text=10), sg.In(size=(7,0), key='column211')],
            [sg.Text('Charts'),                        sg.In(size=(5,0), default_text=150.9, key='arm12'), sg.In(size=(5,0), key='column12', default_text=5),  sg.In(size=(7,0), key='column212')],
            [sg.Text('LHF Evaporator Cabinet'),        sg.In(size=(5,0), default_text=156.3, key='arm13'), sg.In(size=(5,0), key='column13', default_text=5),  sg.In(size=(7,0), key='column213')],
            [sg.Text('RH Slimlime Refreshment Center'),sg.In(size=(5,0), default_text=157.2, key='arm14'), sg.In(size=(5,0), key='column14', default_text=15), sg.In(size=(7,0), key='column214')],
            [sg.Text('LH Aft Vanity'),                 sg.In(size=(5,0), default_text=334.9, key='arm15'), sg.In(size=(5,0), key='column15', default_text=15), sg.In(size=(7,0), key='column215')],
            [sg.Text('Tailcone Baggage'),              sg.In(size=(5,0), default_text=414.6, key='arm16'), sg.In(size=(5,0), key='column16', default_text=40), sg.In(size=(7,0), key='column216')],
            [sg.Push(), sg.Text('TOTAL', pad=(0)),sg.Text('Weight', key='total1', size=(6)), sg.Text('Moment', key='total2', size=(6))],
            [sg.Push(), sg.Button('Calculate', key="calc1"), sg.Push()]
            ]


        tab2_calc2 = [
            [sg.Push(), sg.Text('FUEL'), sg.Push()],
            [sg.Push(), sg.Text('Total fuel - 100 to 4710 lbs (in hundreds):'), sg.In(size=(6,0), key='fuel_weight')],
            [sg.Push(), sg.Text('Fuel to destination (in hundreds):'), sg.In(size=(6,0), key='fuel_to_destination')],
            [sg.Push(), sg.Button('Compute'), sg.Push()],
            [sg.Text()],
            [sg.Push(), sg.Text('ZERO FUEL/RAMP/TAKEOFF/LANDING'), sg.Push()],
            [sg.Text('Weight', size=(7,1)), sg.Text('Moment', size=(7,1))],
            [sg.Text('Basic Empty Weight'),       sg.In(size=(8,0), key='empty_weight', default_text=8305.98),sg.In(size=(9,0), key='empty_moment', default_text=25694.16)],
            [sg.Text('Payload'),                  sg.In(size=(8,0), key='payload_weight'), sg.In(size=(9,0), key='payload_moment')],
            [sg.Text('Zero Fuel Weight'),         sg.In(size=(8,0), key='zerof_weight'),   sg.In(size=(9,0), key='zerof_moment')],
            [sg.Text('ZFW center of gravity', key='cg1')],
            [sg.Text('Useable Fuel Quantity'),    sg.In(size=(8,0), key='fuel_weight_upd'),sg.In(size=(9,0), key='fuel_moment')],
            [sg.Text('Ramp Weight'),              sg.In(size=(8,0), key='ramp_weight'),    sg.In(size=(9,0), key='ramp_moment')],
            [sg.Text('Ramp center of gravity', key='cg2')],
            [sg.Text('Less Fuel for Taxiing (200 lbs)'), sg.In(size=(8,0), key='less_taxi_weight', default_text=200),sg.In(size=(9,0), key='less_taxi_moment')],
            [sg.Text('')],
            [sg.Text('Takeoff Weight'),           sg.In(size=(8,0), key='tkof_weight'),    sg.In(size=(9,0), key='tkof_moment')],
            [sg.Text('Takeoff center of gravity', key='cg3')],
            [sg.Text('Landing Weight'),           sg.In(size=(8,0), key='land_weight'),    sg.In(size=(9,0), key='land_moment')],
            [sg.Text('Landing center of gravity', key='cg4')],
            ]

        cj3_form = [
            [sg.Push(), sg.vtop(sg.Column(tab2_calc1, element_justification='r', key='cj3_sideA')), 
                sg.VerticalSeparator(), 
                sg.vtop(sg.Column(tab2_calc2, element_justification='r', key='cj3_sideB')), 
                sg.Push()]
            ] 

        tab2_layout = [
            [sg.Push(), sg.Radio('CITATION CJ3/525B (PRVNA) - WEIGHT AND BALANCE COMPUTATION FORM', font='Arial', group_id=1, key='cj3_button', enable_events=True), sg.Push()],
            [sg.Push(), sg.Text('Weight in pounds, Arm in inches, Moment = moment/100'), sg.Push()],
            [sg.Frame('Form', cj3_form, visible=False, key='cj3_form')],
            [sg.Push(), sg.Button('Generate CG envelope', key='cg_envelope'), sg.Push()]
            ]

        return tab2_layout
    
    
    def about_tab(self):

        tab3_layout = [
            [sg.Text("This application is a simple graphic user interface")]
            ]

        return tab3_layout
    
    def main_layout(self):

        layout = [
            [sg.TabGroup([
            [sg.Tab('Weather', self.weather_tab()), 
                sg.Tab('W/B', self.weight_and_balance_tab(), element_justification='c'),
                sg.Tab('About', self.about_tab(), element_justification='c')
                ]
            ])]
            ]
        
        return layout

######## - MAIN CLASS - ########
class Program:

    def __init__(self) -> None:
        self.favorites_file = FileHandler()
        self.layouts = Layouts()
        self.environment = Environment()
        self.weather = Weather()
        self.variable = Variables()
        self.envelope = EnvelopeChart()    
        self.window = sg.Window('Electronic Flight Planner - Fabio Weck', self.layouts.main_layout(), finalize=True)
        self.wb = WeightAndBalance(self.window, self.variable)

    def start(self):
        while True:    
            event, values = self.window.read()        
            if event == sg.WIN_CLOSED:             
                break
            if event == 'ADD':
                if len(values['add-favorite']) < 4:
                    sg.popup("4 letters required")
                else:
                    self.favorites_file.add_favorites(values['add-favorite'])
                    self.window['favorites'].update(self.favorites_file.get_favorites())
                    self.window['add-favorite'].update("")
            if event == 'Delete':
                if len(values['favorites']) == 0:
                    pass
                else:
                    self.favorites_file.remove_favorite(values['favorites'][0])
                    self.window['favorites'].update(self.favorites_file.get_favorites())
            if event == 'favorites':
                if len(values['favorites']) == 0:
                    pass
                else:
                    self.window['search_metar'].update(values['favorites'][0])
            if event == 'Search':
                if len(values['search_metar']) < 4:
                    sg.popup("Please type in a valid airpot ICAO code")
                else:
                    self.weather.get_metar(values['search_metar'])
                    self.weather.get_taf(values['search_metar'])
                    self.window['display-weather'].update(self.weather.return_message())
                    
            if event == 'Clear':
                self.window['display-weather'].update('')
                self.weather.clear_message()

            if event == 'calc1':
                self.wb.calc_acft_load(values)

            if event == 'Compute':
                self.wb.compute_weight(values)
            
            if event == 'cg_envelope':
                try:
                    self.envelope.generate_chart(self.variable.get_plots())
                    self.variable.erase_plots()
                except:
                    sg.popup('Please calculate current CG first')   

            if event == 'cj3_button':
                self.window['cj3_form'].update(visible=True)                
     
program = Program()
program.start()