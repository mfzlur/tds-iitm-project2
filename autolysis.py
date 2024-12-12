# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pandas",
#   "numpy",
#   "matplotlib",
#   "seaborn",
#   "chardet",
#   "requests",
#   "python-dotenv",
# ]
# ///

import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pandas as pd
import os
import numpy as np
import chardet
import requests

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the variables
openai_api_key = os.getenv("OPENAI_PROXY_API_KEY")
openai_api_key_personal = os.getenv("OPENAI_KEY")

global df
df = None

# read the file, convert it into dataframe and make directory with filename
folder_name = None
def read_file(filepath):
    global folder_name
    try:
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
            # print(result)
        df = pd.read_csv(filepath, encoding=result['encoding'])
        # Check if df is a valid DataFrame and is not empty
        if isinstance(df, pd.DataFrame) and not df.empty:
            # print('df is a valid DataFrame and is not empty.')
            folder_name = filepath.split(".")[0]
            os.makedirs(folder_name, exist_ok=True)
            return df
        else:
            print("The DataFrame is empty or not a valid DataFrame.")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
df = read_file(sys.argv[1])


# Data Analysis and creating plot images
def get_metadata(df):
    pd.set_option('display.max_columns', None)
    
    # summary stats of numerical cols
    num_cols_summary = df.describe(include='number')
    num_cols = list(num_cols_summary.columns)

    # summary stats of categorical cols
    cat_cols_summary = df.describe(include='object')
    cat_cols = list(cat_cols_summary.columns)


    # Missing values of each cols and percentage
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_df = pd.DataFrame({'column_name': missing_values, 'percentage': missing_percentage})

    corr_matrix = df[num_cols].corr()


    return num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name

def self_analysis(df):
    num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name = get_metadata(df)

    # Correlation matrix and its plot
    corr_matrix = df[num_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.xticks(rotation=45)  # Rotate column names for readability
    plt.savefig(f"{folder_name}/correlation_matrix.png", bbox_inches='tight')
    plt.close()

    # Bar Plot of Missing value
    missing_df_sorted = missing_df.sort_values(by='percentage', ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing_df.index, y='percentage', data=missing_df_sorted, hue=missing_df_sorted.index, legend=False)
    plt.title('Percentage of Missing Values in Each Column')
    plt.xlabel('Columns')
    plt.ylabel('Percentage of Missing Values')
    plt.xticks(rotation=45)
    plt.savefig("media/missing_values.png", bbox_inches='tight')
    plt.close()


    # Boxplot for all numerical columns
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=num_cols_summary)
    plt.title("Summary Statistics (Box Plot) for Num Cols")
    plt.xticks(rotation=45)
    plt.savefig(f"{folder_name}/boxplot_num_cols.png", bbox_inches='tight')
    plt.close()


    # Extracting mean and standard deviation for numerical columns
    means = num_cols_summary.loc['mean']
    stds = num_cols_summary.loc['std']

    # Plot the means as a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(means.index, means, yerr=stds, capsize=5)
    plt.xticks(rotation=45)
    plt.title("Mean with Standard Deviation (Summary Stats)")
    plt.ylabel("Value")
    plt.savefig(f"{folder_name}/mean_as_bar_plots.png", bbox_inches='tight')
    plt.close()

# llm_analysis = None

