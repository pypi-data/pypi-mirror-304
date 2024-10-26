from setuptools import setup, find_packages

# setup(
#     name='finance_calculator',
#     version='0.1.0',
#     packages=find_packages(),
#     install_requires=[
#         'argparse',
#     ],
#     entry_points={
#         'console_scripts': [
#             'finance-calculator=finance:main',
#         ],
#     },
# )

# setup(
#     name='transaction_report',
#     version='0.1.0',
#     packages=find_packages(),
#     install_requires=[
#         'pandas',
#         'argparse',
#     ],
#     entry_points={
#         'console_scripts': [
#             'transaction-report=transaction_report:main',
#         ],
#     },
# )


# setup(
#     name='sales_report',
#     version='0.1.0',
#     packages=find_packages(),
#     install_requires=[
#         'pandas',
#     ],
#     entry_points={
#         'console_scripts': [
#             'sales-report=sales_report:main',
#         ],
#     },
# )

# setup(
#     name='order_receipt',
#     version='0.1.0',
#     packages=find_packages(),
#     install_requires=[],
#     entry_points={
#         'console_scripts': [
#             'order-receipt=order_receipt:main',
#         ],
#     },
# )

setup(
    name='customer_report',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'customer-report=customer_report:main',
        ],
    },
)
