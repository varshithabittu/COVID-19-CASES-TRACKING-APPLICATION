# importing modules

from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import requests
from tkinter import ttk


# storing the url in the form of string
root = Tk()
# setting geometry
root.geometry("700x400")
# setting title
root.title("Get Covid-19 Data Country Wise")
url = "https://api.covid19india.org/state_district_wise.json"
url1 = 'https://www.worldometers.info/coronavirus/'
# Create object page
page = requests.get(url1)
soup = BeautifulSoup(page.text, 'lxml')
table1 = soup.find('table', id='main_table_countries_today')
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)
headers[13] = 'Tests/1M pop'
mydata = pd.DataFrame(columns=headers)
for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row
# Drop and clearing unnecessary rows
mydata.drop(mydata.index[0:7], inplace=True)
mydata.drop(mydata.index[222:229], inplace=True)
mydata.reset_index(inplace=True, drop=True)
# Drop “#” column
mydata.drop('#', inplace=True, axis=1)
# Export to csv
mydata.to_csv('covid_data.csv', index=False)
# Try to read csv
mydata2 = pd.read_csv('covid_data.csv')


def case1():
    global case_1
    case_1 = Toplevel(root)
    case_1.title("India")
    case_1.geometry("612x408")
    bg1 = PhotoImage(file="istockphoto-1209432716-612x612.png")
    my_canvas = Canvas(case_1, width=612, height=408)
    my_canvas.pack()
    my_canvas.create_image(0, 0, image=bg1, anchor="nw")
    state = Label(my_canvas, text="Covid cases in India", fg="black", bg="LightBlue1")
    state.config(font='calibri 30')
    state.place(relx=0.22, rely=0.1)
    ulabel = Label(my_canvas, text="Enter State name:", bg="LightBlue1")
    ulabel.place(relx=0.4, rely=0.27)
    ulabel.config(font="calibri 12")
    user = Entry(my_canvas, bg='#d3d3d3', fg='black', textvariable=data)
    user.config(width=42)
    user.place(relx=0.3, rely=0.35)
    ttk.Button(my_canvas, text="Get Data Graphically", command=casesDataGraph).place(x=250, y=170)
    ttk.Button(my_canvas, text="Show Data", command=casesData).place(x=270, y=200)
    my_canvas.pack()
    my_canvas.mainloop()


def case2():
    case_2 = Toplevel(root)
    case_2.title("Internation")
    case_2.geometry("600x400")
    bg1 = PhotoImage(file="shutterstock_1647268288 (2).png")
    my_canvas1 = Canvas(case_2, width=600, height=400)
    my_canvas1.pack()
    my_canvas1.create_image(0, 0, image=bg1, anchor="nw")

    country = Label(my_canvas1, text="Covid-19 cases across the world", fg="black", bg="gold")
    country.config(font='calibri 20')
    country.place(relx=0.2, rely=0.15)
    ulabel = Label(my_canvas1, text="Enter Country name:", bg="gold")
    ulabel.config(font='calibri 12')
    ulabel.place(relx=0.39, rely=0.27)
    user = Entry(my_canvas1, bg='#d3d3d3', fg='black', textvariable=data1)
    user.config(width=42)
    user.place(relx=0.28, rely=0.35)
    ttk.Button(my_canvas1, text="Get Data Graphically", command=casesDataInternationGraph).place(x=230, y=180)
    ttk.Button(my_canvas1, text="Show Data", command=casesDataInternation).place(x=250, y=220)
    my_canvas1.pack()
    my_canvas1.mainloop()


def casesDataInternation():
    y = data1.get()
    lst = []
    flag = False
    for index, row in mydata2.iterrows():
        if row[0] == y:
            flag = True
            lst = row.tolist()
    if flag:
        newWindow = Toplevel(root)
        newWindow.title("Show Data")

        newWindow.geometry("400x400")
        login_canvas = Canvas(newWindow, width=720, height=440, bg="PeachPuff2")
        login_canvas.pack()
        login_frame = Frame(login_canvas, bg="LightBlue1")
        login_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        print(lst)
        lst2 = list(range(10))
        lst1 = [int(x.replace(',', '')) for x in lst[1:14] if str(x) != 'nan']
        Label(login_frame, text="TotalCases:  {0}\nTotalDeaths:   {1}\nTotalRecovered:  {2}\nActiveCases:  {3}\nSerious/Critical:  {4}\nTotCases/1M pop:  {5}\n Deaths/1M pop:  {6}\nTotalTests:  {7}\nTests/1Mpop:  {8}\nPopulation:  {9}\n".format(lst1[0], lst1[1], lst1[2], lst1[3], lst1[4], lst1[5], lst1[6], lst1[7], lst1[8], lst1[9]), font="TimesNewRoman 15", fg='black', bg='LightBlue1').pack(side=LEFT)


