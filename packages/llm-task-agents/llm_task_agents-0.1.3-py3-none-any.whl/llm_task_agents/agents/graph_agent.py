from ollama import Client
import re
import pandas as pd
import io
import darkdetect
import json
import base64
from typing import Tuple, Optional
import plotly.graph_objects as go
import plotly.io as pio

class GraphAgent:
	def __init__(
		self,
		llm_api_url: str,
		model: str,
		debug: bool = False,
	):
		self.debug = debug

		# LLM configurations
		self.llm_api_url = llm_api_url
		self.model = model

		self.llm = Client(host=llm_api_url)

	def run(self, user_request: str, df: pd.DataFrame, max_retry: int = 3) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
		# Build prompts with a preview of the DataFrame (df.head())
		prompts = self.build_prompts(user_request=user_request, df=df)
		original_prompt = prompts["prompt"]

		# Retry loop for generating the correct figure
		for retry in range(max_retry):
			try:
				# Query LLM with the provided prompts
				response = self.llm.generate(
					model=self.model,
					system=prompts["system_prompt"],
					prompt=prompts["prompt"],
					format="json",
					stream=False
				)

				if "response" in response:
					# Extract JSON figure description and graph title from the LLM response
					extracted_values = self.extract_json_description(
						llm_response=response["response"],
						expected_json_keys=["fig_json", "graph_title"]
					)

					if extracted_values and len(extracted_values) == 2:
						json_fig_description, graph_title = extracted_values
						graph_title = graph_title.strip()
					else:
						print(f"Attempt {retry + 1}: Failed to extract required keys from response.")
						continue  # Proceed to the next retry

					print("extracted_values", extracted_values)

					try:
						# Replace column names in the JSON with actual DataFrame values
						for trace in json_fig_description['data']:
							# Use the column names provided by the LLM for x and y values
							x_col = trace['x']
							y_col = trace['y']
							
							trace['x'] = df[x_col]  # Replace with actual data from the DataFrame
							trace['y'] = df[y_col]  # Replace with actual data from the DataFrame

						# Create the figure from the LLM-provided JSON description
						fig = go.Figure(json_fig_description)

						# Set layout options if desired
						background_color = '#181A1B' if darkdetect.isDark() else 'white'
						fig.update_layout(
							plot_bgcolor=background_color,
							paper_bgcolor=background_color,
							width=None,
							height=400
						)

						# Convert figure to SVG bytes and decode to string
						svg_bytes = fig.to_image(format="svg")
						svg_str = svg_bytes.decode('utf-8')

						# Encode SVG bytes as base64
						img_base64 = base64.b64encode(svg_bytes).decode('ascii')

						# Generate interactive HTML representation of the figure
						html_str = fig.to_html(full_html=False, include_plotlyjs='cdn')

						# Return the SVG string, base64-encoded image, and graph title
						return html_str, svg_str, img_base64, graph_title

					except Exception as e:
						print(f"Error creating figure from JSON: {e}")
						print(f"Previous attempt {retry + 1}:\n{json_fig_description}\n\nExecution error:\n{str(e)}")

						# Update the prompt with each appended error for the next retry
						prompts["prompt"] = (
							f"{original_prompt}\n\n"
							"The previous JSON description resulted in an error:\n"
							f"{str(e)}\n\n"
							"Please revise the JSON to fix the error."
						)
				else:
					print(f"Attempt {retry + 1}: No response from LLM.")

			except Exception as e:
				print(f"Error querying LLM: {e}. Retrying with the same prompt.")

		return None, None, None, None

	def extract_json_description(self, llm_response, expected_json_keys=None):
		try:
			# Attempt to parse the response as JSON
			parsed_json = json.loads(llm_response)
			if expected_json_keys:
				# Extract the values for the expected keys
				extracted_values = [parsed_json.get(key) for key in expected_json_keys]
				if all(extracted_values):
					return extracted_values
				else:
					return []
			else:
				return []
		except json.JSONDecodeError:
			# If JSON parsing fails, attempt to extract JSON from within code fences
			code_block_pattern = re.compile(r'```(?:json|python)?\n(.*?)```', re.DOTALL)
			matches = code_block_pattern.findall(llm_response)
			for match in matches:
				try:
					parsed_json = json.loads(match)
					if expected_json_keys:
						extracted_values = [parsed_json.get(key) for key in expected_json_keys]
						if all(extracted_values):
							return extracted_values
					else:
						continue
				except json.JSONDecodeError:
					continue
			return []

	def remove_leading_based_on_second_line(self, text: str) -> str:
		# Split the text into lines
		lines = text.splitlines()

		if len(lines) < 2:
			return text.strip()  # If there's only one line, return the stripped version

		# Detect the leading spaces or tabs on the second line
		second_line = lines[1]
		leading_whitespace = ''
		for char in second_line:
			if char in (' ', '\t'):
				leading_whitespace += char
			else:
				break

		# Process each line starting from the second one
		stripped_lines = []
		for line in lines:
			if line.startswith(leading_whitespace):
				# Remove the detected leading whitespace from each line
				stripped_lines.append(line[len(leading_whitespace):])
			else:
				stripped_lines.append(line)

		# Join the lines back together and return the result
		return "\n".join(stripped_lines).strip()

	def build_prompts(self, user_request: str, df: pd.DataFrame) -> dict:
		system_prompt = """
		You are an assistant tasked with generating engaging and colorful Plotly figures from JSON descriptions. Follow these guidelines:

		- You will be provided with a pandas DataFrame and a user request.
		- Analyze the DataFrame and the user's request to design the most informative and appropriate visualization.
		- Automatically select the most suitable Plotly graph type based on the structure and content of the DataFrame and the user's needs. Use the following Plotly types:

		- **Scatter** with `"mode": "lines+markers"` should be used for line graphs or trends over time. **Do not use `"type": "line"`; use `"type": "scatter"`** for line charts.
		- **Bar** for comparing categorical data.
		- **Histogram** for displaying frequency distributions of a single variable.
		- **Pie** for showing proportions or percentages of a whole.
		- **Box** for summarizing distributions across groups using medians and quartiles.
		- **Heatmap** for visualizing intensity or correlation between two variables using colors.
		- **Violin** for comparing distributions and densities across groups.
		- **Bubble Chart** for showing relationships between three variables (x, y, and size of points).
		- **Scatter3D** for exploring relationships between three variables in three-dimensional space.
		- **Contour** for representing three-dimensional data in two dimensions using contour lines.
		- **Sunburst** for visualizing hierarchical data with nested sectors.
		- **Treemap** for displaying hierarchical data as nested rectangles.
		- **Candlestick** for illustrating financial data (open, high, low, close prices over time).
		- **Sankey** for depicting flow or transfers between entities.
		- **Parallel Coordinates (Parcoords)** for comparing multivariate data across many dimensions.

		- Always ensure the "data" section of the figure JSON is a **list of dictionaries**, with each dictionary specifying the `type` property explicitly (e.g., `{"type": "scatter"}`). Do not rely on the automatic inference of the graph type. Ensure that each dictionary in the "data" section conforms to Plotly's figure schema.

		- Instead of passing raw data for the `"x"` and `"y"` fields, use the column names from the DataFrame (e.g., `"x": "Month"`, `"y": "TotalIncome"`).
		- Include the necessary metadata directly in the JSON description. Do not use placeholders.
		- Set an appropriate and descriptive title for the figure in the JSON layout.
		- Ensure the JSON is syntactically correct and follows the Plotly figure schema.
		- The output must be valid JSON. Do not include any additional text or commentary.

		Output format:
		{
			"graph_title": "<appropriate graph title>",
			"fig_json": {
				"data": [
					{
						"x": "<column name for x-axis>",  # specify the column name
						"y": "<column name for y-axis>",  # specify the column name
						"type": "<graph type>",  # e.g., 'scatter', 'bar', etc.
						"mode": "<optional mode>",  # e.g., 'lines', 'markers', 'lines+markers'
						"name": "<series name>"  # Optional
					}
				],
				"layout": {
					"title": "<appropriate graph title>",
					"xaxis": {
						"title": "<x-axis label>"
					},
					"yaxis": {
						"title": "<y-axis label>"
					}
				}
			}
		}
		"""

		prompt_template = """
		User request: {user_request}

		DataFrame info:
		{dataframe_info}

		DataFrame describe:
		{dataframe_describe}

		DataFrame shape:
		{dataframe_shape}

		DataFrame types:
		{dataframe_types}

		DataFrame head:
		{dataframe_head}

		Only answer with the following JSON structure:
		{{
			"graph_title": "<appropriate graph title>",
			"fig_json": {{
				<Plotly figure JSON description, use '<<data>>' as a placeholder for data>
			}}
		}}
		"""

		# Capture DataFrame info as a string
		buffer = io.StringIO()
		df.info(buf=buffer)
		dataframe_info = buffer.getvalue()

		prompt = prompt_template.format(
			user_request=user_request,
			dataframe_info=dataframe_info.strip(),
			dataframe_describe=df.describe().to_string().strip(),
			dataframe_shape=df.shape,
			dataframe_types=df.dtypes.to_string().strip(),
			dataframe_head=df.head(10).to_string().strip()  # Increased from head() to head(10)
		)

		# Clean up prompts
		system_prompt = self.remove_leading_based_on_second_line(system_prompt)
		prompt = self.remove_leading_based_on_second_line(prompt)

		if self.debug:
			print("System Prompt:")
			print(system_prompt)
			print("\nUser Prompt:")
			print(prompt)

		return {
			"system_prompt": system_prompt,
			"prompt": prompt
		}
