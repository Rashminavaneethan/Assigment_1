
import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ibdm"
)

cursor = DB_conn.cursor()


cursor.execute("SELECT * FROM movies")
rows = cursor.fetchall()


columns = [i[0] for i in cursor.description]


df = pd.DataFrame(rows, columns=columns)
page = st.sidebar.radio("Go To", ["Home","Visualization", "Filtration"])
#hOME PAGE 
if page == "Home":
    st.title("  IMDB 2024 Data Visualizations")
    st.image("C:/Users/rashm/Pictures/movie.jpg", width=600)
#Visualization
elif page == "Visualization":
    st.markdown("""
    <h2 style='font-size:40px; text-align:center;'>
        Exploring the Film Industry Through Data Visualization
    </h2>
""", unsafe_allow_html=True)
    
    if st.button("Show Ratings Distribution"):
        df_top_votes=df.sort_values('Votes',ascending=False).head(10) #df_top_combined = df.sort_values(by=['Votes', 'Rating'], ascending=False).head(10)
        st.write("Top Votes",df_top_votes)
        df_top_Rates=df.sort_values('Rating',ascending=False).head(10) #df_top_combined = df.sort_values(by=['Votes', 'Rating'], ascending=False).head(10)
        st.write("Top Ratings",df_top_Rates)

    if st.button("Genre Distribution"):
   
        df_Genre=df['Genre'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))  
        df_Genre.plot(kind='bar', rot=0, color='green', ax=ax)

   
        ax.set_title('Bar Plot for Genre', fontsize=16)
        ax.set_xlabel('Genre', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)

        st.pyplot(fig)

    if st.button("Average Duration by Genre"):
        Avg_duration=df.groupby('Genre')['Duration_min'].mean()
        fig, ax = plt.subplots(figsize=(10, 6))  
        Avg_duration.plot(kind='barh', rot=0, color='green', ax=ax)

   
        ax.set_title('Genre Distribution', fontsize=16)
        ax.set_xlabel('Count', fontsize=12)
        ax.set_ylabel('Genre', fontsize=12)

        st.pyplot(fig)

    if st.button("Voting Trends by Genre"):
   
        Avg_Voting=df.groupby('Genre')['Votes'].mean()
        fig, ax = plt.subplots(figsize=(10, 6))  
        Avg_Voting.plot(kind='bar', rot=0, color='green', ax=ax)

   
        ax.set_title('Vote count for each Genre', fontsize=16)
        ax.set_xlabel('Genre', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)

        st.pyplot(fig)

    if st.button("Rating Distribution"):
   
    
        fig, ax = plt.subplots(figsize=(6, 6))  
        ax.boxplot(df['Rating'])

   
        ax.set_title('Ratings for movies', fontsize=16)
        ax.set_xlabel('count', fontsize=12)
        ax.set_ylabel('Rating', fontsize=12)

        st.pyplot(fig)

    if st.button("the top-rated movie for each genre in a table"):
        top_rated_movies= df.sort_values('Rating', ascending=False).groupby('Genre').first()
        st.dataframe(top_rated_movies)

    if st.button("Most Popular Genres by Voting"):
        fig, ax = plt.subplots(figsize=(10, 6))
        genre_counts = df['Genre'].value_counts()

    
        labels = ['Action', 'Adventure', 'Fantasy', 'Animation', 'History']
        values = genre_counts.loc[labels]  

   
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%0.2f%%', radius=1)
        ax.set_title("Genre Distribution")

  
        st.pyplot(fig)

    if st.button("Duration Extremes"):
        shortest = df.loc[df["Duration_min"].idxmin()]
        longest = df.loc[df["Duration_min"].idxmax()]
        table_data = [["Shortest Movie", shortest["Title"], f"{shortest['Duration_min']} min"],
        ["Longest Movie", longest["Title"], f"{longest['Duration_min']} min"]]
        duration_df = pd.DataFrame(table_data, columns=["Type", "Title", "Duration"])

        st.dataframe(duration_df)



    if st.button("compare average ratings across genres"):
        genre_avg = df.groupby("Genre")["Rating"].mean().reset_index()
        pivot = genre_avg.pivot_table(index="Genre", values="Rating")
        fig, ax = plt.subplots(figsize=(6, 6)) 

        sns.heatmap(pivot, annot=True, cmap="coolwarm", fmt=".1f", ax=ax)


        ax.set_title("Average Movie Ratings by Genre")
        ax.set_ylabel("Genre")
        ax.set_xlabel("Average Rating")

    
        plt.tight_layout()
        st.pyplot(fig)


    if st.button("Correlation Analysis"):
        fig,ax=plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df, x="Votes", y="Rating", ax=ax)
        ax.set_title("Ratings vs. Vote Count")
        ax.set_ylabel("Number of Votes")
        ax.set_xlabel("Rating")

    
        plt.tight_layout()
        st.pyplot(fig)

