import pandas as pd
import ipywidgets as widgets
from IPython.display import display


class PandasDropper:
    """
    A class that creates a GUI to select and drop columns from a Pandas DataFrame.

    Parameters:
    -----------
    dataframe : pandas.DataFrame
        The DataFrame to be modified.

    Usage:
    ------
    pd = PandasDropper(df)
    """
    def __init__(self, dataframe):
        self.df = dataframe.copy()
        self.checkboxes = [widgets.Checkbox(value=False, description=column) for column in self.df.columns]
        for checkbox in self.checkboxes:
            checkbox.layout.width = 'auto'
            checkbox.style.description_width = 'initial'
            checkbox.style.font_weight = 'bold'
            checkbox.style.font_size = '16px'
            checkbox.style.description_color = '#333333'
            checkbox.style.background_color = 'lightblue'

        self.submit_button_keep = widgets.Button(
            description='Keep selected',
            disabled=False,
            button_style='', 
            tooltip='Submit',
            icon='')

        self.submit_button_drop = widgets.Button(
            description='Drop selected',
            disabled=False,
            button_style='', 
            tooltip='Submit',
            icon='')

        self.submit_button_rollback = widgets.Button(
            description='Rollback',
            disabled=False,
            button_style='', 
            tooltip='Submit',
            icon='')

        self.checkboxes_box = widgets.VBox(children=self.checkboxes)
        self.submit_box = widgets.VBox(children=[widgets.Label(value=''), self.submit_button_keep, self.submit_button_drop, self.submit_button_rollback])
        self.submit_box.layout.margin = '30px 0px 0px 20px'
        self.full_box = widgets.HBox(children=[self.checkboxes_box, self.submit_box])
        display(self.full_box)

        self.submit_button_keep.on_click(self.on_submit_button_click_keep)
        self.submit_button_drop.on_click(self.on_submit_button_click_drop)
        self.submit_button_rollback.on_click(self.on_submit_button_click_rollback)

    def on_submit_button_click_keep(self, b):
        selected_columns = [checkbox.description for checkbox in self.checkboxes if checkbox.value]
        self.df = self.df[selected_columns]

    def on_submit_button_click_drop(self, b):
        selected_columns = [checkbox.description for checkbox in self.checkboxes if checkbox.value]
        self.df = self.df.drop(selected_columns, axis=1)

    def on_submit_button_click_rollback(self, b):
        self.df = self.df.copy(deep=True)