## llm code for data anlysis
def llm_code_for_data_analysis():
    # global llm_analysis
    api_key = openai_api_key

    # API endpoint
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    global folder_name
    global existing_code
    global caused_error
    existing_code = None
    caused_error = None
    

    prompt = f"""
            code provided by you is {existing_code}
            error on this code is {caused_error}

            if existing_code and caused_error is None do the following
    
            so you need to write python code create some plots

            write a function called "llm_analysis" without any arguements
            do not import any modules inside code assume all the necessary modules are already imported in my main script
            inside the function call get_metadata(df) and store the output in the variables num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name

            now you have all the necessary variables

            do the following
            1. create a bar plot of missing  values missing_df has the missing values data which is stored in a dataframe and have two columns one showing the column name and other showing the percentage of missing values you might need to sort the dataframe by the percentage column
            finally save the plot using the plt.savefig("{folder_name}/missing_values.png", bbox_inches='tight')

            2. the num_cols represents numerical columns and you need to create a correlation matrix plot for numerical columns and save the plot using the plt.savefig("{folder_name}/correlation_matrix.png", bbox_inches='tight')

            3. create a boxplot for all numerical columns to detect outliers and save the plot using the plt.savefig("{folder_name}/boxplot_num_cols.png", bbox_inches='tight')

            4. create a bar plot of mean and standard deviation for numerical columns and save the plot using the plt.savefig("{folder_name}/mean_as_bar_plots.png", bbox_inches='tight')

            finally based on the name of columns and column info you can do some more analysis as you wish and if it makes sense and if you create plots make sure you save the plots as you did in step 1-4

            make sure you enhance plots/charts with titles, axis labels, legends, and annotations, and uses colors effectively


            your output should contain code only and nothing else comments are fine

            there should not be any text outside the code block it should be only code its like when i copy paste the entire output and run it it should work

            otherwise if existing_code and caused_error is not None do the following
            figure out the solution for the error and rewrite the whole code
            again output should be code only
            """

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Request data
    data = {
        "model": "gpt-4o-mini",  
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Make the API call
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        # print(result)  # Print the response from OpenAI
        output = result['choices'][0]['message']['content'] 

        for _ in range(1,11):
            try:
                cleaned_output = output.replace('```python', '').replace('```', '').strip()
                exec(cleaned_output, globals())  # Execute in the global scope
                llm_analysis()

                print(f'Hurray! LLM code worked and executed successfully without any errors on attempt no: {_}')
    
                break
            except Exception as e:
                if _ == 10:
                    print('Maximum Attempts reached discarding the llm generated code' + "\n")
                    break
         
                print(f'Attempt no: {_} for llm generated code execution' + "\n")
                print(f'llm generated code is not getting executed because of the error: {e}' + "\n") 
                print('promting with the error message to the llm again to rewrite the code to make it work' + "\n")
                
                caused_error = e
                existing_code = cleaned_output
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                output = result['choices'][0]['message']['content']


        return output.replace('```python', '').replace('```', '').strip()


    else:
        print(f"Error: {response.status_code}, {response.text}")

    

# openai proxy response
def llm_response(num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name):
    api_key = openai_api_key

    png_files = []

    for file_name in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file_name)
        # Check if it's a file and has '.png' extension
        if os.path.isfile(file_path) and file_name.lower().endswith('.png'):
            png_files.append(file_name)

    png_files_str = ', '.join(png_files)

    # API endpoint
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    prompt = f"""
            Here is the information already available about the data:
            the numercal columns are {num_cols},
            the categorical columns are {cat_cols},
            the summary statistics of numerical column is {num_cols_summary},
            the summary statistics of categorical column is {cat_cols_summary},
            the missing statistics is stored as dataframe with column name and percentage of missing values and the values are {missing_df} and 
            correlation matrix is {corr_matrix}

            there are few plots available too and their analysis text is available in the folder {folder_name} and their names are

            the names of the plots are {png_files_str} separated by commas
            the names are descriptive enough and it tells about what type of plot it is for example

            boxplot_num_cols.png which is a box plot for numerical columns, 
            correlation_matrix.png which is a correlation matrix,
            missing_values.png which shows the percentage of missing values of each columns and
            mean_as_bar_plots.png which is plot forsummary statistics of numerical columns
            there might be other plots as well

            you need to create a story about this dataset 
            be as descriptive as possible,
            do not leave any small information,
            try to make it as longer as possible,
            try to read all the content provided as much as you can and find something interesting out of it and add it to the ,
            you are free to use your own creativity in the ,
            you can add your own insights from all the experiece you have in the world,
            write some summary about each column and plots,
            add recommendations to the reader or developer
            also must embed the summary plot images in the story for link of the image use ![image description](image_file_name.png)

            the story should includes relevant results, ensures proper Markdown formatting, logically sequences the narratives (data description, analysis, insights, implications), integrates visualizations at the right places, and  emphasizes significant findings and implications
        
            the story will be written in readme.md file so give the text output such that the output can directly be pasted at readme.md 
            """

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Request data
    data = {
        "model": "gpt-4o-mini",  
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Make the API call
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        # print(result)  # Print the response from OpenAI
        output = result['choices'][0]['message']['content'] 
        with open(f"{folder_name}/readme.md", 'w') as f:
            f.write(output)


    else:
        print(f"Error: {response.status_code}, {response.text}")

def llm_response_with_function_calling():
    # Retrieve metadata
    num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name = get_metadata(df)



    api_key = openai_api_key

    # Serialize missing_df and corr_matrix for readability
    missing_df_serialized = missing_df.to_dict(orient='records')
    corr_matrix_serialized = corr_matrix.to_dict()

    # Retrieve PNG file names in the folder
    png_files = []
    for file_name in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith('.png'):
            png_files.append(file_name)

    png_files_str = ', '.join(png_files)

    # API endpoint
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    # Pass metadata into the story generation prompt
    prompt = f"""
    Here is the information already available about the data:
    - Numerical columns: {num_cols}
    - Numerical summary: {num_cols_summary}
    - Categorical columns: {cat_cols}
    - Categorical summary: {cat_cols_summary}
    - Missing statistics: {json.dumps(missing_df_serialized, indent=2)}
    - Correlation matrix: {json.dumps(corr_matrix_serialized, indent=2)}

    There are few plots available in the folder '{folder_name}' and their names are:
    {png_files_str}

    You need to create a detailed story about this dataset:
    - Be descriptive and comprehensive.
    - Include insights about each column and the available plots.
    - Add recommendations for further analysis or actions.
    - Embed the plot images using Markdown syntax like ![image description](image_file_name.png).
    - The story should follow logical formatting suitable for a README.md file.
    

    Generate the story such that it can be directly copied and pasted into a README.md file.
    """

    # API request for story generation
    story_data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Make the API call
    story_response = requests.post(url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }, json=story_data)

    if story_response.status_code == 200:
        story_result = story_response.json()
        output = story_result['choices'][0]['message']['content']

        # Save the output to README.md
        readme_path = os.path.join(folder_name, 'readme.md')
        with open(readme_path, 'w') as f:
            f.write(output)

        print("README.md generated successfully.")

    else:
        print(f"Error in story generation: {story_response.status_code}, {story_response.text}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} does not exist.")
        sys.exit(1)
    
    df = read_file(filepath)
    num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name = get_metadata(df)

    cleaned_output = llm_code_for_data_analysis()
    exec(cleaned_output, globals())  # Execute the cleaned_output

    try:

        llm_analysis()
        print("Analysis completed using llm only")
        
    except Exception as e:
        print("Something is wrong with LLM code")
        self_analysis(df)
        
    try:
        llm_response_with_function_calling()

    except:
        llm_response(num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name)

    print('Story created successfully!!')



