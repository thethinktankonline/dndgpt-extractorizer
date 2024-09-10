import pandas as pd
import os
from datetime import datetime

def compare_files(file1, file2, report_file='dndgpt_compare_report.csv'):
    # Load the two CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Ensure the columns are in the same order
    df2 = df2[df1.columns]
    
    # Align the indices (optional, but recommended)
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    # Check if the DataFrames are identical
    if df1.equals(df2):
        print("The files are identical. No differences found.")
        return
    
    # If they are not identical, compare them
    comparison_df = df1.compare(df2)

    # Calculate total rows and columns compared
    total_rows = len(df1)
    total_columns = len(df1.columns)
    total_cells = total_rows * total_columns

    # Calculate the number of differing cells (avoiding double-counting)
    differing_cells = comparison_df.notna().sum().sum() // 2
    difference_percentage = (differing_cells / total_cells) * 100

    # Simplified summary: sum up the differences across columns
    summary = comparison_df.count(axis=0) // 2  # Divide by 2 to combine self/other
    summary = summary[summary > 0].to_frame(name='Total Differences')
    summary['Difference Percentage'] = (summary['Total Differences'] / total_rows) * 100

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the text report
    data_folder = os.path.join('..', 'data')
    text_report_path = os.path.join(data_folder,'reports','dndgpt_compare_report.txt')
    
    with open(text_report_path, 'w') as text_file:
        # Write the header information
        text_file.write(f"Comparison Report\n")
        text_file.write(f"Files compared: {file1} and {file2}\n")
        text_file.write(f"Timestamp: {timestamp}\n")
        text_file.write(f"Differences found! The files differ in {difference_percentage:.2f}% of the data.\n")
        text_file.write(f"Total rows compared: {total_rows}\n")
        text_file.write(f"Total columns compared: {total_columns}\n")
        text_file.write(f"Total cells compared: {total_cells}\n")
        text_file.write(f"Total differing cells: {differing_cells}\n")
        text_file.write(f"Columns with differences: {len(summary)}\n")
        text_file.write("\nSummary of Differences by Column:\n")
        text_file.write(summary.to_string())
        text_file.write("\n\nDetailed Differences:\n")
        text_file.write(comparison_df.to_string())
    
    print(f"Text report saved to: {text_report_path}")

    # Export the summary and comparison report to CSV files
    summary_path = os.path.join(data_folder,'reports','dndgpt_compare_summary.csv')
    details_path = os.path.join(data_folder, report_file)
    
    summary.to_csv(summary_path)
    comparison_df.to_csv(details_path)

    print(f"Summary saved to: {summary_path}")
    print(f"Detailed comparison saved to: {details_path}")

if __name__ == "__main__":
    # Define your file paths
    file1 = os.path.join('..','data','finished_spreadsheets','dndgpt_monsters_7.csv')
    file2 = os.path.join('..','data','finished_spreadsheets','dndgpt_monsters_6.csv')
    
    # Call the comparison function
    compare_files(file1, file2)
