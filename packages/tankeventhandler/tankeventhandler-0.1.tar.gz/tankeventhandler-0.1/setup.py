from setuptools import setup, find_packages

setup(
    name='tankeventhandler',
    version='0.1',
    author='Bhaskar Tank',
    author_email='tankbhaskar@gmail.com',
    description="""The EventScheduler library allows users to schedule events to be triggered
                after a specified delay and to notify registered listeners when those events occur.
                It manages event scheduling and listener registration, facilitating asynchronous event-driven
                programming. Users can define event callbacks and listeners to respond to events, enhancing 
                modularity and responsiveness in their applications. This library is useful for scenarios requiring
                 timed actions and notifications, such as task scheduling and event handling in applications.""",
    packages=find_packages(),
    install_requires=[
        'some_dependency',
    ],
)
