from io import BytesIO 
import base64
import matplotlib.pyplot as plt

def get_graph():
   #create a BytesIO buffer for the image
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   #set cursor to the beginning of the stream
   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   #free up the memory of buffer
   buffer.close ()

   #return the image/graph
   return graph

#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
   #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
   #AGG is preferred solution to write PNG files
   plt.switch_backend('AGG')

   #specify figure size
   fig=plt.figure(figsize=(6,3))

   #select chart_type based on user input from the form
   if chart_type == '#1':
        # Bar chart with recipe names on x-axis and number of ingredients on y-axis
        plt.bar(data['name'], data['number_of_ingredients'])
        plt.xlabel('Recipe Name')  # X-axis label
        plt.ylabel('Number of Ingredients')  # Y-axis label
        plt.title('Number of Ingredients per Recipe')
        plt.xticks(rotation=45)

   elif chart_type == '#2':
       # Pie quadrants labeled as 'easy', 'medium', 'intermediate', 'hard'
       # Quadrant size determined by number of recipes with that difficulty.
        difficulty_counts = kwargs.get('difficulty_counts')
        difficulty_labels = kwargs.get('difficulty_levels')
        plt.pie(difficulty_counts, labels=difficulty_labels, autopct='%1.1f%%')
        plt.title('Recipe Difficulty Distribution') 


   elif chart_type == '#3':
        # Line chart with recipe names on x-axis and cooking time on y-axis
        plt.plot(data['name'], data['cooking_time'])
        plt.xlabel('Recipe Name')  # X-axis label
        plt.ylabel('Cooking Time (minutes)')  # Y-axis label
        plt.title('Cooking Time per Recipe')  
        plt.xticks(rotation=45)
   else:
       print ('unknown chart type')

   #specify layout details
   plt.tight_layout()

   #render the graph to file
   chart =get_graph() 
   return chart      