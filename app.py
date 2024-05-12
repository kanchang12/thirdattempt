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

 Summary Statistics:
First, let's calculate some summary statistics for the numerical variables (age, height, weight) in the dataset.
•	Age:
•	Mean Age: Approximately 32.2 years
•	Median Age: 31.5 years
•	Age Range: 26 to 45 years
•	Height (cm):
•	Mean Height: Approximately 171.4 cm
•	Median Height: 170.5 cm
•	Height Range: 158 cm to 183 cm
•	Weight (kg):
•	Mean Weight: Approximately 68.1 kg
•	Median Weight: 70 kg
•	Weight Range: 53 kg to 85 kg
Gender Distribution:
The dataset contains individuals of two genders, male and female.
•	Male:
•	Count: 10
•	Average Age: Approximately 34.3 years
•	Average Height: Approximately 177.2 cm
•	Average Weight: Approximately 77.2 kg
•	Female:
•	Count: 10
•	Average Age: Approximately 30.1 years
•	Average Height: Approximately 163.6 cm
•	Average Weight: Approximately 59.8 kg
Observations:
•	The average age of males in the dataset is slightly higher than that of females.
•	Males tend to be taller and heavier on average compared to females.
•	The age range for males is wider (26 to 45 years) compared to females (26 to 34 years).
•	The tallest individual in the dataset is William (183 cm) and the shortest is Charlotte (158 cm).
•	The heaviest individual in the dataset is William (85 kg) and the lightest is Charlotte (53 kg).
Insights:
•	There is a correlation between height and weight, with taller individuals generally weighing more.
•	The dataset represents a range of ages and physical characteristics typical of a diverse population sample.
•	Further analysis could explore relationships between variables, such as examining Body Mass Index (BMI) based on height and weight, or studying age distributions within gender groups.


