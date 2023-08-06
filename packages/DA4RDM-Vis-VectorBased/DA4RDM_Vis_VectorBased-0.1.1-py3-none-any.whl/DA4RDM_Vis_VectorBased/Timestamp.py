"""
This function returns the start and end date values for the given project id
"""


def extract_timestamp(data_path, project_id):

    from DA4RDM_Vis_VectorBased.Extract import extract_df
    import sys

    try:
        start = []
        end = []
        df = []
        result_dataframe = extract_df(data_path)
        project_id = project_id.lower()
        df.append(project_id)
        project_filtered = list(result_dataframe[result_dataframe.ProjectId == df[0]].Timestamp)
        project_filtered.sort()
        start.append(project_filtered[0].split(" ")[0])
        end.append(project_filtered[-1].split(" ")[0])
        start = start[0]
        end = end[0]
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Kindly verify the timestamps for the provided Project Id")
    return start, end
