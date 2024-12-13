````markdown
# BookGen: AI-Powered Book Generation with Gemini and ReportLab

BookGen is a Python script that leverages Google's Gemini generative AI model to automatically create the outline and content of a book, and then formats it into a professional-looking PDF using ReportLab. It also generates a plain text version of the book.

## Features

- **Automated Book Outline Generation:** Generates a structured book outline with chapters and subchapters based on a given title and desired number of chapters/subchapters.
- **AI-Powered Content Creation:** Uses the Gemini model to write detailed content for each subchapter, ensuring a comprehensive and engaging book.
- **Dynamic PDF Generation:** Creates a well-formatted PDF document with customizable styles, including title, headings, body text, and first paragraph indentation.
- **Plain Text Output:** Generates a `.txt` file containing the complete book content for easy access and further processing.
- **Error Handling and Retries:** Includes robust error handling to manage potential issues during content generation, with automatic retries to ensure completion.
- **Dynamic Filenames:** Generates unique filenames for the PDF and text files based on the book title and current timestamp, preventing accidental overwrites.

## Prerequisites

- Python 3.7 or higher
- A Google AI Studio API key for the Gemini model

## Installation

1. Clone this repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Configure API Key:**

   - Open the `bookgen.py` file.
   - Replace `"AIzxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"` in the line `genai.configure(api_key="AIzxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")` with your actual Google AI Studio API key.

2. **Set Book Parameters:**

   - Modify the following variables in `bookgen.py` to customize your book:
     - `book_title`: The title of your book (e.g., `"Test-Time Compute: The Next Frontier in AI Scaling"`).
     - `num_chapters`: The desired number of chapters (e.g., `5`).
     - `num_subchapters`: The desired number of subchapters per chapter (e.g., `10`).

3. **Run the Script:**

   ```bash
   python.exe .\bookgen.py
   ```

   The script will generate the book outline, write the content, and create both a PDF and a `.txt` file in the same directory. The filenames will be dynamically generated based on the book title and timestamp.

## Example Output

The script will generate two files:

- `[book_title]_[timestamp].pdf`: The formatted PDF version of the book.
- `[book_title]_[timestamp].txt`: The plain text version of the book.

## Customization

- **PDF Styling:** You can further customize the PDF's appearance by modifying the styles in the `bookgen.py` file. Refer to the ReportLab documentation for more details on styling options.
- **Gemini Model Parameters:** Adjust the `temperature`, and `top_p`, and `max_output_tokens` parameters to fine-tune the generated content's creativity and length.

## Troubleshooting

- **API Key Errors:** Ensure that your API key is correctly configured and that you have access to the Gemini model.
- **Generation Errors:** If the script encounters errors during content generation, it will print debug messages and retry after a short delay. If errors persist, check your network connection and the Gemini model's availability.

## License

This project is licensed under the MIT License

## Keywords

Book generation, AI book generation, automated book writing, book outline generation, AI-powered book creation, PDF book generation, text book generation, Gemini book generator, Gemini book generation
````
