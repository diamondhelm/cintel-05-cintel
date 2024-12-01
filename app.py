# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

# From shiny, import just reactive and render
from shiny import reactive, render

# From shiny.express, import just ui and inputs if needed
from shiny.express import ui

import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats

# --------------------------------------------
# Import icons as you like
# --------------------------------------------

# https://fontawesome.com/v4/cheatsheet/
from faicons import icon_svg

# --------------------------------------------
# Shiny EXPRESS VERSION
# --------------------------------------------

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 3

# --------------------------------------------
# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings
# --------------------------------------------

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# --------------------------------------------
# Initialize a REACTIVE CALC that all display components can call
# to get the latest data and display it.
# The calculation is invalidated every UPDATE_INTERVAL_SECS
# to trigger updates.
# It returns a tuple with everything needed to display the data.
# Very easy to expand or modify.
# --------------------------------------------


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp":temp, "timestamp":timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry




# Define the Shiny UI Page layout
# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI
ui.page_opts(title="Diamond's Live Data Example", fillable=True)

# Sidebar is typically used for user interaction/information
# Note the with statement to create the sidebar followed by a colon
# Everything in the sidebar is indented consistently
with ui.sidebar(open="open"):

    ui.h2("Antarctic Explorer", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )
    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/diamondhelm/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/diamondhelm/cintel-05-cintel/blob/main/app.py",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shinylive.io/py/app/#h=0&code=NobwRAdghgtgpmAXGKAHVA6VBPMAaMAYwHsIAXOcpMAYgAIBaJ5l1t9jjgHQnoEkYqYgCcyAZzpQydMgAs4M4qkZ0ACtgDKsgJYRsdAKIANVQCUDGjXQBqB0xr4B5AHI96nD569MebugDFhYhg6MR09PDptQRFpACsAVzFpYTgoQjJtADcFKAgAEzpUgrhhHgAzIJCw3X1ooVEitIzsuEji-NLfXgCq0PDsDDgAD1RUsTFI+ti6ROS6BO1JAqiIVATxKPK6CDg4TvyKvpq9IdHxiWnGxe6rlLz84KPgunypOEz4KJjGt4pPuDPEIkAA2ILgLVIlx+0k6AEcEoCIHc6KgHlAJBjUYdkTDUSDiGQQYMRmM4BNJBJUMMgf1agB3bT5ADmH2hDRSlE6wgA+qgCUTsLSxIRtDhvhzQmQpGJuu5vArFQw-AJJdoSBBMRJsMQEnQQdoANZI+VKs2cOV0WRkMioMSIAD0DvKpGl9PJwTgGBIMAdWQALA7CPIZfIPg7aeUoOqoRKZjGIDyxFlmZbzen2H4tLVDCZzJYbHYHC4-Bmy8w0+Wy35-NphMlImIPpI6BrknlpABVVQAEQAggAVAx0PjOIemax9gAydBdwkkYP1rVeUigfgAwlDpeRMakFmIElAwfpOuVdPtVgt0KVCBiFOCbaVZT1O02W2RsKgFOFpGRiHQYCgY0omkQhwSgec5CkECAHJMQgVYKFZecAApEEQgBKUsqwzbpu37IceVHcdJynHkNAMdcNHQ3RpAAXjoABmSscPNFVkUyI9tAAL1yOhzD7dcBz4WwbGnTth0ZOQWx9GBSBXaUpWEBIMgSVI-AHeQmnSTIcjoLIj0RKIJCSC8-ylEQFHbCg6BQ3Q50AzJSCwl8m0KAAjfQjxBGQtPybQxH5KB9B9IRdh3XzoLCYh6V8gKlz0v4oAwDSdAkVIdOXAyQSM+KoDoelhDQL95wg3UVnynsDAARQkuhiG2DL-IgZln1NVilW6KraoMci+AALQMGjyDoBiAFYeAyloch5bLER5QritKUbtOmr05rgFD4URFDAOGcEIDo7qJL6waMJc7COs6no+A47QuN4lsBKEkTh3Xad10i6RvNeAKgpC4IwsoTZbwQ28wT8czWV-LSQXeeYkuWQp-MCuG6jIFKek0hRwcIBI4achD4t0bKmXeQo4ByYR9HwwdeuIuxSPIyiNEh-8yGEbRmWQq8-nJTH+E5Mg1M1d8En5BQpNkOhKdKbA5F0Zkdj2A5FF+1Hgt8hQkoFmw5ZljF9HM0kHnq+c5P88pBkuq6FW6HgAAEpt0r1cZQlzT1Wl2eVxn3gnc898ndxAeDoMO6H4CBSb5uKJFx-GpG0eTZepuhacIhmJ2nZmqLVjmuZ58W+efcOvdaDASa4vmeQJ0oUPT+mx0Z7OKKoi6EPD+ge1XOhWV2IrCf1YhmXVUPw4oQQVqCBIChQoqCmCDAZ+0ByUIYABGAAOSIN4ANgwyJ15c0uAXbSeGL5gEMAgGL3YwZJhHKAEUK4MAAFIAE0GDfmBv8KN+AASiA34AFlgGszAMfcOux6Q8n8pCaA1MeTA1TgxEAr8J6oFfogTBkQMHRHJNKQQ2DT5ENQAAX26KXeg0MtavDgAiXIFVrwrDkAoGBMtyDUzHmHZ2rRZqGTgAtIq15hAYGhnfJas8YFwPVITCC2BkFcOwO3ahdAADizZ8piGgHaWQhJ6rbDYa2NSxRYQMKMnOZY+hyhqTYfOMYxBCDkjEIrHh9DGFJl0dFeiZcZobWEUtMREjVGdwCCIOgPY-po3QpuKOpRzGMLVt3aUgRYAKCsSjf67j8jbAYqgfIGAUlQDSfALaFihE6LQD40JYd6D+AiVEjW2B0KaJhveeGsI5FJ0QfoFBQoO5h1rskWRCCFFKI5voBiMj4HyKQf0qhYTTAfBFmLCWBVtDSRTvLcISt3TK32O4+gBgqZGwIQVHGP0FYSFsRABBkR3QwUXLQq58g3wbRLuHVIwthAIW2pU7x+iyCRFyZEYZZBRlzMUQsiA9tYU9B7HAM8uw6HZj0GnPgagoCsn1MFXUZANyvIUIsLA2KhFKHEO7WcM8EFZmbJkIkChzLaPzi1S8CJCTki+hsxcS0IKSHaYoLBPQNDNjPGCKA7lwRqwHMpJl-5TJ0PpPo6VaIcWMnyNJKxxjOx8B4CStV5LUCUoZeCOir8omwFIPkOCU5lzFMMMMWAEtX6RHFXDKVcA6KysRO3egGgmRwHcvy+KH5UDqm8voUyhQrGmXnLRUomVSAOnsiIRyPS-DOE5UqzZ0trJwHgCNcyhAMo2WMa4zowb5wujBDFC8nkZLEAJPC45pyFZst0HQitQaQ2XBKOQC8bYAoUHIMSHgUsFjaHvoGqtKElCUHNWAedsLIEh3haXElsgABML8wB9nIBBFohBHX8ksmUfArY4YTB5IuigwwyAMGcQO89UCw4GpfoM0udBX59noXJTUHNE7yQatpEEDAAQyALSVKQakFBNUVn2ug+7pTCCPclV17jS5gQxGIG9GCRgPqfRQc9eB3GvsnRgWQwh3buM3bvXddqICGntK-cjJKoAfq-eHV+6jNkAISO5OgGhdSocBPgTD4cqNIsXdaW09onQjzkAJ70wQHT+StQUeQIJfSigHWBgADGNR9CaQQYc-SfCC0NF08ilXkQ0ZnS5sanRxiTYceN8YE0h9ADmuNWlSOUGTNo7SOgdIp2QymfRqfuv+-IWmdMmYYIZ4zemHRSuIO5B0gFdAOmKlgIU4nzPj0sx8aztmmM+bDk5jALmwDqDRflyIUmAuv1k8Fp0JxBhCFcRjEgDocARgvShqzr8bNw3K5A2jznOO+dfnVgYJ6LgVa-U1mTrX5MOg61gYg3WVOpYJMyPr23xAbYGAwUkFwBukcK2HIbJWRtlfswVxzlpbpCfmwYc4LjIjbPbUrG+0hO3lpnb2y8xissITRLsUz8KJ0krRviv2OUYCamDu42HU6AnuWIMMabXHor0lvE2OiCYkwpl3QeFdB9XNa3gIu9yzIGDMiKv5YGDApWIgYOsYQLqnvhwwmu6nr91ymOBnQAcUHE0-LE4srjTsuSlAwHegl136HbCyWjHkmDUcq9Lq-PXYA2l0PBdpZqStTbfNWflTBkvYNKTcWAfX1PS7-K8dUoFILyhgs6ZCnp4z+lT2aN7X2PoA67CDuR3zTQfkIXKK-EA4KfekD98o4AMFMEwQALrkLoOuPX66ZtgHpBBeAkFZB5H3IeUzDv88y42dJElt5hBB1sWCJMJa9iHR9XAfn1OG8QXyDyEM3Jd3C+EGYyJ7wkZi4Iax2vpc5clDEUr6nnt1fBU1wQ7XkfdcO934b4xxv4NsvNys3574CFn2UA-e3judfhxd1UvRhIPde4oCM2Zvv5nKID5lGawf-aBw0Z368Kn4x5x4J4f5J5f6TKp6kLOqZ6ULV5yjo7ej94oQt4ght6pALpd6RAwC6CD5wBczWiLr+j6ZvysZrooGN7N74yYEijYGd5yo96fp95N6EFQDD6vwgJHb8QQii7LKcEIaz755hwL7cgYBJQ8iVDpI5JIrqz-RwLlBb4F76776wydIm6KxT4W5n75RJQyFfATp4xj6i5H6tSO7V6R4P6ArP6vCe64pv4QqQG9ITKoJ+JCL-4wCh77BAGR4FL3wfA8gUo9IoQwRr6DAapyAwSRBZq7AYSR70CvgKB7TRAJAhBRGyDU66EIQdAK7FLqKcxBz2F4CZGLrrz6bkEiHjq5oUY0EqFvpTo0EcFcFgDrhl6NATqj7j6ypcjVGfriGlB8gChjqfqr7RLr6npkANFfr1IfDBizh9DGJ8J6S4zUp3KEwr4VKu5P7AolGOGEKJ6uH+4MQrGeFHiEB+zeGAG1KzGGCai27GLFKlIKDxT-YyyCAfh0DuRIqWT4iEiZAtTU4rw7AGK5JDCfEtJO5hJxJUyCpp4X5kIwSthNrpEITmSXznJWI-GPgOICiAmpjAH2HAD4LwCX6vwZ4rQBF-hwLvDPy5IklgBwHEJgAZ63GJE56lpWS3i4n-HSBWLmGfLb4Ryog4ag5+QOHGLQBfAgbGLDAolI4QCRBSnpKGJ0IAyKlXbCl1JT5yTqQq7QlhxnhKz5LDD3w8nEZbSe6Gl0DDC3qInOpLaR7YC3pQZOm+ampeqvzi6CA257iCGm4SATrLJM4uI9J0CMZiZanakepwAghiB0ToJMlulIDfpgA+nQZS62QAAN64WEF6pJhCjpqZ3pM+YA5C0ZwpoIIgsiDBHwlSFSdyXqjJ7OYmlJEeM2RJ9AkZ-KqQoZEw4ZDAFyByhQUMWiS48wsp8gNpkcnQX4-a0gBknMkq0q8pHytkAICRpsbCM5kScA85nQI0S590nqdA+g65KEmCHZXG9AbCSpsEVI3yXxaQYgUaribKIoYogw1kYgGABoEAfZFwQBu5DS848pD4cEvclAkufETYjCTZapCayENyfQ+masB0Vp15X6cFiICFpxeQrIKEGFuS50NpwwAi8ZK0BoyQKEOFlAziWFpcii2UEgF85QjJmCFJc+vmYgBIX4Uwz6zixq7QFFiIkQqAolbQUoA+pQ84DEP5f5uggFLiKE5FLFkQzFR4YgjF9+7FMEPxIyZ4EK-5cAmeK0wAvF86dAAAVLaXQAANSIQ3j7n8kRLymdpqVaUZ7cU3lIb5CjlaTKUDnyQmV5xaTGmwY2nGnVb+Vt5SCWl2kMmFnkmskaV0QMn6WHFGU1zniZ54HECdB0RPLnhiAxE7DpJFUhkXDhmRkwTsm+ZJEFKT7w4bCUgjlmT-h4zJDBA8QZJ2LyBlBEnRVFzvA1x4obCqVQDDABQb6MqLoDhll4DYBTUzWenzUS4Dy24oS5n5n1UgHR6zhczlkZ5AA", target="_blank")
    ui.a(
    
    )

# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("sun"),
        theme="bg-gradient-blue-purple",
    ):

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} C"

        "warmer than usual"

  

    with ui.card(full_screen=True):
        ui.card_header("Current Date and Time")

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"


#with ui.card(full_screen=True, min_height="40%"):
with ui.card(full_screen=True):
    ui.card_header("Most Recent Readings")

    @render.data_frame
    def display_df():
        """Get the latest reading and return a dataframe with current readings"""
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
        pd.set_option('display.width', None)        # Use maximum width
        return render.DataGrid( df,width="100%")

with ui.card():
    ui.card_header("Chart with Current Trend")

    @render_plotly
    def display_plot():
        # Fetch from the reactive calc function
        deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

        # Ensure the DataFrame is not empty before plotting
        if not df.empty:
            # Convert the 'timestamp' column to datetime for better plotting
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Create scatter plot for readings
            # pass in the df, the name of the x column, the name of the y column,
            # and more
        
            fig = px.scatter(df,
            x="timestamp",
            y="temp",
            title="Temperature Readings with Regression Line",
            labels={"temp": "Temperature (°C)", "timestamp": "Time"},
            color_discrete_sequence=["blue"] )
            
            # Linear regression - we need to get a list of the
            # Independent variable x values (time) and the
            # Dependent variable y values (temp)
            # then, it's pretty easy using scipy.stats.linregress()

            # For x let's generate a sequence of integers from 0 to len(df)
            sequence = range(len(df))
            x_vals = list(sequence)
            y_vals = df["temp"]

            slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
            df['best_fit_line'] = [slope * x + intercept for x in x_vals]

            # Add the regression line to the figure
            fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

            # Update layout as needed to customize further
            fig.update_layout(xaxis_title="Time",yaxis_title="Temperature (°C)")

        return fig
