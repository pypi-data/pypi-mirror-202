from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='DA4RDM_Vis_ProcessBased',
      version='0.1.6',
      description='Test package to get visualisation for a given projectid as reference analyzed '
                  'on different RDLC phase process models',
      long_description=readme(),
      classifiers=[
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",	
      ],
      packages = ['DA4RDM_Vis_ProcessBased'],
      package_dir = {'DA4RDM_Vis_ProcessBased': 'src/DA4RDM_Vis_ProcessBased'},
      package_data={'DA4RDM_Vis_ProcessBased': ['PhaseData/*.csv']},
      dependencies=[
        'plotly-express>==0.4.1',
        'numpy >= 1.18.1',
        'pandas >= 1.5.3',
        'python_dateutil >= 2.8.2',
        'pm4py >= 2.7.0',
        'kaleido >= 0.2.1',
        ],
      include_package_data=True,
      )
