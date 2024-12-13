import google.generativeai as genai
import typing_extensions as typing
import json
import time
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
import datetime
import os

# -------------- CONFIGURE THESE VALUES -------------- #

genai.configure(api_key="AIzxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
modelName="gemini-2.0-flash-exp"
book_title = "Test-Time Compute: The Next Frontier in AI Scaling"
num_chapters = 1
num_subchapters = 5
modelTemperature = 0 # leave it a 0 if you don't know what you are doing
modelTopP = 0.95 # leave it a 0.95 if you don't know what you are doing
modelMaxOutputTokens = 8192 # leave it a 8192 if you don't know what you are doing
# --------------  END OF CONFIGURATION  -------------- #

class Subchapter(typing.TypedDict):
    subchapter_title: str

class Chapter(typing.TypedDict):
    chapter_title: str
    subchapters:list[Subchapter]

class BookOutline(typing.TypedDict):
    book_title: str
    chapters: list[Chapter]

model = genai.GenerativeModel(modelName)  # Using gemini-pro as it is more reliable for complex tasks

def create_dynamic_filename(book_title):
  """
  Generates a dynamic PDF filename based on the book title and current timestamp.

  Args:
    book_title: The title of the book.

  Returns:
    A string representing the dynamic PDF filename.
  """

  # 1. Sanitize the book title for filename
  sanitized_title = "".join(c for c in book_title if c.isalnum() or c in (' ', '.', '-', '_')).rstrip()
  sanitized_title = sanitized_title.replace(" ", "_").lower()

  # 2. Get the current timestamp
  now = datetime.datetime.now()
  timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS

  # 3. Construct the dynamic filename
  pdf_filename = f"{sanitized_title}_book_{timestamp}"

  return pdf_filename


# --- First Call: Generate Chapter Titles ---
prompt_chapters = f"""
Generate {num_chapters} chapter titles and for each chapter title, {num_subchapters} sub-chapter titles for a book about the {book_title}.
"""

print(f"DEBUG: Generating outline for book {book_title}")  # Debug print

result_chapters = model.generate_content(
    prompt_chapters,
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=BookOutline,
        temperature=modelTemperature,
        top_p=modelTopP,
        max_output_tokens=modelMaxOutputTokens,
    ),
)

chapter_titles = result_chapters.candidates[0].content.parts[0].text
chapter_titles = eval(chapter_titles)

# --- Second Call & Beyond: Iteratively Generate Content ---

book_content = ""
book_title = chapter_titles.get("book_title", book_title)

# Initialize book_content as a list for ReportLab elements
book_content_elements = []
book_content_text = ""  # Separate string for the .txt file

# --- PDF Setup with ReportLab ---
pdf_filename = f"{create_dynamic_filename(book_title)}.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                        rightMargin=inch, leftMargin=inch,
                        topMargin=inch, bottomMargin=inch)
styles = getSampleStyleSheet()

# Customize existing styles instead of adding new ones with the same name
styles['Title'].fontSize = 28
styles['Title'].alignment = 1  # Center alignment
styles['Title'].leading = 14
styles['Title'].spaceAfter = inch

styles['Heading1'].fontSize = 22
styles['Heading1'].spaceAfter = inch * 0.5

styles['Heading2'].fontSize = 16
styles['Heading2'].spaceAfter = inch * 0.25

# Create a new style for the first paragraph
styles.add(ParagraphStyle(name='FirstParagraph',
                          parent=styles['BodyText'],
                          firstLineIndent=0.5 * inch,
                          fontSize = 11,
                          leading = 14,
                          alignment = 4))

styles['BodyText'].fontSize = 11
styles['BodyText'].leading = 14
styles['BodyText'].alignment = 4  # Justified alignment

# Add Title to PDF
book_content_elements.append(Paragraph(book_title, styles['Title']))
book_content_text += f"# {book_title}\n\n"

for chapter_index, chapter in enumerate(chapter_titles["chapters"]):
    chapter_title = chapter["chapter_title"]
    book_content_text += f"## Chapter {chapter_index + 1}: {chapter_title}\n\n"
    book_content_elements.append(Paragraph(f"Chapter {chapter_index + 1}: {chapter_title}", styles['Heading1']))
    print(f"  DEBUG: Starting Chapter {chapter_index + 1}: {chapter_title}")  # Debug print

    for subchapter in chapter["subchapters"]:
        subchapter_title = subchapter["subchapter_title"]
        book_content_elements.append(Paragraph(subchapter_title, styles['Heading2']))
        book_content_text += f"### {subchapter_title}\n\n"
        print(f"    DEBUG: Starting Subchapter {subchapter_title}")  # Debug print

        prompt_sections = f"""
        Write the content for the subchapter titled '{subchapter_title}' in the chapter '{chapter_title}' of a book about {book_title}. Only output the content, don't output the subchapter title, chapter title and book title. Do not use any markdowns. Make it as detailed as you can.
        """

        while True:
            try:
                result_sections = model.generate_content(
                    prompt_sections,
                    generation_config=genai.GenerationConfig(
                        temperature=modelTemperature,
                        top_p=modelTopP,
                        max_output_tokens=modelMaxOutputTokens,
                    ),
                )
                sections_text = result_sections.text
                # Split the text into sections based on double newlines
                sections = sections_text.split('\n\n')
                # Iterate through each section
                for i, section in enumerate(sections):
                    # Apply 'FirstParagraph' style to the first paragraph after a heading/subheading
                    if i == 0:
                        book_content_elements.append(Paragraph(section, styles['FirstParagraph']))
                    else:
                        book_content_elements.append(Paragraph(section, styles['BodyText']))

                    # Add a spacer after each section except the last one
                    if i < len(sections) - 1:
                        book_content_elements.append(Spacer(1, 6))

                book_content_text += f"{sections_text.strip()}\n\n"
                break  # Exit the loop if successful
            except Exception as e:
                print(f"    DEBUG: An error occurred during generation: {e}")  # Debug print
                print("    DEBUG: Retrying in 5 seconds...")
                time.sleep(5)

# --- Output the Book ---
doc.build(book_content_elements)
with open(f"{create_dynamic_filename(book_title)}.txt", "w", encoding="utf-8") as f:
    f.write(book_content_text)

print(f"Book content written to {book_title}.txt")