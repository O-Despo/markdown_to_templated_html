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
	
	def init_parser(self):
		self.parser = argparse.ArgumentParser(prog = "SSMBS (Static Site Manger for Broke Students", description="ADD DISC")
		self.parser.add_argument("-v", "--verbose", action="store_true", help="The location of the markdown file used for input")
		self.subparsers = self.parser.add_subparsers(help="what action to perform")

		# Markdown
		self.parser_md = self.subparsers.add_parser("markdown", description = "Takes in markdown and outputs html in a template")
		self.parser_md.set_defaults(func=self.md_run)

		self.parser_md.add_argument("template", type=str, help="The filepath of the html file used for input")
		self.parser_md.add_argument("output", type=str, help="The filepath of the html file used for output")
		self.parser_md.add_argument("markdown", type=str, help="The filepath of the markdown file or directory used for input")

		# Directory
		self.parser_dir = self.subparsers.add_parser("dirgen", description = "Takes in a folder and returns a static directory page")
		self.parser_dir.set_defaults(func=self.dir_gen)

		self.parser_dir.add_argument("template", help="the template file to be used")
		self.parser_dir.add_argument("output", help="the location of the output file")
		self.parser_dir.add_argument("folder", help="the folder to map the files form")
		self.parser_dir.add_argument("-sd", help="the start directory")
		self.parser_dir.add_argument("-ft", help="file type")


	def build_from_md(self, md_content_fp, file_name, ):
		with open(md_content_fp) as in_file:
			md_content = in_file.read()

		title = md_content.split("\n")[0].replace("#", "")
	
		html_from_md = markdown.markdown(md_content)

		template = self.env.get_template(self.template_p)

		final_page_content = template.render(
			content=html_from_md,
			date=time.asctime(time.gmtime()),
			title = title
		)

		with open(path.join(self.out_p, file_name), "w+") as out_file:
			out_file.write(final_page_content)

		print(f"Processed {file_name}, saved at {path.join(self.out_p, file_name)}")
	def check_arguments_md(self, md_p, tmpt_p, out_p):
		#Check markdown_path
		if(not path.exists(md_p)):
			raise ArgsIncorrectError(f"The path {md_p} dose not exits")
		
		if(not (path.isdir(md_p) or  path.isfile(md_p))):
			raise ArgsIncorrectError(f"The markdown path {md_p} is not a file or directory")
		# The if statement above is redundent a redundent check with later code to change behavoir based on
		#file or directory. I placed it hear to preserve flow. Which I reuend with this commennt

		#Check template
		if(not path.isfile(tmpt_p)):
			raise ArgsIncorrectError(f"Tempate file is not correct {tmpt_p}")
		
		if(not tmpt_p[-5:] == ".html"):
			raise ArgsIncorrectError(f"Tempate file {tmpt_p} must be html")
	
		#Check output location
		if(not path.isdir(out_p)):
			raise ArgsIncorrectError(f"Output directory {out_p} must be exists")
	
	def check_arguments_dirgen(self, in_fa, out_p, tmpt_p):
		#Check input path
		if(not path.exists(in_fa)):
			raise ArgsIncorrectError(f"The path {in_fa} dose not exits")
		
		if(not (path.isdir(in_fa))):
			raise ArgsIncorrectError(f"The input path {in_fa} is not a directory")

		#Check template
		if(not path.isfile(tmpt_p)):
			raise ArgsIncorrectError(f"Tempate file is not correct {tmpt_p}")
		
		if(not tmpt_p[-5:] == ".html"):
			raise ArgsIncorrectError(f"Tempate file {tmpt_p} must be html")
	
		#Check output location
		dirp = path.split(out_p)
		if(not path.isdir(dirp[0])):
			raise ArgsIncorrectError(f"Output directory {dirp[0]} must be exists")
	

	def call_from_cmd(self):
		self.init_parser()
		args = self.parser.parse_args()
		#try:
		args.func(args)
		#except AttributeError:
		#	self.parser.print_help()

	def dir_gen(self, args):
		in_folder = path.abspath(args.folder)
		output = path.abspath(args.output)
		template = path.abspath(args.template)
		
		try:
			self.check_arguments_dirgen(in_folder, output, template)
		except ArgsIncorrectError as e:
			print(e.value)			
		
		files_found = []
	
		if args.ft != None:
			file_format = args.sd
		else:
			file_format = ".md"#TODO use argparse default
		
		if args.sd != None:
			sd = args.sd
		else:
			sd = path.abspath(os.curdir)

		path_to_be_removed = os.path.commonpath([in_folder, sd])

		for dir_item in os.listdir(in_folder):
			if(dir_item[len(file_format) + 1:] == file_format):
				print(dir_item)
				files_found.append(dir_item.replace(path_to_be_removed, ""))

				if(args.verbose):
					print(f"File Found: {dir_item}")

		template_out = self.env.get_template(template)

		final_page_content = template_out.render(
			links=files_found,
		)
		
		with open(output, "w+") as file:
			file.write(final_page_content)
			print(f"written to {final_page_content}")
	
	def md_run(self, args):
		md_source_p = path.abspath(args.markdown)
		self.template_p = path.abspath(args.template)
		self.out_p = path.abspath(args.output)
			
		try:
			self.check_arguments_md(md_source_p, self.template_p, self.out_p)
		except ArgsIncorrectError as e:
			print(e.value)			

		self.md_input_files = []

		#Change behavoir if markdown is a single file or directory
		if(path.isdir(md_source_p)):

			for dir_item in os.listdir(md_source_p):

				if(dir_item[-3:] == ".md"):
					self.md_input_files.append(dir_item)

					if(args.verbose):
						print(f"Markdown File Found: {dir_item}")
		
		if(path.isfile(md_source_p)):

			md_path_split = path.split(md_source_p)
			md_source_p = md_path_split[0]
			md_file_fp = md_path_split[1]
			#Code above makes a single md_file path match up with the expected format

			if(md_file_fp[-3:] == ".md"):
				self.md_input_files.append(md_file_fp)

				if(args.verbose):
					print(f"Markdown File Found: {md_source_p}")
	
		if(len(self.md_input_files) == 0):
			print("Warning: No Markdown Files found, program will do nothinng")
	
		for md_file in self.md_input_files:
			try:
				full_md_file_path = path.join(md_source_p, md_file)
				file_name = md_file.replace(".md", ".html")
				self.build_from_md(full_md_file_path, file_name)

				if(args.verbose):
					print(f"Finished {md_file}")

			except Exception as e:
				print(f"Failed to parse {md_file}\nUse -v to see full error")
				raise e

if(__name__ == "__main__"):
	obj = md_to_html()
	obj.call_from_cmd()
