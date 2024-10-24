from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'IPEVO python diarization module'
LONG_DESCRIPTION = 'IPEVO python diarization module using pyannote.audio'

# 配置
setup(
        name="ipevo-python-diarization", 
        version=VERSION,
        author="c1ayvveng",
        author_email="kehwaweng@staff.ipevo.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'pyannote.audio', "python-dotenv", 
        ], 
)