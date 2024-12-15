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
import time
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


folder_name = None  # Global variable to store folder name

def read_file(filepath):
    # Detect file encoding
    global folder_name
    try:
        with open(filepath, 'rb') as file:
            encoding_info = chardet.detect(file.read())  # Detect encoding
        file_encoding = encoding_info['encoding']
        
        # Read CSV file with detected encoding
        df = pd.read_csv(filepath, encoding=file_encoding)
        
        # Check if DataFrame is valid and not empty
        if isinstance(df, pd.DataFrame) and not df.empty:
            folder_name = filepath.split(".")[0]  # Extract folder name without extension
            os.makedirs(folder_name, exist_ok=True)  # Create directory
            return df  # Return the DataFrame
        else:
            print("Error: Empty or invalid file.")  # Handle invalid DataFrame
            return None
        
    except Exception as e:  # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None
    
df = read_file(sys.argv[1])

if df is None:
    print("Error: Invalid file type!! unable to convert file into dataframe")
    sys.exit(1)

# Function to analyze data and generate metadata
def get_metadata(df):

    # Generate summary statistics for numerical columns
    num_cols_summary = df.describe(include='number')  # Descriptive stats for numerical columns
    num_cols = list(num_cols_summary.columns)  # List of numerical column names

    # Generate summary statistics for categorical columns
    cat_cols_summary = df.describe(include='object')  # Descriptive stats for categorical columns
    cat_cols = list(cat_cols_summary.columns)  # List of categorical column names

    # Calculate missing values and their percentage for each column
    missing_values = df.isnull().sum()  # Total missing values per column
    missing_percentage = (missing_values / len(df)) * 100  # Percentage of missing values
    missing_df = pd.DataFrame({'column_name': df.columns , 'percentage': missing_percentage})  # Combine into a DataFrame

    # Calculate the correlation matrix for numerical columns
    corr_matrix = df[num_cols].corr()  # Correlation matrix for numerical columns only

    # Return all generated metadata
    return num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix

# Self Analysis in case llm code fails
def self_analysis(df):
    num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix = get_metadata(df)

    if len(num_cols) > 0:

        # Correlation matrix and its plot
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.xticks(rotation=45)  # Rotate column names for readability
        plt.savefig(f"{folder_name}/correlation_matrix.png", bbox_inches='tight')
        plt.close()

        # Bar Plot of Missing value
        missing_df_sorted = missing_df.sort_values(by='percentage', ascending=False)
        plt.figure(figsize=(8,12))
        sns.barplot(y='column_name', x='percentage', data=missing_df_sorted, hue='column_name', legend=False)
        plt.title('percentage of Missing Values in Each Column')
        plt.xlabel('Columns')
        plt.ylabel('percentage of Missing Values')
        plt.savefig(f"{folder_name}/missing_values.png", bbox_inches='tight')
        plt.close()


        # Boxplot for all numerical columns
        df_melted = df[num_cols].melt(var_name="Columns", value_name="Values")
        plt.figure(figsize=(8,12))
        sns.boxplot(data=df_melted, x="Values", y="Columns", width=0.2)
        plt.title("Summary Statistics (Box Plot) for Num Cols")
        plt.savefig(f"{folder_name}/boxplot_num_cols.png", bbox_inches='tight')
        plt.close()

    if len(cat_cols) > 0:


        # Loop through the categorical columns and calculate unique categories
        unique_counts = [df[col].nunique() for col in cat_cols]
        # Create a bar plot
        plt.figure(figsize=(10, 6))
        plt.bar(cat_cols, unique_counts)
        plt.xlabel('Categorical Columns')
        plt.ylabel('Number of Unique Categories')
        plt.title('Number of Unique Categories for Each Categorical Column')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{folder_name}/unique_counts_cat_cols.png", bbox_inches='tight')
        plt.close()

