import setuptools
with open(r'C:\Users\Px228\Desktop\Data_Save\Data_Save\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='Data_Save',
	version='1.1.0',
	author='px228',
	author_email='leka55mapket@gmail.com',
	description='from now on, no more than three checks are possible',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['Data_Save'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)