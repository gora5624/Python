from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.add_font('DejaVu', '', 'D:\DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)
pdf.cell(200, 10, txt="Заявка №_01-000001", ln=1, align="C")
pdf.output("D:\simple_demo.pdf")
