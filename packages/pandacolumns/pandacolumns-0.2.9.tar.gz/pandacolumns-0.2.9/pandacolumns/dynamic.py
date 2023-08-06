import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import ipdb


def pandadropper(df):  
  checkboxes = [widgets.Checkbox(value=False, description=column) for column in df.columns]

  for checkbox in checkboxes:
      checkbox.layout.width = 'auto'
      checkbox.layout.margin = '10px'
      checkbox.style.description_width = 'initial'
      checkbox.style.font_weight = 'bold'
      checkbox.style.font_size = '16px'
      checkbox.style.description_color = '#333333'
      checkbox.style.background_color = 'lightblue'

  submit_button_drop = widgets.Button(
      description='Drop selected',
      disabled=False,
      button_style='', 
      tooltip='Submit',
      icon='')

  def on_submit_button_click_drop(b):
      ipdb.set_trace()
      selected_columns = [checkbox.description for checkbox in checkboxes if checkbox.value]
      nonlocal df
      df = df.drop(selected_columns,axis = 1)
      output_label.value = f"{len(selected_columns)} columns dropped"

  submit_button_drop.on_click(on_submit_button_click_drop)
  checkboxes_box = widgets.VBox(children=checkboxes)
  output_label = widgets.Label(value="")
  submit_box = widgets.VBox(children=[widgets.Label(value=''),submit_button_drop,output_label])
  submit_box.layout.margin = '30px 0px 0px 20px'
  full_box = widgets.HBox(children=[checkboxes_box, submit_box])
  display(full_box)