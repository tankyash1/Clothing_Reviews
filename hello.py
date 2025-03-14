from preswald import text, plotly, connect, get_df, table, query, slider
import pandas as pd
import plotly.express as px

# Load the CSV
connect()  # Load in all sources, which by default is the sample_csv
df = get_df('womens_clothing_reviews')

df = pd.read_csv('data/Womens Clothing E-Commerce Reviews.csv')

# Query to manipulate data
sql = "SELECT * FROM womens_clothing_reviews WHERE Rating > 4"
top_rated_df = query(sql, "womens_clothing_reviews")

# Building Interactive UI
text("# Women's Clothing Reviews Analysis")
table(top_rated_df, title="Reviews with Rating > 4")

# Reduce dataset size further for better visualization
df_sample = df[df['Rating'] > 1].sample(n=500, random_state=42)  # Reduced sample size

# Count occurrences of each rating
rating_counts = df['Rating'].value_counts().sort_index()

# Create bar chart with explicit counts
fig1 = px.bar(
    x=rating_counts.index, 
    y=rating_counts.values, 
    labels={'x': 'Rating', 'y': 'Number of Reviews'}, 
    title="Customer Review Sentiment",
    text_auto=True,
    color_discrete_sequence=['red']
)

# Improve visuals
fig1.update_layout(
    xaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4, 5]),  
    yaxis_title="Number of Reviews",
    xaxis_title="Rating",
    bargap=0.2
)

plotly(fig1)

dept_ratings = df.groupby('Department Name')['Rating'].mean().sort_values()

# Create bar chart
fig2 = px.bar(
    x=dept_ratings.index, 
    y=dept_ratings.values, 
    labels={'x': 'Department Name', 'y': 'Average Rating'}, 
    title="Average Customer Rating by Department",
    text_auto=True,
    color_discrete_sequence=['blue']
)

# Improve visuals
fig2.update_layout(
    yaxis=dict(range=[0, 5]),  # Ratings range from 1 to 5
    xaxis_title="Department Name",
    yaxis_title="Average Rating",
    bargap=0.3
)

# Show the plot
plotly(fig2)

# Visualization 3: Box Plot - Rating Distribution by Age Group**
df['Age Group'] = pd.cut(df['Age'], bins=[18, 25, 35, 45, 55, 65, 80], 
                         labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'])

fig3 = px.box(df, x='Age Group', y='Rating', 
              title='Rating Distribution Across Age Groups', 
              labels={'Rating': 'Customer Rating', 'Age Group': 'Age Group'},
              color_discrete_sequence=['green'])
plotly(fig3)

# Add user control for dynamic filtering
min_rating = slider("Minimum Customer Rating", min_val=1.0, max_val=5.0, default=4.0)
table(df[df["Rating"] > min_rating], title="Dynamic Review List")

# Show the data
table(df)
