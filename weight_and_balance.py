import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from global_variables import Variables

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

class WeightAndBalance:

    def __init__(self, window, variable: Variables) -> None:
        self.window = window
        self.variable = variable

    def calc_acft_load(self, values):
        sum_weight = 0
        try:
            for i in range(1,17):
                sum_weight += float(values[f"column{i}"])
        except:
            sg.popup('Check values/numbers and try again')
            return
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

        try:
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
        except:
            sg.popup('Check values/numbers and try again')
