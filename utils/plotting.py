# import matplotlib.pyplot as plt
import io
import re

# def execute_plot_code(code_block, df):
#     """Execute matplotlib code and return the plot as bytes"""
#     plt.clf() 
#     try:
#         exec(code_block, {'df': df, 'plt': plt})
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png', bbox_inches='tight')
#         plt.close()
#         buf.seek(0)
#         return buf
#     except Exception as e:
#         print(f"Plot execution error: {str(e)}")
#         return None

# def extract_python_code(text):
#     """Extract code between python code block markers"""
#     pattern = r"Action Input:\n(.*?)\n```"
#     match = re.search(pattern, text, re.DOTALL)
#     return match.group(1).strip() if match else None

def fetch_plot_image(image_path):
    """Fetch plot image data"""
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            return image_file.read()
    else:
        return None

def extract_plot_image(text):
    """Extract plot image URL"""
    pattern = r"Observation:\n!\[Plot\]\((.*?)\)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None