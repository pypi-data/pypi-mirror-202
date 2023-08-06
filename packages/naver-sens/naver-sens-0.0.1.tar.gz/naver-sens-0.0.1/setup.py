import setuptools

setuptools.setup(
  name="naver-sens",
  version="0.0.1",
  license='MIT',
  author='jst0951',
  author_email='jst0951@gmail.com',
  description='Naver SENS(Simple & Easy Notification Service) python wrapper',
  long_description="""
  Naver Cloud Platform SENS(Simple & Easy Notification Service) python wrapper\n
  Reference : https://api.ncloud-docs.com/docs/ai-application-service-sens-smsv2\n
  Guide : https://codedbyjst.tistory.com/10\n
  """,
  url="https://github.com/jst0951/naver-sens",
  packages=setuptools.find_packages(),
  install_requires=[
    'requests'
  ],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent"
  ],
)