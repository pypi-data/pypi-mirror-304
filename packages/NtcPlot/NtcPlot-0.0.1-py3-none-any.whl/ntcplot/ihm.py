
from PyQt6.QtWidgets import (QGridLayout, QGroupBox,
        QPushButton, QRadioButton, QVBoxLayout, QWidget)
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import numpy as np
from mpl_toolkits.basemap import Basemap
import os
import re
import matplotlib.pyplot as plt
from .values import version


# class for scrollable label
class ScrollLabel(QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)
        self.label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

class Window(QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

    def class_args(self, v_dict, ncdump_h , ntc_file):
        grid = QGridLayout()
        self.var_dict = v_dict
        self.ntc_file = ntc_file

        # up left panel of parameters
        grid.addWidget(self.createGroup(self.var_dict), 0, 0)
        # down left panel of parameters
        grid.addWidget(self.createMapGroup(self.var_dict), 1, 0)
        # right panel of netcdf information
        grid.addWidget(self.createGroup2(ncdump_h), 0, 1, 0, 1)
        self.setLayout(grid)

        # window name
        self.setWindowTitle("NtcPlot v" + version)
        # window pop up size
        self.resize(600, 400)

    # method for widgets
    def button_click(self, axis):
        # get selected variable from expandable list
        content = self.combo_box.currentText()
        # remove variable dimensions from string
        dim_matches = re.findall(r'\(.*\)', content)
        for d_match in dim_matches:
            content = content.replace(d_match, "")
        # add only the variable name to the QLineEdit
        if axis == "y":
            self.y_values.insert(" {} ".format(content))
        elif axis == "x":
            self.x_values.insert(" {} ".format(content))

    # method for widgets
    def button_click_map(self, axis):
        # get selected variable from expandable list
        content = self.combo_box_map.currentText()
        # remove variable dimensions from string
        dim_matches = re.findall(r'\(.*\)', content)
        for d_match in dim_matches:
            content = content.replace(d_match, "")
        # add only the variable name to the QLineEdit
        if axis == "lon":
            self.lon_values.insert(" {} ".format(content))
        elif axis == "lat":
            self.lat_values.insert(" {} ".format(content))
        elif axis == "point":
            self.points_values.insert(" {} ".format(content))


    # left upper panel
    def createGroup(self, v_dict):
        # name
        groupBox = QGroupBox("Configuration")

        self.choose_var = QLabel("Choose variable")
        self.choose_plt = QLabel("Choose type of Plot")
        self.combo_box = QComboBox()

        # expandable list with netcdf variables and dimensions
        expa_list = []
        var_list = v_dict.keys()
        for var_name in var_list:
            expa_list.append("{}{}".format(var_name, v_dict[var_name]["dims"]))
        # adding list of items to combo box
        self.combo_box.addItems(expa_list)


        # creating push button
        # by clicking this button the value selected on the expandable list
        # will be added to the constracted expression over the selected axis
        x_button = QPushButton("X values ", self)
        x_button.setFixedSize(QtCore.QSize(60, 30))

        y_button = QPushButton("Y values ", self)
        y_button.setFixedSize(QtCore.QSize(60, 30))

        # plot creation with the constracted expressions
        plot_button = QPushButton("Create Plot", self)
        plot_button.clicked.connect(self.make_plot)

        # QLineEdit where the axis expressions are written
        self.x_values = QLineEdit()
        self.x_values.setToolTip("Use python syntax")
        x_button.clicked.connect(lambda: self.button_click("x"))

        # QLineEdit where the axis expressions are written
        self.y_values = QLineEdit()
        self.y_values.setToolTip("Can be 2D, but at least one dimension must match that of X")
        y_button.clicked.connect(lambda: self.button_click("y"))

        # radio style buttons for plot choice
        self.radio1 = QRadioButton("&Scatter")
        self.radio2 = QRadioButton("&Line")

        # QVBoxLayout the following widgets will appear in the called order
        vbox = QVBoxLayout()
        vbox.addWidget(self.choose_var)
        vbox.addWidget(self.combo_box)
        vbox.addWidget(x_button)
        vbox.addWidget(self.x_values)
        vbox.addWidget(y_button)
        vbox.addWidget(self.y_values)
        vbox.addWidget(self.choose_plt)
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        vbox.addWidget(plot_button)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createMapGroup(self, v_dict):
        # name
        groupBox = QGroupBox("Map Configuration")

        self.choose_var = QLabel("Choose variable")
        self.choose_plt = QLabel("Choose type of Plot")
        self.combo_box_map = QComboBox()

        # expandable list
        expa_list = []
        var_list = v_dict.keys()
        for var_name in var_list:
            expa_list.append("{}{}".format(var_name, v_dict[var_name]["dims"]))
        # adding list of items to combo box
        self.combo_box_map.addItems(expa_list)

        # label in group
        self.section = QLabel("Global Map")

        # clicking this button will add current variable of
        # expandable list to QlineEdit
        lat_button = QPushButton("Latitude", self)
        lat_button.setFixedSize(QtCore.QSize(60, 30))
        self.lat_values = QLineEdit()
        lat_button.clicked.connect(lambda: self.button_click_map("lat"))

        lon_button = QPushButton("Longitude", self)
        lon_button.setFixedSize(QtCore.QSize(60, 30))
        self.lon_values = QLineEdit()
        lon_button.clicked.connect(lambda: self.button_click_map("lon"))

        d_points_button = QPushButton("Data Points", self)
        d_points_button.setFixedSize(QtCore.QSize(70, 30))
        self.points_values = QLineEdit()
        self.points_values.setToolTip("Optional")
        d_points_button.clicked.connect(lambda: self.button_click_map("point"))

        # click for plot
        plot_button_m = QPushButton("Create Map", self)
        plot_button_m.clicked.connect(self.make_map)


        # QVBoxLayout the following widgets will appear in the called order
        vbox = QVBoxLayout()
        vbox.addWidget(self.choose_var)
        vbox.addWidget(self.combo_box_map)
        vbox.addWidget(lat_button)
        vbox.addWidget(self.lat_values)
        vbox.addWidget(lon_button)
        vbox.addWidget(self.lon_values)
        vbox.addWidget(d_points_button)
        vbox.addWidget(self.points_values)
        vbox.addWidget(plot_button_m)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    # right pqnel
    def createGroup2(self, ncdump_h):
        groupBox = QGroupBox("Ncdump output")

        vbox = QVBoxLayout()

        # creating scroll label
        label = ScrollLabel(self)

        # setting text to the label
        label.setText(ncdump_h)

        # setting geometry
        label.setGeometry(100, 100, 200, 80)

        vbox.addWidget(label)
        groupBox.setLayout(vbox)

        return groupBox

    # function for classic 2D plots
    def make_plot(self):
        # get written QlineEdit expression from IHM
        y_code_v = self.y_values.text()
        y_unit = self.y_values.text()
        x_code_v = self.x_values.text()
        x_unit = self.x_values.text()
        # for all variables in netcdf
        for v in self.var_dict.keys():
            # if variable in QlineEdit, assign dictionary expression with array values
            if re.search(r'\b{}\b'.format(v), y_code_v):
                y_code_v = re.sub(r'\b{}\b'.format(v), "self.var_dict[\"{}\"]['values']".format(v), y_code_v)
                # if variable in QlineEdit, assign units of variable instead
                y_unit = re.sub(r'\b{}\b'.format(v), self.var_dict[v]['units'][:], y_unit)
            if re.search(r'\b{}\b'.format(v), x_code_v):
                x_code_v = re.sub(r'\b{}\b'.format(v), "self.var_dict[\"{}\"]['values']".format(v), x_code_v)
                x_unit = re.sub(r'\b{}\b'.format(v), self.var_dict[v]['units'][:], x_unit)

        # y_code_v, python expression should always be given
        y_val = eval(y_code_v)
        # x_code_v, if none given, plot range values of y
        if x_code_v == "":
            x_code_v = "np.arange(len(y_val))"
        x_val = eval(x_code_v)

        # remove dimensions from units
        remove_dim = re.findall(r'\[.+?\]', y_unit)
        for r_dim in remove_dim:
            y_unit = y_unit.replace(r_dim, "")
        remove_dim = re.findall(r'\[.+?\]', x_unit)
        for r_dim in remove_dim:
            x_unit = x_unit.replace(r_dim, "")

        # which 2d plot is selected ?
        if self.radio1.isChecked():
            # x and y have same dimensions
            if np.shape(x_val) == np.shape(y_val):
                plt.scatter(x_val, y_val)
            # y has 2 dimensions and one is marching x dimension
            elif np.shape(y_val[:, 0]) == np.shape(x_val):
                for line in range(len(y_val[0, :])):
                    # for the not matching dimension, add lines to plot
                    plt.scatter(x_val, y_val[:, line], label="dim{}".format(line))
                    plt.legend()
            # y has 2 dimensions and one is marching x dimension
            elif np.shape(y_val[0, :]) == np.shape(x_val):
                for line in range(len(y_val[:, 0])):
                    # for the not matching dimension, add lines to plot
                    plt.scatter(x_val, y_val[line, :], label="dim{}".format(line))
                    plt.legend()
            # too many dimensions or not mathing ones
            else:
                print("error in dimensions")

        elif self.radio2.isChecked():
            # x and y have same dimensions
            if np.shape(x_val) == np.shape(y_val):
                plt.plot(x_val, y_val)
            # y has 2 dimensions and one is marching x dimension
            elif np.shape(y_val[:, 0]) == np.shape(x_val):
                # for the not matching dimension, add lines to plot
                for line in range(len(y_val[0, :])):
                    plt.plot(x_val, y_val[:, line], label="dim{}".format(line))
                    plt.legend()
            # y has 2 dimensions and one is marching x dimension
            elif np.shape(y_val[0, :]) == np.shape(x_val):
                # for the not matching dimension, add lines to plot
                for line in range(len(y_val[:, 0])):
                    plt.plot(x_val, y_val[line, :], label="dim{}".format(line))
                    plt.legend()
            # too many dimensions or not mathing ones
            else:
                print("error in dimensions")

        # axis label for units
        plt.ylabel(self.y_values.text() + "\n ({})".format(y_unit))
        plt.xlabel(self.x_values.text() + "\n ({})".format(x_unit))

        plt.title(os.path.basename(self.ntc_file))
        plt.show()


    def make_map(self):
        # get written expression on QlineEdit
        lon_code = self.lon_values.text()
        lat_code = self.lat_values.text()
        d_points_code = self.points_values.text()
        d_points_unit = self.points_values.text()
        for v in self.var_dict.keys():

            if re.search(r'\b{}\b'.format(v), lon_code):
                # replace variable name with dictionary of values
                lon_code = re.sub(r'\b{}\b'.format(v), "self.var_dict[\"{}\"]['values']".format(v), lon_code)
            if re.search(r'\b{}\b'.format(v), lat_code):
                lat_code = re.sub(r'\b{}\b'.format(v), "self.var_dict[\"{}\"]['values']".format(v), lat_code)
            if re.search(r'\b{}\b'.format(v), d_points_code):
                d_points_code = re.sub(r'\b{}\b'.format(v), "self.var_dict[\"{}\"]['values']".format(v), d_points_code)
                # replace variable name with units
                d_points_unit = re.sub(r'\b{}\b'.format(v), self.var_dict[v]['units'][:], d_points_unit)
        lon_val = eval(lon_code)
        lat_val = eval(lat_code)
        if d_points_code != "":
            d_points_val = eval(d_points_code)

        # remove dimensions from units
        remove_dim = re.findall(r'\[.+?\]', d_points_unit)
        for r_dim in remove_dim:
            d_points_unit = d_points_unit.replace(r_dim, "")

        # make longitude values to mathc -180 to 180 degrees
        if np.max(lon_val) > 180:
            lon_val -= 180

        m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, \
                    llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='l')
        x, y = m(lon_val, lat_val)
        m.drawmapboundary(fill_color='#99ffff')
        m.drawcountries(color="grey")
        m.drawcoastlines(color="grey")
        m.drawparallels(np.arange(-90., 99., 30.), labels=[1, 1, 0, 1])
        m.drawmeridians(np.arange(-180., 180., 60.), labels=[1, 1, 0, 1])
        m.fillcontinents(color='#cc9966', lake_color='#99ffff')
        # m.scatter(x, y, 3,marker='o',color='k')
        try:
            d_points_val
        except NameError:
            print('No DataPoints defined')
            plt.scatter(x, y)
            pass
        else:
            colors = d_points_val
            plt.scatter(x, y, c=colors, cmap='viridis')

            clb = plt.colorbar(orientation="horizontal", fraction=0.046, pad=0.04)
            clb.ax.set_xlabel(self.points_values.text() + "\n ({})".format(d_points_unit))
            pass
        plt.title(os.path.basename(self.ntc_file))
        plt.show()