def casesDataInternationGraph():
    # getting the json data by calling api
    y = data1.get()
    lst = []
    flag = False
    for index, row in mydata2.iterrows():
        if row[0] == y:
            flag = True
            lst = row.tolist()
    if flag:
        lst2 = list(range(10))
        lst1 = [int(x.replace(',', '')) for x in lst[1:14] if str(x) != 'nan']
        tick_label = ['TotalCases', 'TotalDeaths', 'TotalRecovered', 'ActiveCases', "Serious,Critical", 'TotCases/1M pop',
                      'Deaths/1M pop', 'TotalTests', 'Tests/1Mpop', 'Population']
        plt.bar(lst2, lst1, color='green', tick_label=tick_label, width=0.7)
        plt.xlabel('x - axis')
        # naming the y-axis
        plt.ylim(0, 7 ** 10)
        plt.ylabel('y - axis')
        # plot title
        plt.title('Covid Data')

        plt.show()


def casesData():
    dataa = ((requests.get(url)).json())
    states = []
    x = data.get()

    # getting states
    for key in dataa.items():
        states.append(key[0])
    # getting statewise data
    for state in states:
        if state == x :
            active, confirmed, deaths, recovered = 0, 0, 0, 0
            newWindow = Toplevel(root)
            newWindow.title("Show Data")

            newWindow.geometry("280x280")
            my_canvas = Canvas(newWindow, width=520, height=440, bg="PeachPuff2")
            my_canvas.pack()
            login_frame = Frame(my_canvas, bg="LightBlue1")
            login_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
            f = (dataa[state]['districtData'])
            tc = []
            dis = []
            act, con, dea, rec = 0, 0, 0, 0

            # getting districtwise data
            for key in (dataa[state]['districtData']).items():
                district = key[0]
                dis.append(district)
                active = dataa[state]['districtData'][district]['active']
                confirmed = dataa[state]['districtData'][district]['confirmed']
                deaths = dataa[state]['districtData'][district]['deceased']
                recovered = dataa[state]['districtData'][district]['recovered']
                if district == 'Unknown':
                    active, confirmed, deaths, recovered = 0, 0, 0, 0
                tc.append([active, confirmed, deaths, recovered])
                act = act + active
                con = con + confirmed
                dea = dea + deaths
                rec = rec + recovered
            tc.append([act, con, dea, rec])
            dis.append('Total')
            Label(login_frame, text="Active:  {}\nConfirmed:  {}\nDeaths:  {}\nRecovered{}\n".format(act, con, dea, rec), font="TimesNewRoman 15", fg='black', bg='LightBlue1').pack(side=LEFT)


def casesDataGraph():
    dataa = ((requests.get(url)).json())
    states = []
    x = data.get()
    root.update()

    # getting states
    for key in dataa.items():
        states.append(key[0])

    # getting statewise data
    for state in states:
        if state == x:
            f = (dataa[state]['districtData'])
            tc = []
            dis = []
            act, con, dea, rec = 0, 0, 0, 0

            # getting districtwise data
            for key in (dataa[state]['districtData']).items():
                district = key[0]
                dis.append(district)
                active = dataa[state]['districtData'][district]['active']
                confirmed = dataa[state]['districtData'][district]['confirmed']
                deaths = dataa[state]['districtData'][district]['deceased']
                recovered = dataa[state]['districtData'][district]['recovered']
                if district == 'Unknown':
                    active, confirmed, deaths, recovered = 0, 0, 0, 0
                tc.append([active, confirmed, deaths, recovered])
                act = act + active
                con = con + confirmed
                dea = dea + deaths
                rec = rec + recovered
            tc.append([act, con, dea, rec])
            dis.append('Total')
            parameters = ['Active', 'Confirmed', 'Deaths', 'Recovered']

            # creating a dataframe
            df = pd.DataFrame(tc, dis, parameters)
            print('COVID - 19', state, 'District Wise Data')
            print(df)

            # plotting of data
            plt.bar(dis, df['Active'], width=0.5, align='center')
            fig = plt.gcf()
            fig.set_size_inches(18.5, 10.5)
            plt.xticks(rotation=75)
            plt.show()


# Driver Code
data = StringVar()
data1 = StringVar()
bg = PhotoImage(file="istockphoto-1213090148-170667a (.png")
my_canvas = Canvas(root, width=700, height=400)
my_canvas.pack(fill='both', expand=True)
my_canvas.create_image(0, 0, image=bg, anchor="nw")
heading = Label(my_canvas, text="Covid-19 Cases Tracker", fg="black", bg="khaki1")
heading.config(font='TimesNewRoman 27')
heading.place(relx=0.22, rely=0.1)
ulabel = Label(my_canvas, text="Select one option", fg='black', bg='khaki1')
ulabel.config(font='TimesNewRoman 18')
ulabel.place(relx=0.36, rely=0.3)

ttk.Button(my_canvas, text="India", command=case1, width=20).place(x=285, y=200)
ttk.Button(my_canvas, text="International", command=case2, width=20).place(x=285, y=290)
my_canvas.pack()
root.mainloop()