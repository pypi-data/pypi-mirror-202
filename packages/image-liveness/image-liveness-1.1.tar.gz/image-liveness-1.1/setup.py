from distutils.core import setup
setup(
  name = 'image-liveness',         
  packages = ['Liveness'],  
  version = '1.1',      
  license='Apache License 2.0',        
  description = 'This library offers a liveness detection on static images, which can be used to distinguish if it is a live capture or a spoofed image based on facial features and other indicators of authenticity.',  
  author = 'Ashish Thapa',                   
  author_email = 'ashish.f1soft@gmail.com',      
  url = 'https://github.com/ashishf1soft',  
  download_url = 'https://github.com/ashishf1soft/liveness-detection/archive/refs/tags/v_01.tar.gz',   
  keywords = ['LIVENESS','FACE FACE','DETECTION'], 
  install_requires=[            # I get to this in a second
          'numpy',
          'opencv-python',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   
    'Programming Language :: Python :: 3.9',
  ],
)