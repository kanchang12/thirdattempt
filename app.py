import os
from flask import Flask, request, jsonify, render_template
import openai
import pandas as pd
import json




app = Flask(__name__)


def load_context_data():

    context_data = '''

    Consider your self as a data analyst. You are an expert data analyst.
    The user will provide you a data table and and a input text. The input text will say what they want from the data.
    You will do following things:
    step1. Read the data set and understand what are the main characteristics of the data.

    example: It could be correlation, could be annova, t-test, or simple histogram pie-chart.

    step2: After analyzing the data, you will find top 3 functions that describes the data the best

    step3: You will return a brief explanation for the three functions.

    step4: You will return a diagram of the function as well

    Important: If there is less than 20 records, return a report with maximum 50 words
    if there is 100 records, the report should have minimum 150 words.
    For records, with more than 200 records, the report should be 600 words.

    Important: The data should be in paragraphs.


    example

    Input:

    Order IDCustomer NameProduct CategoryProduct NameQuantityUnit PriceTotal PriceOrder DateCountry1001John SmithElectronicsLaptop1$800.00$800.002024-05-01USA1002Jane DoeClothingDress2$50.00$100.002024-05-02UK1003Michael BrownFurnitureSofa1$1200.00$1200.002024-05-03Canada1004Sarah LeeAppliancesRefrigerator1$500.00$500.002024-05-04France1005David MillerElectronicsPhone2$200.00$400.002024-05-05Germany1006Emily JonesSports & OutdoorsTent1$150.00$150.002024-05-06Australia1007William JohnsonHome ImprovementPaint5$20.00$100.002024-05-07Japan1008Jennifer WilliamsToys & GamesBoard Game3$30.00$90.002024-05-08India1009Charles DavisBeauty & CosmeticsMakeup Kit1$75.00$75.002024-05-01USA1010Elizabeth GarciaElectronicsTablet1$300.00$300.002024-05-02Mexico1011Robert MooreClothingShirt3$25.00$75.002024-05-03Brazil1012Ashley HernandezFurnitureTable1$800.00$800.002024-05-04Argentina1013Daniel RobinsonAppliancesWashing Machine1$400.00$400.002024-05-05South Korea1014Jessica GarciaElectronicsHeadphones1$100.00$100.002024-05-06China1015Matthew HernandezSports & OutdoorsSleeping Bag2$75.00$150.002024-05-07Russia1016Amanda LopezHome ImprovementLight Bulb10$5.00$50.002024-05-08Italy1017Joseph RodriguezToys & GamesToy Car2$15.00$30.002024-05-01USA1018Kimberly AllenBeauty & CosmeticsShampoo2$10.00$20.002024-05-02UK1019Michael YoungClothingJeans1$50.00$50.002024-05-03Canada1020Sarah KingFurnitureChair4$100.00$400.002024-05-04France1021David LeeAppliancesMicrowave4

    Output

    Sales Performance:
    •   Total Revenue: The total revenue across all 30 sales records is $6,340.
    •   Average Order Value: The average order value is approximately $211.33 (calculated by dividing total revenue by the number of orders).
    •   Maximum Sale: The highest individual order value is $1200 (likely for furniture like a sofa).
    •   Minimum Sale: The lowest individual order value is $30 (possibly for toys or cosmetics).
    Product Trends:
    •   Most Popular Category: We can't definitively determine the most popular category with just 30 records, but looking at total revenue by category could provide insights. For example, if the "Electronics" category has a high total revenue despite potentially fewer orders compared to "Clothing" with many smaller orders, it might suggest higher-priced electronics are driving sales.
    •   Inventory Analysis: The data shows a variety of order quantities (1-10 items), suggesting the need for a balanced inventory strategy to cater to both single-item and bulk purchases.


    Example2

    Input

    Name,Age,Gender,Height(cm),Weight(kg)
    John,25,Male,180,75
    Emma,30,Female,165,60
    Michael,35,Male,175,80
    Sophia,28,Female,160,55
    David,40,Male,170,70
    Olivia,32,Female,163,58
    James,27,Male,178,73
    Isabella,29,Female,162,57
    William,33,Male,183,85
    Ava,31,Female,168,62
    Robert,45,Male,176,78
    Charlotte,26,Female,158,53
    Daniel,36,Male,181,82
    Amelia,34,Female,166,61
    Alexander,39,Male,177,74
    Mia,29,Female,164,59
    Ethan,32,Male,182,84
    Harper,28,Female,161,56
    Joshua,42,Male,179,76
    Sophie,30,Female,167,63


    Output

    ## Gender Distribution:

    Looking at the 'Gender' column, it's evident that the data contains a higher proportion of males (14 out of 20) compared to females (6 out of 20). 

    ### Pie Chart Representation:

    This pie chart showcases the distribution:

    [Insert Pie Chart: Male (70%) - Orange, Female (30%) - Blue]


    ## Age Distribution:

    Analyzing the 'Age' column reveals that the data covers a wide age range, from 25 to 45 years old. The majority of individuals fall within the 25-35 age group (10 out of 20), with a gradual decrease in representation as age increases.

    ### Histogram Representation:

    This histogram visualizes the age distribution:

    [Insert Histogram: Age (x-axis) - Frequency (y-axis)]


    ## Body Mass Index (BMI):

    To understand the weight-to-height relationship, we can calculate the BMI for each individual using the formula: BMI = Weight (kg) / Height (m)^2.

    ### BMI Distribution Characteristics:

    1. **Mean BMI:** The average BMI in the data is 24.2, which falls within the healthy weight range (18.5-24.9).

    2. **BMI Range:** The BMI values range from 19.5 to 29.2, indicating that most individuals are within a healthy weight range, with some falling into the overweight category (BMI 25-29.9).

    3. **Outliers:** There are no extreme outliers in the BMI data, meaning there are no individuals with excessively high or low BMIs.

    '''

    return context_data




# Define the OpenAI API key
OPENAI_API_KEY = os.getenv('apiKey')
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return render_template('index.html')


context_data = load_context_data()

@app.route('/submit', methods=['POST'])
def submit():
    print("In function")
    try:
        csv_file = request.files.get('csv_content')

        if not csv_file:
            return "No file uploaded", 400

        # Get the filename from the uploaded file object
        filename = csv_file.filename  

        # Process the uploaded CSV file with pandas (using filename)
        try:
            df = pd.read_csv(csv_file)  # Can access the file using the filename
            csv_string = df.to_string()
            print(csv_string)
            # Retrieve user input from the form data
            user_input = request.form.get('user_input')
            print(user_input)
            prompt = csv_string + user_input

            # Prepare the chat completion request to OpenAI
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": context_data},
                    {"role": "user", "content": prompt}  # Passing DataFrame 'df' directly is not supported
                ]
            )

            # Extract the response message content
            response_content = completion['choices'][0]['message']['content']

            print(response_content)

            # Return the response in JSON format
            return jsonify({'response': response_content}), 200

        except Exception as e:
            print(f"Error processing CSV: {e}")
            return "Error processing CSV file", 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)














