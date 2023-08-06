"""
This function evaluates the correlations values from the extracted dataset
"""


def eval_corr(data_path, project_id, start_date="", end_date="", operation_list_path="",
              eval_feature="pearson", eval_type="binary"):
    import sys
    from DA4RDM_Vis_VectorBased.Timestamp import extract_timestamp
    from dateutil.relativedelta import relativedelta
    import pandas as pd
    from DA4RDM_Vis_VectorBased.Extract import extract_df

    if project_id == "" or project_id is None:
        sys.exit("Project id missing. Please provide a valid project Id to proceed.")
    if start_date == "" or start_date is None or end_date == "" or end_date is None:
        try:
            proj_start_date, proj_end_date = extract_timestamp(data_path, project_id)
            end_date = pd.to_datetime(proj_end_date) + relativedelta(days=+1)
            start_date = end_date + relativedelta(months=-6)
            end_date = end_date.strftime('%Y-%m-%d')
            start_date = start_date.strftime('%Y-%m-%d')
        except Exception as e:
            sys.exit("Oops! " + str(e.__class__) + " occurred. Please verify the start and end date formats.")

    data = extract_df(data_path)
    project_id = project_id.lower()
    correlation_response = evaluate_sim(data, start_date, end_date, eval_feature, eval_type, project_id,
                                        operation_list_path)
    return correlation_response


if __name__ == "__main__":
    import sys

    args = sys.argv
    globals()[args[1]](*args[2:])


"""
To find the dataframe within the start and end time interval to proceed with visualization
"""


def time_df(data, project_id, start, end):
    from datetime import datetime
    import pandas as pd
    import sys
    try:
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        dataframe = pd.DataFrame()
        pdf = data[data.ProjectId == project_id]
        for i in range(len(pdf)):
            time = datetime.strptime(pdf.Timestamp.iloc[i], '%Y-%m-%d %H:%M:%S.%f')
            if (time >= start_date) and (time <= end_date):
                dataframe = dataframe.append(pdf.iloc[i])
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in retrieving data for the specified timeframe")
    return dataframe


"""
To calculate the pearson correlation between each phase of RDLC and defined vectors for each phase
"""


def pearson_corr(rdlc_vectors, dataset):
    from scipy.stats import pearsonr
    corrl = []
    for phase in range(len(rdlc_vectors)):
        corr, _ = pearsonr(rdlc_vectors[phase], dataset)
        corrl.append(corr)
    return corrl


"""
To calculate cosine similarity between each phase of RDLC and defined vectors for each phase of project
"""


def cosine_similarity(rdlc_vectors, example_dataset):
    from numpy.linalg import norm
    import numpy as np
    cosine_sim = []
    for phase in range(len(rdlc_vectors)):
        cos_sim = np.dot(rdlc_vectors[phase], example_dataset) / (norm(rdlc_vectors[phase]) * norm(example_dataset))
        cosine_sim.append(cos_sim)
    return cosine_sim


"""
To scale the results for Pearson correlation in the range 0 to 1
"""


def normalize(list1):
    op = []
    for i in range(len(list1)):
        op.append((list1[i] - (-1)) / 2)
    return op


"""
This function evaluates the similarity and returns the correlation vectors and dataframe as response
"""


def evaluate_sim(data, start_date, end_date, eval_feature, eval_type, project_id, operation_list_path):
    import json
    import sys
    import numpy as np
    import pandas as pd

    if not operation_list_path:
        operation_list = ['Add Project', 'Edit Project', 'Open Resource(RCV)', 'Add Resource',
                          'Edit Resource', 'Delete Resource', 'Upload File', 'Upload MD', 'Download File',
                          'View MD', 'Delete File', 'Update File', 'Update MD', 'Open User Management',
                          'View Users', 'Add Member', 'Change Role', 'Remove User', 'Open Search',
                          'View Search Results', 'PID Enquiry', 'Create Application Profile',
                          'Admin Project Quota Change', 'Owner Project Quota Change', 'Owner Resource Quota Change',
                          'Invite External User', 'Archive Resource', 'Unarchive Resource']

        planning = [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0]
        production = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        analysis = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        archival = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        access = [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0]
        re_use = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]

    else:
        try:
            json_file_to_use = open(operation_list_path)
            jsonpath = json.load(json_file_to_use)
        except Exception as e:
            sys.exit(
                "Oops! " + str(e.__class__) + "occurred. Please verify the path of the json file for operational data.")
        try:
            operation_list = jsonpath["Operation_List"]
            planning = jsonpath["Planning"]
            production = jsonpath["Production"]
            analysis = jsonpath["Analysis"]
            archival = jsonpath["Archival"]
            access = jsonpath["Access"]
            re_use = jsonpath["Reuse"]
            json_file_to_use.close()
        except Exception as e:
            sys.exit("Oops! " + str(e.__class__) + " occurred. Please verify the contents of the json file for "
                                                   "operational data.")

    rdlc_vectors = [planning, production, analysis, archival, access, re_use]
    example_dataset_full = []
    example_dataset_binary__full = []

    if start_date != "" and end_date != "":
        df = time_df(data, project_id, start_date, end_date)
        if df.empty:
            sys.exit('There are no operations within the specified start and end date!')
    else:
        df = data[data.ProjectId == project_id]
    example_dataset = np.zeros(len(operation_list))
    example_dataset_binary = np.zeros(len(operation_list))

    project_filtered_df = list(df.Operation)

    for j in range(len(project_filtered_df)):
        if project_filtered_df[j] in operation_list:
            index_of_op = operation_list.index(project_filtered_df[j])
            example_dataset[index_of_op] = example_dataset[index_of_op] + 1
            example_dataset_binary[index_of_op] = 1

    example_dataset_full.append(example_dataset)
    example_dataset_binary__full.append(example_dataset_binary)
    correlation_response = []
    try:
        if eval_feature.lower() == "pearson":
            if eval_type.lower() == "weighted":
                corr_list_weighted = pearson_corr(rdlc_vectors, example_dataset)
                pearson_weighted = normalize(corr_list_weighted)
                correlation_response = pearson_weighted
            if eval_type.lower() == "binary":
                corr_list_binary = pearson_corr(rdlc_vectors, example_dataset_binary)
                pearson_binary = normalize(corr_list_binary)
                correlation_response = pearson_binary
        if eval_feature.lower() == "cosine":
            if eval_type.lower() == "weighted":
                cosine_weighted = cosine_similarity(rdlc_vectors, example_dataset)
                correlation_response = cosine_weighted
            if eval_type.lower() == "binary":
                cosine_binary = cosine_similarity(rdlc_vectors, example_dataset_binary)
                correlation_response = cosine_binary

    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in evaluating correlation_response.")

    categories = ['Planning', 'Production', 'Analysis', 'Archival', 'Access', 'Reuse']
    corr_data = pd.DataFrame(dict(RDLC_phase=categories, Correlation_value=correlation_response))
    return corr_data
