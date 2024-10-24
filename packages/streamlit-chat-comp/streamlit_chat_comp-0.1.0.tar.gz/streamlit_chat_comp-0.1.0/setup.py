from setuptools import setup, find_packages

setup(
    name='streamlit_chat_comp',
    version='0.1.0',
    description='A Streamlit component for sending text and audio messages',
    author='Mohammed Bahageel',
    author_email='m.bahageel88@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit',
    ],
    package_data={
        'my_chat_package': ['static/*.html', 'static/*.css', 'static/*.js'],
    },
)