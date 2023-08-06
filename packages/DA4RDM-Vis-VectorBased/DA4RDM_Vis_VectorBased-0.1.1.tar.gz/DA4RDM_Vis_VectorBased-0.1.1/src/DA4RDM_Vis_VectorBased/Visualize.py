"""
This function is used to generate the files for the visualization as specified by user
"""


def visualize(corr_data, save_option):
    import pandas as pd
    import plotly.express as px
    import json
    import sys

    correlation_response = corr_data.Correlation_value.tolist()
    correlation_response = [*correlation_response, correlation_response[0]]
    categories = ['Planning', 'Production', 'Analysis', 'Archival', 'Access', 'Reuse']
    categories = [*categories, categories[0]]
    df1 = pd.DataFrame(dict(
        r=correlation_response,
        theta=categories))
    if save_option.lower() == "png":
        fig = px.line_polar(df1, r='r', theta='theta', line_close=True, range_r=[0, 1], template="plotly_dark")
    else:
        fig = px.line_polar(df1, r='r', theta='theta', line_close=True, range_r=[0, 1], )
    fig.update_traces(fill='toself')
    try:
        if save_option.lower() == "png":
            fig.write_image("Radarchart.png")
        if save_option.lower() == "jpeg":
            fig.write_image("Radarchart.jpeg")
        if save_option.lower() == "pdf":
            fig.write_image("Radarchart.pdf")
        if save_option.lower() == "json":
            my_details = {
                'Similarity': dict(corr_res=correlation_response, rdlc_phase=categories),
            }
            with open('RDLC.json', 'w') as json_file:
                json.dump(my_details, json_file)
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error saving results")


if __name__ == "__main__":
    import sys

    args = sys.argv
    globals()[args[1]](*args[2:])
