import PySimpleGUI as sg
import requests
import os.path
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import platform

#####################################
########### - Classes - #############
#************************************

class FileHandler:

    def __init__(self) -> None:
        path = './favorites.csv'
        check_file = os.path.isfile(path)

        if check_file:
            pass
        else:
            open('favorites.csv', 'w').close()

    def get_favorites(self):   

        with open('favorites.csv') as favorites_file:

            new_list = []
            for fav in favorites_file:
                fav = fav.strip()
                fav = fav.upper()
                new_list.append(fav)
            favorites_file.close()
        
        new_list.sort()
        
        return new_list

        #Adds new location in the favorites file
    def add_favorites(self, location: str):

        with open('favorites.csv', 'a') as favorites_file:
            favorites_file.write(location + "\n")
        favorites_file.close()

        #Removes selected favorite by overwriting original file without chosen location
    def remove_favorite(self, location):

            new_list = [item for item in self.get_favorites() if item != location.upper()]

            with open('favorites.csv', 'w') as favorites_file:

                for item in new_list:
                    favorites_file.write(item + '\n')
            
            favorites_file.close()

class Weather:

    def __init__(self) -> None:
        self.message = ""

    def get_taf(self, location: str):

        response = requests.get(f"https://api-redemet.decea.mil.br/mensagens/taf/{location}?api_key=sJgea8VlPUfxZDd2pH1p3DDw2Vyog6cMNDfres44")
        data = response.json()

        try:
            print(data['data']['data'][0]['mens'])
            self.message += f"{data['data']['data'][0]['mens']}\n{100*'_'}"
        except:
            self.message += f"No TAF for this location\n{100*'_'}"

        

    #Fetches current weather based on specific location
    def get_metar(self, location: str):

        response = requests.get(f"https://api-redemet.decea.mil.br/mensagens/metar/{location}?api_key=sJgea8VlPUfxZDd2pH1p3DDw2Vyog6cMNDfres44")

        data = response.json()

        try:
            print(data['data']['data'][0]['mens'])
            self.message += f"{data['data']['data'][0]['mens']}\n\n"
        except:
            self.message += 'No METAR for this location\n'


    def return_message(self):
        return self.message
    
    def clear_message(self):
        self.message = ""

class Variables:

    def __init__(self) -> None:
        self.cj3_wing_tank_moments = {
            '100': 323.47, '2500': 7771.75,
            '200': 642.06, '2600': 8079.76,
            '300': 958.44, '2700': 8388.09,
            '400': 1273.08, '2800': 8696.24,
            '500': 1586.45, '2900': 9005.37,
            '600': 1898.76, '3000': 9314.40,
            '700': 2210.11, '3100': 9624.26,
            '800': 2520.64, '3200': 9934.08,
            '900': 2830.77, '3300': 10244.52,
            '1000': 3140.40, '3400': 10554.62,
            '1100': 3449.71, '3500': 10864.70,
            '1200': 3759.36, '3600': 11175.12,
            '1300': 4068.74, '3700': 11485.17,
            '1400': 4378.08, '3800': 11795.58,
            '1500': 4687.35, '3900': 12105.60,
            '1600': 4996.32, '4000': 12415.60,
            '1700': 5305.36, '4100': 12725.17,
            '1800': 5614.02, '4200': 13035.12,
            '1900': 5922.87, '4300': 13344.62,
            '2000': 6231.40, '4400': 13654.08,
            '2100': 6539.82, '4500': 13963.50,
            '2200': 6847.94, '4600': 14272.88,
            '2300': 7155.99, '4700': 14581.75,
            '2400': 7463.76, '4710': 14612.81
        }

        self.cg_plots = []

    def get_wing_moments(self):
        return self.cj3_wing_tank_moments

    def add_plots(self, plot: tuple):
        self.cg_plots.append(plot)

    def get_plots(self):
        return self.cg_plots
    
    def erase_plots(self):
        self.cg_plots.clear()

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
 

class EnvelopeChart:

    def __init__(self) -> None:
        pass

    def zfw_limit(self):
        zfuelx = np.array([10510, 10510])
        zfuley = np.array([294.75, 303.59])
        plt.plot(zfuley, zfuelx, ':', label = 'Max zero fuel weight')

    def tkof_limit(self):
        tkofx = np.array([13870, 13870])
        tkofy = np.array([298.42, 304.71])
        plt.plot(tkofy, tkofx, ':', label = 'Max takeoff weight')

    def land_limit(self):
        landx = np.array([12750, 12750])
        landy = np.array([297.20, 304.6])
        plt.plot(landy, landx, ':', label = 'Max landing weight')

    def generate_chart(self, plots: list):

        plt.title("Citation CJ3 - Envelope Chart")
        plt.xlabel("Center of gravity (Inches)")
        plt.ylabel("Weight (Pounds)")
        self.zfw_limit()
        self.tkof_limit()
        self.land_limit()

        xpoints = np.array([9000,   9700,   14070,  14070,   13000,  8000,    8000,    9000])
        ypoints = np.array([293.86, 293.86, 298.64, 304.71 , 304.71, 302.46 , 298.72 , 293.86])

        for plot in plots:
            cgx = np.array([plot[1]])
            cgy = np.array([plot[2]])
            plt.plot(cgy, cgx, plot[3], label = plot[0])

        plt.plot(ypoints, xpoints, 'b--', linewidth = '2.0', label='CG limits')
        plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
        plt.legend()
        plt.show()

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

