try:
	from jinja2 import Environment, FileSystemLoader
	import markdown
	import time
	import argparse
	from os import path
	import os

except ImportError as e:
	print("Modules could not be loaded required modules jinja2, markdown, time, os, argparse\nError below as reported by Python")

class ArgsIncorrectError(Exception):
	def __init__(self, value):
		self.value = value

class md_to_html():
	def __init__(self):
		self.loader = FileSystemLoader("/")
		self.env = Environment(loader = self.loader)
		
	def build_from_md(self, md_content_fp, file_name, ):
		with open(md_content_fp) as in_file:
			md_content = in_file.read()
		title = md_content.split("\n")[0].replace("#", "")
	
		html_from_md = markdown.markdown(md_content)

		template = self.env.get_template(self.template)

		final_page_content = template.render(
			content=html_from_md,
			date=time.asctime(time.gmtime()),
			title = title
		)

		with open(path.join(self.output, file_name), "w+") as out_file:
			out_file.write(final_page_content)

		print(f"Processed {file_name}, saved at {path.join(self.output, file_name)}")

	def call_from_cmd(self):
		self.parser = argparse.ArgumentParser(prog = "MD to Templated HTML",	description = "Takes in markdown and outputs html in a template")

		self.parser.add_argument("template_input", type=str, help="The location of the html file used for input")
		self.parser.add_argument("output_location", type=str, help="The location of the html file used for output")
		self.parser.add_argument("mark_down_input", type=str, help="The location of the markdown file used for input")
		self.parser.add_argument("-v", "--verbose", action="store_true",help="The location of the markdown file used for input")

		args = self.parser.parse_args()
		
		self.md_input_files = []
		self.md_path = path.abspath(args.mark_down_input)
		self.template = path.abspath(args.template_input)
		self.output = path.abspath(args.output_location)

		#Manage input files
		if(not path.exists(self.md_path)):
			raise ArgsIncorrectError(f"The path {self.md_path} dose not exits")

		if(path.isdir(self.md_path)):
			for dir_item in os.listdir(self.md_path):
				if(dir_item[-3:] == ".md"):
					self.md_input_files.append(dir_item)
					if(args.verbose):
						print(f"Markdown File Found: {dir_item}")
		
		if(path.isfile(self.md_path)):
			#This ensures the rest of the program behaves with a single md file provided 
			md_path_split = path.split(self.md_path)
			self.md_path = md_path_split[0]
			md_file_fp = md_path_split[1]

			if(md_file_fp[-3:] == ".md"):
				self.md_input_files.append(md_file_fp)
				if(args.verbose):
					print(f"Markdown File Found: {self.md_path}")
		
		if(len(self.md_input_files) == 0):
			raise ArgsIncorrectError("No Markdown Files found")

		#Manage template
		if(not path.isfile(self.template)):
			raise ArgsIncorrectError(f"Tempate file is not correct {self.template}")
		
		if(not self.template[-5:] == ".html"):
			raise ArgsIncorrectError(f"Tempate file {self.template} must be html")
		
		#Manage output location
		if(not path.isdir(self.output)):
			raise ArgsIncorrectError(f"Output directory {self.output} must be exists")
		
		#Process Files	
		for md_file in self.md_input_files:
			try:
				full_md_file_path = path.join(self.md_path, md_file)
				file_name = md_file.replace(".md", ".html")
				self.build_from_md(full_md_file_path, file_name)

				if(args.verbose):
					print(f"Finished {md_file}")

			except Exception as e:
				print(f"Failed to parse {md_file}\nUse -v to see full error")
				raise e

if(__name__ == "__main__"):
	obj = md_to_html()
	try:
		obj.call_from_cmd()
	except ArgsIncorrectError as e:
		print(e.value)
