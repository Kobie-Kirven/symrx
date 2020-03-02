# a class for genterating the PDF

from fpdf import FPDF

class Generate_pdf():
	"""A way to generate a pdf based on what people select"""

	def __init__(self, v4, v1, v5, v2, v3, patient_name):
		self.dosage_type = v1
		self.quantity = v4
		self.admin_route = v5
		self.eat = v2
		self.time = v3
		self.patient_name = patient_name
	
	def what_selected(self):
		select = []
		list_of_vars = [self.dosage_type, self.quantity, self.admin_route, self.eat, self.time]
		for var in list_of_vars:
			if var != 'NA':
				select.append(var)
		return select

	def build_pdf(self,done):
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font("Arial", size=12)

		pdf.line(115, 20, 115, 4000) # splitting line
		pdf.cell(10, 10, txt="Patient Name: ", ln=1, align="L")
		pdf.line(40, 17, 65, 17)
		pdf.text(40, 15, self.patient_name)
		pdf.image('symrx_logo.png', x=175, y=2, w=30)

		pdf.image('thing_1.png', x=10, y=35 ,w=15)


	
		num = 0
		if self.quantity == 'One':
			num = 1
		elif self.quantity == 'Two':
			num = 2
		elif self.quantity == 'Three':
			num = 3
		elif self.quantity == 'Four':
			num = 4
		elif self.quantity == 'Five':
				num = 5
		else:
			num = 1

		room = (100 // num) -5

		for i in range(num):
			pdf.image((done[0] + '.png'), x= (i * room) + 20, y=50, w=(room//1.5))

		x = 2
		y = 120
		for element in done[2:4]:
			pdf.image((element + '.png'), x=20, y=y ,w=80)
			pdf.image('thing_' + str(x) + '.png', x=10, y=y-10 ,w=15)
			
			y += 120
			x += 1
		pdf.output("finished_picto.pdf")