class WeightAndBalance:

    def __init__(self, window, variable: Variables) -> None:
        self.window = window
        self.variable = variable

    def calc_acft_load(self, values):
        sum_weight = 0
        for i in range(1,17):
            sum_weight += float(values[f"column{i}"])
        self.window['total1'].update(sum_weight)
        self.window['payload_weight'].update(sum_weight)
        find_moment = 0
        moment_total = 0
        for i in range(1,17):
            find_moment = (float(values[f"arm{i}"]) * float(values[f"column{i}"]))/100
            moment_total += find_moment
            self.window[f"column2{i}"].update(find_moment)
        moment_total = round(moment_total, 2)
        self.window['total2'].update(moment_total)
        self.window['payload_moment'].update(moment_total)
        zerof_weight = float(values['empty_weight']) + sum_weight
        zerof_moment = float(values['empty_moment']) + moment_total
        zerof_cg = round(zerof_moment/zerof_weight*100, 1)
        if len(self.variable.get_plots()) == 0:
            self.variable.add_plots(('ZFW CG', zerof_weight, zerof_cg, 'o'))
        else:
            self.variable.erase_plots()
            self.variable.add_plots(('ZFW CG', zerof_weight, zerof_cg, 'o'))
        self.window['zerof_weight'].update(zerof_weight)
        self.window['zerof_moment'].update(zerof_moment)
        self.window['cg1'].update(f"ZFW center of gravity: {zerof_cg}")
        if zerof_weight > 10510:
            sg.popup('Max. zero fuel weight is 10510 lbs')
            self.window['zerof_weight'].update(background_color='red')
        else:
            self.window['zerof_weight'].update(background_color='#d4d4ce')

    def compute_weight(self, values):

        if values['payload_weight'] == '':
                sg.popup('Please calculate payload first')
        elif values['fuel_weight'] == '' and values['fuel_to_destination'] == '':
            sg.popup("Please type in 'total fuel' and 'fuel to destination'")
        elif values['fuel_weight'] == '':
                sg.popup("Please type in 'total fuel'")
        elif values['fuel_to_destination'] == '':
            sg.popup("Please type in 'fuel to destination'")
        elif int(values['fuel_weight']) > 4710:
            sg.popup("Max. fuel total 4710 lbs")
        else:
            #calculate zero fuel weight
            fuel_weight = int(values['fuel_weight'])
            if fuel_weight == 4710:
                fuel_weight = 4700
                print(fuel_weight)
            for fuel in self.variable.get_wing_moments():
                if fuel == str(fuel_weight):
                    self.window['fuel_weight_upd'].update(fuel_weight)
                    fuel_moment = self.variable.get_wing_moments()[fuel]
                    self.window['fuel_moment'].update(fuel_moment)
                    ramp_weight = round(fuel_weight + float(values['zerof_weight']), 2)
                    ramp_moment = round(float(values['zerof_moment']) + self.variable.get_wing_moments()[fuel], 2)
                    ramp_cg = round(ramp_moment/ramp_weight*100,1)
                    self.variable.add_plots(('Ramp CG', ramp_weight, ramp_cg,'go'))
                    self.window['ramp_weight'].update(ramp_weight)
                    self.window['ramp_moment'].update(ramp_moment)
                    self.window['cg2'].update(f"Ramp center of gravity: {ramp_cg}")
                    if ramp_weight > 14070:
                        sg.popup('Max. ramp weight is 14070 lbs')
                        self.window['ramp_weight'].update(background_color='red')
                    else:
                        self.window['ramp_weight'].update(background_color='#d4d4ce')
            
            taxi_moment = round(self.variable.get_wing_moments()[str(fuel_weight)] - self.variable.get_wing_moments()[str(fuel_weight - int(values['less_taxi_weight']))], 2)
            self.window['less_taxi_moment'].update(taxi_moment)
            tkof_weight = round(ramp_weight - int(values['less_taxi_weight']))
            tkof_moment = round(ramp_moment - taxi_moment)
            tkof_cg = round(tkof_moment/tkof_weight*100,1)
            self.variable.add_plots(('Takeoff CG', tkof_weight, tkof_cg,'bo'))
            self.window['tkof_weight'].update(tkof_weight)
            self.window['tkof_moment'].update(tkof_moment)
            self.window['cg3'].update(f"Takeoff center of gravity: {tkof_cg}")
            if tkof_weight > 13870:
                sg.popup('Max. takeoff weight is 13870 lbs')
                self.window['tkof_weight'].update(background_color='red')
            else:
                self.window['tkof_weight'].update(background_color='#d4d4ce')
            land_weight = round(tkof_weight - int(values['fuel_to_destination']))
            land_moment = round(tkof_moment - (self.variable.get_wing_moments()[str(fuel_weight)] - self.variable.get_wing_moments()[str(fuel_weight - int(values['fuel_to_destination']))]))
            land_cg = round(land_moment/land_weight*100,1)
            self.variable.add_plots(('Landing CG', land_weight, land_cg,'ro'))
            self.window['land_weight'].update(land_weight)
            self.window['land_moment'].update(land_moment)
            self.window['cg4'].update(f"Landing center of gravity: {land_cg}")
            if land_weight > 12510:
                sg.popup('Max. landing weight is 12510 lbs')
                self.window['land_weight'].update(background_color='red')
            else:
                self.window['land_weight'].update(background_color='#d4d4ce')

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