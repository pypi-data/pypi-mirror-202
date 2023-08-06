import ipywidgets as widgets
from IPython.display import display
def pandadrop(mydataframe):
  checkboxes = [widgets.Checkbox(value=False, description=column) for column in mydataframe.columns]
  for checkbox in checkboxes:
      checkbox.layout.width = 'auto'
      #checkbox.layout.margin = '10px'
      checkbox.style.description_width = 'initial'
      checkbox.style.font_weight = 'bold'
      checkbox.style.font_size = '16px'
      checkbox.style.description_color = '#333333'
      checkbox.style.background_color = 'lightblue'

  
  df1 = mydataframe.copy()
  

  submit_button_keep = widgets.Button(
      description='Keep selected',
      disabled=False,
      button_style='', 
      tooltip='Submit',
      icon='')

  submit_button_drop = widgets.Button(
      description='Drop selected',
      disabled=False,
      button_style='', 
      tooltip='Submit',
      icon='')

  submit_button_rollback = widgets.Button(
      description='Rollback',
      disabled=False,
      button_style='', 
      tooltip='Submit',
      icon='')

  def on_submit_button_click_keep(b):
      selected_columns = [checkbox.description for checkbox in checkboxes if checkbox.value]
      global mydataframe
      mydataframe = mydataframe[selected_columns]
   

  def on_submit_button_click_drop(b):
      selected_columns = [checkbox.description for checkbox in checkboxes if checkbox.value]
      global mydataframe
      mydataframe = mydataframe.drop(selected_columns,axis = 1)
    

  def on_submit_button_click_rollback(b):
      global mydataframe
      mydataframe = df1.copy()
  
    
  submit_button_keep.on_click(on_submit_button_click_keep)
  submit_button_drop.on_click(on_submit_button_click_drop)
  submit_button_rollback.on_click(on_submit_button_click_rollback)

  checkboxes_box = widgets.VBox(children=checkboxes)
  submit_box = widgets.VBox(children=[widgets.Label(value=''), submit_button_keep, submit_button_drop,submit_button_rollback])
  submit_box.layout.margin = '30px 0px 0px 20px'
  full_box = widgets.HBox(children=[checkboxes_box, submit_box])
  display(full_box)