Cluster Analysis Report
In this analysis, a K-means clustering algorithm was applied to group individuals based on age, height, and weight attributes. The dataset was standardized to ensure consistency in variable scales. Through clustering, three distinct groups were identified:
1.	Cluster 1: Younger individuals with below-average height and weight.
2.	Cluster 2: Middle-aged individuals with average height and weight.
3.	Cluster 3: Older individuals with above-average height and weight.
This clustering reveals distinct patterns based on age and physical characteristics. Further exploration of cluster characteristics can provide insights into demographic trends and health profiles within the dataset.
Regression Analysis Report: Exploring the Relationship between Age, Height, and Weight
Introduction: The objective of this report is to investigate how age and height influence weight among individuals based on a dataset containing information about individuals' demographics and physical characteristics.
Methodology: We utilized a multiple linear regression model to analyze the relationship between weight (dependent variable) and two independent variables: age and height. The regression model is expressed as: Weight=�0+�1×Age+�2×Height+�Weight=β0+β1×Age+β2×Height+ϵ where:
•	�0β0 is the intercept,
•	�1β1 is the coefficient for age,
•	�2β2 is the coefficient for height,
•	�ϵ is the error term.
Data Analysis: The dataset was divided into a training set and a testing set to train and evaluate the regression model. The regression coefficients ( �0β0, �1β1, and �2β2 ) were estimated using the training data to quantify the relationships between age, height, and weight.
Results: The regression analysis produced the following results:
•	Intercept ( �0β0 ): The intercept represents the estimated weight when age and height are zero.
•	Coefficient for Age ( �1β1 ): The coefficient for age indicates the estimated change in weight associated with a one-unit increase in age, holding height constant.
•	Coefficient for Height ( �2β2 ): The coefficient for height signifies the estimated change in weight associated with a one-unit increase in height, holding age constant.
Interpretation:
•	The regression coefficients provide valuable insights into the impact of age and height on weight. A positive coefficient for age suggests that weight tends to increase with age, while a positive coefficient for height indicates that weight tends to increase with height.
•	The R-squared value (or adjusted R-squared) measures the proportion of variance in weight explained by age and height. A higher R-squared value indicates a better fit of the regression model to the data.
Conclusion: In conclusion, the regression analysis reveals significant relationships between age, height, and weight among the individuals in the dataset. The findings highlight the influence of age and height on individual weight variations, contributing to our understanding of these demographic and physical factors.





    Input 
    
    Player,Sport,Country,Age,Height (cm),Weight (kg),Wins,Losses
    LeBron James,Basketball,USA,36,203,113,800,247
    Serena Williams,Tennis,USA,40,175,70,851,145
    Lionel Messi,Soccer,Argentina,34,170,72,705,137
    Simone Biles,Gymnastics,USA,24,145,47,32,2
    Tom Brady,Football,USA,44,198,102,264,79
    Usain Bolt,Track and Field,Jamaica,35,195,94,52,10
    Naomi Osaka,Tennis,Japan,24,180,69,25,14
    Cristiano Ronaldo,Soccer,Portugal,36,187,84,725,176
    Michael Phelps,Swimming,USA,36,193,88,28,7
    Maria Sharapova,Tennis,Russia,34,188,59,36,11
    Kyrie Irving,Basketball,USA,29,191,88,400,125
    Roger Federer,Tennis,Switzerland,40,185,85,1033,269
    Kevin Durant,Basketball,USA,33,208,108,600,234
    Megan Rapinoe,Soccer,USA,36,168,60,65,23
    Katie Ledecky,Swimming,USA,24,183,70,37,9
    Mohamed Salah,Soccer,Egypt,29,175,71,179,46
    Simona Halep,Tennis,Romania,30,168,60,23,7
    Chris Froome,Cycling,UK,36,186,71,42,15
    Carli Lloyd,Soccer,USA,39,170,68,140,33
    Novak Djokovic,Tennis,Serbia,34,188,77,88,17
    Russell Westbrook,Basketball,USA,33,191,91,300,180
    Alex Morgan,Soccer,USA,32,170,60,125,40
    Lewis Hamilton,Formula 1,UK,37,174,68,95,17
    Seth Rollins,Wrestling,USA,35,185,98,45,12
    ...


    Output

    
    Descriptive Statistics
    
    This report provides a comprehensive descriptive analysis of sports data encompassing a diverse range of player profiles. The dataset includes statistics on male and female athletes, offering insights into age distribution, height, weight, and performance metrics such as scoring averages and game statistics. The average age of players is 25 years, with a balanced representation of genders across teams. This analysis underscores the dynamic and competitive nature of sports, highlighting the varied talents and capabilities exhibited by athletes. The dataset illuminates trends in sports demographics, showcasing a spectrum of player attributes and achievements across different disciplines.
    
    Histogram
    
    The histogram illustrates the distribution of player ages in the sports dataset, showcasing a bell-shaped curve centered around 25 years. The majority of athletes fall within the 20-30 age range, indicating a youthful demographic. This visualization highlights the dataset's focus on prime-age athletes and offers insights into age-related trends in sports participation.
    
    
    Cluster Analysis
    This report outlines the application of K-means clustering to sports statistics data comprising 100 records. The objective was to identify inherent patterns and groupings within the dataset based on players' performance metrics. The analysis revealed three distinct clusters, each representing a unique player profile. Cluster 1 consists of high-scoring players with exceptional performance metrics. Cluster 2 includes players with moderate statistics across various attributes. Cluster 3 comprises players with lower overall performance. The clustering process provided valuable insights into player segmentation, allowing for targeted strategies in team formation and player development. Visual representations, such as scatter plots and centroid markers, enhance the interpretation of cluster patterns.
    

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
            
            # Retrieve user input from the form data
            user_input = request.form.get('user_input')
           
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

            

            # Return the response in JSON format
            return jsonify({'response': response_content}), 200

        except Exception as e:
            print(f"Error processing CSV: {e}")
            return "Error processing CSV file", 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)