#FILTRATION
elif page == "Filtration":
    st.markdown("""
    <h2 style='font-size:40px; text-align:center;'>
        Filter & Analyze Movie Trends
    </h2>
""", unsafe_allow_html=True)
    

    duration = st.radio(
    "Select the Movie Duration Range:",
    ("< 2 hrs", "2–3 hrs", "> 3 hrs")
)

# Build dynamic SQL query
    if duration == "< 2 hrs":
        output = """
        SELECT *, Duration_min / 60.0 AS Duration_hr
        FROM movies
        WHERE Duration_min / 60.0 < 2
        """
    elif duration == "2–3 hrs":
        output = """
        SELECT *, Duration_min / 60.0 AS Duration_hr
        FROM movies
        WHERE Duration_min / 60.0 BETWEEN 2 AND 3
        """
    else:
        output = """
        SELECT *, Duration_min / 60.0 AS Duration_hr
        FROM movies
        WHERE Duration_min / 60.0 > 3
        """


    cursor.execute(output)


    rows = cursor.fetchall()


    columns = [desc[0] for desc in cursor.description]


    filtered_df = pd.DataFrame(rows, columns=columns)
    st.write(f"Show the movies within the duration of: **{duration}**")


    st.dataframe(filtered_df)


    min_votes = st.number_input("Minimum number of votes", min_value=1000, value=100000, step=50000)
    output = f"SELECT * FROM movies WHERE Votes >= {min_votes}"


    cursor.execute(output)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    filtered_df = pd.DataFrame(rows, columns=columns)

    st.write(f"Showing movies with **≥ {min_votes} votes**")
    st.dataframe(filtered_df)


    cursor = DB_conn.cursor()
    cursor.execute("SELECT DISTINCT Genre FROM movies WHERE Genre IS NOT NULL")
    genres = [row[0] for row in cursor.fetchall()]


    selected_genres = st.multiselect("Select Genre(s)", options=sorted(genres))

    if selected_genres:
        placeholders = ','.join(['%s'] * len(selected_genres))  # Create %s, %s, %s for IN query
        query = f"SELECT * FROM movies WHERE Genre IN ({placeholders})"
        cursor.execute(query, selected_genres)
    else:
        query = "SELECT * FROM movies"
        cursor.execute(query)


    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    filtered_df = pd.DataFrame(rows, columns=columns)


    st.write(f"Showing movies in genres: **{', '.join(selected_genres) if selected_genres else 'All'}**")
    st.dataframe(filtered_df)

    st.subheader("🎬 Movie Filter Panel")


    with st.form("movie_filter_form"):
  
   
        duration_option = st.radio("Select Duration:", ("< 2 hrs", "2–3 hrs", "> 3 hrs"))

        min_rating = st.slider("Minimum IMDb Rating:", 0.0, 10.0, 8.0, 0.1)

        min_votes = st.number_input("Minimum number of votes", min_value=0, value=50000, step=10000)

  
        cursor.execute("SELECT DISTINCT Genre FROM movies WHERE Genre IS NOT NULL")
        unique_genres = [row[0] for row in cursor.fetchall()]
        selected_genres = st.multiselect("Select Genre(s):", sorted(unique_genres))

    
        submitted = st.form_submit_button("Submit Filters")


    if submitted:
        where_clauses = []

   
        if duration_option == "< 2 hrs":
            where_clauses.append("Duration_min / 60.0 < 2")
        elif duration_option == "2–3 hrs":
            where_clauses.append("Duration_min / 60.0 BETWEEN 2 AND 3")
        else:
            where_clauses.append("Duration_min / 60.0 > 3")

   
        where_clauses.append("Rating >= %s")

   
        where_clauses.append("Votes >= %s")

        query_params = [min_rating, min_votes]

        if selected_genres:
            placeholders = ",".join(["%s"] * len(selected_genres))
            where_clauses.append(f"Genre IN ({placeholders})")
            query_params.extend(selected_genres)

    
        where_sql = " AND ".join(where_clauses)
        query = f"""
        SELECT *, Duration_min / 60.0 AS Duration_hr
        FROM movies
        WHERE {where_sql}
        """

    
        cursor.execute(query, query_params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

    
        filtered_df = pd.DataFrame(rows, columns=columns)

    # --- Show Results ---
        st.markdown(f"#### 🎯 Filtered Results: {len(filtered_df)} movies found")
        st.dataframe(filtered_df.reset_index(drop=True))

    