## llm code for data anlysis
def llm_code_for_data_analysis():

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
            inside the function call get_metadata(df) and store the output in the variables num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix

            now you have all the necessary variables

            do the following
            1. create a bar plot of missing  values, missing_df has the missing values data which is stored in a dataframe and have two columns one showing the column name and other showing the percentage of missing values you might need to sort the dataframe by the percentage column
            finally save the plot using the plt.savefig("{folder_name}/missing_values.png", bbox_inches='tight')

            2. the num_cols represents numerical columns and you need to create a correlation matrix plot for numerical columns and save the plot using the plt.savefig("{folder_name}/correlation_matrix.png", bbox_inches='tight')

            3. create a boxplot for all numerical columns to detect outliers and save the plot using the plt.savefig("{folder_name}/boxplot_num_cols.png", bbox_inches='tight')

            4. the cat_cols represents all categorical columns, create a bar plot for number of Unique Categories for Each Categorical Column and save the plot using the plt.savefig("{folder_name}/mean_as_bar_plots.png", bbox_inches='tight')

            finally based on the name of columns and column info you can do some more analysis as you wish and if you can, create few more plots  too and if you create plots make sure you save the plots as you did in step 1-4 and apply plt.close() after each plot

            make sure you enhance plots/charts with titles, axis labels, legends, and annotations, and uses colors effectively


            your output should contain python code only and nothing else comments are fine

            you are only allowed to use the following modules: numpy, pandas, matplotlib, seaborn

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
        output = result['choices'][0]['message']['content'] 
        time_threshold = 60
        start_time = time.time()

        for _ in range(1,11):
            try:
                if time.time() - start_time > time_threshold:
                    print('Maximum time limit reached discarding the llm generated code' + "\n")
                    break
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

                error_type = type(e).__name__  
                error_message = str(e)   
                caused_error = f"{error_type}: {error_message}"

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

            there are few plots available to you which is stored in the folder {folder_name}

            the names of the plots are {png_files_str} separated by commas
            the names are descriptive enough and it tells about what type of plot it is,

            for example,
            boxplot_num_cols.png which is a box plot for numerical columns, 
            correlation_matrix.png which is a correlation matrix,
            missing_values.png which shows the percentage of missing values of each columns and
            mean_as_bar_plots.png which is plot forsummary statistics of numerical columns
            there might be other plots as well

            assume that proper analysis is done and all the data provided to you are good and well analysed

            you need to create a story about this dataset 
            be as descriptive as possible,
            be comprehensive,
            do not leave any small information,
            try to make it as longer as possible,
            try to read all the content provided as much as you can and find something interesting out of it and add it to the ,
            you are free to use your own creativity in the ,
            you can add your own insights from all the experiece you have in the world,
            write some summary about each column and plots,
            add recommendations to the reader or developer
            also must embed all the plot images in the story for link of the image use ![image description](image_file_name.png) do not put folder name in the image name

            the story should includes relevant results, ensures proper Markdown formatting, logically sequences the narratives (data description, analysis, insights, implications), integrates visualizations at the right places, and  emphasizes significant findings and implications

            the story should show some deep understanding of the dataset, and should not be too short.
        
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
        output = result['choices'][0]['message']['content'] 

        cleaned_output = output.replace("```markdown", "").replace("```", "").strip()

        with open(f"{folder_name}/readme.md", 'w') as f:
            f.write(cleaned_output)


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
        be as descriptive as possible,
        be comprehensive,
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

        cleaned_output = output.replace("```markdown", "").replace("```", "").strip()

        # Save the output to README.md
        readme_path = os.path.join(folder_name, 'readme.md')
        with open(readme_path, 'w') as f:
            f.write(cleaned_output)

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
    num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix = get_metadata(df)

    cleaned_output = llm_code_for_data_analysis()
    exec(cleaned_output, globals())  # Execute the cleaned_output

    try:

        llm_analysis()
        print("Analysis completed using llm only")
        print("Now creating a story for the dataset...")
        
    except Exception as e:
        print("Something is wrong with LLM code")
        self_analysis(df)
        
    try:
        llm_response_with_function_calling()
        print('Story created with function calling successfully!!')
        llm_response(num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name)

    except:
        llm_response(num_cols, num_cols_summary, cat_cols, cat_cols_summary, missing_df, corr_matrix, folder_name)
        print('Story created successfully!!')
