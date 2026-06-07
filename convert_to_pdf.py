from markdown_pdf import Section, MarkdownPdf

if __name__ == "__main__":
    pdf = MarkdownPdf(toc_level=2)
    with open("project_documentation.md", "r", encoding="utf-8") as f:
        md_text = f.read()
    
    pdf.add_section(Section(md_text))
    pdf.save("project_documentation.pdf")
    print("PDF successfully generated.")
