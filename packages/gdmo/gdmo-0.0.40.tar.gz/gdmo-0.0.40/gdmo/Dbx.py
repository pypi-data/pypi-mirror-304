import py4j
import re

class DbxWidget:
    """
    A utility class for interacting with Databricks widgets to read and create widget values.

    Usage:
    - To read the value from an existing widget:
        value = DbxWidget(dbutils, widget_name)

    - To create a new widget with specified type and options:
        value = DbxWidget(dbutils, widget_name, type='dropdown', defaultValue='Red', choices=["Red", "Blue", "Yellow"])

    Inputs:
    - dbutils: Databricks utility object for widget operations
    - name: Name of the widget
    - type: Type of the widget (text, dropdown, multiselect, combobox). Defaults to Text if not provided
    - defaultValue: Default value for the widget. Defaults to blank
    - **kwargs: Additional keyword arguments for widget creation

    Example:
    - Existing method:
        dbutils.widgets.dropdown("colour", "Red", "Enter Colour", ["Red", "Blue", "Yellow"])
        colour = dbutils.widgets.read("colour")

    - New method:
        colour = DbxWidget(dbutils, "colour", 'dropdown', "Red", choices=["Red", "Blue", "Yellow"])
    """

    def __new__(self, dbutils, name, type='text', defaultValue='', **kwargs):
        if name is None:
            raise ValueError("Widget name cannot be blank")
        
        if not re.match(r'^\w+$', name):
            raise ValueError("Widget name must contain only alphanumeric characters or underscores")
        
        if type not in ['text', 'dropdown', 'multiselect', 'combobox']:
            raise ValueError("Invalid widget type. Supported types: text, dropdown, multiselect, combobox")
        
        if type in ['dropdown', 'multiselect'] and 'choices' not in kwargs:
            raise ValueError("Choices list is required for dropdown widgets")            

        widgetName = re.sub(r'\W|^(?=\d)', '_', name)
        
        widgetConstructor = {
            'text': dbutils.widgets.text,
            'dropdown': dbutils.widgets.dropdown,
            'multiselect': dbutils.widgets.multiselect,
            'combobox': dbutils.widgets.combobox
        }[type]
        
        try:
            returnValue = dbutils.widgets.get(widgetName)
        except py4j.protocol.Py4JJavaError as e:
            if 'No input widget' in str(e.java_exception):
                try:
                    widgetConstructor(name=widgetName, defaultValue=defaultValue, label=name, **kwargs)
                    returnValue = dbutils.widgets.get(widgetName)
                except Exception as e:
                    raise ValueError(f"Error creating widget: {e}")
            else:
                raise e
        
        return returnValue